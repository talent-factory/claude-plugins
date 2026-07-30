import json
import sys
from pathlib import Path

import yaml

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


def test_migrate_person_returns_original_bytes_when_nothing_changes():
    # Feed it formatting the renderer would never produce. Without the
    # early exit this comes back reformatted, and the test above cannot
    # tell the difference because it feeds back the renderer's own output.
    t = ("---\ntags:\n    - person\nkind: contact\n"
         "company:\n    - '[[BEDAG Informatik AG]]'\n---\n\nB\n")
    out, changes = c.migrate_person(t, {})
    assert out == t
    assert changes == []


def test_migrate_person_preserves_body_and_other_fields():
    out, _ = c.migrate_person(PERSON_OLD, ALIAS)
    assert out.rstrip().endswith("Text.")
    assert "role: Berater" in out


def test_render_key_uses_obsidian_list_indent():
    assert c._render_key("tags", ["person", "x"]) == ["tags:", "  - person", "  - x"]


def test_render_key_writes_empty_not_null():
    # Obsidian's property editor shows the literal word "null" otherwise.
    assert c._render_key("company", []) == ["company:"]


def test_render_key_double_quotes_wikilinks():
    assert c._render_key("company", ["[[BEDAG Informatik AG]]"]) == [
        "company:", '  - "[[BEDAG Informatik AG]]"']


def test_migrate_person_leaves_untouched_fields_byte_identical():
    # The whole point of surgical editing: a timestamp, a block scalar and a
    # long prose value must survive unchanged.
    text = (
        "---\n"
        "tags:\n  - person\n"
        "company: bedag\n"
        "termin: 2026-06-19T15:00:00\n"
        "telefon: 0313456\n"
        "notiz: |-\n  Zeile eins\n  Zeile zwei\n"
        "rolle: " + "x" * 120 + "\n"
        "---\n\nText.\n"
    )
    out, changes = c.migrate_person(text, ALIAS)
    assert changes
    assert "termin: 2026-06-19T15:00:00" in out
    assert "telefon: 0313456" in out
    assert "notiz: |-\n  Zeile eins\n  Zeile zwei" in out
    assert "rolle: " + "x" * 120 in out


def test_migrate_person_refuses_ambiguous_delimiters():
    # A "---" inside a value: validate.parse_frontmatter would split there and
    # evict every later key into the body.
    text = ("---\ntags:\n  - person\n"
            "notiz: |\n  Erstkontakt\n  ---\n  Nachfass\n"
            "company: bedag\n---\n\nText.\n")
    out, changes = c.migrate_person(text, ALIAS)
    assert out == text
    assert changes == []


def test_migrate_person_merges_existing_company_legacy():
    text = ("---\ntags:\n  - person\ncompany: unbekannt2\n"
            "company_legacy:\n  - alte-firma-ag\n---\n\nX.\n")
    out, _ = c.migrate_person(text, ALIAS)
    assert "alte-firma-ag" in out
    assert "unbekannt2" in out


def test_infer_kind_uses_pre_migration_company():
    # Someone with a module AND an unresolvable company is alumni, not
    # student — the company field is empty only because we just emptied it.
    fm = {"module": ["hf-2024a-os"], "company": []}
    assert c.infer_kind(fm, has_company=True) == "alumni"


# Fix round 1, item 1: infer_kind's has_school widening. The real-world
# trigger is "30 Persons/Aaron Venetz.md" — tags carry the module code,
# frontmatter carries the module's per-field grade tracking, no `school:`/
# `module:`/`class:` key anywhere. Each test's mutation check: temporarily
# comment out the corresponding `or _has_...(fm)` clause in infer_kind and
# confirm the test goes red before restoring it (see task-8-report.md, Fix
# round 1, item 1a for the recorded before/after run).

def test_infer_kind_module_field_key_signal():
    # Isolates the frontmatter-key signal: tag is plain "person" (does not
    # itself match the module-code tag pattern), so only the per-module
    # frontmatter fields (modulnote/gitlab/group/aufgabe — Aaron Venetz's
    # actual field set) can trigger the classification.
    fm = {
        "tags": ["person"],
        "inf-p-se003-modulnote": "5.7",
        "inf-p-se003-gitlab": "https://git.ffhs.ch/aaron.venetz/dua-aufgaben",
        "inf-p-se003-group": 9,
        "inf-p-se003-aufgabe": False,
    }
    assert c.infer_kind(fm) == "student"


