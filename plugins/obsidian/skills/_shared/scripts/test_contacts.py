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
    assert len(idx["persons"]) == 3


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
