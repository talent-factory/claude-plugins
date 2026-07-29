import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import contacts as c


def test_normalize_slug_expands_umlauts():
    assert c.normalize_slug("Bürgi & Partner") == "buergipartner"
    assert c.normalize_slug("buergi-partner") == "buergipartner"


def test_normalize_slug_strips_punctuation_and_case():
    assert c.normalize_slug("ict.ch") == "ictch"
    assert c.normalize_slug("BEDAG Informatik AG") == "bedaginformatikag"


def test_normalize_slug_handles_sharp_s():
    assert c.normalize_slug("Weiß AG") == "weissag"


def test_is_wikilink():
    assert c.is_wikilink("[[BEDAG Informatik AG]]") is True
    assert c.is_wikilink("bedag") is False
    assert c.is_wikilink("") is False


def test_company_values_from_list():
    fm = {"company": ["[[BEDAG Informatik AG]]", "bedag"]}
    assert c.company_values(fm) == ["[[BEDAG Informatik AG]]", "bedag"]


def test_company_values_from_scalar():
    assert c.company_values({"company": "bedag"}) == ["bedag"]


def test_company_values_drops_empty_and_placeholder():
    assert c.company_values({"company": None}) == []
    assert c.company_values({"company": []}) == []
    assert c.company_values({"company": "[]"}) == []


def test_company_values_missing_field():
    assert c.company_values({"tags": ["person"]}) == []


FIXTURE = Path(__file__).parent / "fixtures" / "vault"


def test_build_index_finds_companies_persons_and_wiki():
    idx = c.build_index(FIXTURE)
    assert "BEDAG Informatik AG" in idx["companies"]
    assert "Coding-Agents" in idx["wiki"]
    # membership, not an exact count — later tasks add more person fixtures
    assert {r["path"].stem for r in idx["persons"]} >= {"Anna Beispiel"}


def test_build_index_maps_slug_and_alias_to_company():
    idx = c.build_index(FIXTURE)
    assert idx["company_norm"]["bedag"] == ["BEDAG Informatik AG"]
    assert "BEDAG Informatik AG" in idx["company_norm"]["bedaginformatikag"]


def _rule(findings, rule):
    return [f for f in findings if f["rule"] == rule]


def test_frontmatter_flags_missing_kind():
    idx = c.build_index(FIXTURE)
    out = c.CHECKS["frontmatter"](idx)
    msgs = [f["message"] for f in out if f["file"].stem == "Bruno Altfall"]
    assert any("kind" in m for m in msgs)


def test_frontmatter_flags_scalar_company_not_list():
    idx = c.build_index(FIXTURE)
    out = c.CHECKS["frontmatter"](idx)
    msgs = [f["message"] for f in out if f["file"].stem == "Bruno Altfall"]
    assert any("Liste" in m for m in msgs)


def test_frontmatter_accepts_valid_person():
    idx = c.build_index(FIXTURE)
    out = c.CHECKS["frontmatter"](idx)
    assert not [f for f in out if f["file"].stem == "Anna Beispiel"]


def test_slug_drift_flags_plain_slug_and_is_autofixable():
    idx = c.build_index(FIXTURE)
    out = _rule(c.CHECKS["slug-drift"](idx), "slug-drift")
    hit = [f for f in out if f["file"].stem == "Bruno Altfall"]
    assert len(hit) == 1
    assert hit[0]["autofixable"] is True


def test_slug_drift_ignores_wikilink():
    idx = c.build_index(FIXTURE)
    out = c.CHECKS["slug-drift"](idx)
    assert not [f for f in out if f["file"].stem == "Anna Beispiel"]


def test_deadlinks_flags_unknown_company_and_topic():
    idx = c.build_index(FIXTURE)
    out = c.CHECKS["deadlinks"](idx)
    msgs = [f["message"] for f in out if f["file"].stem == "Carla Totlink"]
    assert any("Gibt Es Nicht AG" in m for m in msgs)
    assert any("Kein Wiki Eintrag" in m for m in msgs)


def test_deadlinks_clean_for_valid_person():
    idx = c.build_index(FIXTURE)
    out = c.CHECKS["deadlinks"](idx)
    assert not [f for f in out if f["file"].stem == "Anna Beispiel"]


def test_deadlinks_accepts_alias_link():
    # Obsidian resolves [[Bedag]] via the company's `aliases:` front matter.
    idx = c.build_index(FIXTURE)
    out = c.CHECKS["deadlinks"](idx)
    assert not [f for f in out if f["file"].stem == "Dora Aliaslink"]


def test_code_blocks_extracts_lang_and_body():
    text = "vor\n```dataview\nabc\n```\nnach\n```base\nxyz\n```\n"
    blocks = c.code_blocks(text)
    assert [b[0] for b in blocks] == ["dataview", "base"]
    assert blocks[0][1].strip() == "abc"


def test_company_predicate_matches_both_forms():
    assert c.COMPANY_PREDICATE_RE.search('contains(company, "bedag")')
    assert c.COMPANY_PREDICATE_RE.search('company = "bedag"')
    assert not c.COMPANY_PREDICATE_RE.search('contains(tags, "bedag")')


def test_query_drift_flags_hardcoded_slug():
    idx = c.build_index(FIXTURE)
    out = c.CHECKS["query-drift"](idx)
    hits = [f for f in out if f["file"].stem == "BEDAG Informatik AG"]
    assert len(hits) == 1
    assert hits[0]["autofixable"] is True


def test_query_drift_flags_tag_only_query_as_manual():
    idx = c.build_index(FIXTURE)
    out = c.CHECKS["query-drift"](idx)
    hits = [f for f in out if f["file"].stem == "Tagbasiert AG"]
    assert len(hits) == 1
    assert hits[0]["autofixable"] is False


def test_orphan_company_flags_company_without_person():
    idx = c.build_index(FIXTURE)
    out = c.CHECKS["orphan-company"](idx)
    stems = {f["file"].stem for f in out}
    assert "Waisen AG" in stems
    assert "BEDAG Informatik AG" not in stems


def test_orphan_company_counts_alias_links_as_linked():
    # Dora Aliaslink references BEDAG via [[Bedag]], an alias — that company
    # is not an orphan even though nobody links its canonical name.
    idx = c.build_index(FIXTURE)
    idx["persons"] = [r for r in idx["persons"]
                      if r["path"].stem in ("Dora Aliaslink",)]
    out = c.CHECKS["orphan-company"](idx)
    assert "BEDAG Informatik AG" not in {f["file"].stem for f in out}


def test_dupes_flags_shared_email():
    idx = c.build_index(FIXTURE)
    out = c.CHECKS["dupes"](idx)
    assert any("anna@example.ch" in f["message"] for f in out)


def test_run_returns_findings_for_selected_rules_only():
    out = c.run(FIXTURE, ["slug-drift"])
    assert out and {f["rule"] for f in out} == {"slug-drift"}


def test_main_exits_1_on_critical(capsys):
    rc = c.main(["--vault-root", str(FIXTURE), "--rules", "deadlinks"])
    payload = json.loads(capsys.readouterr().out)
    assert rc == 1
    assert any(f["rule"] == "deadlinks" for f in payload)
