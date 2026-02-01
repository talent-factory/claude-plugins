---
description: Implementiere einen kompletten EPIC automatisiert mit parallelen Agents (Ralph Wiggum Pattern)
argument-hint: "[epic-id | plan-name] [--linear] [--max-parallel 3] [--max-iterations 30]"
allowed-tools:
  - Read
  - Write
  - Edit
  - TodoWrite
  - AskUserQuestion
  - Glob
  - Bash
  - Task
---

# Implement EPIC

Automatisierte, parallele Umsetzung aller Tasks eines EPICs mit dem **Ralph Wiggum Pattern** für autonome Entwicklungsschleifen.

## Übersicht

Dieser Command orchestriert die **vollautomatische Umsetzung eines EPICs**:

1. **EPIC laden** - Aus `.plans/` oder Linear
2. **Dependency-Graph analysieren** - Parallelisierbare Tasks identifizieren
3. **Parallel starten** - Pro unabhängigem Task ein Agent im eigenen Worktree
4. **Autonome Implementation** - Ralph-Loop bis Completion-Promise
5. **Automatischer Review** - Code-Review Agent mit iterativer Verbesserung
6. **Status-Update** - Kontinuierliche Aktualisierung von STATUS.md
7. **Nächste Runde** - Neu verfügbare Tasks starten

## Verwendung

```bash
# Filesystem-basiert (Standard)
/implement-epic                           # Interaktive Auswahl
/implement-epic dark-mode-toggle          # Plan-Name
/implement-epic --plan .plans/feature/    # Expliziter Pfad

# Linear-basiert
/implement-epic --linear                  # Interaktive Auswahl
/implement-epic --linear PROJ-123         # EPIC-ID

# Mit Optionen
/implement-epic feature-x --max-parallel 5 --max-iterations 50
```

## Voraussetzungen

### Ralph Wiggum Plugin

> ⚠️ **WICHTIG**: Das Ralph Wiggum Plugin muss installiert sein!

```bash
# Installation prüfen
claude plugins list | grep ralph-wiggum

# Falls nicht installiert
/plugin install ralph-wiggum@claude-plugins-official
```

### Projekt-Struktur

Der EPIC muss via `/create-plan` erstellt worden sein:

```
.plans/[feature-name]/
├── EPIC.md          # Feature-Übersicht
├── STATUS.md        # Progress-Tracking
└── tasks/
    ├── task-001-*.md
    ├── task-002-*.md
    └── ...
```

## Workflow-Details

### Phase 1: EPIC-Analyse

```mermaid
graph LR
    A[EPIC laden] --> B[Tasks einlesen]
    B --> C[Dependency-Graph]
    C --> D[Parallelisierbare Tasks]
```

**Dependency-Analyse**:
- Lese `Dependencies.Requires` aus jeder Task-Datei
- Baue gerichteten Graphen auf
- Identifiziere Tasks ohne offene Blocker (Einstiegspunkte)

**Beispiel Dependency-Graph**:
```
task-001 ──┬──► task-003 ──► task-005
           │
task-002 ──┘

task-004 (unabhängig)
```

→ **Parallel startbar**: task-001, task-002, task-004

### Phase 2: Parallele Implementation

Für jeden unabhängigen Task wird ein **separater Agent** gestartet:

```bash
# Pro Task in eigenem Worktree:
Task Agent (fresh context):
│
├── 1. Worktree erstellen
│      git worktree add -b feature/task-001 .worktrees/task-001 origin/main
│
├── 2. Ralph-Loop für Implementation
│      /ralph-loop "
│        Implementiere Task task-001:
│        [Task-Beschreibung]
│
│        Akzeptanzkriterien:
│        - [ ] Kriterium 1
│        - [ ] Kriterium 2
│
│        Wenn alle Kriterien erfüllt:
│        Output: <promise>TASK_COMPLETE</promise>
│
│        Bei unlösbaren Blockern:
│        Output: <promise>TASK_BLOCKED</promise>
│      " --max-iterations $MAX_ITERATIONS --completion-promise "TASK_COMPLETE|TASK_BLOCKED"
│
├── 3. Commit & Push
│      git add . && git commit -m "✨ feat(task-001): [description]"
│      git push -u origin feature/task-001
│
└── 4. Draft-PR erstellen
       gh pr create --draft --title "[task-001] Task-Titel"
```

### Phase 3: Automatischer Review

Nach Implementation startet automatisch der **Review-Loop**:

```bash
Review Agent (fresh context):
│
├── 1. PR-Diff laden
│      gh pr diff [pr-number]
│
├── 2. Ralph-Loop für Review
│      /ralph-loop "
│        Review PR #[number] für Task task-001:
│
│        1. Analysiere alle Änderungen
│        2. Prüfe Code-Qualität (siehe code-reviewer Checkliste)
│        3. Identifiziere Probleme
│        4. Behebe ALLE gefundenen Issues selbst
│        5. Committe Fixes mit aussagekräftigen Messages
│
│        Wenn alle Probleme behoben:
│        Output: <promise>REVIEW_COMPLETE</promise>
│
│        Bei Problemen die User-Eingriff benötigen:
│        - Dokumentiere Problem in PR-Kommentar
│        - Update Task-Status auf 'needs_attention'
│        Output: <promise>REVIEW_NEEDS_ATTENTION</promise>
│      " --max-iterations 15 --completion-promise "REVIEW_COMPLETE|REVIEW_NEEDS_ATTENTION"
│
└── 3. PR finalisieren
       gh pr ready [pr-number]  # Wenn REVIEW_COMPLETE
```

### Phase 4: Status-Update & Nächste Runde

Nach jedem abgeschlossenen Task:

1. **STATUS.md aktualisieren**
   - Task auf `completed` / `needs_attention` setzen
   - Progress-Statistik neu berechnen
   - Mermaid-Graph aktualisieren

2. **Dependency-Graph re-evaluieren**
   - Welche Tasks sind jetzt freigeschaltet?
   - Neue parallele Agents starten

3. **Loop bis EPIC complete**
   - Wiederholen bis alle Tasks erledigt
   - Oder nur noch blockierte Tasks übrig

## Orchestrator-Logik

```python
# Pseudo-Code für den EPIC-Orchestrator

def implement_epic(epic_id, max_parallel=3, max_iterations=30):
    epic = load_epic(epic_id)
    tasks = load_all_tasks(epic)

    while not all_tasks_complete(tasks):
        # Identifiziere startbare Tasks
        ready_tasks = [t for t in tasks
                       if t.status == 'pending'
                       and all_dependencies_complete(t, tasks)]

        # Limitiere Parallelität
        to_start = ready_tasks[:max_parallel - active_agents_count()]

        for task in to_start:
            # Starte Agent in eigenem Worktree
            spawn_task_agent(
                task=task,
                max_iterations=max_iterations,
                on_complete=lambda: handle_task_complete(task),
                on_blocked=lambda: handle_task_blocked(task)
            )

        # Warte auf nächsten Abschluss
        wait_for_any_completion()

        # Status-Update
        update_status_md(epic)

    # Finalisierung
    generate_epic_summary(epic)
    notify_user_completion(epic)
```

## Worktree-Management

> ⚠️ **KRITISCH**: Jeder Task arbeitet in einem **isolierten Worktree**!

### Warum Worktrees?

- **Parallele Arbeit**: Mehrere Tasks gleichzeitig ohne Branch-Konflikte
- **Isolation**: Kein gegenseitiges Überschreiben
- **Saubere Historie**: Klare Commit-Trennung pro Task

### Worktree-Struktur

```
project/
├── .worktrees/
│   ├── task-001/          # Worktree für Task 001
│   │   ├── src/
│   │   └── ...
│   ├── task-002/          # Worktree für Task 002
│   │   ├── src/
│   │   └── ...
│   └── task-004/          # Worktree für Task 004
│       ├── src/
│       └── ...
├── src/                   # Hauptrepo (main branch)
└── .plans/
    └── feature/
        ├── EPIC.md
        └── tasks/
```

### Worktree-Lifecycle

```bash
# 1. Erstellen (pro Task)
git worktree add -b feature/task-001 .worktrees/task-001 origin/main

# 2. Arbeiten (im Worktree-Verzeichnis)
cd .worktrees/task-001
# ... Implementation ...

# 3. Nach PR-Merge: Cleanup
git worktree remove .worktrees/task-001
git branch -d feature/task-001
```

## Status-Tracking

### STATUS.md Updates

Der Orchestrator aktualisiert kontinuierlich:

```markdown
## Tasks by Status

### Completed ✅
- **task-001**: UI Toggle Component (3 SP) - PR #12 merged

### In Progress 🚧
- **task-002**: Theme State Management (5 SP) - PR #13 in review
- **task-004**: Settings Integration (2 SP) - implementing...

### Pending 📋
- **task-003**: LocalStorage Persistence (3 SP) - waiting for task-002
- **task-005**: E2E Tests (5 SP) - waiting for task-003

### Needs Attention ⚠️
[Leer oder Tasks die User-Eingriff benötigen]
```