def test_infer_kind_module_tag_signal():
    # Module-code tag alone (no matching frontmatter field, no company) —
    # covers the "#inf-p-se017-ol-fs24" shape (leading "#" must be stripped).
    fm = {"tags": ["person", "#inf-p-se017-ol-fs24"]}
    assert c.infer_kind(fm) == "student"


def test_infer_kind_student_email_domain_signal():
    # Student mail domain alone (no tag, no frontmatter field, no company).
    fm = {"tags": ["person"], "email": "aaron.venetz@students.ffhs.ch"}
    assert c.infer_kind(fm) == "student"


def test_infer_kind_student_email_domain_precision():
    # Table-driven: the first domain label must be exactly "stud",
    # "student", or "students" — not merely start with "stud". Guards
    # against the over-broad `@stud[a-z]*\.` shape (fixed in
    # task-8-report.md, Fix round 2) that misclassified real domains like
    # "studio.com" as student/alumni evidence.
    cases = [
        # (email, expect_student, label)
        ("person@students.ffhs.ch", True, "attested: students.ffhs.ch"),
        ("person@stud.gibb.ch", True, "attested: stud.gibb.ch"),
        ("person@student.education.ch", True, "attested: student.education.ch"),
        ("person@studio.com", False, "false positive: studio.com"),
        ("person@studieren.de", False, "false positive: studieren.de"),
        ("person@studentx.io", False, "false positive: studentx.io"),
        ("person@studmail.example.com", False, "false positive: studmail.example.com"),
    ]
    for email, expect_student, label in cases:
        fm = {"tags": ["person"], "email": email}
        kind = c.infer_kind(fm)
        if expect_student:
            assert kind == "student", f"{label}: expected student, got {kind!r}"
        else:
            assert kind != "student", f"{label}: expected not student, got {kind!r}"


def test_infer_kind_student_email_domain_in_list():
    # `email` may be a list (a private + a student address) — the domain
    # check must scan every item, not just fm["email"] as a scalar.
    fm = {"tags": ["person"], "email": ["alita@gmail.com", "alita.seehawat@students.ffhs.ch"]}
    assert c.infer_kind(fm) == "student"


def test_infer_kind_plain_contact_stays_contact():
    # Negative: a real contact with an ordinary word tag, a plain business
    # domain, and no module-shaped frontmatter keys must not be reclassified.
    fm = {
        "tags": ["person", "talent-factory"],
        "email": "info@acme.ch",
        "role": "CTO",
        "company": ["[[Acme AG]]"],
    }
    assert c.infer_kind(fm) == "contact"


def test_load_alias_map_rejects_pipe_in_target(tmp_path):
    p = tmp_path / "a.yaml"
    p.write_text("s:\n  target: A AG | B AG\n")
    try:
        c.load_alias_map(p)
    except ValueError as e:
        assert "|" in str(e)
    else:
        raise AssertionError("expected ValueError")


def test_migrate_person_keeps_unresolved_slug_as_legacy():
    text = "---\ntags:\n  - person\ncompany: gibtesnicht\n---\n\nX.\n"
    out, _ = c.migrate_person(text, ALIAS)
    assert "company_legacy: gibtesnicht" in out
    # Empty company renders as a bare "company:", not "company: []" — see
    # test_render_key_writes_empty_not_null, which is authoritative for
    # _render_key's empty-value behaviour (carried over from the brief that
    # predates surgical editing; PyYAML's `yaml.safe_dump([])` used to
    # produce "[]" here, `_render_key` deliberately does not).
    assert "company:\n" in out


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


def test_render_key_quotes_yaml_significant_values():
    # An f-string interpolation is not safe here: each of these breaks the
    # parser, silently becomes a different type, or (the `#`-prefixed one)
    # turns into a YAML comment — see contacts.py's _scalar docstring.
    hostile = [
        "Firma: Abteilung",
        "[[Foo AG]] (ehemals)",
        "#inf-p-se017",
        "yes",
        "null",
        "*star",
        "- dash",
        "{a}",
    ]
    for v in hostile:
        rendered = c._render_key("company_legacy", [v])[1].removeprefix("  - ")
        assert yaml.safe_load(rendered) == v, f"{v!r} round-tripped to something else"


