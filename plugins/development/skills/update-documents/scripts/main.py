#!/usr/bin/env python3
"""
Documentation Sync Tool - Hauptscript.

Synchronisiert Dokumentation zwischen CLAUDE.md, README.md und docs/.
"""

import argparse
import json
import sys
from pathlib import Path

from extractor import extract_section
from sync_rules import load_rules
from writer import update_section


def get_project_root() -> Path:
    """Findet das Projekt-Root (enthält CLAUDE.md)."""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / "CLAUDE.md").exists():
            return current
        current = current.parent
    # Fallback: 4 Ebenen hoch von scripts/
    return Path(__file__).resolve().parent.parent.parent.parent.parent


def analyze(project_root: Path, config_path: Path) -> dict:
    """
    Analysiert Unterschiede zwischen Source und Targets.

    Returns:
        Dict mit Analyse-Ergebnissen
    """
    rules = load_rules(config_path)
    results = {"rules": [], "summary": {"total": 0, "outdated": 0, "missing": 0, "ok": 0}}

    for rule in rules:
        source_path = project_root / rule.source_file
        source_content = extract_section(source_path, rule.source_section)

        rule_result = {
            "id": rule.id,
            "source": {
                "file": rule.source_file,
                "section": rule.source_section,
                "content": source_content,
                "exists": source_content is not None,
            },
            "targets": [],
        }

        if source_content is None:
            rule_result["status"] = "source_missing"
            results["summary"]["missing"] += 1
        else:
            all_ok = True
            for target in rule.targets:
                target_path = project_root / target.file
                target_content = extract_section(target_path, target.section)

                target_result = {
                    "file": target.file,
                    "section": target.section,
                    "exists": target_content is not None,
                    "content": target_content,
                    "needs_update": False,
                }

                if target_content is None:
                    target_result["status"] = "missing"
                    target_result["needs_update"] = True
                    all_ok = False
                elif _normalize(target_content) != _normalize(source_content):
                    target_result["status"] = "outdated"
                    target_result["needs_update"] = True
                    all_ok = False
                else:
                    target_result["status"] = "ok"

                rule_result["targets"].append(target_result)

            rule_result["status"] = "ok" if all_ok else "needs_sync"
            if all_ok:
                results["summary"]["ok"] += 1
            else:
                results["summary"]["outdated"] += 1

        results["rules"].append(rule_result)
        results["summary"]["total"] += 1

    return results


def _normalize(content: str) -> str:
    """Normalisiert Content für Vergleich (ignoriert Whitespace-Unterschiede)."""
    lines = content.strip().split("\n")
    return "\n".join(line.strip() for line in lines if line.strip())


def sync(project_root: Path, config_path: Path) -> dict:
    """
    Synchronisiert alle Targets mit ihren Sources.

    Returns:
        Dict mit Sync-Ergebnissen
    """
    rules = load_rules(config_path)
    results = {"updated": [], "skipped": [], "errors": []}

    for rule in rules:
        source_path = project_root / rule.source_file
        source_content = extract_section(source_path, rule.source_section)

        if source_content is None:
            results["errors"].append(
                {
                    "rule": rule.id,
                    "error": f"Source section '{rule.source_section}' "
                    f"not found in {rule.source_file}",
                }
            )
            continue

        for target in rule.targets:
            target_path = project_root / target.file

            if not target_path.exists():
                results["errors"].append(
                    {
                        "rule": rule.id,
                        "target": target.file,
                        "error": f"Target file not found: {target.file}",
                    }
                )
                continue

            target_content = extract_section(target_path, target.section)

            if target_content is not None and _normalize(target_content) == _normalize(
                source_content
            ):
                results["skipped"].append(
                    {
                        "rule": rule.id,
                        "target": target.file,
                        "section": target.section,
                        "reason": "already_in_sync",
                    }
                )
                continue

            success = update_section(target_path, target.section, source_content)

            if success:
                results["updated"].append(
                    {
                        "rule": rule.id,
                        "target": target.file,
                        "section": target.section,
                    }
                )
            else:
                results["errors"].append(
                    {
                        "rule": rule.id,
                        "target": target.file,
                        "error": f"Section '{target.section}' not found in {target.file}",
                    }
                )

    return results


def main():
    parser = argparse.ArgumentParser(description="Documentation Sync Tool")
    parser.add_argument(
        "--analyze",
        action="store_true",
        help="Analysiere Unterschiede (kein Schreiben)",
    )
    parser.add_argument(
        "--sync",
        action="store_true",
        help="Synchronisiere alle Targets",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Pfad zur sync_rules.json",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=None,
        help="Projekt-Root-Verzeichnis",
    )
    parser.add_argument(
        "--format",
        choices=["json", "text"],
        default="text",
        help="Output-Format",
    )

    args = parser.parse_args()

    # Pfade bestimmen
    project_root = args.project_root or get_project_root()
    config_path = args.config or (Path(__file__).parent.parent / "config" / "sync_rules.json")

    if not config_path.exists():
        print(f"Error: Config not found: {config_path}", file=sys.stderr)
        sys.exit(1)

    if args.analyze:
        results = analyze(project_root, config_path)
        if args.format == "json":
            print(json.dumps(results, indent=2, ensure_ascii=False))
        else:
            print_analysis(results)

    elif args.sync:
        results = sync(project_root, config_path)
        if args.format == "json":
            print(json.dumps(results, indent=2, ensure_ascii=False))
        else:
            print_sync_results(results)

    else:
        parser.print_help()
        sys.exit(1)


def print_analysis(results: dict):
    """Gibt Analyse-Ergebnisse formatiert aus."""
    summary = results["summary"]
    print("Dokumentations-Analyse")
    print("=" * 40)
    print(f"Regeln gesamt: {summary['total']}")
    print(f"  ✓ Synchron:  {summary['ok']}")
    print(f"  ⚠ Veraltet:  {summary['outdated']}")
    print(f"  ✗ Fehlend:   {summary['missing']}")
    print()

    for rule in results["rules"]:
        status_icon = "✓" if rule["status"] == "ok" else "⚠"
        print(f"{status_icon} {rule['id']}")
        print(f"  Source: {rule['source']['file']} → {rule['source']['section']}")

        for target in rule.get("targets", []):
            t_icon = "✓" if target["status"] == "ok" else "⚠"
            print(f"  {t_icon} Target: {target['file']} → {target['section']}")


def print_sync_results(results: dict):
    """Gibt Sync-Ergebnisse formatiert aus."""
    print("Dokumentations-Sync")
    print("=" * 40)

    if results["updated"]:
        print("\n✓ Aktualisiert:")
        for item in results["updated"]:
            print(f"  - {item['target']}: {item['section']}")

    if results["skipped"]:
        print("\n○ Unverändert:")
        for item in results["skipped"]:
            print(f"  - {item['target']}: {item['section']}")

    if results["errors"]:
        print("\n✗ Fehler:")
        for item in results["errors"]:
            print(f"  - {item.get('target', item['rule'])}: {item['error']}")

    print()
    print(
        f"Zusammenfassung: {len(results['updated'])} aktualisiert, "
        f"{len(results['skipped'])} unverändert, {len(results['errors'])} Fehler"
    )


if __name__ == "__main__":
    main()
