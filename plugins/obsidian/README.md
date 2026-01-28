# Obsidian Integration Plugin

Integration mit Obsidian via TaskNotes Plugin API - Aufgabenverwaltung direkt aus Claude Code.

## Version 1.0.1

## Features

- **Aufgaben auflisten** - "zeige meine Aufgaben" / "show my tasks"
- **Aufgaben erstellen** - "erstelle eine Aufgabe für X" / "create a task for X"
- **Aufgaben aktualisieren** - Status ändern, Details hinzufügen
- **Aufgaben löschen** - Tasks entfernen
- **Arbeitsempfehlungen** - "was soll ich machen?" / "what should I work on?"

## Voraussetzungen

### 1. TaskNotes Plugin in Obsidian

1. Obsidian Community Plugins öffnen
2. "TaskNotes" suchen und installieren
3. Plugin aktivieren

### 2. HTTP API aktivieren

1. Obsidian Einstellungen → TaskNotes
2. "HTTP API" Toggle aktivieren
3. Port setzen (Standard: 8080)
4. Optional: API Token für Sicherheit setzen

### 3. Umgebungsvariablen (optional)

Falls Authentifizierung verwendet wird, `.env` Datei im Obsidian Vault erstellen:

```env
TASKNOTES_API_PORT=8080
TASKNOTES_API_KEY=dein_geheimer_token
```

Alternativ kann `OBSIDIAN_VAULT_PATH` als Umgebungsvariable gesetzt werden, um den Vault-Pfad anzugeben.

## Installation

### Via Marketplace

```json
{
  "enabledPlugins": {
    "obsidian@talent-factory": true
  }
}
```

### Lokales Testing

```bash
claude --plugin-dir ./plugins/obsidian
```

## Verwendung

### Natürliche Sprache (Deutsch)

```
zeige meine Aufgaben
erstelle eine Aufgabe um die Landing Page fertigzustellen
was soll ich machen?
markiere "Tasks/landing-page.md" als erledigt
```

### Natürliche Sprache (Englisch)

```
show my tasks
create a task to finish the landing page
what should I work on?
mark "Tasks/landing-page.md" as done
```

### CLI-Befehle

Das Plugin stellt auch direkte CLI-Befehle bereit:

```bash
# Aufgaben auflisten
uv run tasks.py list --table

# Aufgabe erstellen
uv run tasks.py create "Meeting vorbereiten" --project "Arbeit" --priority high

# Status aktualisieren
uv run tasks.py update "Tasks/meeting.md" --status done
```

## Skills

See [Skills & Agents Activation Guide](../reference/skills-agents-activation.md) for detailed activation instructions.

### tasknotes

Main skill for task management. Automatically activated for:

- Aufgaben-bezogenen Anfragen
- Task-Management-Fragen
- Produktivitäts-Workflows

## Projektstruktur

```text
obsidian/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── tasknotes/
│       ├── SKILL.md
│       └── scripts/
│           └── tasks.py
└── README.md
```

## Lizenz

MIT
