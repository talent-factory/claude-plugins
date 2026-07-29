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
