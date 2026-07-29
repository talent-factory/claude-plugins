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
                findings.append({
                    "file": rec["path"], "severity": "minor", "rule": "slug-drift",
                    "message": f"company als Freitext statt Wikilink: {v!r}",
                    "autofixable": True,
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
