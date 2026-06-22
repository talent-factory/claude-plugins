#!/usr/bin/env python3
"""Deterministic structural and link validation for the LLM-Wiki schema.

Importable functions are used by the obsidian plugin's wiki skills; the CLI
(`main`) prints a JSON array of findings. PyYAML is required; when absent the
CLI exits 2 with a JSON error so the calling skill can fall back to prose rules.
"""
import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # graceful degradation — see Global Constraints
    yaml = None

WIKI_TYPES = {"concept", "tool", "compare", "hub", "note", "thinking"}
SOURCE_TYPES = {"clipping", "chat", "note", "transcript"}
MEDIA_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".pdf", ".svg", ".mp4", ".mov"}

CHECKS = {}


def register(name):
    def deco(fn):
        CHECKS[name] = fn
        return fn
    return deco


def parse_frontmatter(text):
    if not text.startswith("---"):
        return None, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None, text
    if yaml is None:
        return None, parts[2]
    try:
        fm = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return "INVALID", parts[2]
    if not isinstance(fm, dict):
        return None, parts[2]
    return fm, parts[2]


def strip_code(text):
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"`[^`\n]*`", "", text)
    return text


def normalize_link(inner):
    inner = inner.replace("\\|", "|").split("|")[0]
    inner = inner.split("#")[0]
    inner = inner.rsplit("/", 1)[-1]
    if inner.endswith(".md"):
        inner = inner[:-3]
    return inner.strip()


def normalize_ref(s):
    s = str(s).strip()
    m = re.search(r"\[\[([^\]]+)\]\]", s)
    if m:
        return normalize_link(m.group(1))
    return normalize_link(s)


def fm_related(fm):
    rel = fm.get("related")
    if rel is None:
        return []
    if isinstance(rel, str):
        return [rel]
    if isinstance(rel, list):
        return [str(x) for x in rel]
    return []


def load_record(path):
    text = path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    return {"path": path, "fm": fm, "body": body, "text": text}


def build_index(vault_root):
    names = set()
    related = {}
    wiki = vault_root / "_wiki"
    raw = vault_root / "_raw"
    for base in (wiki, raw):
        if base.exists():
            for p in base.rglob("*.md"):
                names.add(p.stem)
    for p in vault_root.rglob("*"):
        if p.is_file() and p.suffix.lower() in MEDIA_EXTS:
            names.add(p.stem)
    if wiki.exists():
        for p in wiki.rglob("*.md"):
            rec = load_record(p)
            if isinstance(rec["fm"], dict):
                related[p.stem] = {normalize_ref(r) for r in fm_related(rec["fm"])}
    return {"names": names, "related": related}


def _scope_records(vault_root, target):
    if target is not None:
        return [load_record(target)]
    records = []
    for sub in ("_wiki", "_raw"):
        base = vault_root / sub
        if base.exists():
            for p in sorted(base.rglob("*.md")):
                records.append(load_record(p))
    return records


def run(vault_root, rules, target):
    index = build_index(vault_root)
    records = _scope_records(vault_root, target)
    findings = []
    for name in rules:
        fn = CHECKS.get(name)
        if fn:
            findings.extend(fn(records, index))
    return findings


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate LLM-Wiki files.")
    parser.add_argument("--vault-root", required=True)
    parser.add_argument("--target", default=None)
    parser.add_argument("--rules", default=",".join(CHECKS.keys()))
    parser.add_argument("--format", default="json", choices=["json"])
    args = parser.parse_args(argv)
    if yaml is None:
        print(json.dumps({"error": "PyYAML not installed", "fallback": "prose"}))
        return 2
    rules = [r.strip() for r in args.rules.split(",") if r.strip()]
    target = Path(args.target) if args.target else None
    findings = run(Path(args.vault_root), rules, target)
    print(json.dumps([{**f, "file": str(f["file"])} for f in findings], indent=2))
    return 1 if any(f["severity"] == "critical" for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
