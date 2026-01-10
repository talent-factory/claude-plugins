# Workflow: Task Implementation

Detaillierter Workflow für die Implementierung von Tasks (Filesystem oder Linear).

## Übersicht

Der Workflow ist in 8 Phasen unterteilt:

```
1. Task-Identifikation
   ↓
2. Task-Daten einlesen
   ↓
3. Worktree-Erstellung
   ↓
4. Branch-Erstellung (inkl. Submodule)
   ↓
5. Task-Status Update
   ↓
6. Implementierung
   ↓
7. PR-Erstellung
   ↓
8. Finalisierung & Cleanup
```

## Phase 1: Task-Identifikation

### Mit Task-ID Argument

**Filesystem**: `/implement-task task-001`
**Linear**: `/implement-task --linear PROJ-123`

**Workflow**:
1. Task-ID parsen und validieren
2. Task abrufen (Filesystem: `.plans/*/tasks/`, Linear: MCP)
3. Bei mehreren Matches: Interaktive Auswahl

### Ohne Argument (Interaktiv)

**Filesystem**: `/implement-task`
**Linear**: `/implement-task --linear`

**Workflow**:
1. Verfügbare Tasks auflisten
2. User wählt Task aus
3. Task-Daten laden

### Validierungs-Checks

- ✅ Task existiert
- ✅ Task ist nicht bereits abgeschlossen
- ✅ Task hat validen Status (pending/Backlog)
- ✅ Dependencies erfüllt (nur Filesystem)

## Phase 2: Task-Daten einlesen

### Gemeinsame Daten

| Feld | Filesystem | Linear |
|------|------------|--------|
| Titel | Aus Markdown | `issue.title` |
| Beschreibung | `## Description` | `issue.description` |
| Labels | `**Labels**:` | `issue.labels.nodes` |
| Status | `**Status**:` | `issue.state.name` |
| Akzeptanzkriterien | `## Acceptance Criteria` | Aus Description parsen |

### Datenstruktur

```python
task = {
    "id": "task-001" | "PROJ-123",
    "title": "UI Toggle Component",
    "description": "...",
    "status": "pending" | "Backlog",
    "labels": ["feature", "ui"],
    "acceptance_criteria": [
        "Toggle button renders correctly",
        "State persists in localStorage"
    ],
    "provider": "filesystem" | "linear"
}
```

## Phase 3: Worktree-Erstellung

> ⚠️ **WICHTIG**: Für paralleles Arbeiten an mehreren Tasks werden Git Worktrees verwendet!

### Worktree-Konzept

Jeder Task wird in einem eigenen Worktree bearbeitet:
- **Verzeichnis**: `.worktrees/task-<task-id>/`
- **Ermöglicht**: Parallele Arbeit an mehreren Tasks ohne Branch-Wechsel
- **Isoliert**: Jeder Task hat seine eigene Arbeitskopie

### Pre-Worktree-Checks

```bash
# 1. Working Directory sauber?
git status --porcelain

# 2. Remote up-to-date?
git fetch origin

# 3. Worktree-Verzeichnis existiert?
mkdir -p .worktrees

# 4. Worktree für diese Task existiert noch nicht?
git worktree list | grep "task-<task-id>"
```

### Worktree erstellen

```bash
# Branch-Name bestimmen
TASK_ID="task-001"  # oder "proj-123" für Linear
DESCRIPTION="ui-toggle-component"
BRANCH_NAME="feature/${TASK_ID}-${DESCRIPTION}"

# Worktree mit neuem Branch erstellen
git worktree add -b "$BRANCH_NAME" ".worktrees/task-${TASK_ID}" origin/main

# In Worktree wechseln
cd ".worktrees/task-${TASK_ID}"
```

## Phase 4: Branch-Erstellung (inkl. Submodule)

### Branch-Naming

**Einheitliches Format für alle Provider**:

```
feature/<ISSUE-ID>-<description>
```

| Provider | Beispiel |
|----------|----------|
| Filesystem | `feature/task-001-ui-toggle-component` |
| Linear | `feature/proj-123-user-authentication` |

