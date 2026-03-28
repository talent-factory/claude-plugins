"""Markdown section extractor."""

import re
from pathlib import Path

# Regex to strip emoji characters (including modifiers and ZWJ sequences)
_EMOJI_RE = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map
    "\U0001F1E0-\U0001F1FF"  # flags
    "\U00002702-\U000027B0"  # dingbats
    "\U0001F900-\U0001F9FF"  # supplemental symbols
    "\U0001FA00-\U0001FA6F"  # chess symbols & extended pictographs
    "\U0001FA70-\U0001FAFF"  # symbols extended-A
    "\U00002600-\U000026FF"  # misc symbols
    "\U0000FE0F"             # variation selector
    "\U0000200D"             # ZWJ
    "]+",
)


def _normalize_title(title: str) -> str:
    """Strip emojis, collapse whitespace, and lowercase for comparison."""
    return " ".join(_EMOJI_RE.sub("", title).split()).lower()


def extract_section(file_path: Path, section_name: str) -> str | None:
    """
    Extract the content of a section from a Markdown file.

    Args:
        file_path: Path to the Markdown file
        section_name: Name of the heading (without #)

    Returns:
        Section content or None if not found
    """
    if not file_path.exists():
        return None

    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    section_start = None
    section_level = None
    result_lines = []
    in_code_block = False

    for i, line in enumerate(lines):
        # Track fenced code blocks
        if line.strip().startswith("```"):
            in_code_block = not in_code_block

        # Only process headings outside of code blocks
        if not in_code_block:
            heading_match = re.match(r"^(#{1,6})\s+(.+)$", line)

            if heading_match:
                level = len(heading_match.group(1))
                title = heading_match.group(2).strip()

                # Match section heading (emoji-tolerant comparison)
                if section_start is None and _normalize_title(title) == _normalize_title(section_name):
                    section_start = i
                    section_level = level
                    continue

                # End of section (same or higher heading level)
                if section_start is not None and level <= section_level:
                    break

        # Collect lines within the section
        if section_start is not None:
            result_lines.append(line)

    if section_start is None:
        return None

    # Remove leading/trailing blank lines
    while result_lines and not result_lines[0].strip():
        result_lines.pop(0)
    while result_lines and not result_lines[-1].strip():
        result_lines.pop()

    return "\n".join(result_lines)


def list_sections(file_path: Path) -> list[dict]:
    """
    List all sections of a Markdown file.

    Returns:
        List of {level, title, line_number}
    """
    if not file_path.exists():
        return []

    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")
    sections = []
    in_code_block = False

    for i, line in enumerate(lines):
        # Track fenced code blocks
        if line.strip().startswith("```"):
            in_code_block = not in_code_block

        # Only process headings outside of code blocks
        if not in_code_block:
            heading_match = re.match(r"^(#{1,6})\s+(.+)$", line)
            if heading_match:
                sections.append(
                    {
                        "level": len(heading_match.group(1)),
                        "title": heading_match.group(2).strip(),
                        "line_number": i + 1,
                    }
                )

    return sections
