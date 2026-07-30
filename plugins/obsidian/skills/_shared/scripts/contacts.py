#!/usr/bin/env python3
"""Deterministic validation and migration for Obsidian contact/company links.

Sibling to validate.py. Reads `30 Persons`, `35 Companies` and `85 Wissen/_wiki`
from an Obsidian vault root, emits JSON findings, and performs the one-off
slug-to-wikilink migration. PyYAML is required; when absent the CLI exits 2 with
a JSON error so the calling skill can fall back to prose rules.
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from validate import (  # noqa: E402  reuse — do not duplicate
    load_record,
    normalize_ref,
    parse_frontmatter,
    strip_code,
)

try:
    import yaml
except ImportError:  # graceful degradation — mirrors validate.py
    yaml = None

PERSONS_DIR = "30 Persons"
COMPANIES_DIR = "35 Companies"
WIKI_DIR = "85 Wissen/_wiki"
KINDS = {"contact", "student", "alumni"}

CHECKS = {}

_UMLAUTS = {"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"}


def register(name):
    def deco(fn):
        CHECKS[name] = fn
        return fn
    return deco


def normalize_slug(s):
    s = str(s).lower()
    for k, v in _UMLAUTS.items():
        s = s.replace(k, v)
    return re.sub(r"[^a-z0-9]", "", s)


def is_wikilink(s):
    return bool(re.search(r"\[\[[^\]]+\]\]", str(s)))


def company_values(fm):
    if not isinstance(fm, dict):
        return []
    raw = fm.get("company")
    if raw is None:
        return []
    items = raw if isinstance(raw, list) else [raw]
    out = []
    for x in items:
        s = str(x).strip()
        if s and s != "[]":
            out.append(s)
    return out


def build_index(vault_root):
    vault_root = Path(vault_root)
    companies = {}
    company_records = []
    cdir = vault_root / COMPANIES_DIR
    if cdir.exists():
        for p in sorted(cdir.glob("*.md")):
            companies[p.stem] = p
            company_records.append(load_record(p))
    company_norm = {}
    for stem in companies:
        company_norm.setdefault(normalize_slug(stem), []).append(stem)
    for rec in company_records:
        fm = rec["fm"]
        if not isinstance(fm, dict):
            continue
        aliases = fm.get("aliases") or []
        if isinstance(aliases, str):
            aliases = [aliases]
        stem = rec["path"].stem
        for a in list(aliases) + ([fm["slug"]] if fm.get("slug") else []):
            bucket = company_norm.setdefault(normalize_slug(a), [])
            if stem not in bucket:
                bucket.append(stem)
    wiki = set()
    wdir = vault_root / WIKI_DIR
    if wdir.exists():
        for p in wdir.rglob("*.md"):
            wiki.add(p.stem)
    persons = []
    pdir = vault_root / PERSONS_DIR
    if pdir.exists():
        for p in sorted(pdir.glob("*.md")):
            persons.append(load_record(p))
    return {
        "companies": companies,
        "company_norm": company_norm,
        "wiki": wiki,
        "persons": persons,
        "company_records": company_records,
    }


def _topic_values(fm):
    if not isinstance(fm, dict):
        return []
    raw = fm.get("topics")
    if raw is None:
        return []
    items = raw if isinstance(raw, list) else [raw]
    return [str(x).strip() for x in items if str(x).strip()]


@register("frontmatter")
def check_frontmatter(index):
    findings = []
    for rec in index["persons"]:
        fm = rec["fm"]
        if fm is None or fm == "INVALID":
            findings.append({
                "file": rec["path"], "severity": "critical", "rule": "frontmatter",
                "message": "fehlendes oder defektes YAML-Frontmatter",
                "autofixable": False,
            })
            continue
        tags = fm.get("tags") or []
        if isinstance(tags, str):
            tags = [tags]
        if "person" not in tags:
            findings.append({
                "file": rec["path"], "severity": "minor", "rule": "frontmatter",
                "message": "tags enthaelt kein 'person'", "autofixable": True,
            })
        kind = fm.get("kind")
        if kind not in KINDS:
            findings.append({
                "file": rec["path"], "severity": "minor", "rule": "frontmatter",
                "message": f"kind fehlt oder ungueltig: {kind!r} (erlaubt: {sorted(KINDS)})",
                "autofixable": True,
            })
        if "company" in fm and fm["company"] is not None \
                and not isinstance(fm["company"], list):
            findings.append({
                "file": rec["path"], "severity": "minor", "rule": "frontmatter",
                "message": "company muss eine Liste sein", "autofixable": True,
            })
    return findings


@register("slug-drift")
def check_slug_drift(index):
    findings = []
    for rec in index["persons"]:
        for v in company_values(rec["fm"]):
            if not is_wikilink(v):
                # autofixable only when the slug resolves to exactly one
                # company. Everything else needs the reviewed alias map —
                # an `autofixable: True` we cannot honour would invite a guess.
                cands = index["company_norm"].get(normalize_slug(v), [])
                findings.append({
                    "file": rec["path"], "severity": "minor", "rule": "slug-drift",
                    "message": f"company als Freitext statt Wikilink: {v!r}",
                    "autofixable": len(cands) == 1,
                })
    return findings


@register("deadlinks")
def check_deadlinks(index):
    findings = []
    known_companies = set(index["companies"])
    for rec in index["persons"]:
        for v in company_values(rec["fm"]):
            if not is_wikilink(v):
                continue
            target = normalize_ref(v)
            # Obsidian resolves [[Bedag]] through the company's `aliases:`
            # front matter, so an alias link is valid, not dead.
            if (target not in known_companies
                    and normalize_slug(target) not in index["company_norm"]):
                findings.append({
                    "file": rec["path"], "severity": "critical", "rule": "deadlinks",
                    "message": f"company zeigt ins Leere: [[{target}]]",
                    "autofixable": False,
                })
        for v in _topic_values(rec["fm"]):
            if not is_wikilink(v):
                continue
            target = normalize_ref(v)
            if target not in index["wiki"]:
                findings.append({
                    "file": rec["path"], "severity": "critical", "rule": "deadlinks",
                    "message": f"topics zeigt ins Leere: [[{target}]]",
                    "autofixable": False,
                })
    return findings


# The negative lookbehind keeps `!contains(company, "x")` out: rewriting a
# negated predicate to the canonical form would invert the query's meaning.
COMPANY_PREDICATE_RE = re.compile(
    r'(?<!!)contains\(\s*company\s*,\s*"[^"]*"\s*\)|company\s*=\s*"[^"]*"'
)
CANONICAL_PREDICATE = "contains(company, this.file.link)"
_BLOCK_RE = re.compile(r"```([a-zA-Z0-9_-]*)\n(.*?)```", re.DOTALL)


def code_blocks(text):
    return [(m.group(1), m.group(2), m.start(), m.end())
            for m in _BLOCK_RE.finditer(text or "")]


@register("query-drift")
def check_query_drift(index):
    findings = []
    for rec in index["company_records"]:
        for lang, body, _s, _e in code_blocks(rec["text"]):
            if lang not in ("dataview", "base"):
                continue
            if CANONICAL_PREDICATE in body:
                continue                      # already migrated
            if COMPANY_PREDICATE_RE.search(body):
                findings.append({
                    "file": rec["path"], "severity": "minor", "rule": "query-drift",
                    "message": "Query nutzt hartkodierten Slug statt this.file.link",
                    "autofixable": lang == "dataview",
                })
            elif "company" in body:
                # mentions company in a form we will not rewrite (negated,
                # !=, startsWith). Report it — never drop it silently.
                findings.append({
                    "file": rec["path"], "severity": "minor", "rule": "query-drift",
                    "message": "company-Praedikat in nicht umschreibbarer Form — "
                               "manuelle Pruefung noetig",
                    "autofixable": False,
                })
            else:
                findings.append({
                    "file": rec["path"], "severity": "minor", "rule": "query-drift",
                    "message": "Query filtert nicht ueber company — manuelle Pruefung noetig",
                    "autofixable": False,
                })
    return findings


@register("orphan-company")
def check_orphan_company(index):
    linked = set()
    for rec in index["persons"]:
        for v in company_values(rec["fm"]):
            if is_wikilink(v):
                linked.add(normalize_slug(normalize_ref(v)))
    findings = []
    for stem, path in index["companies"].items():
        # a person may link the canonical name or any registered alias —
        # same rule as check_deadlinks
        keys = {normalize_slug(stem)}
        keys |= {k for k, stems in index["company_norm"].items() if stem in stems}
        if not (keys & linked):
            findings.append({
                "file": path, "severity": "minor", "rule": "orphan-company",
                "message": "keine Person verweist auf diese Firma",
                "autofixable": False,
            })
    return findings


@register("dupes")
def check_dupes(index):
    by_email = {}
    by_name = {}
    for rec in index["persons"]:
        fm = rec["fm"]
        if isinstance(fm, dict) and fm.get("email"):
            by_email.setdefault(str(fm["email"]).strip().lower(), []).append(rec["path"])
        base = re.sub(r"\s*\(\d+\)$", "", rec["path"].stem)
        by_name.setdefault(normalize_slug(base), []).append(rec["path"])
    findings = []
    for email, paths in sorted(by_email.items()):
        if len(paths) > 1:
            others = ", ".join(sorted(p.stem for p in paths))
            for p in paths:
                findings.append({
                    "file": p, "severity": "minor", "rule": "dupes",
                    "message": f"gleiche E-Mail {email} auf: {others}",
                    "autofixable": False,
                })
    for _norm, paths in sorted(by_name.items()):
        if len(paths) > 1:
            others = ", ".join(sorted(p.stem for p in paths))
            for p in paths:
                findings.append({
                    "file": p, "severity": "minor", "rule": "dupes",
                    "message": f"Namensdublette: {others}", "autofixable": False,
                })
    return findings


def _first_token(stem):
    # Hyphens stay inside the first word: splitting on them would make
    # "T-Systems Schweiz AG" reachable only by the slug "t".
    parts = [p for p in re.split(r"[\s,&]+", stem) if p]
    return normalize_slug(parts[0]) if parts else ""


def _resolve_slug(slug, index):
    """Strict resolution. Exact normalised match, else first-word match.

    Substring matching is deliberately absent: it would map "bsi" onto
    "AI21 Labs Inc." via "labsinc".
    """
    ns = normalize_slug(slug)
    if not ns:
        return []
    exact = sorted(set(index["company_norm"].get(ns, [])))
    if exact:
        return exact
    return sorted({stem for stem in index["companies"] if _first_token(stem) == ns})


_WHOLE_WIKILINK_RE = re.compile(r"^\[\[[^\]]+\]\]$")


def propose_aliases(vault_root):
    index = build_index(vault_root)
    counts = {}
    for rec in index["persons"]:
        for v in company_values(rec["fm"]):
            if _WHOLE_WIKILINK_RE.match(v.strip()):
                continue
            counts[v] = counts.get(v, 0) + 1
    out = {}
    for slug, n in sorted(counts.items()):
        cands = _resolve_slug(slug, index)
        exact = bool(index["company_norm"].get(normalize_slug(slug)))
        if len(cands) == 1:
            target = cands[0]
        elif len(cands) > 1:
            target = "CHOOSE: " + " | ".join(cands)
        else:
            target = None
        # "match" lets the human triage: an "exact" hit is a declared
        # identifier (stem/slug/alias), while "first-word" is a heuristic —
        # e.g. the slug "inetum" resolves to "Inetum Polska sp. z o.o." for
        # ten Swiss contacts, which is plausible but not verified identity.
        # candidates, not target, stays authoritative for the human review.
        out[slug] = {
            "count": n,
            "target": target,
            "candidates": cands,
            "match": "exact" if exact else ("first-word" if cands else "none"),
        }
    return out


def run(vault_root, rules):
    index = build_index(vault_root)
    findings = []
    for name in rules:
        fn = CHECKS.get(name)
        if fn:
            findings.extend(fn(index))
    return findings


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Validate and migrate Obsidian contact/company links.")
    parser.add_argument("--vault-root", required=True)
    parser.add_argument("--rules", default=",".join(CHECKS.keys()))
    parser.add_argument("--propose-aliases", action="store_true")
    parser.add_argument("--migrate", action="store_true")
    parser.add_argument("--alias-map", default=None)
    parser.add_argument("--apply", action="store_true",
                        help="write changes; without it the migration is a dry run")
    parser.add_argument("--format", default="json", choices=["json"])
    args = parser.parse_args(argv)
    if yaml is None:
        print(json.dumps({"error": "PyYAML not installed", "fallback": "prose"}))
        return 2
    if args.propose_aliases:
        root = Path(args.vault_root)
        # A mistyped --vault-root would otherwise yield an empty proposal and
        # exit 0 — a silent green light for a 550-file migration.
        missing = [d for d in (PERSONS_DIR, COMPANIES_DIR) if not (root / d).is_dir()]
        if missing:
            print(json.dumps({"error": f"vault-root fehlt: {', '.join(missing)}"}))
            return 2
        proposal = propose_aliases(root)
        print(yaml.safe_dump(proposal, allow_unicode=True, sort_keys=True))
        return 0
    if args.migrate:
        if not args.alias_map:
            print(json.dumps({"error": "--migrate requires --alias-map"}))
            return 2
        root = Path(args.vault_root)
        # Same guard as --propose-aliases. It matters more here: this is the
        # branch that writes.
        missing = [d for d in (PERSONS_DIR, COMPANIES_DIR) if not (root / d).is_dir()]
        if missing:
            print(json.dumps({"error": f"vault-root fehlt: {', '.join(missing)}"}))
            return 2
        try:
            amap = load_alias_map(Path(args.alias_map))
        except (ValueError, OSError, yaml.YAMLError, AttributeError) as e:
            print(json.dumps({"error": f"{type(e).__name__}: {e}"}))
            return 2
        result = {
            "persons": migrate_persons(Path(args.vault_root), amap,
                                        dry_run=not args.apply),
            "companies": migrate_companies(Path(args.vault_root), amap,
                                            dry_run=not args.apply),
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    rules = [r.strip() for r in args.rules.split(",") if r.strip()]
    findings = run(Path(args.vault_root), rules)
    print(json.dumps([{**f, "file": str(f["file"])} for f in findings], indent=2))
    return 1 if any(f["severity"] == "critical" for f in findings) else 0


def load_alias_map(path):
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError("Alias-Map muss ein Mapping sein")
    out = {}
    for slug, entry in data.items():
        target = entry.get("target") if isinstance(entry, dict) else entry
        if target is None:
            continue
        if not isinstance(target, str) or not target.strip():
            raise ValueError(f"target fuer Slug {slug!r} ist kein Text: {target!r}")
        t = target.strip()
        # Tolerant on purpose: a human deleting only the "CHOOSE: " prefix but
        # leaving both candidates would otherwise create the dead link
        # [[A AG | B AG]] on every affected person.
        if t.upper().startswith("CHOOSE"):
            raise ValueError(
                f"unaufgeloester CHOOSE-Marker fuer Slug {slug!r} — "
                "bitte in der Alias-Map entscheiden")
        if "|" in t:
            raise ValueError(
                f"target fuer Slug {slug!r} enthaelt '|': {t!r} — "
                "sieht nach zwei nicht entschiedenen Kandidaten aus")
        out[str(slug)] = t
    return out


def infer_kind(fm, has_company=None):
    """`has_company` must reflect the state BEFORE migration.

    Deriving it from `fm` after the company field was emptied misclassifies
    everyone whose slug the alias map could not resolve: they lose their
    company, so they look like a pure student. And the mistake is sticky —
    `kind` is then valid, so a later run with a better alias map never
    revisits it.
    """
    if has_company is None:
        has_company = bool(company_values(fm))
    has_school = any(fm.get(k) for k in ("school", "module", "class"))
    if has_company and has_school:
        return "alumni"
    if has_company:
        return "contact"
    if has_school:
        return "student"
    return "contact"


# Surgical frontmatter editing.
#
# Re-rendering the whole frontmatter through PyYAML was measured against the
# 1257 real person files and rewrites data it has no business touching:
# 13 exam timestamps lose their `T` separator (2026-06-19T15:00 ->
# 2026-06-19 15:00), a `|-` block scalar is reflowed, long values wrap at
# column 80, and 600 files change quote style or list indent. A migration
# that converts company links must leave every other line byte-identical.
#
# So: parse to decide, then replace only the touched keys in the original
# text. Only the individual values a change touches go through PyYAML, for
# quoting — never the whole block.

_FM_RE = re.compile(r"\A(---[ \t]*\r?\n)(.*?)(\r?\n---[ \t]*(?:\r?\n|\Z))", re.S)


def _fm_parts(text):
    """Line-anchored frontmatter split: (open, fm_text, close, body) or None.

    `validate.parse_frontmatter` splits on the literal `---`, which is not
    line-anchored — a `---` inside a value would evict every later key into
    the body. `_FM_RE` fixes the common case by requiring the closing `---`
    to sit at column 0, immediately after a newline, so a body-level
    horizontal rule after the real close never confuses it.

    But a `---` line indented as part of a block scalar's *value* (e.g.
    `notiz: |\n  Erstkontakt\n  ---\n  Nachfass`) would silently pass the
    column-0 check on the wrong line only by luck of indentation depth — we
    would be trusting indentation to prove intent, which is not something a
    regex can verify. So once the closing `---` is found, the captured
    frontmatter text is re-scanned for any *other* line that strips down to
    exactly `---`, at any indentation. Finding one means the boundary is
    genuinely ambiguous — the file is refused, never guessed at.
    """
    m = _FM_RE.match(text)
    if not m:
        return None
    open_, fm_text, close = m.group(1), m.group(2), m.group(3)
    if any(line.strip() == "---" for line in fm_text.split("\n")):
        return None
    return open_, fm_text, close, text[m.end():]


def _tag_list(fm):
    tags = fm.get("tags") or []
    if isinstance(tags, str):
        tags = [tags]
    return [str(t) for t in tags] if isinstance(tags, list) else []


class _Unsafe(Exception):
    """This frontmatter cannot be edited surgically without guessing."""


def _key_span(lines, key):
    """[start, end) of `key:` plus its indented continuation lines.

    Fails closed rather than guesses on two shapes a line-anchored scan
    cannot edit safely: a duplicate key (YAML resolves duplicates
    last-wins, but editing the first match would silently destroy the
    value that actually takes effect) and a multi-line flow collection
    whose closing bracket sits at column 0 (`company: [\n  a,\n  b\n]` —
    the "indented continuation" scan below stops one line short of it,
    which would leave a dangling `]` in the output). The bracket count is
    deliberately crude: a false positive refuses a file and reports it,
    which is the safe direction.
    """
    pat = re.compile(rf"^{re.escape(key)}\s*:")
    hits = [i for i, line in enumerate(lines) if pat.match(line)]
    if not hits:
        return None
    if len(hits) > 1:
        raise _Unsafe(f"Schluessel {key!r} kommt {len(hits)}x vor")
    i = hits[0]
    j = i + 1
    while j < len(lines) and lines[j][:1] in (" ", "\t"):
        j += 1
    block = "\n".join(lines[i:j])
    # Two guards, both fail-closed. Counting brackets alone misses a `]`
    # inside a quoted scalar, so also refuse any value line that ends in a
    # bare opening bracket — that is what starts a multi-line flow
    # collection whose close sits outside this span.
    if (re.search(r"[\[{]\s*$", lines[i])
            or block.count("[") != block.count("]")
            or block.count("{") != block.count("}")):
        raise _Unsafe(f"Schluessel {key!r} hat eine unabgeschlossene Flow-Collection")
    return i, j


def _scalar(value):
    """Render one value so YAML reads it back unchanged.

    An f-string interpolation (`f"  - {s}"`) is not safe: a value like
    `Firma: Abteilung` or `[[Foo AG]] (ehemals)` breaks the parser, `yes`
    or `null` silently become booleans/None, and `#tag` becomes a comment
    (8 real vault files carry `#`-prefixed tags). Let PyYAML do the quoting
    instead. Whole wikilinks are the one deliberate exception — they stay
    Obsidian's own double-quote style rather than PyYAML's default single
    quotes.
    """
    s = str(value)
    if _WHOLE_WIKILINK_RE.match(s.strip()):
        # `[[...]]` may itself contain a quote or backslash — the pattern
        # allows anything but `]`. Only keep Obsidian's double quotes when
        # they actually survive a round trip.
        q = f'"{s}"'
        try:
            if yaml.safe_load(q) == s:
                return q
        except yaml.YAMLError:
            pass
    d = yaml.safe_dump(s, default_flow_style=True, allow_unicode=True, width=10 ** 9)
    return d.removesuffix("\n").removesuffix("...").strip()


def _render_key(key, value):
    """Render one key as a list of lines, in Obsidian's own style."""
    if value is None or value == [] or value == "":
        return [f"{key}:"]
    if isinstance(value, list):
        return [f"{key}:"] + [f"  - {_scalar(v)}" for v in value]
    return [f"{key}: {_scalar(value)}"]


