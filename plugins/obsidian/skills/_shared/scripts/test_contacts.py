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
    assert len(idx["persons"]) == 1


def test_build_index_maps_slug_and_alias_to_company():
    idx = c.build_index(FIXTURE)
    assert idx["company_norm"]["bedag"] == ["BEDAG Informatik AG"]
    assert "BEDAG Informatik AG" in idx["company_norm"]["bedaginformatikag"]
