# Obsidian Second-Brain Integration (v1.4.0) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend the `obsidian` plugin with a shared validation module, a write-time validation gate, contradiction-reconcile in `wiki-ingest`, and two new skills (`wiki-think`, `wiki-maintain`), shipped as v1.4.0.

**Architecture:** A single shared module (`skills/_shared/`) holds the authoritative validation rules — deterministic checks in a testable `validate.py` (Python + PyYAML, with a prose fallback), semantic checks in `validation-rules.md`. The existing wiki skills delegate to this module instead of inlining rules, eliminating the rule drift that caused v1.3.1 false positives. New skills reuse the module.

**Tech Stack:** Markdown skill files (Claude Code plugin format), Python 3 standard library + PyYAML for `validate.py`, pytest for the validator test suite. No build step in the repo.

## Global Constraints

- **Branch:** all work on `feature/obsidian-second-brain-integration` (already checked out, spec committed).
- **Version target:** `obsidian` 1.3.1 → **1.4.0** (semantic versioning).
- **Commit format:** Emoji Conventional Commits (e.g. `✨ feat:`, `🐛 fix:`, `📚 docs:`, `🧪 test:`, `♻️ refactor:`). **Never** append `Co-Authored-By: Claude` or `Generated with Claude Code` (project CLAUDE.md rule).
- **Documentation language:** professional English; any remaining German uses Swiss orthography (`ss` not `ß`, proper umlauts).
- **`validate.py` dependencies:** Python stdlib + PyYAML only. Must degrade gracefully (exit code 2 + JSON error) when PyYAML is absent, so skills fall back to the prose rules.
- **`validate.py` scope:** only inspects files under `<vault-root>/_wiki/` and `<vault-root>/_raw/`; ignores everything else.
- **Allowed wiki types:** `concept`, `tool`, `compare`, `hub`, `note`, `thinking`. Allowed source types: `clipping`, `chat`, `note`, `transcript`.
- **Finding schema:** every finding is `{file, severity, rule, message, autofixable}` with `severity ∈ {critical, minor}`.
- **Severity policy:** missing required frontmatter fields and `kind`/`type` violations are `critical` (block plugin writes until fixed/confirmed); dead links and asymmetric `related:` are `minor` (report only — a dead link may be a legitimate forward reference).
- **Test command:** `python3 -m pytest plugins/obsidian/skills/_shared/scripts/ -v` (requires `pyyaml` and `pytest` installed).

---

## File Structure

**Created:**
- `plugins/obsidian/skills/_shared/validation-rules.md` — authoritative description of all checks
- `plugins/obsidian/skills/_shared/scripts/validate.py` — deterministic checks (CLI + importable functions)
- `plugins/obsidian/skills/_shared/scripts/test_validate.py` — pytest suite
- `plugins/obsidian/skills/wiki-think/SKILL.md` — thinking-tools skill
- `plugins/obsidian/skills/wiki-think/references/thinking-modes.md`
- `plugins/obsidian/skills/wiki-maintain/SKILL.md` — non-interactive maintenance skill
- `plugins/obsidian/skills/wiki-maintain/references/cron-recipes.md`

**Modified:**
- `plugins/obsidian/skills/wiki-lint/SKILL.md` — delegate deterministic checks to `_shared`
- `plugins/obsidian/skills/wiki-ingest/SKILL.md` — pre-write gate + contradiction-reconcile
- `plugins/obsidian/skills/wiki-migrate-file/SKILL.md` — pre-write gate
- `plugins/obsidian/.claude-plugin/plugin.json` — version 1.4.0
- `.claude-plugin/marketplace.json` — obsidian entry to 1.4.0
- `plugins/obsidian/README.md` — new skills, dependency note, changelog
- `docs/plugins/index.md` — version line
- `CHANGELOG.md` — v1.4.0 entry

---

## Phase 1 — Foundation: the shared validator

### Task 1: Validator skeleton (parsing, normalization, index, dispatch)

**Files:**
- Create: `plugins/obsidian/skills/_shared/scripts/validate.py`
- Test: `plugins/obsidian/skills/_shared/scripts/test_validate.py`

**Interfaces:**
- Produces:
  - `parse_frontmatter(text: str) -> tuple[dict | None | str, str]` — returns `(fm, body)`; `fm` is a dict, `None` (no frontmatter), or the string `"INVALID"` (YAML error).
  - `normalize_link(inner: str) -> str` — `[[path/Target#anchor|alias]]` inner text → `"Target"`.
  - `normalize_ref(s: str) -> str` — a `related:` entry like `"[[Target|alias]]"` → `"Target"`.
  - `strip_code(text: str) -> str` — removes fenced and inline code spans.
  - `fm_related(fm: dict) -> list[str]` — normalizes the `related:` field to a list of raw strings.
  - `load_record(path: Path) -> dict` — `{path, fm, body, text}`.
  - `build_index(vault_root: Path) -> dict` — `{"names": set[str], "related": dict[str, set[str]]}`.
  - `register(name)` decorator + `CHECKS: dict[str, callable]` registry. Each check is `fn(records: list[dict], index: dict) -> list[dict]`.
  - `run(vault_root: Path, rules: list[str], target: Path | None) -> list[dict]`.

- [ ] **Step 1: Install test dependencies**

Run:
```bash
python3 -m pip install --quiet pyyaml pytest
```
Expected: completes without error (already-satisfied is fine).

- [ ] **Step 2: Write the failing test**

Create `plugins/obsidian/skills/_shared/scripts/test_validate.py`:
```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import validate as v


def test_parse_frontmatter_valid():
    text = "---\nkind: wiki\ntype: concept\n---\nbody here"
    fm, body = v.parse_frontmatter(text)
    assert fm == {"kind": "wiki", "type": "concept"}
    assert body.strip() == "body here"


def test_parse_frontmatter_none_when_absent():
    fm, body = v.parse_frontmatter("no frontmatter at all")
    assert fm is None


def test_parse_frontmatter_invalid_yaml():
    fm, _ = v.parse_frontmatter("---\nkind: : :\n bad\n---\nx")
    assert fm == "INVALID"


def test_normalize_link_strips_alias_path_anchor():
    assert v.normalize_link("_wiki/tools/Docling#setup|Docling") == "Docling"
    assert v.normalize_link("RAG") == "RAG"
    assert v.normalize_link("Target\\|alias") == "Target"


def test_normalize_ref_extracts_wikilink():
    assert v.normalize_ref('"[[TF-Obsidian-Plugin]]"') == "TF-Obsidian-Plugin"
    assert v.normalize_ref("[[A|b]]") == "A"


def test_strip_code_removes_fenced_and_inline():
    out = v.strip_code("a `[[x]]` b\n```\n[[y]]\n```\nc")
    assert "[[x]]" not in out
    assert "[[y]]" not in out


def test_build_index_collects_stems_and_related(tmp_path):
    wiki = tmp_path / "_wiki"
    wiki.mkdir()
    (wiki / "A.md").write_text(
        "---\nkind: wiki\ntype: concept\nrelated:\n  - \"[[B]]\"\n---\nx", encoding="utf-8"
    )
    (wiki / "B.md").write_text("---\nkind: wiki\ntype: concept\n---\nx", encoding="utf-8")
    raw = tmp_path / "_raw"
    raw.mkdir()
    (raw / "img.png").write_bytes(b"\x89PNG")
    index = v.build_index(tmp_path)
    assert "A" in index["names"] and "B" in index["names"] and "img" in index["names"]
    assert index["related"]["A"] == {"B"}


def test_run_returns_empty_when_no_rules_registered_match(tmp_path):
    (tmp_path / "_wiki").mkdir()
    assert v.run(tmp_path, rules=["nonexistent"], target=None) == []
```

- [ ] **Step 3: Run the tests to verify they fail**

Run: `python3 -m pytest plugins/obsidian/skills/_shared/scripts/test_validate.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'validate'`.

