#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "python-dotenv"]
# ///
"""
TaskNotes CLI - Aufgabenverwaltung in Obsidian via TaskNotes Plugin API.

Verwendung:
    uv run tasks.py list [--status STATUS] [--project PROJECT] [--limit N]
    uv run tasks.py create "Titel" [--project PROJECT] [--priority PRIORITY] [--status STATUS]
    uv run tasks.py update "Tasks/datei.md" [--status STATUS] [--priority PRIORITY]
    uv run tasks.py delete "Tasks/datei.md"
    uv run tasks.py stats
    uv run tasks.py options

Umgebungsvariablen:
    TASKNOTES_API_KEY - API Authentifizierungs-Token (optional, abhängig von TaskNotes-Einstellungen)
    TASKNOTES_API_PORT - API Port (Standard: 8080)
    OBSIDIAN_VAULT_PATH - Pfad zum Obsidian Vault (optional, für .env Datei-Suche)
"""

import argparse
import json
import os
import sys
import urllib.parse
from pathlib import Path

import requests
from dotenv import load_dotenv

# .env Datei laden - mehrere Orte prüfen
def find_and_load_env():
    """Suche und lade .env Datei aus verschiedenen möglichen Orten."""
    possible_paths = []

    # 1. Expliziter Vault-Pfad via Umgebungsvariable
    if vault_path := os.getenv("OBSIDIAN_VAULT_PATH"):
        possible_paths.append(Path(vault_path) / ".env")

    # 2. Aktuelles Arbeitsverzeichnis
    possible_paths.append(Path.cwd() / ".env")

    # 3. Home-Verzeichnis
    possible_paths.append(Path.home() / ".env")

    # 4. Relativ zum Script (Legacy-Unterstützung)
    script_dir = Path(__file__).parent
    possible_paths.append(script_dir.parent.parent.parent.parent / ".env")

    for env_path in possible_paths:
        if env_path.exists():
            load_dotenv(env_path)
            return env_path

    return None

find_and_load_env()

API_KEY = os.getenv("TASKNOTES_API_KEY")
API_PORT = os.getenv("TASKNOTES_API_PORT", "8080")
BASE_URL = f"http://localhost:{API_PORT}/api"


def get_headers():
    """Erstelle HTTP-Header für API-Anfragen."""
    headers = {"Content-Type": "application/json"}
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"
    return headers


def api_request(method: str, endpoint: str, params: dict = None, data: dict = None):
    """Führe API-Anfrage aus und gib JSON-Antwort zurück."""
    url = f"{BASE_URL}{endpoint}"
    try:
        response = requests.request(
            method, url, headers=get_headers(), params=params, json=data, timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Keine Verbindung zur TaskNotes API. Läuft Obsidian mit aktivierter TaskNotes API?"}
    except requests.exceptions.HTTPError as e:
        try:
            return response.json()
        except Exception:
            return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}


def list_tasks(args):
    """Liste Aufgaben mit optionalen Filtern auf."""
    params = {}
    if args.status:
        params["status"] = args.status
    if args.project:
        params["project"] = args.project
    if args.priority:
        params["priority"] = args.priority
    if args.limit:
        params["limit"] = args.limit
    if args.overdue:
        params["overdue"] = "true"

    result = api_request("GET", "/tasks", params=params)

    if "error" in result:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    tasks = result.get("data", {}).get("tasks", [])

    if args.table:
        # Menschenlesbare Tabellenausgabe
        if not tasks:
            print("Keine Aufgaben gefunden.")
            return
        print(f"{'Status':<15} {'Priorität':<10} {'Titel':<50} {'Projekt'}")
        print("-" * 100)
        for t in tasks:
            status = t.get("status", "keine")
            priority = t.get("priority", "keine")
            title = t.get("title", "")[:48]
            projects = ", ".join(t.get("projects", []))[:30]
            print(f"{status:<15} {priority:<10} {title:<50} {projects}")
        print(f"\nGesamt: {len(tasks)} Aufgaben")
    else:
        # JSON-Ausgabe für Agenten
        output = {
            "success": True,
            "count": len(tasks),
            "tasks": [
                {
                    "id": t.get("id"),
                    "title": t.get("title"),
                    "status": t.get("status"),
                    "priority": t.get("priority"),
                    "projects": t.get("projects", []),
                    "due": t.get("due"),
                    "scheduled": t.get("scheduled"),
                }
                for t in tasks
            ],
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))


