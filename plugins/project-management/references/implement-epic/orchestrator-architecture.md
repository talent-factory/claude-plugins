# EPIC-Orchestrator Architektur

Technische Details zur Implementierung des EPIC-Orchestrators.

## Architektur-Übersicht

```
┌─────────────────────────────────────────────────────────────────┐
│                     EPIC Orchestrator (Main)                    │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │ EPIC Loader │  │ Dependency  │  │    Agent Coordinator    │ │
│  │             │  │   Resolver  │  │                         │ │
│  └──────┬──────┘  └──────┬──────┘  └───────────┬─────────────┘ │
│         │                │                      │               │
│         └────────────────┼──────────────────────┘               │
│                          │                                      │
└──────────────────────────┼──────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│  Task Agent   │  │  Task Agent   │  │  Task Agent   │
│  (Worktree 1) │  │  (Worktree 2) │  │  (Worktree N) │
│               │  │               │  │               │
│ ┌───────────┐ │  │ ┌───────────┐ │  │ ┌───────────┐ │
│ │Ralph Loop │ │  │ │Ralph Loop │ │  │ │Ralph Loop │ │
│ └───────────┘ │  └───────────┘ │  │ └───────────┘ │
│               │  │               │  │               │
│ ┌───────────┐ │  │ ┌───────────┐ │  │ ┌───────────┐ │
│ │Review Loop│ │  │ │Review Loop│ │  │ │Review Loop│ │
│ └───────────┘ │  │ └───────────┘ │  │ └───────────┘ │
└───────────────┘  └───────────────┘  └───────────────┘
```

## Komponenten

### 1. EPIC Loader

Lädt EPIC-Daten aus Filesystem oder Linear:

```python
class EPICLoader:
    def load_from_filesystem(self, plan_path: str) -> EPIC:
        """
        Lädt EPIC aus .plans/[feature]/

        Returns:
            EPIC mit:
            - metadata (aus EPIC.md)
            - tasks (aus tasks/*.md)
            - status (aus STATUS.md)
        """
        epic_path = plan_path / "EPIC.md"
        status_path = plan_path / "STATUS.md"
        tasks_dir = plan_path / "tasks"

        return EPIC(
            metadata=parse_epic_md(epic_path),
            tasks=[parse_task_md(f) for f in tasks_dir.glob("*.md")],
            status=parse_status_md(status_path)
        )

    def load_from_linear(self, epic_id: str) -> EPIC:
        """
        Lädt EPIC aus Linear via MCP.

        Uses:
            - mcp__linear__get_issue(id=epic_id)
            - mcp__linear__list_issues(parentId=epic_id)
        """
        # Linear API calls via MCP
        pass
```

### 2. Dependency Resolver

Analysiert Task-Dependencies und ermittelt Ausführungsreihenfolge:

```python
from dataclasses import dataclass
from typing import List, Set, Dict

@dataclass
class Task:
    id: str
    status: str  # pending, in_progress, completed, blocked
    requires: List[str]  # Task-IDs die vorher fertig sein müssen
    blocks: List[str]    # Task-IDs die auf diesen warten

class DependencyResolver:
    def __init__(self, tasks: List[Task]):
        self.tasks = {t.id: t for t in tasks}
        self.graph = self._build_graph()

    def _build_graph(self) -> Dict[str, Set[str]]:
        """Baut Dependency-Graph auf."""
        graph = {t.id: set() for t in self.tasks.values()}
        for task in self.tasks.values():
            for req in task.requires:
                graph[task.id].add(req)
        return graph

    def get_ready_tasks(self) -> List[Task]:
        """
        Gibt Tasks zurück, die gestartet werden können:
        - Status = pending
        - Alle Dependencies sind completed
        """
        ready = []
        for task in self.tasks.values():
            if task.status != 'pending':
                continue

            deps_complete = all(
                self.tasks[dep].status == 'completed'
                for dep in task.requires
                if dep in self.tasks
            )

            if deps_complete:
                ready.append(task)

        return ready

    def has_circular_dependency(self) -> bool:
        """Prüft auf zirkuläre Dependencies."""
        visited = set()
        rec_stack = set()

        def dfs(node):
            visited.add(node)
            rec_stack.add(node)

            for neighbor in self.graph.get(node, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True

            rec_stack.remove(node)
            return False

        for node in self.graph:
            if node not in visited:
                if dfs(node):
                    return True
        return False

    def get_critical_path(self) -> List[str]:
        """
        Berechnet den kritischen Pfad (längste Kette).
        Nützlich für Zeitschätzung.
        """
        # Topologische Sortierung + längster Pfad
        pass
```