def test_key_span_refuses_duplicate_key():
    # YAML resolves duplicate keys last-wins; editing the first match would
    # silently destroy the value that actually takes effect.
    lines = ["company: slug-a", "other: x", "company: slug-b"]
    try:
        c._key_span(lines, "company")
    except c._Unsafe as e:
        assert "company" in str(e)
    else:
        raise AssertionError("expected _Unsafe")


def test_key_span_refuses_dangling_flow_collection():
    # The column-0 closing `]` of a multi-line flow collection is not an
    # indented continuation line, so the span scan stops one line short —
    # editing this would leave a dangling `]` behind and break the YAML.
    lines = ["company: [", "  a,", "  b", "]"]
    try:
        c._key_span(lines, "company")
    except c._Unsafe as e:
        assert "company" in str(e)
    else:
        raise AssertionError("expected _Unsafe")


def test_skip_reason_reports_broken_yaml_not_silence():
    # Round 1's classifier (parse_frontmatter in (None, "INVALID")) caught
    # this; the surgical rewrite's migrate_persons must not let a file with
    # valid delimiters but broken YAML fall through touched and skipped both.
    text = "---\nkind: : :\n bad\n---\nx"
    reason = c.skip_reason(text)
    assert reason is not None
    assert "YAML" in reason


def test_scalar_survives_quotes_inside_a_wikilink():
    # _WHOLE_WIKILINK_RE permits anything but `]` inside the target, so a
    # naive `f'"{s}"'` fast path breaks on a quote or backslash. _scalar
    # must fall through to PyYAML quoting when the double-quoted form
    # would not round-trip.
    for v in ['[[Foo "Bar" AG]]', "[[Back\\slash AG]]"]:
        rendered = c._scalar(v)
        assert yaml.safe_load(rendered) == v, f"{v!r} round-tripped to something else"


def test_key_span_refuses_bracket_inside_quoted_item():
    # Counting brackets alone misses a `]` inside a quoted scalar (here
    # balancing at 1/1) — the closing `]` of the flow collection still
    # sits outside the indented-continuation span and would be dropped.
    lines = ["company: [", '  "a]",', "  b", "]"]
    try:
        c._key_span(lines, "company")
    except c._Unsafe as e:
        assert "company" in str(e)
    else:
        raise AssertionError("expected _Unsafe")


def test_key_span_allows_single_line_flow_collections():
    assert c._key_span(["company: [a, b]"], "company") == (0, 1)
    assert c._key_span(["company: {a: 1}"], "company") == (0, 1)


def test_migrate_persons_buckets_refused_files_with_reasons(tmp_path):
    # N6 regression coverage: migrate_persons's bucketing could be deleted
    # and the suite would stay green without this — everything else tests
    # skip_reason/migrate_person in isolation, nothing asserted that the
    # batch runner actually routes a refused file into `skipped` with a
    # non-empty reason.
    persons = tmp_path / c.PERSONS_DIR
    persons.mkdir(parents=True)
    (persons / "clean.md").write_text("---\ntags:\n  - x\n---\n\nBody.\n", encoding="utf-8")
    (persons / "duplicate.md").write_text(
        "---\ncompany: slug-a\ntags:\n  - person\ncompany: slug-b\n---\n\nBody.\n",
        encoding="utf-8",
    )
    (persons / "broken.md").write_text("---\nkind: : :\n bad\n---\n\nBody.\n", encoding="utf-8")

    result = c.migrate_persons(tmp_path, {}, dry_run=True)

    assert len(result["touched"]) == 1
    assert len(result["skipped"]) == 2
    assert all(s["reason"] for s in result["skipped"])
    assert result["failed"] == []


COMPANY_OLD = (
    "---\ntags:\n  - company\n---\n\n### Mitarbeiter\n\n"
    "```dataview\ntable role as Funktion\n"
    '\twhere contains(tags, "person") and contains(company, "bedag")\n'
    "\tsort file.name asc\n```\n"
)