def _set_key(lines, key, value):
    rendered = _render_key(key, value)
    span = _key_span(lines, key)
    if span is None:
        return lines + rendered
    return lines[:span[0]] + rendered + lines[span[1]:]


_TOUCHED_KEYS = ("company", "kind", "tags", "company_legacy")


def skip_reason(text):
    """Why this file cannot be migrated, or None when it can.

    Single classifier shared by `migrate_person` (bails when this returns
    non-None) and `migrate_persons` (records the reason in `skipped`
    instead of silently dropping the file from every bucket). Also the
    only place that pre-validates the keys `migrate_person` is about to
    touch — a file with a duplicate `company:` or a dangling multi-line
    flow collection must never reach `_set_key`.
    """
    parts = _fm_parts(text)
    if parts is None:
        return "kein oder mehrdeutig abgegrenztes Frontmatter"
    try:
        fm = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        return f"YAML nicht lesbar: {type(e).__name__}"
    if not isinstance(fm, dict):
        return "Frontmatter ist kein Mapping"
    lines = parts[1].split("\n")
    for k in _TOUCHED_KEYS:
        try:
            _key_span(lines, k)
        except _Unsafe as e:
            return str(e)
    return None


def migrate_person(text, alias_map):
    if skip_reason(text) is not None:
        return text, []          # unsafe to edit surgically — never write
    open_, fm_text, close, body = _fm_parts(text)
    fm = yaml.safe_load(fm_text)
    changes = []
    raw = company_values(fm)
    resolved, legacy = [], []
    for v in raw:
        if _WHOLE_WIKILINK_RE.match(v.strip()):
            resolved.append(v)
            continue
        target = alias_map.get(v)
        if target:
            resolved.append(f"[[{target}]]")
            changes.append(f"company {v!r} -> [[{target}]]")
        else:
            legacy.append(v)
            changes.append(f"company {v!r} unaufloesbar -> company_legacy")
    lines = fm_text.split("\n")
    if changes:
        lines = _set_key(lines, "company", resolved)
    if legacy:
        # Merge, never overwrite: a partially migrated and hand-corrected
        # file already carries values here, and losing them is unrecoverable.
        prev = fm.get("company_legacy") or []
        if isinstance(prev, str):
            prev = [prev]
        merged = list(prev) + [v for v in legacy if v not in prev]
        # A single legacy value renders as a plain scalar (`company_legacy:
        # foo`); only once there is more than one does it become a list —
        # matches _render_key's list branch, which always uses block style.
        lines = _set_key(lines, "company_legacy",
                         merged[0] if len(merged) == 1 else merged)
    kind = fm.get("kind")
    if not isinstance(kind, str) or kind not in KINDS:
        # `raw`, not the emptied field — see infer_kind's docstring.
        new_kind = infer_kind(fm, has_company=bool(raw) or bool(fm.get("company_legacy")))
        lines = _set_key(lines, "kind", new_kind)
        changes.append(f"kind -> {new_kind}")
    tags = _tag_list(fm)
    if "person" not in tags:
        lines = _set_key(lines, "tags", tags + ["person"])
        changes.append("tags += person")
    if not changes:
        return text, []
    return open_ + "\n".join(lines) + close + body, changes


