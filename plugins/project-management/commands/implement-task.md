---
description: Implementiere Task mit Worktree, Branch-Erstellung und PR (Filesystem oder Linear)
argument-hint: "[task-ID] [--linear]"
allowed-tools:
  - Read
  - Write
  - Edit
  - TodoWrite
  - AskUserQuestion
  - Glob
  - Bash
---

# Implement Task

Automatisierte Umsetzung von Tasks: Worktree erstellen, Branch erstellen (inkl. Submodule), implementieren und Pull Request erstellen.

## Übersicht

Dieser Command orchestriert den kompletten Workflow von Task bis Pull Request:

1. **Task auswählen** - Aus Filesystem oder Linear (via `--linear` Flag)
2. **Worktree erstellen** - In `.worktrees/task-<task-id>/` für parallele Arbeit
3. **Branch erstellen** - Im Hauptrepo und allen Submodulen
4. **Draft-PR vorbereiten** - Frühzeitige PR-Erstellung für Sichtbarkeit und CI/CD
5. **Status aktualisieren** - Task auf "In Progress" setzen
6. **Implementierung** - Code-Änderungen basierend auf Task-Beschreibung
7. **PR finalisieren** - Draft-PR zum Review freigeben
8. **Finalisierung** - Task-Status auf "Completed", Tracking aktualisieren

## Verwendung

```bash
# Filesystem-basiert (Standard)
/implement-task              # Interaktive Auswahl
/implement-task task-001     # Mit Task-ID
/implement-task --plan dark-mode task-003  # Mit Plan-Kontext

# Linear-basiert
/implement-task --linear           # Interaktive Auswahl
/implement-task --linear PROJ-123  # Mit Issue-ID
```

## Provider-Auswahl

### Filesystem (Standard)

**Wann verwenden**: Tasks wurden via `/create-plan` erstellt und liegen in `.plans/*/tasks/`.

**Erwartete Struktur**:
```
.plans/[feature-name]/
├── EPIC.md
├── STATUS.md
└── tasks/
    ├── task-001-*.md
    ├── task-002-*.md
    └── ...
```

### Linear (`--linear`)

**Wann verwenden**: Tasks werden in Linear verwaltet.

**Voraussetzung**: Linear MCP Server muss konfiguriert sein.

```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-linear"],
      "env": { "LINEAR_API_KEY": "<your-api-key>" }
    }
  }
}
```

## Gemeinsamer Workflow

### 1. Task-Identifikation

**Mit Argument**: Task-ID validieren und abrufen
**Ohne Argument**: Verfügbare Tasks auflisten, User wählt interaktiv

### 2. Task-Daten einlesen

Folgende Informationen extrahieren:
- **Titel & Beschreibung** - Für Branch-Name und Kontext
- **Labels/Tags** - Für Commit-Typ-Bestimmung
- **Status** - Muss "pending" / "Backlog" sein
- **Akzeptanzkriterien** - Als Test-Plan-Checkliste
- **Dependencies** - Vor Start prüfen (nur Filesystem)

### 3. Worktree & Branch-Erstellung

> ⚠️ **WICHTIG**: Für paralleles Arbeiten an mehreren Tasks werden Git Worktrees verwendet!

#### Worktree-Konzept

Jeder Task wird in einem eigenen Worktree bearbeitet:
- **Verzeichnis**: `.worktrees/task-<task-id>/`
- **Ermöglicht**: Parallele Arbeit an mehreren Tasks ohne Branch-Wechsel
- **Isoliert**: Jeder Task hat seine eigene Arbeitskopie

#### Workflow

