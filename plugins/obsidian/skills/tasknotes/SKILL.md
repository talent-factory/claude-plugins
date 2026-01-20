---
name: tasknotes
description: Dieser Skill wird verwendet, wenn der Benutzer nach "zeige meine Aufgaben", "show my tasks", "erstelle eine Aufgabe", "create a task", "was soll ich machen", "what should I work on", "markiere als erledigt", "mark as done" fragt, oder Aufgaben nach Status/Projekt filtern möchte.
---

# TaskNotes Skill

Aufgabenverwaltung in Obsidian via TaskNotes Plugin HTTP API.

<example>
User: "zeige meine Aufgaben"
Action: Führe `list --table` aus um alle Aufgaben anzuzeigen
</example>

<example>
User: "erstelle eine Aufgabe um die Landing Page zu erledigen"
Action: Führe `create "Landing Page erledigen"` aus
</example>

<example>
User: "was soll ich machen?"
Action: Führe `list --status in-progress --table` aus um aktive Aufgaben zu zeigen
</example>

<example>
User: "show my tasks"
Action: Run `list --table` to show all tasks
</example>

<example>
User: "create a task to finish landing page"
Action: Run `create "Finish landing page"`
</example>

## Voraussetzungen

1. **TaskNotes Plugin** in Obsidian installiert
2. **HTTP API aktivieren** in TaskNotes Einstellungen:
   - Obsidian Einstellungen öffnen → TaskNotes
   - "HTTP API" Toggle aktivieren
   - API Port setzen (Standard: 8080)
   - API Token: leer lassen für keine Authentifizierung, oder Token für Sicherheit setzen
3. **Umgebungsvariablen** in `.env` Datei im Vault-Root (falls Authentifizierung verwendet wird):
   ```
   TASKNOTES_API_PORT=8080
   TASKNOTES_API_KEY=dein_token_hier
   ```
   Falls TaskNotes kein Auth-Token gesetzt hat, ist keine `.env` Datei nötig.

## CLI-Befehle

Das Script befindet sich unter `${CLAUDE_PLUGIN_ROOT}/skills/tasknotes/scripts/tasks.py`.

```bash
# Alle Aufgaben auflisten
uv run ${CLAUDE_PLUGIN_ROOT}/skills/tasknotes/scripts/tasks.py list

# Nach Status filtern (verwende deine konfigurierten Status-Werte)
uv run ${CLAUDE_PLUGIN_ROOT}/skills/tasknotes/scripts/tasks.py list --status "in-progress"

# Nach Projekt filtern
uv run ${CLAUDE_PLUGIN_ROOT}/skills/tasknotes/scripts/tasks.py list --project "Mein Projekt"

# Aufgabe erstellen
uv run ${CLAUDE_PLUGIN_ROOT}/skills/tasknotes/scripts/tasks.py create "Aufgabentitel" --project "Mein Projekt" --priority high

# Aufgabe mit geplantem Zeitpunkt erstellen
uv run ${CLAUDE_PLUGIN_ROOT}/skills/tasknotes/scripts/tasks.py create "Meeting-Vorbereitung" --scheduled "2025-01-15T14:00:00"

# Aufgaben-Status aktualisieren
uv run ${CLAUDE_PLUGIN_ROOT}/skills/tasknotes/scripts/tasks.py update "Tasks/aufgabe.md" --status done

# Beschreibung hinzufügen/aktualisieren
uv run ${CLAUDE_PLUGIN_ROOT}/skills/tasknotes/scripts/tasks.py update "Tasks/aufgabe.md" --details "Zusätzlicher Kontext hier."

# Aufgabe löschen
uv run ${CLAUDE_PLUGIN_ROOT}/skills/tasknotes/scripts/tasks.py delete "Tasks/aufgabe.md"

# Verfügbare Optionen abrufen (Status, Prioritäten, Projekte)
uv run ${CLAUDE_PLUGIN_ROOT}/skills/tasknotes/scripts/tasks.py options --table

# Menschenlesbare Ausgabe (--table hinzufügen)
uv run ${CLAUDE_PLUGIN_ROOT}/skills/tasknotes/scripts/tasks.py list --table
```