def test_migrate_company_queries_replaces_predicate_only():
    out, changes = c.migrate_company_queries(COMPANY_OLD)
    assert "contains(company, this.file.link)" in out
    assert '"bedag"' not in out
    assert 'contains(tags, "person")' in out      # rest of query untouched
    assert "sort file.name asc" in out
    assert changes


def test_migrate_company_queries_handles_equals_form():
    text = '```dataview\nwhere tags = "person" and company = "bedag"\n```\n'
    out, _ = c.migrate_company_queries(text)
    assert "contains(company, this.file.link)" in out


def test_migrate_company_queries_leaves_tag_only_query_alone():
    text = ('```dataview\nwhere contains(tags, "person") '
            'and contains(tags, "bedag")\n```\n')
    out, changes = c.migrate_company_queries(text)
    assert out == text
    assert changes == []


def test_migrate_company_queries_leaves_base_blocks_alone():
    # `company.contains("bedag")` (the round-1 body) is not matched by
    # COMPANY_PREDICATE_RE at all, so this used to pass whether or not
    # `lang != "dataview"` was even checked. Use a body the regex *would*
    # match, so the guard is the only thing keeping it untouched.
    text = '```base\nfilters:\n  - where: company = "bedag"\n```\n'
    out, changes = c.migrate_company_queries(text)
    assert out == text
    assert changes == []


def test_migrate_company_queries_is_idempotent():
    once, _ = c.migrate_company_queries(COMPANY_OLD)
    twice, changes = c.migrate_company_queries(once)
    assert once == twice
    assert changes == []


def test_migrate_company_frontmatter_adds_slug():
    out, changes = c.migrate_company_frontmatter(COMPANY_OLD, ["bedag"])
    assert "slug: bedag" in out
    assert changes


def test_migrate_company_frontmatter_puts_extra_slugs_into_aliases():
    # `"bedag-informatik" in out` alone would pass if the value landed under
    # `slug:` or leaked into the body — assert on the parsed structure.
    out, _ = c.migrate_company_frontmatter(
        COMPANY_OLD, ["bedag", "bedag-informatik", "bedag.ch"])
    fm = yaml.safe_load(c._fm_parts(out)[1])
    assert fm["slug"] == "bedag"
    assert set(fm["aliases"]) == {"bedag-informatik", "bedag.ch"}


def test_migrate_company_frontmatter_merges_existing_aliases():
    # Covers a requirement round 1 had zero coverage for: pre-existing
    # aliases must survive (a mutant reducing the union to just the new
    # extras passed the full suite), and a curated `slug:` that disagrees
    # with the new primary must be preserved as an alias, not discarded —
    # the same merge-never-overwrite rule this module already applies to
    # `company_legacy`.
    text = ("---\ntags:\n  - company\nslug: bedag-informatik\n"
            "aliases:\n  - bedag-alt\n---\n\nBody.\n")
    out, changes = c.migrate_company_frontmatter(text, ["bedag", "bedag.ch"])
    fm = yaml.safe_load(c._fm_parts(out)[1])
    assert fm["slug"] == "bedag"
    assert set(fm["aliases"]) == {"bedag-alt", "bedag-informatik", "bedag.ch"}
    assert changes


def test_migrate_company_frontmatter_idempotent():
    once, _ = c.migrate_company_frontmatter(COMPANY_OLD, ["bedag", "bedag.ch"])
    twice, changes = c.migrate_company_frontmatter(once, ["bedag", "bedag.ch"])
    assert once == twice
    assert changes == []


def test_migrate_company_frontmatter_noop_without_slugs():
    out, changes = c.migrate_company_frontmatter(COMPANY_OLD, [])
    assert out == COMPANY_OLD
    assert changes == []


def test_migrate_company_frontmatter_refuses_ambiguous_delimiters():
    # A "---" inside a block-scalar value: the naive `validate.parse_frontmatter`
    # split would evict every later key into the body; `_fm_parts` must
    # refuse instead of guessing, and this function must leave the file
    # byte-identical when it does.
    text = ("---\ntags:\n  - company\n"
            "notiz: |\n  Erstkontakt\n  ---\n  Nachfass\n"
            "---\n\nText.\n")
    out, changes = c.migrate_company_frontmatter(text, ["bedag"])
    assert out == text
    assert changes == []


