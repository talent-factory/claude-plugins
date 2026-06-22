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
