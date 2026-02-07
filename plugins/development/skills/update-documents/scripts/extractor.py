"""Markdown section extractor."""

import re
from pathlib import Path


def extract_section(file_path: Path, section_name: str) -> str | None:
    """
    Extrahiert den Inhalt eines Abschnitts aus einer Markdown-Datei.

    Args:
        file_path: Pfad zur Markdown-Datei
        section_name: Name des Headings (ohne #)

    Returns:
        Inhalt des Abschnitts oder None wenn nicht gefunden
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

                # Gefundenes Section-Heading
                if section_start is None and title.lower() == section_name.lower():
                    section_start = i
                    section_level = level
                    continue

                # Ende der Section (gleiches oder höheres Level)
                if section_start is not None and level <= section_level:
                    break

        # Sammle Zeilen innerhalb der Section
        if section_start is not None:
            result_lines.append(line)

    if section_start is None:
        return None

    # Entferne führende/trailing Leerzeilen
    while result_lines and not result_lines[0].strip():
        result_lines.pop(0)
    while result_lines and not result_lines[-1].strip():
        result_lines.pop()

    return "\n".join(result_lines)


def list_sections(file_path: Path) -> list[dict]:
    """
    Listet alle Sections einer Markdown-Datei auf.

    Returns:
        Liste von {level, title, line_number}
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
