#!/usr/bin/env python3
"""Utility functions for commit workflow."""

import os
import sys
from typing import Optional


def print_header(text: str):
    """Print formatted header."""
    print(f"\n{'=' * 60}")
    print(f"  {text}")
    print(f"{'=' * 60}\n")


def print_success(text: str):
    """Print success message."""
    print(f"✓ {text}")


def print_error(text: str):
    """Print error message."""
    print(f"✗ {text}", file=sys.stderr)


def print_warning(text: str):
    """Print warning message."""
    print(f"⚠️  {text}")


def print_info(text: str):
    """Print info message."""
    print(f"ℹ️  {text}")


def confirm(question: str, default: bool = True) -> bool:
    """Ask user for confirmation."""
    suffix = " [Y/n]" if default else " [y/N]"
    response = input(f"{question}{suffix} ").strip().lower()

    if not response:
        return default

    return response in ['y', 'yes', 'ja']


def get_skill_root() -> str:
    """Get skill root directory."""
    # This file is in scripts/, so parent is skill root
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_json_config(filename: str) -> dict:
    """Load JSON configuration file."""
    import json
    from pathlib import Path

    config_path = Path(get_skill_root()) / "config" / filename

    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print_error(f"Configuration file not found: {config_path}")
        return {}
    except json.JSONDecodeError as e:
        print_error(f"Invalid JSON in {filename}: {e}")
        return {}


def format_file_list(files: list, max_display: int = 10) -> str:
    """Format file list for display."""
    if not files:
        return "  (keine)"

    lines = []
    for i, filepath in enumerate(files[:max_display]):
        lines.append(f"  - {filepath}")

    if len(files) > max_display:
        lines.append(f"  ... und {len(files) - max_display} weitere")

    return '\n'.join(lines)


def truncate_text(text: str, max_length: int = 80) -> str:
    """Truncate text to max length."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


class Colors:
    """ANSI color codes for terminal output."""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'

    @classmethod
    def is_supported(cls) -> bool:
        """Check if terminal supports colors."""
        return sys.stdout.isatty() and os.getenv('TERM') != 'dumb'


def colorize(text: str, color: str) -> str:
    """Colorize text if terminal supports it."""
    if not Colors.is_supported():
        return text

    color_code = getattr(Colors, color.upper(), Colors.RESET)
    return f"{color_code}{text}{Colors.RESET}"