- [ ] **Step 4: Write the skeleton implementation**

Create `plugins/obsidian/skills/_shared/scripts/validate.py`:
```python
#!/usr/bin/env python3
"""Deterministic structural and link validation for the LLM-Wiki schema.

Importable functions are used by the obsidian plugin's wiki skills; the CLI
(`main`) prints a JSON array of findings. PyYAML is required; when absent the
CLI exits 2 with a JSON error so the calling skill can fall back to prose rules.
"""
import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # graceful degradation — see Global Constraints
    yaml = None

WIKI_TYPES = {"concept", "tool", "compare", "hub", "note", "thinking"}
SOURCE_TYPES = {"clipping", "chat", "note", "transcript"}
MEDIA_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".pdf", ".svg", ".mp4", ".mov"}

CHECKS = {}


def register(name):
    def deco(fn):
        CHECKS[name] = fn
        return fn
    return deco


def parse_frontmatter(text):
    if not text.startswith("---"):
        return None, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None, text
    try:
        fm = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return "INVALID", parts[2]
    if not isinstance(fm, dict):
        return None, parts[2]
    return fm, parts[2]


def strip_code(text):
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"`[^`\n]*`", "", text)
    return text


def normalize_link(inner):
    inner = inner.replace("\\|", "|").split("|")[0]
    inner = inner.split("#")[0]
    inner = inner.rsplit("/", 1)[-1]
    if inner.endswith(".md"):
        inner = inner[:-3]
    return inner.strip()


def normalize_ref(s):
    s = str(s).strip()
    m = re.search(r"\[\[([^\]]+)\]\]", s)
    if m:
        return normalize_link(m.group(1))
    return normalize_link(s)


def fm_related(fm):
    rel = fm.get("related")
    if rel is None:
        return []
    if isinstance(rel, str):
        return [rel]
    if isinstance(rel, list):
        return [str(x) for x in rel]
    return []


def load_record(path):
    text = path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    return {"path": path, "fm": fm, "body": body, "text": text}


def build_index(vault_root):
    names = set()
    related = {}
    wiki = vault_root / "_wiki"
    raw = vault_root / "_raw"
    for base in (wiki, raw):
        if base.exists():
            for p in base.rglob("*.md"):
                names.add(p.stem)
    for p in vault_root.rglob("*"):
        if p.is_file() and p.suffix.lower() in MEDIA_EXTS:
            names.add(p.stem)
    if wiki.exists():
        for p in wiki.rglob("*.md"):
            rec = load_record(p)
            if isinstance(rec["fm"], dict):
                related[p.stem] = {normalize_ref(r) for r in fm_related(rec["fm"])}
    return {"names": names, "related": related}


def _scope_records(vault_root, target):
    if target is not None:
        return [load_record(target)]
    records = []
    for sub in ("_wiki", "_raw"):
        base = vault_root / sub
        if base.exists():
            for p in sorted(base.rglob("*.md")):
                records.append(load_record(p))
    return records


def run(vault_root, rules, target):
    index = build_index(vault_root)
    records = _scope_records(vault_root, target)
    findings = []
    for name in rules:
        fn = CHECKS.get(name)
        if fn:
            findings.extend(fn(records, index))
    return findings


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate LLM-Wiki files.")
    parser.add_argument("--vault-root", required=True)
    parser.add_argument("--target", default=None)
    parser.add_argument("--rules", default=",".join(CHECKS.keys()))
    parser.add_argument("--format", default="json", choices=["json"])
    args = parser.parse_args(argv)
    if yaml is None:
        print(json.dumps({"error": "PyYAML not installed", "fallback": "prose"}))
        return 2
    rules = [r.strip() for r in args.rules.split(",") if r.strip()]
    target = Path(args.target) if args.target else None
    findings = run(Path(args.vault_root), rules, target)
    print(json.dumps([{**f, "file": str(f["file"])} for f in findings], indent=2))
    return 1 if any(f["severity"] == "critical" for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 5: Run the tests to verify they pass**

Run: `python3 -m pytest plugins/obsidian/skills/_shared/scripts/test_validate.py -v`
Expected: PASS (8 tests).

- [ ] **Step 6: Commit**

```bash
git add plugins/obsidian/skills/_shared/scripts/validate.py plugins/obsidian/skills/_shared/scripts/test_validate.py
git commit -m "✨ feat(obsidian): scaffold shared wiki validator (parsing, index, dispatch)"
```

---

### Task 2: Frontmatter completeness check

**Files:**
- Modify: `plugins/obsidian/skills/_shared/scripts/validate.py` (append check)
- Modify: `plugins/obsidian/skills/_shared/scripts/test_validate.py` (append tests)

**Interfaces:**
- Consumes: `register`, `load_record`, finding schema from Task 1.
- Produces: a `"frontmatter"` entry in `CHECKS`. Emits `critical` findings for missing/invalid frontmatter and for each missing required field. Required = `kind, type, title, domain, status, tags, created`; plus `updated` when `kind == wiki`; plus `ingested` when `kind == source`. `_wiki/log.md` is exempt. Missing `created`/`domain` are marked `autofixable: True`.

- [ ] **Step 1: Write the failing tests**

Append to `test_validate.py`:
```python
def _rec(tmp_path, name, fm_text, body="x"):
    sub = tmp_path / "_wiki"
    sub.mkdir(exist_ok=True)
    p = sub / name
    p.write_text(f"---\n{fm_text}\n---\n{body}", encoding="utf-8")
    return v.load_record(p)


def test_frontmatter_flags_missing_required(tmp_path):
    rec = _rec(tmp_path, "A.md", "kind: wiki\ntype: concept\ntitle: A")
    findings = v.CHECKS["frontmatter"]([rec], {"names": set(), "related": {}})
    missing = {f["message"] for f in findings}
    assert any("domain" in m for m in missing)
    assert all(f["severity"] == "critical" for f in findings)


def test_frontmatter_wiki_requires_updated(tmp_path):
    fm = "kind: wiki\ntype: concept\ntitle: A\ndomain: d\nstatus: active\ntags: [x]\ncreated: 2026-01-01"
    rec = _rec(tmp_path, "A.md", fm)
    findings = v.CHECKS["frontmatter"]([rec], {"names": set(), "related": {}})
    assert any("updated" in f["message"] for f in findings)


def test_frontmatter_source_requires_ingested_not_updated(tmp_path):
    fm = "kind: source\ntype: clipping\ntitle: A\ndomain: d\nstatus: active\ntags: [x]\ncreated: 2026-01-01"
    rec = _rec(tmp_path, "A.md", fm)
    findings = v.CHECKS["frontmatter"]([rec], {"names": set(), "related": {}})
    msgs = {f["message"] for f in findings}
    assert any("ingested" in m for m in msgs)
    assert not any("updated" in m for m in msgs)


def test_frontmatter_complete_wiki_is_clean(tmp_path):
    fm = ("kind: wiki\ntype: concept\ntitle: A\ndomain: d\nstatus: active\n"
          "tags: [x]\ncreated: 2026-01-01\nupdated: 2026-01-02")
    rec = _rec(tmp_path, "A.md", fm)
    findings = v.CHECKS["frontmatter"]([rec], {"names": set(), "related": {}})
    assert findings == []


def test_frontmatter_log_md_is_exempt(tmp_path):
    sub = tmp_path / "_wiki"
    sub.mkdir(exist_ok=True)
    p = sub / "log.md"
    p.write_text("## [2026-01-01] ingest\n- x", encoding="utf-8")
    rec = v.load_record(p)
    assert v.CHECKS["frontmatter"]([rec], {"names": set(), "related": {}}) == []


def test_frontmatter_missing_block_is_critical(tmp_path):
    sub = tmp_path / "_wiki"
    sub.mkdir(exist_ok=True)
    p = sub / "A.md"
    p.write_text("no frontmatter", encoding="utf-8")
    rec = v.load_record(p)
    findings = v.CHECKS["frontmatter"]([rec], {"names": set(), "related": {}})
    assert findings and findings[0]["severity"] == "critical"
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m pytest plugins/obsidian/skills/_shared/scripts/test_validate.py -k frontmatter -v`
Expected: FAIL — `KeyError: 'frontmatter'`.

- [ ] **Step 3: Implement the check**

Append to `validate.py` (above `def main`):
```python
REQUIRED = ["kind", "type", "title", "domain", "status", "tags", "created"]
AUTOFIXABLE_FIELDS = {"created", "domain"}


@register("frontmatter")
def check_frontmatter(records, index):
    findings = []
    for rec in records:
        if rec["path"].name == "log.md":
            continue
        fm = rec["fm"]
        if fm is None or fm == "INVALID":
            findings.append({
                "file": rec["path"],
                "severity": "critical",
                "rule": "frontmatter",
                "message": "missing or invalid YAML frontmatter",
                "autofixable": False,
            })
            continue
        required = list(REQUIRED)
        if fm.get("kind") == "wiki":
            required.append("updated")
        elif fm.get("kind") == "source":
            required.append("ingested")
        for field in required:
            if field not in fm or fm[field] in (None, ""):
                findings.append({
                    "file": rec["path"],
                    "severity": "critical",
                    "rule": "frontmatter",
                    "message": f"missing required field: {field}",
                    "autofixable": field in AUTOFIXABLE_FIELDS,
                })
    return findings
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python3 -m pytest plugins/obsidian/skills/_shared/scripts/test_validate.py -k frontmatter -v`
Expected: PASS (6 tests).

- [ ] **Step 5: Commit**

```bash
git add plugins/obsidian/skills/_shared/scripts/validate.py plugins/obsidian/skills/_shared/scripts/test_validate.py
git commit -m "✨ feat(obsidian): add frontmatter completeness check to validator"
```

---

### Task 3: kind/type consistency check (includes `type: thinking`)

**Files:**
- Modify: `plugins/obsidian/skills/_shared/scripts/validate.py`
- Modify: `plugins/obsidian/skills/_shared/scripts/test_validate.py`

**Interfaces:**
- Consumes: `register`, `WIKI_TYPES`, `SOURCE_TYPES` from Task 1.
- Produces: a `"kindtype"` entry in `CHECKS`. `critical` when `kind` is not `wiki`/`source`, or when `type` is outside the allowed set for that `kind`. Records with no/invalid frontmatter are skipped (Task 2 already reports those). `log.md` exempt.

- [ ] **Step 1: Write the failing tests**

Append to `test_validate.py`:
```python
def test_kindtype_accepts_thinking(tmp_path):
    rec = _rec(tmp_path, "A.md", "kind: wiki\ntype: thinking\ntitle: A")
    assert v.CHECKS["kindtype"]([rec], {"names": set(), "related": {}}) == []


def test_kindtype_rejects_bad_wiki_type(tmp_path):
    rec = _rec(tmp_path, "A.md", "kind: wiki\ntype: clipping\ntitle: A")
    findings = v.CHECKS["kindtype"]([rec], {"names": set(), "related": {}})
    assert findings and findings[0]["severity"] == "critical"


def test_kindtype_rejects_unknown_kind(tmp_path):
    rec = _rec(tmp_path, "A.md", "kind: banana\ntype: concept\ntitle: A")
    findings = v.CHECKS["kindtype"]([rec], {"names": set(), "related": {}})
    assert findings and "kind" in findings[0]["message"]


def test_kindtype_skips_missing_frontmatter(tmp_path):
    sub = tmp_path / "_wiki"
    sub.mkdir(exist_ok=True)
    p = sub / "A.md"
    p.write_text("no fm", encoding="utf-8")
    rec = v.load_record(p)
    assert v.CHECKS["kindtype"]([rec], {"names": set(), "related": {}}) == []
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m pytest plugins/obsidian/skills/_shared/scripts/test_validate.py -k kindtype -v`
Expected: FAIL — `KeyError: 'kindtype'`.

- [ ] **Step 3: Implement the check**

Append to `validate.py` (above `def main`):
```python
@register("kindtype")
def check_kindtype(records, index):
    findings = []
    for rec in records:
        if rec["path"].name == "log.md":
            continue
        fm = rec["fm"]
        if not isinstance(fm, dict):
            continue
        kind = fm.get("kind")
        typ = fm.get("type")
        if kind == "wiki":
            allowed = WIKI_TYPES
        elif kind == "source":
            allowed = SOURCE_TYPES
        else:
            findings.append({
                "file": rec["path"],
                "severity": "critical",
                "rule": "kindtype",
                "message": f"invalid kind: {kind!r} (expected wiki or source)",
                "autofixable": False,
            })
            continue
        if typ not in allowed:
            findings.append({
                "file": rec["path"],
                "severity": "critical",
                "rule": "kindtype",
                "message": f"invalid type {typ!r} for kind {kind} (allowed: {sorted(allowed)})",
                "autofixable": False,
            })
    return findings
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python3 -m pytest plugins/obsidian/skills/_shared/scripts/test_validate.py -k kindtype -v`
Expected: PASS (4 tests).

- [ ] **Step 5: Commit**

```bash
git add plugins/obsidian/skills/_shared/scripts/validate.py plugins/obsidian/skills/_shared/scripts/test_validate.py
git commit -m "✨ feat(obsidian): add kind/type consistency check incl. thinking type"
```

---

### Task 4: Dead-link check (normalization, code-skipping, report exemptions)

**Files:**
- Modify: `plugins/obsidian/skills/_shared/scripts/validate.py`
- Modify: `plugins/obsidian/skills/_shared/scripts/test_validate.py`

**Interfaces:**
- Consumes: `register`, `strip_code`, `normalize_link`, `build_index` (`index["names"]`).
- Produces: a `"deadlinks"` entry in `CHECKS`. For each `[[X]]` in the body (after `strip_code`), if `normalize_link(X)` is not in `index["names"]`, emit a `minor` finding. Skip `log.md`, `lint-report-*.md`, and `maintain-report-*.md`.

- [ ] **Step 1: Write the failing tests**

Append to `test_validate.py`:
```python
def test_deadlinks_flags_missing_target(tmp_path):
    rec = _rec(tmp_path, "A.md", "kind: wiki\ntype: concept\ntitle: A", body="see [[Ghost]]")
    findings = v.CHECKS["deadlinks"]([rec], {"names": {"A"}, "related": {}})
    assert findings and findings[0]["severity"] == "minor"
    assert "Ghost" in findings[0]["message"]


def test_deadlinks_resolves_alias_and_path(tmp_path):
    rec = _rec(tmp_path, "A.md", "kind: wiki\ntype: concept\ntitle: A",
               body="[[_wiki/tools/Docling|Docling]] and [[RAG#intro]]")
    findings = v.CHECKS["deadlinks"]([rec], {"names": {"A", "Docling", "RAG"}, "related": {}})
    assert findings == []


def test_deadlinks_skips_code_spans(tmp_path):
    rec = _rec(tmp_path, "A.md", "kind: wiki\ntype: concept\ntitle: A",
               body="inline `[[vm]]` and\n```\n[[fenced]]\n```")
    assert v.CHECKS["deadlinks"]([rec], {"names": {"A"}, "related": {}}) == []


def test_deadlinks_exempts_reports_and_log(tmp_path):
    sub = tmp_path / "_wiki"
    sub.mkdir(exist_ok=True)
    for name in ("log.md", "lint-report-2026-01-01.md", "maintain-report-2026-01-01.md"):
        p = sub / name
        p.write_text("see [[Ghost]]", encoding="utf-8")
        rec = v.load_record(p)
        assert v.CHECKS["deadlinks"]([rec], {"names": set(), "related": {}}) == []
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m pytest plugins/obsidian/skills/_shared/scripts/test_validate.py -k deadlinks -v`
Expected: FAIL — `KeyError: 'deadlinks'`.

- [ ] **Step 3: Implement the check**

Append to `validate.py` (above `def main`):
```python
def _is_report_or_log(name):
    return (name == "log.md"
            or name.startswith("lint-report-")
            or name.startswith("maintain-report-"))


@register("deadlinks")
def check_deadlinks(records, index):
    findings = []
    for rec in records:
        if _is_report_or_log(rec["path"].name):
            continue
        body = strip_code(rec["body"] or "")
        for inner in re.findall(r"\[\[([^\]]+)\]\]", body):
            target = normalize_link(inner)
            if not target:
                continue
            if target not in index["names"]:
                findings.append({
                    "file": rec["path"],
                    "severity": "minor",
                    "rule": "deadlinks",
                    "message": f"dead wikilink: [[{target}]]",
                    "autofixable": False,
                })
    return findings
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python3 -m pytest plugins/obsidian/skills/_shared/scripts/test_validate.py -k deadlinks -v`
Expected: PASS (4 tests).

- [ ] **Step 5: Commit**

```bash
git add plugins/obsidian/skills/_shared/scripts/validate.py plugins/obsidian/skills/_shared/scripts/test_validate.py
git commit -m "✨ feat(obsidian): add dead-link check with normalization and exemptions"
```

---

### Task 5: Asymmetric `related:` check

**Files:**
- Modify: `plugins/obsidian/skills/_shared/scripts/validate.py`
- Modify: `plugins/obsidian/skills/_shared/scripts/test_validate.py`

**Interfaces:**
- Consumes: `register`, `build_index` (`index["related"]`: `dict[stem -> set[normalized refs]]`).
- Produces: an `"asymmetric"` entry in `CHECKS`. For each record with a wiki stem, for each `ref` in `index["related"][stem]`: if `ref` is itself a known wiki stem (a key in `index["related"]`) and `stem` is not in `index["related"][ref]`, emit a `minor`, `autofixable: True` finding. Refs to non-wiki targets (raw sources, media) are ignored.

- [ ] **Step 1: Write the failing tests**

Append to `test_validate.py`:
```python
def test_asymmetric_flags_one_way_link(tmp_path):
    sub = tmp_path / "_wiki"
    sub.mkdir(exist_ok=True)
    (sub / "A.md").write_text(
        "---\nkind: wiki\ntype: concept\nrelated:\n  - \"[[B]]\"\n---\nx", encoding="utf-8")
    (sub / "B.md").write_text("---\nkind: wiki\ntype: concept\n---\nx", encoding="utf-8")
    index = v.build_index(tmp_path)
    rec = v.load_record(sub / "A.md")
    findings = v.CHECKS["asymmetric"]([rec], index)
    assert findings and findings[0]["severity"] == "minor"
    assert findings[0]["autofixable"] is True


def test_asymmetric_clean_when_bidirectional(tmp_path):
    sub = tmp_path / "_wiki"
    sub.mkdir(exist_ok=True)
    (sub / "A.md").write_text(
        "---\nkind: wiki\ntype: concept\nrelated:\n  - \"[[B]]\"\n---\nx", encoding="utf-8")
    (sub / "B.md").write_text(
        "---\nkind: wiki\ntype: concept\nrelated:\n  - \"[[A]]\"\n---\nx", encoding="utf-8")
    index = v.build_index(tmp_path)
    rec = v.load_record(sub / "A.md")
    assert v.CHECKS["asymmetric"]([rec], index) == []


def test_asymmetric_ignores_non_wiki_refs(tmp_path):
    sub = tmp_path / "_wiki"
    sub.mkdir(exist_ok=True)
    (sub / "A.md").write_text(
        "---\nkind: wiki\ntype: concept\nrelated:\n  - \"[[some-raw-source]]\"\n---\nx",
        encoding="utf-8")
    index = v.build_index(tmp_path)
    rec = v.load_record(sub / "A.md")
    assert v.CHECKS["asymmetric"]([rec], index) == []
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m pytest plugins/obsidian/skills/_shared/scripts/test_validate.py -k asymmetric -v`
Expected: FAIL — `KeyError: 'asymmetric'`.

- [ ] **Step 3: Implement the check**

Append to `validate.py` (above `def main`):
```python
@register("asymmetric")
def check_asymmetric(records, index):
    findings = []
    related = index["related"]
    for rec in records:
        if not isinstance(rec["fm"], dict):
            continue
        stem = rec["path"].stem
        for ref in related.get(stem, set()):
            if ref in related and stem not in related[ref]:
                findings.append({
                    "file": rec["path"],
                    "severity": "minor",
                    "rule": "asymmetric",
                    "message": f"asymmetric related: [[{ref}]] does not link back to [[{stem}]]",
                    "autofixable": True,
                })
    return findings
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python3 -m pytest plugins/obsidian/skills/_shared/scripts/test_validate.py -k asymmetric -v`
Expected: PASS (3 tests).

- [ ] **Step 5: Commit**

```bash
git add plugins/obsidian/skills/_shared/scripts/validate.py plugins/obsidian/skills/_shared/scripts/test_validate.py
git commit -m "✨ feat(obsidian): add asymmetric related-field check to validator"
```

---

### Task 6: End-to-end CLI behaviour (scope, --rules, --target, exit codes)

**Files:**
- Modify: `plugins/obsidian/skills/_shared/scripts/test_validate.py`
- (No `validate.py` change expected — this task verifies the wiring from Task 1 against all registered checks. If a test fails, fix `main`/`run`/`_scope_records` minimally.)

**Interfaces:**
- Consumes: `main(argv)`, `run(...)` from Task 1; all checks from Tasks 2–5.

- [ ] **Step 1: Write the failing tests**

Append to `test_validate.py`:
```python
import json as _json


def _make_vault(tmp_path):
    wiki = tmp_path / "_wiki"
    wiki.mkdir()
    (wiki / "Good.md").write_text(
        "---\nkind: wiki\ntype: concept\ntitle: Good\ndomain: d\nstatus: active\n"
        "tags: [x]\ncreated: 2026-01-01\nupdated: 2026-01-02\n---\nbody", encoding="utf-8")
    (wiki / "Bad.md").write_text(
        "---\nkind: wiki\ntype: concept\ntitle: Bad\n---\nsee [[Ghost]]", encoding="utf-8")
    return tmp_path


def test_run_all_rules_finds_bad_file(tmp_path):
    vault = _make_vault(tmp_path)
    findings = v.run(vault, rules=list(v.CHECKS.keys()), target=None)
    files = {f["file"].name for f in findings}
    assert "Bad.md" in files
    assert "Good.md" not in files


def test_run_target_limits_scope(tmp_path):
    vault = _make_vault(tmp_path)
    findings = v.run(vault, rules=list(v.CHECKS.keys()), target=vault / "_wiki" / "Good.md")
    assert findings == []


def test_main_emits_json_and_exit_code(tmp_path, capsys):
    vault = _make_vault(tmp_path)
    code = v.main(["--vault-root", str(vault), "--rules", "frontmatter"])
    out = capsys.readouterr().out
    data = _json.loads(out)
    assert isinstance(data, list)
    assert all("file" in d and isinstance(d["file"], str) for d in data)
    assert code == 1  # Bad.md has critical frontmatter findings
```

- [ ] **Step 2: Run the tests to verify status**

Run: `python3 -m pytest plugins/obsidian/skills/_shared/scripts/test_validate.py -k "run_ or main_" -v`
Expected: PASS if Task 1 wiring is correct. If any FAIL, fix `run`/`_scope_records`/`main` in `validate.py` minimally, then re-run until PASS.

- [ ] **Step 3: Run the full suite**

Run: `python3 -m pytest plugins/obsidian/skills/_shared/scripts/ -v`
Expected: PASS (all tests across Tasks 1–6).

- [ ] **Step 4: Commit**

```bash
git add plugins/obsidian/skills/_shared/scripts/validate.py plugins/obsidian/skills/_shared/scripts/test_validate.py
git commit -m "🧪 test(obsidian): cover validator CLI scope, rules, and exit codes"
```

---

### Task 7: Authoritative `validation-rules.md`

**Files:**
- Create: `plugins/obsidian/skills/_shared/validation-rules.md`

**Interfaces:**
- Consumes: nothing (prose reference).
- Produces: the single source of truth that `wiki-lint`, `wiki-ingest`, `wiki-migrate-file`, and `wiki-maintain` cite. Documents which rules are deterministic (run via `validate.py`) and which are semantic (LLM judgement).

- [ ] **Step 1: Write the file**

Create `plugins/obsidian/skills/_shared/validation-rules.md`:
```markdown
# LLM-Wiki Validation Rules (shared)

Single source of truth for wiki validation. The deterministic rules are
implemented in `scripts/validate.py`; the semantic rules are applied by the
calling skill via LLM judgement. Skills MUST cite this file rather than
re-stating rules inline, to prevent drift.

## How to run the deterministic checks

```bash
python3 <plugin>/skills/_shared/scripts/validate.py \
  --vault-root <vault-root> [--target <file.md>] [--rules frontmatter,kindtype,deadlinks,asymmetric]
```

Output is a JSON array of findings: `{file, severity, rule, message, autofixable}`,
`severity ∈ {critical, minor}`. Exit code `1` when any finding is `critical`,
`0` otherwise, `2` when PyYAML is missing (fall back to the prose rules below).

## Severity policy

- **critical** — blocks plugin-driven writes until fixed or user-confirmed:
  missing/invalid frontmatter, missing required field, invalid `kind`/`type`.
- **minor** — reported, never blocks: dead links (may be legitimate forward
  references), asymmetric `related:` fields.

## Deterministic rules (validate.py)

1. **Frontmatter completeness.** Required for all: `kind, type, title, domain,
   status, tags, created`. Wiki pages also require `updated`; sources require
   `ingested` (not `updated`). `_wiki/log.md` is exempt. Missing `created`/`domain`
   are auto-fixable (derive `created` from git, set `domain` from the vault).
2. **`kind`/`type` consistency.** `kind: wiki` → `type ∈ {concept, tool, compare,
   hub, note, thinking}`. `kind: source` → `type ∈ {clipping, chat, note,
   transcript}`.
3. **Dead links.** Wikilinks `[[X]]` must resolve against `_wiki/`/`_raw/` basenames
   or vault media files. Normalize: strip alias (`[[T|a]]`, `[[T\|a]]`), strip
   `#anchor`, resolve full paths by basename, drop `.md`. Skip links inside inline
   code or fenced code blocks. Skip `log.md`, `lint-report-*.md`, `maintain-report-*.md`.
4. **Asymmetric `related:`.** If `A.related` resolves to wiki page `B`, then
   `B.related` must resolve back to `A`. Refs to non-wiki targets are ignored.
   Auto-fixable (add the missing back-reference).

## Semantic rules (LLM judgement, not in validate.py)

5. **Stale claims.** A wiki page whose `updated` is older than six months while a
   `sources:` entry has an `ingested` date newer than `last_synthesized`.
6. **Contradiction detection.** Pages that share an entity in `related:` but make
   conflicting claims. On ingest, this triggers Contradiction-Reconcile.
7. **Hub gaps.** Five or more pages sharing a tag/theme with no `type: hub` page.
8. **Source gaps.** A wiki page with empty `sources:` that asserts factual claims.
   `type: thinking` pages are EXEMPT — derived reasoning is not a factual assertion,
   so an empty `sources:` is allowed.

## Template compliance (semantic)

- `type: tool` → `## Setup` heading (informational only for hosted/hardware tools).
- `type: compare` → a table under `## Options` or `## Direktvergleich`.
- `type: hub` → all five sections: `## Overview`, `## Concepts`, `## Tools`,
  `## Compare Pages`, `## Related Hubs`.
```

- [ ] **Step 2: Verify the file is valid Markdown and self-consistent**

Run: `python3 -c "import pathlib; t=pathlib.Path('plugins/obsidian/skills/_shared/validation-rules.md').read_text(); assert 'thinking' in t and 'validate.py' in t; print('ok')"`
Expected: `ok`.

- [ ] **Step 3: Commit**

```bash
git add plugins/obsidian/skills/_shared/validation-rules.md
git commit -m "📚 docs(obsidian): add shared LLM-Wiki validation rules reference"
```

---

## Phase 2 — Refactor wiki-lint onto the shared module

### Task 8: wiki-lint delegates deterministic checks to `_shared`

**Files:**
- Modify: `plugins/obsidian/skills/wiki-lint/SKILL.md`

**Interfaces:**
- Consumes: `_shared/validation-rules.md`, `_shared/scripts/validate.py`.
- Produces: a `wiki-lint` that runs `validate.py` for deterministic findings and keeps the semantic checks, citing the shared rules. Report format and log entry are unchanged (regression-safe).

- [ ] **Step 1: Replace the "Structural / Linking Checks" sections with delegation**

In `plugins/obsidian/skills/wiki-lint/SKILL.md`, replace the `### Structural Checks` and `### Linking Checks` blocks (the numbered items 1–6) with:
```markdown
### Deterministic Checks (shared validator)

Run the shared validator over the whole wiki and parse its JSON findings:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/validate.py" \
  --vault-root "<wiki-root>/.." --rules frontmatter,kindtype,deadlinks,asymmetric
```

If the validator exits with code 2 (PyYAML missing), fall back to applying the
deterministic rules manually from `${CLAUDE_PLUGIN_ROOT}/skills/_shared/validation-rules.md`.

Map findings into the report: `critical` findings go under **Critical Issues**
(Structural for `frontmatter`/`kindtype`, Linking for `deadlinks`/`asymmetric`);
`minor` findings go under **Minor Issues**. All rule definitions live in
`_shared/validation-rules.md` — do not restate them here.
```

(Note: if `${CLAUDE_PLUGIN_ROOT}` is unavailable in the runtime, resolve the path relative to this skill: `../_shared/scripts/validate.py`.)

- [ ] **Step 2: Point the remaining content checks at the shared reference**

In the same file, replace the `### Content Checks`, `### Tag Discipline`, `### Hub Suggestions`, and `### Source Gaps` numbered items with a citation:
```markdown
### Semantic Checks (LLM judgement)

Apply semantic rules 5–8 and template-compliance from
`${CLAUDE_PLUGIN_ROOT}/skills/_shared/validation-rules.md` (stale claims,
contradiction detection, hub gaps, source gaps — `type: thinking` exempt from
source gaps). Keep the Tag Discipline checks (singleton tags, status-as-tag) and
the Migration Backlog soft-cap check as they are today.
```

Leave the `## Auto-Fix Mode`, `## Output`, and log-entry sections unchanged.

- [ ] **Step 3: Verify frontmatter still parses and the skill loads**

Run:
```bash
python3 -c "import pathlib,yaml; t=pathlib.Path('plugins/obsidian/skills/wiki-lint/SKILL.md').read_text(); fm=t.split('---')[1]; d=yaml.safe_load(fm); assert d['name']=='wiki-lint' and d.get('description'); print('ok')"
```
Expected: `ok`.

- [ ] **Step 4: Regression smoke test (manual)**

Run `claude --plugin-dir ./plugins/obsidian`, then in-session run `/wiki:lint` against a known vault. Confirm the report still lists the same families of issues (frontmatter, dead links, asymmetric, stale, hub) as the last committed `lint-report-*.md`. Note any divergence; deterministic findings should now be a consistent subset.

- [ ] **Step 5: Commit**

```bash
git add plugins/obsidian/skills/wiki-lint/SKILL.md
git commit -m "♻️ refactor(obsidian): wiki-lint delegates deterministic checks to _shared"
```

---

## Phase 3 — Write-time validation gate

### Task 9: wiki-ingest pre-write validation gate

**Files:**
- Modify: `plugins/obsidian/skills/wiki-ingest/SKILL.md`

**Interfaces:**
- Consumes: `_shared/scripts/validate.py`.
- Produces: a wiki-ingest whose "write or update wiki pages" step validates each touched file after writing and blocks completion on unresolved `critical` findings.

- [ ] **Step 1: Insert the validation gate into the write step**

In `plugins/obsidian/skills/wiki-ingest/SKILL.md`, immediately after step 4 ("Write or update wiki pages …"), insert a new step:
```markdown
4a. **Validate before finalizing (write-time gate).** After writing each touched
    wiki/raw file, run the shared validator on it:

    ```bash
    python3 "${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/validate.py" \
      --vault-root "<wiki-root>/.." --target "<touched-file>" \
      --rules frontmatter,kindtype,deadlinks,asymmetric
    ```

    - **critical** findings: fix them (auto-fixable ones — `created`, `domain`,
      asymmetric back-refs — apply directly; others surface to the user with the
      finding text), then re-validate. Do NOT report the page as ingested while a
      critical finding remains.
    - **minor** findings: include them in the final summary; do not block.
    - Validator exit code 2 (PyYAML missing): fall back to the deterministic rules
      in `${CLAUDE_PLUGIN_ROOT}/skills/_shared/validation-rules.md` and continue.
```

- [ ] **Step 2: Reference the gate in the Output section**

In the `## Output` section of the same file, add a bullet:
```markdown
- Validation summary: critical findings resolved, minor findings listed
```

- [ ] **Step 3: Verify frontmatter parses**

Run:
```bash
python3 -c "import pathlib,yaml; t=pathlib.Path('plugins/obsidian/skills/wiki-ingest/SKILL.md').read_text(); d=yaml.safe_load(t.split('---')[1]); assert d['name']=='wiki-ingest'; print('ok')"
```
Expected: `ok`.

- [ ] **Step 4: Commit**

```bash
git add plugins/obsidian/skills/wiki-ingest/SKILL.md
git commit -m "✨ feat(obsidian): add write-time validation gate to wiki-ingest"
```

---

### Task 10: wiki-migrate-file pre-write validation gate

**Files:**
- Modify: `plugins/obsidian/skills/wiki-migrate-file/SKILL.md`

**Interfaces:**
- Consumes: `_shared/scripts/validate.py`.
- Produces: a wiki-migrate-file that validates the migrated target file(s) before declaring the migration complete.

- [ ] **Step 1: Read the file to locate the write step**

Run: `sed -n '1,200p' plugins/obsidian/skills/wiki-migrate-file/SKILL.md`
Expected: shows the workflow; identify the step where target wiki/raw files are written.

- [ ] **Step 2: Insert the validation gate after the write step**

Add, immediately after the step that writes the migrated target files:
```markdown
**Validate before finalizing (write-time gate).** Run the shared validator on each
written target file:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/validate.py" \
  --vault-root "<wiki-root>/.." --target "<written-file>" \
  --rules frontmatter,kindtype,deadlinks,asymmetric
```

Resolve all **critical** findings before deleting the original legacy file; list
**minor** findings in the summary. On validator exit code 2, fall back to the
deterministic rules in `${CLAUDE_PLUGIN_ROOT}/skills/_shared/validation-rules.md`.
Never delete the original until the migrated file is free of critical findings.
```

- [ ] **Step 3: Verify frontmatter parses**

Run:
```bash
python3 -c "import pathlib,yaml; t=pathlib.Path('plugins/obsidian/skills/wiki-migrate-file/SKILL.md').read_text(); d=yaml.safe_load(t.split('---')[1]); assert d['name']=='wiki-migrate-file'; print('ok')"
```
Expected: `ok`.

- [ ] **Step 4: Commit**

```bash
git add plugins/obsidian/skills/wiki-migrate-file/SKILL.md
git commit -m "✨ feat(obsidian): add write-time validation gate to wiki-migrate-file"
```

---

## Phase 4 — Contradiction-Reconcile

### Task 11: wiki-ingest contradiction propose-and-confirm

**Files:**
- Modify: `plugins/obsidian/skills/wiki-ingest/SKILL.md`

**Interfaces:**
- Consumes: the existing "update instead of creating" edge case; `_shared/validation-rules.md` semantic rule 6.
- Produces: a propose-and-confirm reconcile flow that replaces the prior "flag in the lint report" edge case.

- [ ] **Step 1: Replace the contradiction edge case with the reconcile flow**

In `plugins/obsidian/skills/wiki-ingest/SKILL.md`, in the `## Edge Cases` section, replace the bullet beginning "**Wiki page on this topic already exists:**" with:
```markdown
- **Wiki page on this topic already exists:** update instead of creating. When the
  new source contradicts an existing claim on the page (semantic rule 6 in
  `${CLAUDE_PLUGIN_ROOT}/skills/_shared/validation-rules.md`), run
  **Contradiction-Reconcile** before writing:
    1. Present both sides explicitly:
       `OLD: "<claim>" (sources: …)` vs. `NEW: "<claim>" (source: <new source>)`.
    2. Propose a concrete resolved wording, noting whether the old claim is
       superseded (and add a timeline note if the page tracks one).
    3. Ask the user to confirm.
       - **Confirm** → revise the page with the resolved wording; log
         `reconcile | <old> → <new>`.
       - **Reject** → do not overwrite; add a contradiction callout to the page
         (`> [!warning] Contradiction: …`) and log `contradiction-flagged`.
    Never silently overwrite a curated claim.
```

- [ ] **Step 2: Add a reconcile note to the log-entry template**

In the same file's step 7 (log entry), add a line to the example log block so reconciles are recorded:
```markdown
    - reconcile: <none | "<old> → <new>" | contradiction-flagged>
```

- [ ] **Step 3: Verify frontmatter parses and reconcile text is present**

Run:
```bash
python3 -c "import pathlib,yaml; t=pathlib.Path('plugins/obsidian/skills/wiki-ingest/SKILL.md').read_text(); d=yaml.safe_load(t.split('---')[1]); assert d['name']=='wiki-ingest'; assert 'Contradiction-Reconcile' in t; print('ok')"
```
Expected: `ok`.

- [ ] **Step 4: Commit**

```bash
git add plugins/obsidian/skills/wiki-ingest/SKILL.md
git commit -m "✨ feat(obsidian): add contradiction propose-and-confirm to wiki-ingest"
```

---

## Phase 5 — New skills

### Task 12: wiki-maintain skill + cron recipes

**Files:**
- Create: `plugins/obsidian/skills/wiki-maintain/SKILL.md`
- Create: `plugins/obsidian/skills/wiki-maintain/references/cron-recipes.md`

**Interfaces:**
- Consumes: `_shared/scripts/validate.py`, `_shared/validation-rules.md`, the existing `wiki-lint` auto-fix conventions.
- Produces: a non-interactive `/wiki:maintain [--auto-fix] [--quiet]` skill and a documented scheduling recipe.

- [ ] **Step 1: Write the SKILL.md**

Create `plugins/obsidian/skills/wiki-maintain/SKILL.md`:
```markdown
---
name: wiki-maintain
description: Runs non-interactive maintenance on an Obsidian-based LLM knowledge wiki — deterministic validation, semantic health checks, trivial auto-fixes, and a written report. Built to be scheduled (cron/launchd). Triggers when the user runs /wiki:maintain, asks to "run wiki maintenance", or "auto-fix the wiki".
---

# wiki-maintain

## When to invoke

The user runs `/wiki:maintain [--auto-fix] [--quiet]`, asks to run wiki
maintenance, or schedules it (see `references/cron-recipes.md`). Unlike
`wiki-lint` (read-only, interactive), this skill applies trivial fixes and is
safe to run unattended.

## Configuration

Same vault layout as `wiki-ingest`/`wiki-lint`. Rules live in
`${CLAUDE_PLUGIN_ROOT}/skills/_shared/validation-rules.md`.

## Flags

- `--auto-fix` — apply trivial, reversible fixes (asymmetric back-references,
  missing `created` from git, missing `domain` from the vault). Default off.
- `--quiet` — non-interactive: no prompts, one stdout line, machine-readable exit
  code. Required for cron. Implies that destructive operations are skipped.

## Workflow

1. **Deterministic pass.** Run the shared validator over the whole wiki:

    ```bash
    python3 "${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/validate.py" \
      --vault-root "<wiki-root>/.." --rules frontmatter,kindtype,deadlinks,asymmetric
    ```

    On validator exit code 2 (PyYAML missing), fall back to the deterministic
    rules in the shared reference and continue.

2. **Semantic pass.** Apply semantic rules 5–8 from the shared reference (stale
   claims, contradiction detection, hub gaps, source gaps — `type: thinking`
   exempt from source gaps).

3. **Auto-fix (only with `--auto-fix`).** Apply trivial fixes for findings whose
   `autofixable` is true. In interactive mode, show a diff per fix and confirm; in
   `--quiet` mode, apply auto-fixable findings directly and record them. Never
   perform destructive contradiction reconciles in `--quiet` mode — those require
   confirmation and only happen interactively in `wiki-ingest`.

4. **Write the report** to `<wiki-root>/_wiki/maintain-report-YYYY-MM-DD.md` with
   frontmatter `kind: wiki, type: note`, summarizing files checked, findings by
   severity, and fixes applied.

5. **Append a log entry** to `<wiki-root>/_wiki/log.md`:

    ```text
    ## [YYYY-MM-DD HH:MM] maintain | <report-name>
    - findings: M (X critical, Y minor)
    - auto-fixes applied: K
    ```

6. **Output.**
   - Interactive: the report path, finding counts, and fixes applied.
   - `--quiet`: a single stdout line `maintain: M findings (X critical), K fixes`
     and a non-zero process exit when unresolved critical findings remain.

## Edge Cases

- **Runs alongside manual editing:** only writes its own report plus auto-fixable
  changes with a git-inspectable diff. No interactive reconciles in `--quiet` mode.
- **No vault configured:** abort early with a clear message.
```

- [ ] **Step 2: Write the cron recipes reference**

Create `plugins/obsidian/skills/wiki-maintain/references/cron-recipes.md`:
```markdown
# Scheduling wiki-maintain

A distributed plugin cannot start a daemon on your machine — you schedule it. Both
recipes run a weekly unattended maintenance pass.

## crontab (Linux/macOS)

Edit your crontab (`crontab -e`) and add — adjust the path to your vault:

```cron
# Weekly wiki maintenance, Mondays 08:17
17 8 * * 1 cd /path/to/your/vault && claude -p "/wiki:maintain --auto-fix --quiet" >> "$HOME/.wiki-maintain.log" 2>&1
```

## launchd (macOS, survives reboots)

Create `~/Library/LaunchAgents/ch.talent-factory.wiki-maintain.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>ch.talent-factory.wiki-maintain</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/zsh</string>
    <string>-lc</string>
    <string>cd /path/to/your/vault && claude -p "/wiki:maintain --auto-fix --quiet"</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict><key>Weekday</key><integer>1</integer><key>Hour</key><integer>8</integer><key>Minute</key><integer>17</integer></dict>
  <key>StandardOutPath</key><string>/tmp/wiki-maintain.out</string>
  <key>StandardErrorPath</key><string>/tmp/wiki-maintain.err</string>
</dict>
</plist>
```

Load it: `launchctl load ~/Library/LaunchAgents/ch.talent-factory.wiki-maintain.plist`

## Notes

- Use an off-minute (`:17`) rather than `:00` to avoid load spikes.
- `--quiet` exits non-zero when unresolved critical findings remain — your wrapper
  can alert on that.
```

- [ ] **Step 3: Verify frontmatter parses and skill loads**

Run:
```bash
python3 -c "import pathlib,yaml; t=pathlib.Path('plugins/obsidian/skills/wiki-maintain/SKILL.md').read_text(); d=yaml.safe_load(t.split('---')[1]); assert d['name']=='wiki-maintain' and len(d['description'])>40; print('ok')"
```
Expected: `ok`.

- [ ] **Step 4: Commit**

```bash
git add plugins/obsidian/skills/wiki-maintain/
git commit -m "✨ feat(obsidian): add wiki-maintain skill with cron/launchd recipes"
```

---

### Task 13: wiki-think skill + thinking modes

**Files:**
- Create: `plugins/obsidian/skills/wiki-think/SKILL.md`
- Create: `plugins/obsidian/skills/wiki-think/references/thinking-modes.md`

**Interfaces:**
- Consumes: index-first page loading (same pattern as `wiki-query`), `_shared/scripts/validate.py` (when `--save` writes a page).
- Produces: a `/wiki:think <topic|page> [--mode ...] [--save]` skill with three modes and optional `type: thinking` wiki output.

- [ ] **Step 1: Write the SKILL.md**

Create `plugins/obsidian/skills/wiki-think/SKILL.md`:
```markdown
---
name: wiki-think
description: Argues with your notes in an Obsidian-based LLM knowledge wiki — challenges assumptions (devil's advocate), surfaces non-obvious connections, or asks Socratic questions. Optionally saves the result as a wiki page. Triggers when the user runs /wiki:think, asks to "challenge this note", "poke holes in my thinking", "find connections between my notes", or "ask me Socratic questions about X".
---

# wiki-think

## When to invoke

The user runs `/wiki:think <topic-or-page> [--mode challenge|connect|socratic] [--save]`,
or asks the assistant to challenge a note, find connections across notes, or ask
probing questions about a topic in the wiki.

## Configuration

Same vault layout as `wiki-ingest`. Default mode (no `--mode`) is `challenge`.
Modes are combinable: `--mode challenge,connect`.

## Workflow

1. **Load context (index-first).** Read `<wiki-root>/_wiki/index.md`, identify the
   page(s) matching the topic, and read them plus their directly `related:` pages.
2. **Apply the requested mode(s)** using `references/thinking-modes.md`:
   - `challenge` — surface weak assumptions, counter-examples, and blind spots.
   - `connect` — find non-obvious links between distant pages; propose new
     cross-references or a hub theme.
   - `socratic` — ask a short sequence of probing questions instead of answering.
3. **Output to terminal** by default.
4. **`--save`** → write `<wiki-root>/_wiki/thinking/<slug>.md` with frontmatter
   `kind: wiki, type: thinking`, `sources:` set to the referenced page paths,
   `related:` set to those pages (bidirectional — add the back-reference on each).
   Then run the write-time validation gate:

    ```bash
    python3 "${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/validate.py" \
      --vault-root "<wiki-root>/.." --target "<thinking-file>" \
      --rules frontmatter,kindtype,deadlinks,asymmetric
    ```

    Resolve critical findings before finalizing. `type: thinking` is exempt from
    the empty-`sources:` semantic rule, so a thinking page with no sources is valid.

## Output

- Terminal: the challenge / connections / questions for the chosen mode(s).
- With `--save`: the created `thinking/<slug>.md` path and any cross-references added.
```

- [ ] **Step 2: Write the thinking-modes reference**

Create `plugins/obsidian/skills/wiki-think/references/thinking-modes.md`:
```markdown
# Thinking Modes

## challenge (devil's advocate)

Goal: strengthen the user's reasoning by attacking it fairly.
- State the page's central claim in one sentence.
- List the load-bearing assumptions; mark each as well-supported or shaky.
- Give concrete counter-examples or conditions under which the claim fails.
- Name blind spots: what the note does not consider.
- End with the single strongest objection and what evidence would settle it.

## connect (synthesis)

Goal: surface non-obvious structure across distant notes.
- From the loaded pages, identify shared entities, mechanisms, or tensions that are
  not already cross-linked.
- Propose specific new `related:` links (bidirectional) with a one-line rationale each.
- If five or more pages cluster around a theme without a hub, propose a
  `type: hub` page with a title and the member pages.

## socratic (questions)

Goal: drive the user's own thinking, not provide answers.
- Ask 4–7 progressively deeper questions about the topic.
- Each question targets an assumption, a definition, a boundary, or an implication.
- Do not answer them; end by inviting the user to pick one to explore.
```

- [ ] **Step 3: Verify frontmatter parses and skill loads**

Run:
```bash
python3 -c "import pathlib,yaml; t=pathlib.Path('plugins/obsidian/skills/wiki-think/SKILL.md').read_text(); d=yaml.safe_load(t.split('---')[1]); assert d['name']=='wiki-think' and len(d['description'])>40; print('ok')"
```
Expected: `ok`.

- [ ] **Step 4: Confirm validator already accepts `type: thinking`**

Run: `python3 -m pytest plugins/obsidian/skills/_shared/scripts/test_validate.py -k thinking -v`
Expected: PASS (`test_kindtype_accepts_thinking`).

- [ ] **Step 5: Commit**

```bash
git add plugins/obsidian/skills/wiki-think/
git commit -m "✨ feat(obsidian): add wiki-think skill (challenge/connect/socratic)"
```

---

## Phase 6 — Release

### Task 14: Version bumps and catalog entries

**Files:**
- Modify: `plugins/obsidian/.claude-plugin/plugin.json`
- Modify: `.claude-plugin/marketplace.json`
- Modify: `docs/plugins/index.md`

**Interfaces:**
- Consumes: nothing.
- Produces: version `1.4.0` consistently across catalog files.

- [ ] **Step 1: Inspect current version strings**

Run:
```bash
grep -n '"version"' plugins/obsidian/.claude-plugin/plugin.json
grep -n '1.3.1\|"obsidian"' .claude-plugin/marketplace.json | head
grep -n 'obsidian' docs/plugins/index.md | head
```
Expected: shows the `1.3.1` occurrences to update.

- [ ] **Step 2: Update `plugin.json`**

In `plugins/obsidian/.claude-plugin/plugin.json`, change `"version": "1.3.1"` → `"version": "1.4.0"`.

- [ ] **Step 3: Update `marketplace.json`**

In `.claude-plugin/marketplace.json`, set the obsidian plugin entry version to `1.4.0` (match the field used by the existing entry).

- [ ] **Step 4: Update `docs/plugins/index.md`**

Update the obsidian version line to `1.4.0`.

- [ ] **Step 5: Validate JSON**

Run:
```bash
python3 -c "import json; json.load(open('plugins/obsidian/.claude-plugin/plugin.json')); json.load(open('.claude-plugin/marketplace.json')); print('json ok')"
```
Expected: `json ok`.

- [ ] **Step 6: Commit**

```bash
git add plugins/obsidian/.claude-plugin/plugin.json .claude-plugin/marketplace.json docs/plugins/index.md
git commit -m "🔖 chore(obsidian): bump version to 1.4.0 across catalogs"
```

---

### Task 15: README and CHANGELOG

**Files:**
- Modify: `plugins/obsidian/README.md`
- Modify: `CHANGELOG.md`

**Interfaces:**
- Consumes: the new skills and the shared module.
- Produces: user-facing documentation for v1.4.0.

- [ ] **Step 1: Add the two new skills and the dependency note to the README**

In `plugins/obsidian/README.md`:
- Add `wiki-think` and `wiki-maintain` to the slash-command list and the skill descriptions section.
- Add trigger examples: `/obsidian:wiki-think`, `/obsidian:wiki-maintain`.
- Add a "Validation" note: deterministic checks use `skills/_shared/scripts/validate.py`, which requires **PyYAML** (`pip install pyyaml`); without it skills fall back to prose rules.
- Reference scheduling via `wiki-maintain/references/cron-recipes.md`.
- Update the skill count and the version header to `1.4.0`.

- [ ] **Step 2: Add the v1.4.0 changelog section to the README**

Add to the README changelog:
```markdown
### Version 1.4.0 (2026-06-22)

- Added shared validation module (`skills/_shared/`): `validate.py` (deterministic
  frontmatter/kind-type/dead-link/asymmetric checks, pytest-covered) + authoritative
  `validation-rules.md`.
- Added write-time validation gate to `wiki-ingest` and `wiki-migrate-file`.
- Added contradiction propose-and-confirm to `wiki-ingest`.
- Added `wiki-think` skill (challenge / connect / socratic, optional `type: thinking` page).
- Added `wiki-maintain` skill (non-interactive lint + auto-fix + report) with cron/launchd recipes.
- Refactored `wiki-lint` to delegate deterministic checks to the shared module.
```

- [ ] **Step 3: Add the v1.4.0 entry to the root CHANGELOG**

Add the same summary to `CHANGELOG.md` under a `## [1.4.0] - 2026-06-22` heading, matching the file's existing format.

- [ ] **Step 4: Verify the docs mention every new artifact**

Run:
```bash
python3 -c "import pathlib; r=pathlib.Path('plugins/obsidian/README.md').read_text(); assert all(s in r for s in ['wiki-think','wiki-maintain','1.4.0','PyYAML']); print('ok')"
```
Expected: `ok`.

- [ ] **Step 5: Commit**

```bash
git add plugins/obsidian/README.md CHANGELOG.md
git commit -m "📚 docs(obsidian): document v1.4.0 second-brain integration"
```

---

### Task 16: Final validation and smoke tests

**Files:** none (verification only).

- [ ] **Step 1: Run the full validator test suite**

Run: `python3 -m pytest plugins/obsidian/skills/_shared/scripts/ -v`
Expected: PASS (all tests).

- [ ] **Step 2: Run structural plugin checks**

Run `claude --plugin-dir ./plugins/obsidian`, then in-session: `/core:check-commands` and `/core:check-agents`.
Expected: both pass (no command/agent regressions; the plugin ships skills, so these check the existing surfaces).

- [ ] **Step 3: Confirm all skills load**

In the same session, run `/help` and confirm `wiki-think` and `wiki-maintain` appear alongside the existing obsidian skills.

- [ ] **Step 4: Smoke-test the validator gate against a broken page**

Create a temporary vault with a deliberately broken wiki page (missing `domain`, bad `type`), run:
```bash
python3 plugins/obsidian/skills/_shared/scripts/validate.py --vault-root <tmp-vault> --rules frontmatter,kindtype
```
Expected: JSON lists the `critical` findings; process exit code is `1`.

- [ ] **Step 5: Smoke-test PyYAML fallback path**

Run the validator under an interpreter without PyYAML (or temporarily rename the import) to confirm it prints the JSON `{"error": ..., "fallback": "prose"}` and exits `2`.
Expected: exit code `2`, JSON error emitted.

- [ ] **Step 6: Final commit (if any fixes were made)**

```bash
git add -A
git commit -m "🧪 test(obsidian): final validation of v1.4.0 integration"
```

(If no changes were needed, skip this commit.)

---

## Self-Review Notes

- **Spec coverage:** Write-Time-Validator → Tasks 1–6, 9, 10; Contradiction-Reconcile → Task 11; Thinking-Tools → Task 13; Scheduled-Maintenance → Task 12; shared module → Tasks 1–7; wiki-lint refactor → Task 8; `type: thinking` cross-cutting → Task 3 (validator) + Task 7 (rules) + Task 13 (skill); versioning/docs → Tasks 14–15; testing → Tasks 1–6, 16. All spec sections mapped.
- **Severity policy** is consistent across the validator (Tasks 2–5), the rules doc (Task 7), and the gate skills (Tasks 9–10).
- **Function/type names** (`run`, `build_index`, `CHECKS`, `register`, `normalize_link`, `normalize_ref`, `_is_report_or_log`) are defined in Task 1 and reused unchanged in later tasks.
```
