#!/usr/bin/env python3
"""
Insert or replace a daily briefing section in an Obsidian daily note.

Usage:
    python3 update_daily_note.py <YYYY-MM-DD> "<briefing_markdown>"
                                 [--vault /path/to/vault]
                                 [--daily-dir "Daily"]
                                 [--template "Templates/Daily Note.md"]
                                 [--section-heading "### :LiSun: Daily Briefing"]
                                 [--anchor "> ![[tasks-default.base]]"]

Configuration resolution (highest to lowest priority):
  1. CLI flags (--vault, --daily-dir, --template, --section-heading, --anchor)
  2. Environment variables: OBSIDIAN_VAULT, OBSIDIAN_DAILY_DIR, OBSIDIAN_TEMPLATE_DAILY
  3. CLAUDE.md keys: obsidian_vault, obsidian_daily_dir, obsidian_template_daily
  4. Auto-detection: vault via '.obsidian' marker, email via git config
  5. Built-in defaults

Built-in defaults:
  daily_dir:        Daily
  template:         <vault>/Templates/Daily Note.md
  section_heading:  ### :LiSun: Daily Briefing
  anchor:           > ![[tasks-default.base]]
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path


# ── Default constants ─────────────────────────────────────────────────────────
DEFAULT_DAILY_DIR = "Daily"
DEFAULT_TEMPLATE_REL = "Templates/Daily Note.md"
DEFAULT_SECTION_HEADING = "### :LiSun: Daily Briefing"
DEFAULT_ANCHOR = "> ![[tasks-default.base]]"


def _read_claude_md() -> str:
    """Return the content of ~/.claude/CLAUDE.md or empty string."""
    p = Path.home() / ".claude" / "CLAUDE.md"
    try:
        return p.read_text(encoding="utf-8")
    except OSError:
        return ""


def _claude_md_value(text: str, key: str) -> str:
    """Extract a scalar value from a CLAUDE.md key: value line."""
    m = re.search(rf"^{re.escape(key)}:\s*(.+)", text, re.MULTILINE)
    if m:
        return m.group(1).strip().replace("~", str(Path.home()))
    return ""


def _auto_detect_vault() -> str:
    """Find the Obsidian vault root by locating the nearest .obsidian folder."""
    try:
        result = subprocess.run(
            ["find", str(Path.home()), "-maxdepth", "5", "-name", ".obsidian", "-type", "d"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        hits = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        if hits:
            return str(Path(hits[0]).parent)
    except (OSError, subprocess.TimeoutExpired):
        pass
    return ""


def resolve_config(args: argparse.Namespace) -> dict[str, str]:
    """Build the effective configuration by merging all sources."""
    claude_md = _read_claude_md()
    cfg: dict[str, str] = {}

    # 1. CLAUDE.md
    for key, cfg_key in [
        ("obsidian_vault", "vault"),
        ("obsidian_daily_dir", "daily_dir"),
        ("obsidian_template_daily", "template"),
    ]:
        val = _claude_md_value(claude_md, key)
        if val:
            cfg[cfg_key] = val

    # 2. Environment variables
    if "OBSIDIAN_VAULT" in os.environ:
        cfg["vault"] = os.environ["OBSIDIAN_VAULT"]
    if "OBSIDIAN_DAILY_DIR" in os.environ:
        cfg["daily_dir"] = os.environ["OBSIDIAN_DAILY_DIR"]
    if "OBSIDIAN_TEMPLATE_DAILY" in os.environ:
        cfg["template"] = os.environ["OBSIDIAN_TEMPLATE_DAILY"]

    # 3. CLI flags (highest priority)
    if args.vault:
        cfg["vault"] = args.vault
    if args.daily_dir:
        cfg["daily_dir"] = args.daily_dir
    if args.template:
        cfg["template"] = args.template

    # 4. Auto-detect vault if still not set
    if "vault" not in cfg:
        detected = _auto_detect_vault()
        if detected:
            cfg["vault"] = detected

    if "vault" not in cfg:
        print(
            "Error: Obsidian vault not found.\n"
            "Set 'obsidian_vault: /path/to/vault' in ~/.claude/CLAUDE.md\n"
            "or export OBSIDIAN_VAULT=/path/to/vault",
            file=sys.stderr,
        )
        sys.exit(1)

    # 5. Apply defaults for remaining keys
    vault = Path(cfg["vault"])
    cfg.setdefault("daily_dir", DEFAULT_DAILY_DIR)
    cfg.setdefault("template", str(vault / DEFAULT_TEMPLATE_REL))

    # Section heading and anchor come from CLI only (or built-in defaults)
    cfg["section_heading"] = args.section_heading or DEFAULT_SECTION_HEADING
    cfg["anchor"] = args.anchor or DEFAULT_ANCHOR

    return cfg


def create_note(note_path: Path, template_path: Path, target_date: date) -> None:
    """Create a new daily note from the template, substituting date placeholders."""
    yesterday = (target_date - timedelta(days=1)).strftime("%Y-%m-%d")
    tomorrow = (target_date + timedelta(days=1)).strftime("%Y-%m-%d")
    tp = Path(template_path)
    if tp.exists():
        text = tp.read_text(encoding="utf-8")
        text = text.replace("{{yesterday}}", yesterday).replace("{{tomorrow}}", tomorrow)
    else:
        text = f"# {target_date.isoformat()}\n"
    note_path.parent.mkdir(parents=True, exist_ok=True)
    note_path.write_text(text, encoding="utf-8")


def update_note(note_path: Path, briefing: str, heading: str, anchor: str) -> None:
    """Insert or replace the briefing section in an existing note."""
    text = note_path.read_text(encoding="utf-8")

    if heading in text:
        # Replace the existing briefing block (up to the next ### heading or EOF)
        text = re.sub(
            rf"{re.escape(heading)}.*?(?=\n### |\Z)",
            briefing.rstrip() + "\n",
            text,
            flags=re.DOTALL,
        )
    elif anchor in text:
        # Insert immediately after the anchor line
        text = text.replace(anchor, anchor + "\n\n" + briefing.rstrip())
    else:
        # Fallback: append at end of file
        text = text.rstrip() + "\n\n" + briefing.rstrip() + "\n"

    note_path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Insert or replace a daily briefing section in an Obsidian daily note."
    )
    parser.add_argument("date", help="Target date in YYYY-MM-DD format")
    parser.add_argument("briefing", help="Briefing markdown content")
    parser.add_argument("--vault", help="Path to Obsidian vault root")
    parser.add_argument("--daily-dir", dest="daily_dir", help="Daily notes folder (relative to vault)")
    parser.add_argument("--template", help="Path to daily note template")
    parser.add_argument(
        "--section-heading",
        dest="section_heading",
        help=f"Heading used to find/replace the briefing block (default: '{DEFAULT_SECTION_HEADING}')",
    )
    parser.add_argument(
        "--anchor",
        help=f"Anchor line after which the briefing is inserted on first run (default: '{DEFAULT_ANCHOR}')",
    )
    args = parser.parse_args()

    cfg = resolve_config(args)

    vault = Path(cfg["vault"])
    if not vault.exists():
        print(f"Error: Vault not found at {vault}", file=sys.stderr)
        sys.exit(1)

    daily_dir = vault / cfg["daily_dir"]
    target_date = date.fromisoformat(args.date)
    note_path = daily_dir / f"{target_date.isoformat()}.md"

    if not note_path.exists():
        create_note(note_path, Path(cfg["template"]), target_date)
        print(f"Created: {note_path.relative_to(vault)}")

    update_note(note_path, args.briefing, cfg["section_heading"], cfg["anchor"])
    print(f"Updated: {note_path.relative_to(vault)}")


if __name__ == "__main__":
    main()