```bash
# 1. Vorbereitungen im Hauptrepo
git fetch origin
git status  # Muss sauber sein

# 2. Worktree-Verzeichnis erstellen (falls nicht vorhanden)
mkdir -p .worktrees

# 3. Branch-Name bestimmen (basierend auf Issue-Type/Labels)
# Labels → Branch-Prefix Mapping:
# - bug, fix → bugfix/<task-id>-<description>
# - feature, enhancement → feature/<task-id>-<description>
# - docs, documentation → docs/<task-id>-<description>
# - refactor → refactor/<task-id>-<description>
# - performance → perf/<task-id>-<description>
# - test → test/<task-id>-<description>
# Default: feature/<task-id>-<description>
BRANCH_NAME="<type>/<task-id>-<description>"

# 4. Worktree mit neuem Branch erstellen
git worktree add -b "$BRANCH_NAME" ".worktrees/task-<task-id>" origin/main

# 5. In Worktree wechseln
cd ".worktrees/task-<task-id>"
```

#### Submodule-Handling

> ⚠️ **Bei Projekten mit Submodulen**: Auch diese müssen in eigene Branches ausgecheckt werden!

```bash
# 1. Im Worktree: Submodule initialisieren
cd ".worktrees/task-<task-id>"
git submodule update --init --recursive

# 2. Für jedes Submodul: Branch erstellen (gleicher Type wie Hauptrepo)
git submodule foreach --recursive '
  git fetch origin
  git checkout -b "<type>/<task-id>-<description>" origin/main
'
```

**Submodule-Check**:
```bash
# Prüfen ob Submodule vorhanden sind
git submodule status
```

#### Branch-Naming

**Format basierend auf Issue-Type/Labels**:

```
<type>/<ISSUE-ID>-<description>
```

**Labels → Branch-Prefix Mapping**:
- `bug`, `fix` → `bugfix/`
- `feature`, `enhancement` → `feature/`
- `docs`, `documentation` → `docs/`
- `refactor` → `refactor/`
- `performance` → `perf/`
- `test` → `test/`
- Default: `feature/`

| Type | Filesystem | Linear |
|------|------------|--------|
| Feature | `feature/task-001-ui-toggle-component` | `feature/proj-123-user-auth` |
| Bug | `bugfix/task-002-login-crash` | `bugfix/proj-124-api-error` |
| Docs | `docs/task-003-api-documentation` | `docs/proj-125-readme-update` |
| Refactor | `refactor/task-004-auth-module` | `refactor/proj-126-db-layer` |

#### Pre-Worktree-Checks

- ✅ Working Directory sauber (git status)
- ✅ Remote ist up-to-date (git fetch)
- ✅ `.worktrees/` existiert oder wird erstellt
- ✅ Worktree existiert noch nicht für diese Task-ID

### 3b. Draft-PR Vorbereitung (OBLIGATORISCH)

> ⚠️ **WICHTIG**: Direkt nach Branch-Erstellung wird ein Draft-PR erstellt!

Der Draft-PR dient als:
- **Frühzeitige Sichtbarkeit**: Team sieht, dass am Task gearbeitet wird
- **CI/CD-Integration**: Automatische Checks laufen von Anfang an
- **Review-Vorbereitung**: Reviewer können früh Feedback geben
- **Task-Verlinkung**: PR ist von Beginn an mit Task verknüpft

#### Draft-PR Workflow

```bash
# 1. Im Worktree: Initial-Commit erstellen (falls nötig)
cd ".worktrees/task-<task-id>"
git commit --allow-empty -m "🚧 wip: Starte Arbeit an <task-id>"

# 2. Branch pushen
git push -u origin "$BRANCH_NAME"

# 3. Draft-PR erstellen via /git-workflow:create-pr
/git-workflow:create-pr --draft --target main
```

#### Alternative: Manueller Draft-PR mit gh CLI

Falls `/git-workflow:create-pr` nicht verfügbar:

```bash
# Draft-PR mit GitHub CLI erstellen
gh pr create --draft \
  --title "🚧 WIP: [<task-id>] <Task-Titel>" \
  --body "$(cat <<'EOF'
## Beschreibung

Implementierung von Task <task-id>: <Task-Titel>

## Status

🚧 **Work in Progress** - Dieser PR ist noch nicht bereit für Review.

## Task-Referenz

- **Task-ID**: <task-id>
- **Provider**: Filesystem / Linear
- **Link**: [Task-Details](<link-to-task>)

## Geplante Änderungen

- [ ] <Akzeptanzkriterium 1>
- [ ] <Akzeptanzkriterium 2>
- [ ] <Akzeptanzkriterium 3>

## Test-Plan

- [ ] Unit Tests
- [ ] Integration Tests
- [ ] Manuelle Verifikation

---
*Dieser Draft-PR wurde automatisch erstellt via `/implement-task`*
EOF
)"
```