### Submodule-Handling

> ⚠️ **Bei Projekten mit Submodulen**: Auch diese müssen in eigene Branches ausgecheckt werden!

```bash
# 1. Prüfen ob Submodule vorhanden sind
git submodule status

# 2. Falls ja: Submodule initialisieren
git submodule update --init --recursive

# 3. Für jedes Submodul: Branch erstellen
git submodule foreach --recursive '
  echo "Creating branch in submodule: $name"
  git fetch origin
  git checkout -b "feature/<task-id>-<description>" origin/main
'
```

### Submodule-Validierung

```bash
# Alle Submodule auf korrektem Branch?
git submodule foreach --recursive 'git branch --show-current'
```

## Phase 5: Task-Status Update

### Filesystem

```markdown
# Vorher
- **Status**: pending

# Nachher
- **Status**: in_progress
- **Updated**: 2024-11-18
```

**Commit**: `🔄 chore: Start task-001 implementation`

### Linear

Via MCP: `linear_update_issue_state()` → "In Progress"

**Optional Comment**:
```markdown
🚀 Implementation gestartet in Worktree: `.worktrees/task-proj-123/`
Branch: `feature/proj-123-...`
```

## Phase 6: Implementierung

### Strategie

1. **Task-Beschreibung analysieren** - Betroffene Dateien identifizieren
2. **Akzeptanzkriterien als Checklist** - TodoWrite nutzen
3. **Code-Änderungen durchführen** - Basierend auf Beschreibung
4. **Tests schreiben** - Unit/Integration Tests

### Labels → Commit-Typ Mapping

```python
label_to_commit = {
    "bug": "🐛 fix",
    "feature": "✨ feat",
    "docs": "📚 docs",
    "refactor": "♻️ refactor",
    "performance": "⚡ perf",
    "test": "🧪 test"
}
```

### Atomare Commits

```bash
# Commit 1: Feature
git commit -m "✨ feat: Add ThemeToggle component"

# Commit 2: Tests
git commit -m "🧪 test: Add ThemeToggle tests"
```

## Phase 7: PR-Erstellung

### PR-Body Template

```markdown
## Task: [ID] - [Titel]

**Beschreibung**:
<Task-Beschreibung>

**Änderungen**:
- <Änderung 1>
- <Änderung 2>

**Test-Plan**:
- [x] <Akzeptanzkriterium 1>
- [x] <Akzeptanzkriterium 2>

**Status**: In Progress → Completed/In Review
```

### PR erstellen

```bash
# Aus dem Worktree heraus
cd .worktrees/task-<task-id>
git push -u origin <branch-name>
gh pr create --title "[ID]: [Titel]" --body "..."
```

## Phase 8: Finalisierung & Cleanup

### Task-Status Update

#### Filesystem

1. Task-Status → `completed`
2. STATUS.md aktualisieren
3. Commit: `✅ chore: Mark task-001 as completed`

#### Linear

1. Issue-Status → `In Review` oder `Done`
2. Optional: PR-Link als Comment

### Worktree-Cleanup (nach PR-Merge)

Nach erfolgreichem Merge kann der Worktree aufgeräumt werden:

```bash
# Vom Hauptrepo aus (nicht aus dem Worktree!)
cd <projekt-root>

# 1. Worktree entfernen
git worktree remove .worktrees/task-<task-id>

# 2. Lokalen Branch löschen (falls gewünscht)
git branch -d feature/<task-id>-<description>

# 3. Bei Submodulen: Branches dort auch löschen
git submodule foreach --recursive '
  git checkout main
  git branch -d "feature/<task-id>-<description>" 2>/dev/null || true
'
```

### Worktree-Übersicht

```bash
# Alle aktiven Worktrees anzeigen
git worktree list

# Verwaiste Worktrees aufräumen
git worktree prune
```

## Siehe auch

- [filesystem.md](./filesystem.md) - Filesystem-spezifische Details
- [linear.md](./linear.md) - Linear-spezifische Details
- [best-practices.md](./best-practices.md) - Best Practices
- [troubleshooting.md](./troubleshooting.md) - Problemlösungen