def test_migrate_companies_buckets_refused_files_with_reasons(tmp_path):
    companies = tmp_path / c.COMPANIES_DIR
    companies.mkdir(parents=True)
    (companies / "clean.md").write_text(
        "---\ntags:\n  - company\n---\n\nBody.\n", encoding="utf-8")
    (companies / "duplicate.md").write_text(
        "---\nslug: a\ntags:\n  - company\nslug: b\n---\n\nBody.\n",
        encoding="utf-8",
    )
    (companies / "broken.md").write_text(
        "---\nkind: : :\n bad\n---\n\nBody.\n", encoding="utf-8")

    result = c.migrate_companies(tmp_path, {"x": "clean"}, dry_run=True)

    assert len(result["touched"]) == 1
    assert len(result["skipped"]) == 2
    assert all(s["reason"] for s in result["skipped"])
    assert result["failed"] == []


def test_migrate_companies_reports_unknown_targets(tmp_path):
    # `migrate_companies` is the only function that enumerates COMPANIES_DIR,
    # so it is the only place that can catch an alias-map target with no
    # matching company page before migrate_persons writes a wikilink to it —
    # a link that would then never resolve against `this.file.link`.
    companies = tmp_path / c.COMPANIES_DIR
    companies.mkdir(parents=True)
    (companies / "Bedag Informatik AG.md").write_text(
        "---\ntags:\n  - company\n---\n\nBody.\n", encoding="utf-8")

    result = c.migrate_companies(
        tmp_path, {"tippfehler": "Bedag Informatk AG"}, dry_run=True)

    assert result["unknown_targets"] == ["Bedag Informatk AG"]


# Round 2: a curated `slug:`/`aliases:` can be structurally well-delimited
# (passes `_key_span` cleanly) and still be the wrong *type* — `slug: 2024`,
# `slug: off` (YAML-1.1 bool-like), `aliases: {a: b}` (flow mapping), or
# `aliases: bedag-alt` (plain scalar). `company_skip_reason` did not check
# value types before this fix, so these passed the gate and were then either
# silently overwritten (`slug`) or silently dropped (`aliases`) inside
# `migrate_company_frontmatter` — never reported, never refused.

def test_company_skip_reason_refuses_non_string_slug_numeric():
    text = "---\ntags:\n  - company\nslug: 2024\n---\n\nBody.\n"
    assert c.company_skip_reason(text) is not None


def test_company_skip_reason_refuses_non_string_slug_boollike():
    text = "---\ntags:\n  - company\nslug: off\n---\n\nBody.\n"
    assert c.company_skip_reason(text) is not None


def test_company_skip_reason_refuses_flow_mapping_aliases():
    text = "---\ntags:\n  - company\naliases: {a: b}\n---\n\nBody.\n"
    assert c.company_skip_reason(text) is not None


def test_company_skip_reason_refuses_scalar_string_aliases():
    text = "---\ntags:\n  - company\naliases: bedag-alt\n---\n\nBody.\n"
    assert c.company_skip_reason(text) is not None


def test_migrate_company_frontmatter_refuses_non_string_slug_numeric():
    text = "---\ntags:\n  - company\nslug: 2024\n---\n\nBody.\n"
    out, changes = c.migrate_company_frontmatter(text, ["bedag"])
    assert out == text
    assert changes == []


def test_migrate_company_frontmatter_refuses_non_string_slug_boollike():
    text = "---\ntags:\n  - company\nslug: off\n---\n\nBody.\n"
    out, changes = c.migrate_company_frontmatter(text, ["bedag"])
    assert out == text
    assert changes == []


def test_migrate_company_frontmatter_refuses_flow_mapping_aliases():
    text = "---\ntags:\n  - company\naliases: {a: b}\n---\n\nBody.\n"
    out, changes = c.migrate_company_frontmatter(text, ["bedag"])
    assert out == text
    assert changes == []


def test_migrate_company_frontmatter_refuses_scalar_string_aliases():
    text = "---\ntags:\n  - company\naliases: bedag-alt\n---\n\nBody.\n"
    out, changes = c.migrate_company_frontmatter(text, ["bedag"])
    assert out == text
    assert changes == []