def _atomic_write(path, text):
    """Write via a temp file in the same directory, then rename.

    `Path.write_text` truncates first; an interruption mid-write loses the
    file. Over 1257 files that risk is not hypothetical.
    """
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def migrate_persons(vault_root, alias_map, dry_run=True):
    vault_root = Path(vault_root)
    touched, skipped, failed = [], [], []
    for p in sorted((vault_root / PERSONS_DIR).glob("*.md")):
        # One unreadable file must not abort a 1257-file run and leave the
        # operator without a manifest of what was already written.
        try:
            text = p.read_text(encoding="utf-8")
            reason = skip_reason(text)
            if reason is not None:
                skipped.append({"file": str(p), "reason": reason})
                continue
            new, changes = migrate_person(text, alias_map)
            if not changes:
                continue
            touched.append({"file": str(p), "changes": changes})
            if not dry_run:
                _atomic_write(p, new)
        except Exception as e:                       # noqa: BLE001 — reported
            failed.append({"file": str(p), "error": f"{type(e).__name__}: {e}"})
    return {"touched": touched, "skipped": skipped, "failed": failed,
            "dry_run": dry_run}


def migrate_company_queries(text):
    """Rewrite `company == "slug"` predicates to `this.file.link`.

    Only the `dataview` code block's `company` predicate is touched — the
    `tags` condition, `sort`, column list, and any `base` block stay
    byte-identical. A block with no matching predicate is not rewritten at
    all, which is why tag-only queries and Bases blocks pass through
    unchanged (Bases has no verified self-reference equivalent, so
    `query-drift` reports those for manual handling instead).
    """
    changes = []
    out = []
    last = 0
    for lang, body, start, end in code_blocks(text):
        if lang != "dataview":
            continue
        if not COMPANY_PREDICATE_RE.search(body):
            continue
        new_body, n = COMPANY_PREDICATE_RE.subn(CANONICAL_PREDICATE, body)
        if n == 0 or new_body == body:
            continue
        out.append(text[last:start])
        out.append(f"```{lang}\n{new_body}```")
        last = end
        changes.append(f"{n} company-Praedikat(e) -> this.file.link")
    if not changes:
        return text, []
    out.append(text[last:])
    return "".join(out), changes