### Echtzeit-Fortschritt

```
╔═══════════════════════════════════════════════════════════╗
║  EPIC: Dark Mode Toggle                                   ║
╠═══════════════════════════════════════════════════════════╣
║  Progress: ████████░░░░░░░░░░░░░░░░░░░░░░  40% (2/5)     ║
║                                                           ║
║  Active Agents:                                           ║
║  • task-002 (Theme State)     [████████░░] 80% iter 24/30║
║  • task-004 (Settings)        [██████░░░░] 60% iter 18/30║
║                                                           ║
║  Completed: task-001                                      ║
║  Waiting:   task-003 → task-002                           ║
║             task-005 → task-003                           ║
╚═══════════════════════════════════════════════════════════╝
```

## Error-Handling

### Task Blocked

Wenn ein Task nicht abgeschlossen werden kann:

1. **Status setzen**: `blocked` oder `needs_attention`
2. **Dokumentation**: Grund in Task-Datei und PR-Kommentar
3. **User-Notification**: Zusammenfassung was fehlt
4. **Andere Tasks**: Weitermachen mit unabhängigen Tasks

### Agent-Timeout

Bei Erreichen von `--max-iterations`:

1. **Fortschritt sichern**: Commit aller Änderungen
2. **Status**: `in_progress` mit Notiz
3. **User-Option**: Manuell fortsetzen oder überspringen

### Merge-Konflikte

Falls Main sich ändert während EPIC läuft:

```bash
# Im Worktree
git fetch origin
git rebase origin/main

# Bei Konflikten: Task auf 'needs_attention'
```

## Best Practices

### DO ✅

- **Klare Akzeptanzkriterien**: Testbar und messbar
- **Kleine Tasks**: Ideal 1-5 Story Points
- **Gute Dependencies**: Korrekte Reihenfolge
- **Realistische Iterations**: 20-50 für komplexe Tasks
- **Max-Parallel anpassen**: Nach CPU/Memory

### DON'T ❌

- **Riesige Tasks**: > 8 SP schwer automatisierbar
- **Zirkuläre Dependencies**: Führt zu Deadlock
- **Vage Kriterien**: "Code soll gut sein"
- **Zu viele parallel**: > 5 kann System überlasten
- **Ohne Tests**: Automatische Validierung fehlt

## Optionen

| Option | Default | Beschreibung |
|--------|---------|--------------|
| `--max-parallel` | 3 | Maximale gleichzeitige Agents |
| `--max-iterations` | 30 | Max. Iterationen pro Task-Loop |
| `--linear` | false | Linear statt Filesystem |
| `--skip-review` | false | Review-Phase überspringen |
| `--dry-run` | false | Nur Analyse, keine Ausführung |

## Kosten-Schätzung

> ⚠️ **ACHTUNG**: Autonome Loops können signifikante API-Kosten verursachen!

**Faustformel**:
- ~$0.50-2.00 pro Task (je nach Komplexität)
- Review: ~$0.20-0.50 pro Task
- EPIC mit 10 Tasks: ~$10-30

**Kostenkontrolle**:
```bash
# Konservativ
/implement-epic feature-x --max-iterations 20 --max-parallel 2

# Schnell aber teurer
/implement-epic feature-x --max-iterations 50 --max-parallel 5
```

## Detail-Dokumentation

- **[orchestrator-architecture.md](../references/implement-epic/orchestrator-architecture.md)** - Technische Details
- **[ralph-integration.md](../references/implement-epic/ralph-integration.md)** - Ralph Wiggum Konfiguration
- **[parallel-strategies.md](../references/implement-epic/parallel-strategies.md)** - Parallelisierungs-Patterns
- **[troubleshooting.md](../references/implement-epic/troubleshooting.md)** - Häufige Probleme

## Siehe auch

- **[/project-management:create-plan](./create-plan.md)** - EPIC/Tasks erstellen
- **[/project-management:implement-task](./implement-task.md)** - Einzelne Tasks
- **[/code-quality:code-reviewer](../../code-quality/agents/code-reviewer.md)** - Review Agent
- **[Ralph Wiggum Plugin](https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum)** - Autonome Loops

---

**Arguments**: $ARGUMENTS
