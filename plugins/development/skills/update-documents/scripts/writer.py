"""Markdown section writer."""

import re
from pathlib import Path

from extractor import _normalize_title


def _write_cleaned(file_path: Path, lines: list[str]) -> None:
    """Remove consecutive blank lines and write with trailing newline."""
    cleaned_lines = []
    prev_empty = False
    for line in lines:
        is_empty = not line.strip()
        if is_empty and prev_empty:
            continue
        cleaned_lines.append(line)
        prev_empty = is_empty

    result = "\n".join(cleaned_lines)
    if not result.endswith("\n"):
        result += "\n"

    file_path.write_text(result, encoding="utf-8")


def update_section(
    file_path: Path,
    section_name: str,
    new_content: str,
    create_if_missing: bool = False,
) -> bool:
    """
    Update a section in a Markdown file.

    Args:
        file_path: Path to the Markdown file
        section_name: Name of the heading (without #)
        new_content: New content for the section
        create_if_missing: If True, create the section at the end if not found

    Returns:
        True if successful, False if section not found and create_if_missing=False
    """
    if not file_path.exists():
        return False

    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    section_start = None
    section_end = None
    section_level = None
    in_code_block = False

    for i, line in enumerate(lines):
        # Track fenced code blocks
        if line.strip().startswith("```"):
            in_code_block = not in_code_block

        # Only process headings outside of code blocks
        if in_code_block:
            continue

        heading_match = re.match(r"^(#{1,6})\s+(.+)$", line)

        if heading_match:
            level = len(heading_match.group(1))
            title = heading_match.group(2).strip()

            if section_start is None and _normalize_title(title) == _normalize_title(section_name):
                section_start = i
                section_level = level
                continue

            if section_start is not None and level <= section_level:
                section_end = i
                break

    if section_start is None:
        if not create_if_missing:
            return False
        # Create new section at the end
        return _create_section(file_path, section_name, new_content, lines)

    # If no end found, extend to end of file
    if section_end is None:
        section_end = len(lines)

    # Build new lines
    new_lines = (
        lines[: section_start + 1]  # Everything before and including heading
        + [""]  # Blank line after heading
        + new_content.split("\n")  # New content
        + [""]  # Blank line before next section
        + lines[section_end:]  # Rest of file
    )

    _write_cleaned(file_path, new_lines)
    return True


def _create_section(
    file_path: Path, section_name: str, content: str, lines: list[str]
) -> bool:
    """
    Create a new section at the end of the file.

    Args:
        file_path: Path to the Markdown file
        section_name: Name of the heading (without #)
        content: Content for the section
        lines: Existing lines of the file

    Returns:
        True if successful
    """
    # Determine heading level (default to ## for new sections)
    heading_level = 2

    # Build new section
    new_section = (
        ["", f"{'#' * heading_level} {section_name}", ""] + content.split("\n") + [""]
    )

    # Append to existing content
    new_lines = lines + new_section

    _write_cleaned(file_path, new_lines)
    return True


def create_backup(file_path: Path) -> Path:
    """Create a backup of a file."""
    backup_path = file_path.with_suffix(file_path.suffix + ".bak")
    backup_path.write_text(file_path.read_text(encoding="utf-8"), encoding="utf-8")
    return backup_path