### 3. Agent Coordinator

Verwaltet Task-Agents und deren Lifecycle:

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

class AgentCoordinator:
    def __init__(self, max_parallel: int = 3):
        self.max_parallel = max_parallel
        self.active_agents: Dict[str, TaskAgent] = {}
        self.executor = ThreadPoolExecutor(max_workers=max_parallel)

    async def spawn_task_agent(self, task: Task, config: AgentConfig) -> TaskAgent:
        """
        Startet einen neuen Task-Agent.

        1. Worktree erstellen
        2. Agent mit frischem Kontext spawnen
        3. Ralph-Loop für Implementation starten
        """
        # Warten bis Slot frei
        while len(self.active_agents) >= self.max_parallel:
            await self._wait_for_completion()

        agent = TaskAgent(task, config)
        self.active_agents[task.id] = agent

        # Agent in eigenem Thread starten
        future = self.executor.submit(agent.run)
        agent.future = future

        return agent

    async def _wait_for_completion(self):
        """Wartet bis ein Agent fertig ist."""
        while True:
            for task_id, agent in list(self.active_agents.items()):
                if agent.is_complete():
                    del self.active_agents[task_id]
                    return agent
            await asyncio.sleep(5)

    def get_status(self) -> Dict:
        """Aktueller Status aller Agents."""
        return {
            task_id: {
                'status': agent.status,
                'iteration': agent.current_iteration,
                'progress': agent.estimated_progress
            }
            for task_id, agent in self.active_agents.items()
        }
```

### 4. Task Agent

Einzelner Agent für Task-Implementation:

```python
class TaskAgent:
    def __init__(self, task: Task, config: AgentConfig):
        self.task = task
        self.config = config
        self.worktree_path = f".worktrees/task-{task.id}"
        self.status = "initializing"
        self.current_iteration = 0

    def run(self):
        """Hauptloop des Task-Agents."""
        try:
            self._setup_worktree()
            self._create_draft_pr()

            # Phase 1: Implementation
            self.status = "implementing"
            impl_result = self._run_implementation_loop()

            if impl_result == "TASK_BLOCKED":
                self._handle_blocked()
                return

            # Phase 2: Review
            self.status = "reviewing"
            review_result = self._run_review_loop()

            if review_result == "REVIEW_NEEDS_ATTENTION":
                self._handle_needs_attention()
                return

            # Phase 3: Finalisierung
            self.status = "finalizing"
            self._finalize_pr()
            self._update_task_status("completed")

        except Exception as e:
            self._handle_error(e)

    def _setup_worktree(self):
        """Git Worktree erstellen."""
        branch_name = f"feature/task-{self.task.id}"

        # Worktree erstellen
        subprocess.run([
            "git", "worktree", "add",
            "-b", branch_name,
            self.worktree_path,
            "origin/main"
        ], check=True)

        # Submodule initialisieren
        subprocess.run([
            "git", "submodule", "update",
            "--init", "--recursive"
        ], cwd=self.worktree_path, check=True)

    def _run_implementation_loop(self) -> str:
        """
        Ralph-Loop für Implementation.

        Returns:
            "TASK_COMPLETE" oder "TASK_BLOCKED"
        """
        prompt = self._build_implementation_prompt()

        # Task-Tool mit frischem Kontext nutzen
        result = spawn_subagent(
            type="implementation",
            prompt=prompt,
            working_dir=self.worktree_path,
            max_iterations=self.config.max_iterations,
            completion_promise="TASK_COMPLETE|TASK_BLOCKED"
        )

        return result.completion_promise

    def _run_review_loop(self) -> str:
        """
        Ralph-Loop für Review.

        Returns:
            "REVIEW_COMPLETE" oder "REVIEW_NEEDS_ATTENTION"
        """
        prompt = self._build_review_prompt()

        result = spawn_subagent(
            type="review",
            prompt=prompt,
            working_dir=self.worktree_path,
            max_iterations=15,  # Reviews brauchen weniger Iterationen
            completion_promise="REVIEW_COMPLETE|REVIEW_NEEDS_ATTENTION"
        )

        return result.completion_promise

    def _build_implementation_prompt(self) -> str:
        """Baut den Implementation-Prompt."""
        return f"""
Implementiere Task {self.task.id}: {self.task.title}

## Beschreibung
{self.task.description}

## Akzeptanzkriterien
{self._format_acceptance_criteria()}

## Arbeitsverzeichnis
Du arbeitest in: {self.worktree_path}

## Anweisungen
1. Analysiere die Aufgabe
2. Implementiere Schritt für Schritt
3. Schreibe Tests für jedes Akzeptanzkriterium
4. Führe Tests aus und behebe Fehler
5. Committe regelmässig mit aussagekräftigen Messages

## Completion
Wenn alle Akzeptanzkriterien erfüllt:
Output: <promise>TASK_COMPLETE</promise>

Bei unlösbaren Blockern (fehlende Dependencies, unklare Anforderungen):
- Dokumentiere den Blocker
- Output: <promise>TASK_BLOCKED</promise>
"""

    def _build_review_prompt(self) -> str:
        """Baut den Review-Prompt."""
        return f"""
Review PR für Task {self.task.id}

## Aufgabe
1. Lade PR-Diff: gh pr diff
2. Prüfe nach Code-Review-Checkliste:
   - Grundlegende Qualität (Lesbarkeit, Naming, Duplikation)
   - Sicherheit (keine Secrets, Input-Validierung)
   - Robustheit (Error-Handling, Logging)
   - Wartbarkeit (Tests, Dokumentation)
   - Performance (Algorithmus-Effizienz)

3. Für jedes gefundene Problem:
   - Behebe es selbst
   - Committe mit klarer Message

## Completion
Wenn alle Issues behoben:
Output: <promise>REVIEW_COMPLETE</promise>

Bei Problemen die User-Eingriff benötigen:
- Dokumentiere in PR-Kommentar
Output: <promise>REVIEW_NEEDS_ATTENTION</promise>
"""
```

## State Management

### EPIC State

```python
@dataclass
class EPICState:
    epic_id: str
    status: str  # planned, in_progress, completed, blocked
    tasks: Dict[str, TaskState]
    started_at: datetime
    updated_at: datetime

    def to_status_md(self) -> str:
        """Generiert STATUS.md Inhalt."""
        # Template-basierte Generierung
        pass

    @classmethod
    def from_status_md(cls, content: str) -> 'EPICState':
        """Parst STATUS.md."""
        pass