def create_task(args):
    """Erstelle eine neue Aufgabe."""
    data = {"title": args.title}

    if args.project:
        # Projekt in [[ ]] einschliessen falls nicht bereits vorhanden
        project = args.project
        if not project.startswith("[["):
            project = f"[[{project}]]"
        data["projects"] = [project]

    if args.priority:
        data["priority"] = args.priority
    if args.status:
        data["status"] = args.status
    if args.due:
        data["due"] = args.due
    if args.scheduled:
        data["scheduled"] = args.scheduled
    if args.contexts:
        data["contexts"] = args.contexts.split(",")
    if args.time_estimate:
        data["timeEstimate"] = args.time_estimate
    if args.details:
        data["details"] = args.details

    result = api_request("POST", "/tasks", data=data)

    if args.table:
        if "error" in result:
            print(f"Fehler: {result['error']}")
        elif result.get("success"):
            task = result.get("data", {})
            print(f"Aufgabe erstellt: {task.get('title')}")
            print(f"  Pfad: {task.get('path')}")
            print(f"  Status: {task.get('status')}")
            print(f"  Priorität: {task.get('priority')}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


def update_task(args):
    """Aktualisiere eine bestehende Aufgabe."""
    task_id = urllib.parse.quote(args.task_id, safe="")
    data = {}

    if args.status:
        data["status"] = args.status
    if args.priority:
        data["priority"] = args.priority
    if args.title:
        data["title"] = args.title
    if args.due:
        data["due"] = args.due
    if args.scheduled:
        data["scheduled"] = args.scheduled
    if args.details:
        data["details"] = args.details

    if not data:
        print(json.dumps({"error": "Keine Aktualisierungen angegeben"}, ensure_ascii=False))
        return

    result = api_request("PUT", f"/tasks/{task_id}", data=data)

    if args.table:
        if "error" in result:
            print(f"Fehler: {result['error']}")
        elif result.get("success"):
            print(f"Aufgabe aktualisiert: {args.task_id}")
            task = result.get("data", {})
            if args.status:
                print(f"  Neuer Status: {task.get('status')}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


def delete_task(args):
    """Lösche eine Aufgabe."""
    task_id = urllib.parse.quote(args.task_id, safe="")
    result = api_request("DELETE", f"/tasks/{task_id}")

    if args.table:
        if "error" in result:
            print(f"Fehler: {result['error']}")
        elif result.get("success"):
            print(f"Aufgabe gelöscht: {args.task_id}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


def get_stats(args):
    """Hole Aufgabenstatistiken."""
    result = api_request("GET", "/stats")

    if args.table:
        if "error" in result:
            print(f"Fehler: {result['error']}")
        elif result.get("success"):
            data = result.get("data", {})
            print("Aufgabenstatistik:")
            print(f"  Gesamt: {data.get('total', 0)}")
            print(f"  Aktiv: {data.get('active', 0)}")
            print(f"  Abgeschlossen: {data.get('completed', 0)}")
            print(f"  Überfällig: {data.get('overdue', 0)}")
            print(f"  Archiviert: {data.get('archived', 0)}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


def get_options(args):
    """Hole verfügbare Filteroptionen (Projekte, Status, etc.)."""
    result = api_request("GET", "/filter-options")

    if args.table:
        if "error" in result:
            print(f"Fehler: {result['error']}")
        elif result.get("success"):
            data = result.get("data", {})
            print("Verfügbare Projekte:")
            for p in data.get("projects", []):
                print(f"  - {p}")
            print("\nVerfügbare Status:")
            for s in data.get("statuses", []):
                print(f"  - {s}")
            print("\nVerfügbare Prioritäten:")
            for p in data.get("priorities", []):
                print(f"  - {p}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="TaskNotes CLI - Obsidian Aufgabenverwaltung")
    parser.add_argument("--table", action="store_true", help="Menschenlesbare Ausgabe")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # List Befehl
    list_parser = subparsers.add_parser("list", help="Aufgaben auflisten")
    list_parser.add_argument("--status", help="Nach Status filtern")
    list_parser.add_argument("--project", help="Nach Projekt filtern")
    list_parser.add_argument("--priority", help="Nach Priorität filtern")
    list_parser.add_argument("--limit", type=int, help="Ergebnisse limitieren")
    list_parser.add_argument("--overdue", action="store_true", help="Nur überfällige anzeigen")
    list_parser.add_argument("--table", action="store_true", help="Menschenlesbare Ausgabe")

    # Create Befehl
    create_parser = subparsers.add_parser("create", help="Aufgabe erstellen")
    create_parser.add_argument("title", help="Aufgabentitel")
    create_parser.add_argument("--project", help="Projekt-/Zielname")
    create_parser.add_argument("--priority", help="Aufgabenpriorität (siehe TaskNotes-Konfiguration)")
    create_parser.add_argument("--status", help="Aufgabenstatus (siehe TaskNotes-Konfiguration)")
    create_parser.add_argument("--due", help="Fälligkeitsdatum (YYYY-MM-DD)")
    create_parser.add_argument("--scheduled", help="Geplantes Datum/Zeit (YYYY-MM-DD oder YYYY-MM-DDTHH:MM:SS)")
    create_parser.add_argument("--contexts", help="Komma-getrennte Kontexte")
    create_parser.add_argument("--time-estimate", type=int, help="Zeitschätzung in Minuten")
    create_parser.add_argument("--details", help="Aufgabenbeschreibung (Agent-Handoff-Kontext)")
    create_parser.add_argument("--table", action="store_true", help="Menschenlesbare Ausgabe")

    # Update Befehl
    update_parser = subparsers.add_parser("update", help="Aufgabe aktualisieren")
    update_parser.add_argument("task_id", help="Aufgaben-Dateipfad (z.B. Tasks/meine-aufgabe.md)")
    update_parser.add_argument("--status", help="Aufgabenstatus (siehe TaskNotes-Konfiguration)")
    update_parser.add_argument("--priority", help="Aufgabenpriorität (siehe TaskNotes-Konfiguration)")
    update_parser.add_argument("--title", help="Neuer Titel")
    update_parser.add_argument("--due", help="Fälligkeitsdatum (YYYY-MM-DD)")
    update_parser.add_argument("--scheduled", help="Geplantes Datum/Zeit (YYYY-MM-DD oder YYYY-MM-DDTHH:MM:SS)")
    update_parser.add_argument("--details", help="Aufgabenbeschreibung (Agent-Handoff-Kontext)")
    update_parser.add_argument("--table", action="store_true", help="Menschenlesbare Ausgabe")

    # Delete Befehl
    delete_parser = subparsers.add_parser("delete", help="Aufgabe löschen")
    delete_parser.add_argument("task_id", help="Aufgaben-Dateipfad")
    delete_parser.add_argument("--table", action="store_true", help="Menschenlesbare Ausgabe")

    # Stats Befehl
    stats_parser = subparsers.add_parser("stats", help="Statistiken abrufen")
    stats_parser.add_argument("--table", action="store_true", help="Menschenlesbare Ausgabe")

    # Options Befehl
    options_parser = subparsers.add_parser("options", help="Filteroptionen abrufen")
    options_parser.add_argument("--table", action="store_true", help="Menschenlesbare Ausgabe")

    args = parser.parse_args()

    commands = {
        "list": list_tasks,
        "create": create_task,
        "update": update_task,
        "delete": delete_task,
        "stats": get_stats,
        "options": get_options,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
