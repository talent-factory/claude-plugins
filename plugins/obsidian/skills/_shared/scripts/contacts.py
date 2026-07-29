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
    parts = [p for p in re.split(r"[\s,&\-]+", stem) if p]
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


def propose_aliases(vault_root):
    index = build_index(vault_root)
    counts = {}
    for rec in index["persons"]:
        for v in company_values(rec["fm"]):
            if is_wikilink(v):
                continue
            counts[v] = counts.get(v, 0) + 1
    out = {}
    for slug, n in sorted(counts.items()):
        cands = _resolve_slug(slug, index)
        if len(cands) == 1:
            target = cands[0]
        elif len(cands) > 1:
            target = "CHOOSE: " + " | ".join(cands)
        else:
            target = None
        out[slug] = {"count": n, "target": target, "candidates": cands}
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
    parser.add_argument("--format", default="json", choices=["json"])
    args = parser.parse_args(argv)
    if yaml is None:
        print(json.dumps({"error": "PyYAML not installed", "fallback": "prose"}))
        return 2
    if args.propose_aliases:
        proposal = propose_aliases(Path(args.vault_root))
        print(yaml.safe_dump(proposal, allow_unicode=True, sort_keys=True))
        return 0
    rules = [r.strip() for r in args.rules.split(",") if r.strip()]
    findings = run(Path(args.vault_root), rules)
    print(json.dumps([{**f, "file": str(f["file"])} for f in findings], indent=2))
    return 1 if any(f["severity"] == "critical" for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