def test_migrate_companies_buckets_bad_slug_and_aliases_types_as_skipped(tmp_path):
    # With an empty alias map both files would get no slugs assigned and the
    # invisibility bug (finding B) would not be exercised (empty-slugs is
    # already a legitimate no-op, not a defect). Route real slugs at both
    # stems via the alias map so `migrate_company_frontmatter` actually has
    # to read the bad `slug:`/`aliases:` values.
    companies = tmp_path / c.COMPANIES_DIR
    companies.mkdir(parents=True)
    (companies / "badslug.md").write_text(
        "---\ntags:\n  - company\nslug: 2024\n---\n\nBody.\n", encoding="utf-8")
    (companies / "badaliases.md").write_text(
        "---\ntags:\n  - company\naliases: {a: b}\n---\n\nBody.\n",
        encoding="utf-8")

    alias_map = {"badslug-alt": "badslug", "badaliases-alt": "badaliases"}
    result = c.migrate_companies(tmp_path, alias_map, dry_run=True)

    assert result["touched"] == []
    assert len(result["skipped"]) == 2
    assert all(s["reason"] for s in result["skipped"])
    assert result["failed"] == []
    badslug_text = (companies / "badslug.md").read_text(encoding="utf-8")
    assert "slug: 2024" in badslug_text


def test_person_mentions_finds_wikilinked_person():
    m = c.person_mentions(FIXTURE, None)
    hit = [x for x in m if x["person"] == "Anna Beispiel"]
    assert len(hit) == 1
    assert hit[0]["linked"] is True
    assert "Coding-Agents" in hit[0]["context"]


def test_person_mentions_finds_plaintext_person():
    m = c.person_mentions(FIXTURE, None)
    hit = [x for x in m if x["person"] == "Bruno Altfall"]
    assert len(hit) == 1
    assert hit[0]["linked"] is False


def test_person_mentions_respects_since():
    assert c.person_mentions(FIXTURE, "2026-08-01") == []
    assert c.person_mentions(FIXTURE, "2026-06-01")


def test_person_mentions_ignores_code_blocks():
    m = [x for x in c.person_mentions(FIXTURE, "2026-07-02")
         if x["daily"] == "2026-07-02"]
    assert m == []


def test_person_mentions_only_filter_restricts_names():
    m = c.person_mentions(FIXTURE, None, only=["Anna Beispiel"])
    assert {x["person"] for x in m} == {"Anna Beispiel"}


def test_person_mentions_respects_name_boundaries():
    # "Patrick Lang" must not be reported for a daily that names
    # "Patrick Langloh" — both exist in the real vault.
    m = [x for x in c.person_mentions(FIXTURE, "2026-07-03")
         if x["daily"] == "2026-07-03"]
    assert {x["person"] for x in m} == {"Patrick Langloh"}


def test_mention_match_prefers_plaintext_when_wikilink_follows():
    # Plain text first, wikilink later — the still-actionable plain-text
    # occurrence at position 0 must win, not the already-linked one at 54.
    text = ("Bruno Altfall hat geschrieben. Später erwähnte auch "
            "[[Bruno Altfall]] das Projekt.")
    pos, linked = c._mention_match(text, "Bruno Altfall")
    assert (pos, linked) == (0, False)


def test_mention_match_prefers_plaintext_when_wikilink_precedes():
    # Same pair, reversed order — the plain-text occurrence still wins,
    # regardless of where in the text it sits relative to the wikilink.
    text = ("Zuerst erwähnt als [[Bruno Altfall]]. Später schrieb "
            "Bruno Altfall selbst dazu.")
    pos, linked = c._mention_match(text, "Bruno Altfall")
    assert linked is False
    assert text[pos:pos + len("Bruno Altfall")] == "Bruno Altfall"
    assert text[pos - 2:pos] != "[["


def test_mention_match_returns_linked_true_for_wikilink_only():
    # No plain-text occurrence anywhere — must still report linked=True,
    # so the precedence fix does not silently make everything unlinked.
    text = "Notiz zu [[Bruno Altfall]] und dem naechsten Termin."
    pos, linked = c._mention_match(text, "Bruno Altfall")
    assert linked is True
    assert text[pos - 2:pos] == "[["