def migrate_company_frontmatter(text, slugs):
    """Freeze the reviewed slug mapping: first slug becomes `slug`, rest `aliases`.

    Surgical, like `migrate_person`: only the two keys are rewritten, every
    other line of the company page's frontmatter stays byte-identical. A
    duplicate `slug:`/`aliases:` key or an unclosed flow collection makes
    `_key_span` raise `_Unsafe`; that propagates out of here uncaught, and
    `migrate_companies` below catches it per-file so one unsafe page cannot
    abort the whole run.
    """
    parts = _fm_parts(text)
    if parts is None or not slugs:
        return text, []
    open_, fm_text, close, body = parts
    try:
        fm = yaml.safe_load(fm_text)
    except yaml.YAMLError:
        return text, []
    if not isinstance(fm, dict):
        return text, []
    primary, extra = slugs[0], sorted(slugs[1:])
    existing = fm.get("aliases") or []
    if isinstance(existing, str):
        existing = [existing]
    merged = sorted(set(existing) | set(extra))
    changes = []
    lines = fm_text.split("\n")
    if fm.get("slug") != primary:
        lines = _set_key(lines, "slug", primary)
        changes.append(f"slug -> {primary}")
    if merged and list(existing) != merged:
        lines = _set_key(lines, "aliases", merged)
        changes.append(f"aliases -> {merged}")
    if not changes:
        return text, []
    return open_ + "\n".join(lines) + close + body, changes


