"""Sync rules loader and manager."""

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Target:
    """Ein Sync-Target."""

    file: str
    section: str


@dataclass
class SyncRule:
    """Eine Sync-Regel."""

    id: str
    source_file: str
    source_section: str
    targets: list[Target]


def load_rules(config_path: Path) -> list[SyncRule]:
    """
    Lädt Sync-Regeln aus JSON-Konfiguration.

    Args:
        config_path: Pfad zur sync_rules.json

    Returns:
        Liste von SyncRule-Objekten
    """
    if not config_path.exists():
        raise FileNotFoundError(f"Config not found: {config_path}")

    with open(config_path, encoding="utf-8") as f:
        data = json.load(f)

    rules = []
    for rule_data in data.get("rules", []):
        targets = [
            Target(file=t["file"], section=t["section"]) for t in rule_data.get("targets", [])
        ]
        rules.append(
            SyncRule(
                id=rule_data["id"],
                source_file=rule_data["source"]["file"],
                source_section=rule_data["source"]["section"],
                targets=targets,
            )
        )

    return rules


def rules_to_dict(rules: list[SyncRule]) -> list[dict]:
    """Konvertiert Regeln zurück zu Dict für JSON-Output."""
    return [
        {
            "id": r.id,
            "source": {"file": r.source_file, "section": r.source_section},
            "targets": [{"file": t.file, "section": t.section} for t in r.targets],
        }
        for r in rules
    ]
