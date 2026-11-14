#!/usr/bin/env python3
"""Validate the frontmatter of Claude Code plugin commands and agents.

Usage: validate_frontmatter.py PATH [PATH ...] [--kind commands|agents]

PATH is a Markdown file or a directory. The kind is taken from the parent
folder name (commands/ or agents/) unless --kind is given. Prints one line per
finding (ERROR or WARNING) and exits 1 if there is any ERROR, 2 if PyYAML is
missing.
"""
import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML is required: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
COMMAND_FIELDS = {"description", "allowed-tools", "category", "argument-hint", "model", "disable-model-invocation"}
COMMAND_INVALID = {"name", "usage"}
AGENT_FIELDS = {"name", "description", "tools", "disallowedTools", "model", "permissionMode", "maxTurns", "skills",
                "mcpServers", "hooks", "memory", "background", "isolation", "category", "color"}
AGENT_REQUIRED = ("name", "description", "category", "model", "color")
MODELS = {"sonnet", "opus", "haiku"}


def frontmatter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None, "no frontmatter block (--- ... ---) at the start of the file"
    try:
        data = yaml.safe_load(m.group(1))
    except yaml.YAMLError as exc:
        return None, "frontmatter is not valid YAML: " + str(exc).splitlines()[0]
    if not isinstance(data, dict):
        return None, "frontmatter is not a mapping"
    return data, None


def check(path, kind):
    """Return a list of (severity, message) for one file."""
    text = path.read_text(encoding="utf-8")
    data, err = frontmatter(text)
    if err:
        return [("ERROR", err)]
    out = []
    desc = data.get("description")
    if not isinstance(desc, str) or not desc.strip():
        out.append(("ERROR", "description is missing or empty"))
    if not re.search(r"^# \S", text.split("\n---\n", 1)[-1], re.M):
        out.append(("WARNING", "no H1 heading in the body"))
    if not KEBAB.match(path.stem):
        out.append(("ERROR", "file name must be lowercase kebab-case"))
    if kind == "commands":
        for f in sorted(COMMAND_INVALID & set(data)):
            out.append(("ERROR", f"field '{f}' is not valid in a command and breaks registration"))
        for f in sorted(set(data) - COMMAND_FIELDS - COMMAND_INVALID):
            out.append(("WARNING", f"unknown field '{f}'"))
        if "allowed-tools" not in data:
            out.append(("ERROR", "allowed-tools is missing"))
        elif not isinstance(data["allowed-tools"], (list, str)):
            out.append(("ERROR", "allowed-tools must be a list or a string"))
    else:
        for f in AGENT_REQUIRED:
            if not data.get(f):
                out.append(("ERROR", f"{f} is missing"))
        name = data.get("name")
        if name and not KEBAB.match(str(name)):
            out.append(("ERROR", "name must be lowercase kebab-case"))
        elif name and str(name) != path.stem:
            out.append(("WARNING", f"name '{name}' differs from the file name"))
        model = data.get("model")
        if model and model not in MODELS:
            out.append(("ERROR", f"model '{model}' must be one of sonnet, opus, haiku (no full model IDs)"))
        for f in sorted(set(data) - AGENT_FIELDS):
            out.append(("WARNING", f"non-standard field '{f}'"))
        if isinstance(desc, str) and re.search(r"\b(I|you|we)\b", desc):
            out.append(("WARNING", "description should be in the third person"))
    return out


def files(path):
    p = Path(path)
    return sorted(p.rglob("*.md")) if p.is_dir() else [p]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--kind", choices=["commands", "agents"])
    args = ap.parse_args()
    errors = 0
    for target in args.paths:
        for f in files(target):
            kind = args.kind or f.parent.name
            if kind not in ("commands", "agents"):
                print(f"WARNING {f}: cannot tell commands from agents, use --kind")
                continue
            for sev, msg in check(f, kind):
                print(f"{sev} {f}: {msg}")
                errors += sev == "ERROR"
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
