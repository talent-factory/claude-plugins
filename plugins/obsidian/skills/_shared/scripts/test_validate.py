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


def test_parse_frontmatter_returns_none_when_yaml_missing(monkeypatch):
    monkeypatch.setattr(v, "yaml", None)
    fm, body = v.parse_frontmatter("---\nkind: wiki\n---\nbody")
    assert fm is None
    assert "body" in body


def test_run_returns_empty_when_no_rules_registered_match(tmp_path):
    (tmp_path / "_wiki").mkdir()
    assert v.run(tmp_path, rules=["nonexistent"], target=None) == []


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


def test_frontmatter_exempts_report_files(tmp_path):
    sub = tmp_path / "_wiki"
    sub.mkdir(exist_ok=True)
    for name in ("lint-report-2026-01-01.md", "maintain-report-2026-01-01.md"):
        p = sub / name
        p.write_text("---\nkind: wiki\ntype: note\n---\n# report\n- findings: 0",
                     encoding="utf-8")
        rec = v.load_record(p)
        assert v.CHECKS["frontmatter"]([rec], {"names": set(), "related": {}}) == []
        assert v.CHECKS["kindtype"]([rec], {"names": set(), "related": {}}) == []


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


def test_deadlinks_resolves_media_embed_with_extension(tmp_path):
    sub = tmp_path / "_wiki"
    sub.mkdir(exist_ok=True)
    (tmp_path / "_raw").mkdir(exist_ok=True)
    (tmp_path / "_raw" / "diagram.png").write_bytes(b"\x89PNG")
    rec = _rec(tmp_path, "A.md", "kind: wiki\ntype: concept\ntitle: A",
               body="embed ![[diagram.png]] and bare [[diagram]]")
    index = v.build_index(tmp_path)
    assert v.CHECKS["deadlinks"]([rec], index) == []


def test_deadlinks_exempts_reports_and_log(tmp_path):
    sub = tmp_path / "_wiki"
    sub.mkdir(exist_ok=True)
    for name in ("log.md", "lint-report-2026-01-01.md", "maintain-report-2026-01-01.md"):
        p = sub / name
        p.write_text("see [[Ghost]]", encoding="utf-8")
        rec = v.load_record(p)
        assert v.CHECKS["deadlinks"]([rec], {"names": set(), "related": {}}) == []


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
