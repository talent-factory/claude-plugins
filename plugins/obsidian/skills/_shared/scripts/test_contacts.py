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


def test_slug_drift_unresolvable_slug_is_not_autofixable():
    # No company page carries this slug, so the tool must not claim it can
    # fix it — that would be a guess.
    idx = c.build_index(FIXTURE)
    out = c.CHECKS["slug-drift"](idx)
    hit = [f for f in out if f["file"].stem == "Erwin Unbekannt"]
    assert len(hit) == 1
    assert hit[0]["autofixable"] is False


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


def _index_with_company_body(body):
    # Minimal synthetic index — check_query_drift only reads
    # company_records[i]["path"] and ["text"], never touches disk.
    text = f"```dataview\ntable role\n\twhere {body}\n```\n"
    return {"company_records": [{"path": Path("Synthetic AG.md"), "text": text}]}


def test_query_drift_negated_predicate_is_not_autofixable():
    idx = _index_with_company_body('!contains(company, "waisen")')
    out = c.check_query_drift(idx)
    assert len(out) == 1
    assert out[0]["autofixable"] is False
    assert "nicht umschreibbarer Form" in out[0]["message"]


def test_query_drift_comparison_operator_is_reported_not_dropped():
    idx = _index_with_company_body('company != "waisen"')
    out = c.check_query_drift(idx)
    assert len(out) == 1
    assert out[0]["autofixable"] is False


def test_query_drift_canonical_predicate_is_clean():
    idx = _index_with_company_body(c.CANONICAL_PREDICATE)
    out = c.check_query_drift(idx)
    assert out == []


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


def test_propose_aliases_resolves_exact_slug():
    # Bruno Altfall and Frieda Doppelslug both carry "bedag" — without a
    # second person the count assertion below survives the mutant
    # `counts[v] = 1`.
    p = c.propose_aliases(FIXTURE)
    assert p["bedag"]["target"] == "BEDAG Informatik AG"
    assert p["bedag"]["count"] == 2


def test_propose_aliases_marks_ambiguous_with_choose():
    p = c.propose_aliases(FIXTURE)
    assert p["schneeberger"]["target"].startswith("CHOOSE:")
    assert len(p["schneeberger"]["candidates"]) == 2


def test_propose_aliases_leaves_unresolved_empty():
    p = c.propose_aliases(FIXTURE)
    assert p["gibtesnicht"]["target"] is None
    assert p["gibtesnicht"]["candidates"] == []


def test_propose_aliases_never_substring_matches():
    # The one hard rule. Inject into BOTH structures, so the first-word path
    # is exercised too — 78 of 91 real resolutions come through it, and a
    # test that only touches company_norm leaves that path unguarded.
    idx = c.build_index(FIXTURE)
    idx["companies"]["AI21 Labs Inc."] = None
    idx["company_norm"].setdefault("ai21labsinc", []).append("AI21 Labs Inc.")
    assert c._resolve_slug("bsi", idx) == []      # substring of the norm key
    assert c._resolve_slug("labs", idx) == []     # substring of stem, not first word
    assert c._resolve_slug("ai2", idx) == []       # prefix of the first word
    assert c._resolve_slug("ai21", idx) == ["AI21 Labs Inc."]   # first word, exact


def test_propose_aliases_skips_already_migrated():
    # A wholly-migrated value must not surface under its bracketed key. The
    # mixed value from Finding 4 ("Bedag [[Foo]]") is the sole exception —
    # it is not wholly a wikilink and must still be reported.
    p = c.propose_aliases(FIXTURE)
    assert [k for k in p if "[[" in k] == ["Bedag [[Foo]]"]


def test_propose_aliases_keeps_mixed_value_with_wikilink():
    # "Bedag [[Foo]]" is not a migrated value; it must not vanish silently.
    p = c.propose_aliases(FIXTURE)
    assert "Bedag [[Foo]]" in p


def test_first_token_keeps_hyphenated_names_whole():
    idx = c.build_index(FIXTURE)
    idx["companies"]["T-Systems Schweiz AG"] = None
    assert c._resolve_slug("t-systems", idx) == ["T-Systems Schweiz AG"]
    assert c._resolve_slug("t", idx) == []


def test_propose_aliases_marks_match_kind():
    p = c.propose_aliases(FIXTURE)
    assert p["bedag"]["match"] == "exact"          # BEDAG declares slug: bedag
    assert p["gibtesnicht"]["match"] == "none"


PERSON_OLD = (
    "---\ntags:\n  - person\ncompany: bedag\nrole: Berater\n---\n\nText.\n"
)
ALIAS = {"bedag": "BEDAG Informatik AG"}


def test_migrate_person_converts_slug_to_wikilink_list():
    out, changes = c.migrate_person(PERSON_OLD, ALIAS)
    assert 'company:\n  - "[[BEDAG Informatik AG]]"' in out
    assert changes


def test_migrate_person_sets_kind_contact_when_company_present():
    out, _ = c.migrate_person(PERSON_OLD, ALIAS)
    assert "kind: contact" in out


def test_migrate_person_is_idempotent():
    once, _ = c.migrate_person(PERSON_OLD, ALIAS)
    twice, changes = c.migrate_person(once, ALIAS)
    assert once == twice
    assert changes == []


def test_migrate_person_preserves_body_and_other_fields():
    out, _ = c.migrate_person(PERSON_OLD, ALIAS)
    assert out.rstrip().endswith("Text.")
    assert "role: Berater" in out


def test_render_fm_keeps_obsidian_list_indent():
    assert c._render_fm({"tags": ["person", "x"]}) == "tags:\n  - person\n  - x"


def test_render_fm_writes_empty_not_null():
    # Obsidian's property editor shows the literal word "null" otherwise.
    assert c._render_fm({"company": None}) == "company:"


def test_migrate_person_keeps_unresolved_slug_as_legacy():
    text = "---\ntags:\n  - person\ncompany: gibtesnicht\n---\n\nX.\n"
    out, _ = c.migrate_person(text, ALIAS)
    assert "company_legacy: gibtesnicht" in out
    assert "company: []" in out


def test_migrate_person_skips_invalid_yaml():
    text = "---\nkind: : :\n bad\n---\nx"
    out, changes = c.migrate_person(text, ALIAS)
    assert out == text
    assert changes == []


def test_migrate_person_skips_missing_frontmatter():
    text = "Kein Frontmatter hier.\n"
    out, changes = c.migrate_person(text, ALIAS)
    assert out == text
    assert changes == []


def test_infer_kind_student_from_module():
    assert c.infer_kind({"module": ["hf-2024a-os"]}) == "student"


def test_infer_kind_alumni_when_both():
    fm = {"module": ["hf-2024a-os"], "company": ["[[BEDAG Informatik AG]]"]}
    assert c.infer_kind(fm) == "alumni"


def test_load_alias_map_rejects_choose_marker(tmp_path):
    p = tmp_path / "a.yaml"
    p.write_text("schneeberger:\n  count: 3\n  target: 'CHOOSE: A | B'\n")
    try:
        c.load_alias_map(p)
    except ValueError as e:
        assert "schneeberger" in str(e)
    else:
        raise AssertionError("expected ValueError")