```

### Persistence

Der Orchestrator speichert seinen State:

```
.plans/[feature]/
├── .orchestrator/
│   ├── state.json       # Aktueller Orchestrator-State
│   ├── agents.json      # Aktive Agent-States
│   └── logs/
│       ├── task-001.log
│       └── task-002.log
```

Dies ermöglicht:
- **Resume nach Crash**: Orchestrator kann fortgesetzt werden
- **Status-Abfrage**: `/implement-epic --status feature-x`
- **Debugging**: Logs pro Task

## Event-System

```python
class EPICOrchestrator:
    def __init__(self):
        self.events = EventEmitter()

    def run(self, epic_id: str):
        self.events.emit('epic_started', epic_id)

        while not self._is_complete():
            ready_tasks = self._get_ready_tasks()

            for task in ready_tasks:
                agent = self._spawn_agent(task)
                agent.on('iteration', lambda i: self.events.emit('task_progress', task.id, i))
                agent.on('complete', lambda: self._handle_task_complete(task))
                agent.on('blocked', lambda: self._handle_task_blocked(task))

            self._wait_for_next_event()
            self._update_status()

        self.events.emit('epic_completed', epic_id)
```

### Event-Handler

```python
# Status-Updates
orchestrator.events.on('task_progress', lambda task_id, iteration:
    update_progress_display(task_id, iteration)
)

# Slack-Notifications (optional)
orchestrator.events.on('epic_completed', lambda epic_id:
    send_slack_notification(f"EPIC {epic_id} completed!")
)
```

## Error Recovery

### Checkpoint-System

```python
class CheckpointManager:
    def save_checkpoint(self, state: EPICState):
        """Speichert Checkpoint für Recovery."""
        checkpoint = {
            'state': state.to_dict(),
            'timestamp': datetime.now().isoformat(),
            'active_agents': self._serialize_agents()
        }
        self._write_checkpoint(checkpoint)

    def restore_from_checkpoint(self) -> EPICState:
        """Stellt State aus letztem Checkpoint wieder her."""
        checkpoint = self._read_latest_checkpoint()
        return EPICState.from_dict(checkpoint['state'])
```

### Recovery-Strategien

| Fehler | Recovery |
|--------|----------|
| Agent-Crash | Worktree behalten, neuen Agent starten |
| Orchestrator-Crash | Von Checkpoint fortsetzen |
| Git-Konflikt | Task auf `needs_attention` setzen |
| API-Limit | Exponential Backoff, dann fortsetzen |