def migrate_companies(vault_root, alias_map, dry_run=True):
    vault_root = Path(vault_root)
    reverse = {}
    for slug, target in sorted(alias_map.items()):
        reverse.setdefault(target, []).append(slug)
    touched, skipped, failed = [], [], []
    for p in sorted((vault_root / COMPANIES_DIR).glob("*.md")):
        # Mirrors migrate_persons: one unsafe or unreadable file must not
        # abort the run and must still show up in the manifest.
        try:
            text = p.read_text(encoding="utf-8")
            if parse_frontmatter(text)[0] in (None, "INVALID"):
                skipped.append({"file": str(p),
                                 "reason": "kein oder ungueltiges Frontmatter"})
                continue
            new, changes = migrate_company_queries(text)
            new2, ch2 = migrate_company_frontmatter(new, reverse.get(p.stem, []))
            changes = changes + ch2
            if not changes:
                continue
            touched.append({"file": str(p), "changes": changes})
            if not dry_run:
                _atomic_write(p, new2)
        except Exception as e:                        # noqa: BLE001 — reported
            failed.append({"file": str(p), "error": f"{type(e).__name__}: {e}"})
    return {"touched": touched, "skipped": skipped, "failed": failed,
            "dry_run": dry_run}


if __name__ == "__main__":
    sys.exit(main())