#### Submodule Draft-PRs

> ⚠️ **Bei Projekten mit Submodulen**: Auch für Submodule werden Draft-PRs erstellt!

```bash
# Für jedes Submodul mit Änderungen: Draft-PR erstellen
git submodule foreach --recursive '
  # Nur wenn Branch gepusht werden kann
  git push -u origin "<type>/<task-id>-<description>" 2>/dev/null && \
  gh pr create --draft \
    --title "🚧 WIP: [<task-id>] <Task-Titel> (Submodule: $(basename $PWD))" \
    --body "Part of parent PR for <task-id>"
'
```

#### Draft-PR Checkliste

- ✅ Branch ist gepusht (`git push -u origin`)
- ✅ Draft-PR ist erstellt (`gh pr create --draft`)
- ✅ PR-Titel enthält Task-ID und WIP-Marker
- ✅ PR-Body enthält Task-Referenz und Akzeptanzkriterien
- ✅ Submodule haben eigene Draft-PRs (falls betroffen)

### 4. Status-Update (KRITISCH für paralleles Arbeiten)

> ⚠️ **WICHTIG**: Das Status-Update muss **im Hauptbranch** erfolgen, damit andere Entwickler sehen, dass der Task in Bearbeitung ist! Dies verhindert Überschneidungen bei paralleler Arbeit.

| Provider | Transition | Ort |
|----------|------------|-----|
| Filesystem | `pending` → `in_progress` in Task-Datei + STATUS.md | **Hauptbranch** |
| Linear | `Backlog` → `In Progress` via MCP | Remote (automatisch sichtbar) |

#### Filesystem Status-Update Workflow

> 🔴 **OBLIGATORISCH**: Diese Schritte MÜSSEN ausgeführt werden, bevor mit der Implementierung begonnen wird!

```bash
# 1. Zurück zum Hauptverzeichnis (Hauptbranch)
cd <projekt-root>

# 2. Sicherstellen, dass wir auf dem Hauptbranch sind (main/develop)
git checkout main  # oder develop, je nach Projekt
git pull origin main
```

**Task-Datei aktualisieren** (mit Edit-Tool):

```python
# In der Task-Datei: Status ändern
old_string = "- **Status**: pending"
new_string = "- **Status**: in_progress"

# Updated-Datum aktualisieren
from datetime import date
today = date.today().isoformat()
# - **Updated**: <altes-datum> → - **Updated**: <heute>
```

**STATUS.md regenerieren**:

Die STATUS.md im Plan-Verzeichnis muss ebenfalls aktualisiert werden:
- Abschnitt "In Progress 🚧" um den Task erweitern
- Abschnitt "Pending ⏳" entsprechend reduzieren
- Progress-Übersicht anpassen (Prozentangaben)

**Änderungen committen**:

```bash
# 3. Änderungen stagen und committen
git add .plans/<feature-name>/tasks/task-<id>-*.md
git add .plans/<feature-name>/STATUS.md
git commit -m "🔄 chore: Starte task-<id> Implementierung"

# 4. Zum Remote pushen (damit andere es sehen!)
git push origin main  # oder develop
```

**Dann erst in Worktree wechseln**:

```bash
# 5. In den Worktree wechseln für die eigentliche Implementierung
cd ".worktrees/task-<task-id>"
```

#### Filesystem Status-Update Checkliste

