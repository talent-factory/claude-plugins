#!/usr/bin/env python3
"""Deterministic validation and migration for Obsidian contact/company links.

Sibling to validate.py. Reads `30 Persons`, `35 Companies` and `85 Wissen/_wiki`
from an Obsidian vault root, emits JSON findings, and performs the one-off
slug-to-wikilink migration. PyYAML is required; when absent the CLI exits 2 with
a JSON error so the calling skill can fall back to prose rules.
"""
import argparse
import json
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
        try:
            amap = load_alias_map(Path(args.alias_map))
        except ValueError as e:
            print(json.dumps({"error": str(e)}))
            return 2
        result = migrate_persons(Path(args.vault_root), amap,
                                 dry_run=not args.apply)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    rules = [r.strip() for r in args.rules.split(",") if r.strip()]
    findings = run(Path(args.vault_root), rules)
    print(json.dumps([{**f, "file": str(f["file"])} for f in findings], indent=2))
    return 1 if any(f["severity"] == "critical" for f in findings) else 0


def load_alias_map(path):
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    out = {}
    for slug, entry in data.items():
        target = entry.get("target") if isinstance(entry, dict) else entry
        if target is None:
            continue
        if str(target).startswith("CHOOSE:"):
            raise ValueError(
                f"unaufgeloester CHOOSE-Marker fuer Slug {slug!r} — "
                "bitte in der Alias-Map entscheiden")
        out[slug] = str(target)
    return out


def infer_kind(fm):
    has_company = bool(company_values(fm))
    has_school = any(fm.get(k) for k in ("school", "module", "class"))
    if has_company and has_school:
        return "alumni"
    if has_company:
        return "contact"
    if has_school:
        return "student"
    return "contact"


class _ObsidianDumper(yaml.SafeDumper):
    """Obsidian indents list items by two spaces; PyYAML flushes them left.

    Without this, migrating rewrites the frontmatter formatting of 1111 of
    1257 person files, burying the 400 real changes in whitespace churn.
    """
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)


def _empty_none(dumper, _value):
    # `company:` reads as empty in Obsidian's property editor.
    # `company: null` shows the user the literal word "null".
    return dumper.represent_scalar("tag:yaml.org,2002:null", "")


_ObsidianDumper.add_representer(type(None), _empty_none)


def _represent_str(dumper, value):
    # PyYAML's default style for strings needing quotes (e.g. "[[Foo]]",
    # which starts with a flow-sequence indicator) is single quotes.
    # Obsidian's own writer always double-quotes wikilinks, so a plain
    # `yaml.safe_dump` migration would reformat every quoted value on the
    # very first pass — a spurious diff on top of the real change. Forcing
    # double quotes for wikilink-shaped values keeps that quiet.
    style = '"' if is_wikilink(value) else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", value, style=style)


_ObsidianDumper.add_representer(str, _represent_str)


def _render_fm(fm):
    return yaml.dump(fm, Dumper=_ObsidianDumper, allow_unicode=True,
                     sort_keys=False, default_flow_style=False).rstrip("\n")


def migrate_person(text, alias_map):
    fm, body = parse_frontmatter(text)
    if not isinstance(fm, dict):
        return text, []          # missing or INVALID — never write
    changes = []
    raw = company_values(fm)
    resolved, legacy = [], []
    for v in raw:
        if is_wikilink(v):
            resolved.append(v)
            continue
        target = alias_map.get(v)
        if target:
            resolved.append(f"[[{target}]]")
            changes.append(f"company {v!r} -> [[{target}]]")
        else:
            legacy.append(v)
            changes.append(f"company {v!r} unaufloesbar -> company_legacy")
    if raw or "company" in fm:
        fm["company"] = resolved
    if legacy:
        fm["company_legacy"] = ", ".join(legacy)
    if fm.get("kind") not in KINDS:
        fm["kind"] = infer_kind(fm)   # after company is set — order matters
        changes.append(f"kind -> {fm['kind']}")
    tags = fm.get("tags") or []
    if isinstance(tags, str):
        tags = [tags]
    if "person" not in tags:
        tags = list(tags) + ["person"]
        fm["tags"] = tags
        changes.append("tags += person")
    if not changes:
        return text, []
    return f"---\n{_render_fm(fm)}\n---{body}", changes


def migrate_persons(vault_root, alias_map, dry_run=True):
    vault_root = Path(vault_root)
    touched, skipped = [], []
    for p in sorted((vault_root / PERSONS_DIR).glob("*.md")):
        text = p.read_text(encoding="utf-8")
        new, changes = migrate_person(text, alias_map)
        if not changes:
            if parse_frontmatter(text)[0] in (None, "INVALID"):
                skipped.append(str(p))
            continue
        touched.append({"file": str(p), "changes": changes})
        if not dry_run:
            p.write_text(new, encoding="utf-8")
    return {"touched": touched, "skipped": skipped, "dry_run": dry_run}


if __name__ == "__main__":
    sys.exit(main())