## Aufgaben-Eigenschaften

**Status- und Prioritätswerte:** In den TaskNotes Plugin-Einstellungen konfiguriert. Den `options`-Befehl ausführen, um verfügbare Werte zu sehen:

```bash
uv run ${CLAUDE_PLUGIN_ROOT}/skills/tasknotes/scripts/tasks.py options --table
```

**Weitere Felder:**
- `projects` - Array von Projekt-Links, z.B. `["[[Projektname]]"]`
- `contexts` - Array wie `["office", "energy-high"]`
- `due` - Fälligkeitsdatum (YYYY-MM-DD)
- `scheduled` - Geplantes Datum/Zeit (YYYY-MM-DD oder YYYY-MM-DDTHH:MM:SS)
- `timeEstimate` - Minuten (Zahl)
- `tags` - Array von Tags
- `details` - Aufgabenbeschreibung (schreibt in Markdown-Body, nicht Frontmatter)

## API-Referenz

Basis-URL: `http://localhost:8080/api`

| Methode | Endpunkt | Beschreibung |
|---------|----------|--------------|
| GET | /tasks | Aufgaben auflisten (unterstützt Filter) |
| POST | /tasks | Aufgabe erstellen |
| GET | /tasks/{id} | Einzelne Aufgabe abrufen |
| PUT | /tasks/{id} | Aufgabe aktualisieren |
| DELETE | /tasks/{id} | Aufgabe löschen |
| GET | /filter-options | Verfügbare Status, Prioritäten, Projekte |

### Query-Parameter für GET /tasks

- `status` - Nach Status filtern
- `project` - Nach Projektname filtern
- `priority` - Nach Priorität filtern
- `tag` - Nach Tag filtern
- `overdue` - true/false
- `sort` - Sortierfeld
- `limit` - Max. Ergebnisse
- `offset` - Paginierungs-Offset

## Verwendungsmuster

| Benutzeranfrage | Aktion |
|-----------------|--------|
| "erstelle eine Aufgabe für X" | Aufgabe erstellen |
| "zeige meine Aufgaben" | Alle Aufgaben auflisten |
| "zeige laufende Aufgaben" | list --status in-progress |
| "markiere X als erledigt" | Aufgaben-Status auf done setzen |
| "was soll ich machen" | Aufgaben nach Status auflisten |
| "show my tasks" | Alle Aufgaben auflisten |
| "create a task for X" | Aufgabe erstellen |
| "what should I work on" | Aufgaben nach Status auflisten |

## Beispiel-Workflow

```bash
# Morgens: Prüfen woran gearbeitet werden soll
uv run ${CLAUDE_PLUGIN_ROOT}/skills/tasknotes/scripts/tasks.py list --status in-progress --table
uv run ${CLAUDE_PLUGIN_ROOT}/skills/tasknotes/scripts/tasks.py list --limit 5 --table

# Aufgabe mit Projekt-Verknüpfung erstellen
uv run ${CLAUDE_PLUGIN_ROOT}/skills/tasknotes/scripts/tasks.py create "Landing Page fertigstellen" \
  --project "Website Redesign" \
  --priority high

# Aufgabe abschliessen
uv run ${CLAUDE_PLUGIN_ROOT}/skills/tasknotes/scripts/tasks.py update "Tasks/landing-page-fertigstellen.md" --status done
```

## Wichtige Hinweise

- **JSON-Ausgabe** (Standard): Für programmatische Verarbeitung geeignet
- **Table-Ausgabe** (`--table`): Für menschenlesbare Darstellung
- **Vault-Pfad**: Das Script erwartet die `.env` Datei im Vault-Root (4 Verzeichnisse über dem Script)
- **Fehlerbehandlung**: Bei Verbindungsfehlern prüfen, ob Obsidian läuft und TaskNotes API aktiviert ist
