"""Markdown section writer."""

import re
from pathlib import Path


def update_section(
    file_path: Path,
    section_name: str,
    new_content: str,
    create_if_missing: bool = False,
) -> bool:
    """
    Aktualisiert einen Abschnitt in einer Markdown-Datei.

    Args:
        file_path: Pfad zur Markdown-Datei
        section_name: Name des Headings (ohne #)
        new_content: Neuer Inhalt für den Abschnitt
        create_if_missing: Wenn True, wird die Section am Ende erstellt falls nicht vorhanden

    Returns:
        True wenn erfolgreich, False wenn Section nicht gefunden und create_if_missing=False
    """
    if not file_path.exists():
        return False

    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    section_start = None
    section_end = None
    section_level = None

    for i, line in enumerate(lines):
        heading_match = re.match(r"^(#{1,6})\s+(.+)$", line)

        if heading_match:
            level = len(heading_match.group(1))
            title = heading_match.group(2).strip()

            if section_start is None and title.lower() == section_name.lower():
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

    # Wenn kein Ende gefunden, bis zum Dateiende
    if section_end is None:
        section_end = len(lines)

    # Neue Zeilen zusammenbauen
    new_lines = (
        lines[: section_start + 1]  # Alles vor und inkl. Heading
        + [""]  # Leerzeile nach Heading
        + new_content.split("\n")  # Neuer Inhalt
        + [""]  # Leerzeile vor nächster Section
        + lines[section_end:]  # Rest der Datei
    )

    # Doppelte Leerzeilen entfernen
    cleaned_lines = []
    prev_empty = False
    for line in new_lines:
        is_empty = not line.strip()
        if is_empty and prev_empty:
            continue
        cleaned_lines.append(line)
        prev_empty = is_empty

    # Trailing newline sicherstellen
    result = "\n".join(cleaned_lines)
    if not result.endswith("\n"):
        result += "\n"

    file_path.write_text(result, encoding="utf-8")
    return True


def _create_section(
    file_path: Path, section_name: str, content: str, lines: list[str]
) -> bool:
    """
    Erstellt eine neue Section am Ende der Datei.

    Args:
        file_path: Pfad zur Markdown-Datei
        section_name: Name des Headings (ohne #)
        content: Inhalt für den Abschnitt
        lines: Bestehende Zeilen der Datei

    Returns:
        True wenn erfolgreich
    """
    # Determine heading level (default to ## for new sections)
    heading_level = 2

    # Build new section
    new_section = (
        ["", f"{'#' * heading_level} {section_name}", ""] + content.split("\n") + [""]
    )

    # Append to existing content
    new_lines = lines + new_section

    # Doppelte Leerzeilen entfernen
    cleaned_lines = []
    prev_empty = False
    for line in new_lines:
        is_empty = not line.strip()
        if is_empty and prev_empty:
            continue
        cleaned_lines.append(line)
        prev_empty = is_empty

    # Trailing newline sicherstellen
    result = "\n".join(cleaned_lines)
    if not result.endswith("\n"):
        result += "\n"

    file_path.write_text(result, encoding="utf-8")
    return True


def create_backup(file_path: Path) -> Path:
    """Erstellt ein Backup einer Datei."""
    backup_path = file_path.with_suffix(file_path.suffix + ".bak")
    backup_path.write_text(file_path.read_text(encoding="utf-8"), encoding="utf-8")
    return backup_path