- ✅ Im Hauptbranch (nicht Worktree) arbeiten
- ✅ Task-Datei: `pending` → `in_progress`
- ✅ Task-Datei: `Updated`-Datum aktualisiert
- ✅ STATUS.md: Task unter "In Progress" verschoben
- ✅ STATUS.md: Progress-Übersicht aktualisiert
- ✅ Änderungen committed: `🔄 chore: Starte task-<id> Implementierung`
- ✅ Änderungen gepusht zum Remote
- ✅ Erst dann in Worktree wechseln

#### Linear Status-Update

Bei Linear ist das Update einfacher, da der Status zentral gespeichert wird:

```python
# Via MCP-Tool
linear_update_issue(
    issue_id="PROJ-123",
    state="In Progress"
)

# Optional: Kommentar hinzufügen
linear_create_comment(
    issue_id="PROJ-123",
    body="🚀 Implementierung gestartet\n- Branch: `feature/proj-123-...`\n- Worktree: `.worktrees/task-proj-123/`"
)
```

### 5. Implementierung

1. **Task-Beschreibung analysieren** - Betroffene Dateien identifizieren
2. **Akzeptanzkriterien als Checklist** - Schritt für Schritt abarbeiten
3. **Code-Änderungen durchführen** - Basierend auf Task-Beschreibung
4. **Tests schreiben** - Unit/Integration Tests für Akzeptanzkriterien

**Labels → Commit-Typ Mapping**:
- `bug`, `fix` → 🐛 fix
- `feature`, `enhancement` → ✨ feat
- `docs`, `documentation` → 📚 docs
- `refactor` → ♻️ refactor
- `performance` → ⚡ perf
- `test` → 🧪 test
- Default: ✨ feat

### 6. PR-Erstellung

PR mit Task-Verlinkung erstellen:
- Titel: Task-Titel
- Body: Beschreibung, Änderungen, Test-Plan
- Labels: Basierend auf Task-Labels

### 7. Finalisierung (OBLIGATORISCH)

> ⚠️ **WICHTIG**: Dieser Schritt ist NICHT optional!

| Provider | Aktionen |
|----------|----------|
| Filesystem | Task-Status → `completed`, STATUS.md aktualisieren |
| Linear | Issue-Status → `In Review` oder `Done` via MCP |

#### Worktree-Cleanup (nach PR-Merge)

Nach erfolgreichem Merge kann der Worktree aufgeräumt werden:

```bash
# Vom Hauptrepo aus
git worktree remove .worktrees/task-<task-id>
git branch -d <type>/<task-id>-<description>  # lokaler Branch

# Bei Submodulen: Branches dort auch löschen (falls nicht gemerged)
```

## Error Handling

- **Task nicht gefunden**: Validierung, Alternativen vorschlagen
- **Worktree existiert bereits**: Warnung, Option zum Wechseln in existierenden Worktree
- **Branch existiert bereits**: Warnung, Option zum Wechseln
- **Submodule-Branch-Konflikt**: Interaktive Auflösung anbieten
- **Dependencies nicht erfüllt** (FS): Liste anzeigen, User-Entscheidung
- **Linear MCP nicht verfügbar**: Fehlermeldung mit Setup-Anleitung

## Detail-Dokumentation

### Allgemein
- **[workflow.md](../references/implement-task/workflow.md)** - Detaillierter Workflow mit Beispielen
- **[best-practices.md](../references/implement-task/best-practices.md)** - Branch-Naming, Commits, PR-Gestaltung
- **[troubleshooting.md](../references/implement-task/troubleshooting.md)** - Häufige Probleme und Lösungen

### Provider-spezifisch
- **[filesystem.md](../references/implement-task/filesystem.md)** - Filesystem-Tasks, STATUS.md
- **[linear.md](../references/implement-task/linear.md)** - Linear MCP Setup, API-Details

## Siehe auch

- **[/project-management:create-plan](./create-plan.md)** - Projektplanung (Filesystem/Linear)
- **[/git-workflow:commit](../../git-workflow/commands/commit.md)** - Professionelle Git-Commits
- **[/git-workflow:create-pr](../../git-workflow/commands/create-pr.md)** - Pull Request-Erstellung

---

**Arguments**: $ARGUMENTS

