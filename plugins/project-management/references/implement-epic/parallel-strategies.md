# Parallelisierungs-Strategien

Strategien für effiziente parallele Task-Ausführung.

## Dependency-Analyse

### Graph-Typen

**Sequentiell (Kette)**:
```
task-001 → task-002 → task-003 → task-004
```
- Parallelisierung: Keine
- Strategie: Nacheinander abarbeiten

**Breit (Viele unabhängige)**:
```
task-001 ─┐
task-002 ─┼→ task-005
task-003 ─┤
task-004 ─┘
```
- Parallelisierung: Hoch (4 parallel)
- Strategie: Alle starten, dann zusammenführen

**Hybrid (Typisch)**:
```
task-001 ──┬──→ task-003 ──┬──→ task-005
           │               │
task-002 ──┘               └──→ task-006

task-004 (unabhängig)
```
- Parallelisierung: Mittel
- Strategie: Wellenbasiert

## Scheduling-Algorithmen

### Topologische Sortierung

```python
def topological_sort(tasks: List[Task]) -> List[List[Task]]:
    """
    Gruppiert Tasks in Wellen basierend auf Dependencies.

    Returns:
        Liste von Wellen, jede Welle ist parallel ausführbar
    """
    waves = []
    remaining = set(t.id for t in tasks)
    completed = set()

    while remaining:
        # Tasks ohne offene Dependencies
        wave = [
            t for t in tasks
            if t.id in remaining
            and all(dep in completed for dep in t.requires)
        ]

        if not wave:
            raise CircularDependencyError()

        waves.append(wave)
        for t in wave:
            remaining.remove(t.id)
            completed.add(t.id)

    return waves
```

**Beispiel**:
```
Tasks: 001(none), 002(none), 003(001,002), 004(none), 005(003,004)

Welle 1: [001, 002, 004]  ← Alle parallel
Welle 2: [003]            ← Wartet auf 001, 002
Welle 3: [005]            ← Wartet auf 003, 004
```

### Kritischer Pfad

```python
def critical_path(tasks: List[Task]) -> List[str]:
    """
    Findet den längsten Pfad durch den Dependency-Graph.
    Dieser bestimmt die minimale Gesamtzeit.
    """
    # SP-gewichteter längster Pfad
    def max_path_length(task_id, memo={}):
        if task_id in memo:
            return memo[task_id]

        task = tasks[task_id]
        if not task.requires:
            result = task.story_points
        else:
            result = task.story_points + max(
                max_path_length(dep, memo)
                for dep in task.requires
            )

        memo[task_id] = result
        return result

    # Task mit längster Pfadlänge finden
    lengths = {t.id: max_path_length(t.id) for t in tasks}
    return _reconstruct_path(lengths)
```

## Resource-Management

### Worker-Pool

```python
class WorkerPool:
    def __init__(self, max_workers: int):
        self.max_workers = max_workers
        self.active_workers = {}
        self.queue = asyncio.Queue()

    async def submit(self, task: Task) -> Future:
        """Task zur Ausführung einreihen."""
        future = asyncio.Future()
        await self.queue.put((task, future))
        return future

    async def _worker_loop(self, worker_id: int):
        """Worker-Schleife."""
        while True:
            task, future = await self.queue.get()

            try:
                result = await self._execute_task(task)
                future.set_result(result)
            except Exception as e:
                future.set_exception(e)

            self.queue.task_done()
```

### Dynamische Skalierung

```python
class AdaptiveScheduler:
    def __init__(self, min_parallel=1, max_parallel=5):
        self.min_parallel = min_parallel
        self.max_parallel = max_parallel
        self.current_parallel = min_parallel

    def adjust_parallelism(self, metrics: SystemMetrics):
        """
        Passt Parallelität basierend auf System-Metriken an.
        """
        if metrics.cpu_usage > 80:
            # System überlastet, reduzieren
            self.current_parallel = max(
                self.min_parallel,
                self.current_parallel - 1
            )
        elif metrics.cpu_usage < 40 and metrics.memory_available > 2_000_000_000:
            # Kapazität verfügbar, erhöhen
            self.current_parallel = min(
                self.max_parallel,
                self.current_parallel + 1
            )
```

## Worktree-Optimierung

### Worktree-Reuse

Statt Worktrees immer neu zu erstellen:

```python
class WorktreePool:
    def __init__(self, pool_size: int = 5):
        self.pool = []
        self._initialize_pool(pool_size)

    def _initialize_pool(self, size):
        """Erstellt Pool von Worktrees."""
        for i in range(size):
            path = f".worktrees/pool-{i}"
            subprocess.run([
                "git", "worktree", "add",
                "--detach", path
            ])
            self.pool.append(WorktreeSlot(path, available=True))

    def acquire(self, branch_name: str) -> str:
        """Worktree aus Pool holen."""
        for slot in self.pool:
            if slot.available:
                slot.available = False
                # Branch wechseln
                subprocess.run([
                    "git", "checkout", "-b", branch_name
                ], cwd=slot.path)
                return slot.path
        raise NoWorktreeAvailable()

    def release(self, path: str):
        """Worktree zurückgeben."""
        for slot in self.pool:
            if slot.path == path:
                # Cleanup
                subprocess.run(["git", "reset", "--hard"], cwd=path)
                subprocess.run(["git", "checkout", "main"], cwd=path)
                slot.available = True
                return
```

### Shared Dependencies

Bei vielen Tasks mit gleichen Dependencies:

```bash
# Basis-Worktree mit npm install
git worktree add .worktrees/base origin/main
cd .worktrees/base && npm ci

# Für Tasks: Nur Branch wechseln
cd .worktrees/base
git checkout -b feature/task-001
# node_modules bereits vorhanden!
```

## Conflict-Prevention

### Datei-Locking

```python
class FileLockManager:
    def __init__(self):
        self.locks = {}  # file_path -> task_id

    def can_modify(self, task_id: str, files: List[str]) -> bool:
        """Prüft ob Task Dateien modifizieren darf."""
        for file in files:
            if file in self.locks and self.locks[file] != task_id:
                return False
        return True

    def acquire_locks(self, task_id: str, files: List[str]):
        """Dateien für Task sperren."""
        for file in files:
            self.locks[file] = task_id

    def release_locks(self, task_id: str):
        """Alle Locks eines Tasks freigeben."""
        self.locks = {
            f: t for f, t in self.locks.items()
            if t != task_id
        }
```

### Conflict-Detection

```python
def detect_potential_conflicts(tasks: List[Task]) -> List[Tuple[str, str, str]]:
    """
    Erkennt Tasks die gleiche Dateien ändern könnten.

    Returns:
        Liste von (task1_id, task2_id, shared_file) Tupeln
    """
    conflicts = []

    for i, task1 in enumerate(tasks):
        for task2 in tasks[i+1:]:
            shared_files = set(task1.affected_files) & set(task2.affected_files)
            for file in shared_files:
                conflicts.append((task1.id, task2.id, file))

    return conflicts
```

### Conflict-Resolution

Bei unvermeidlichen Konflikten:

```python
def resolve_conflict(task1: Task, task2: Task, file: str):
    """
    Strategien zur Konfliktauflösung.
    """
    # Strategie 1: Sequentialisieren
    task2.requires.append(task1.id)

    # Strategie 2: Datei aufteilen (wenn möglich)
    # z.B. utils.py → utils/helpers.py + utils/formatters.py

    # Strategie 3: Merge später
    # Beide parallel, aber mit manuellem Merge-Step
```

## Monitoring & Metrics

### Progress-Tracking

```python
@dataclass
class ParallelMetrics:
    total_tasks: int
    completed_tasks: int
    active_tasks: int
    blocked_tasks: int
    total_iterations: int
    estimated_cost: float
    elapsed_time: timedelta
    estimated_remaining: timedelta

    @property
    def parallelism_efficiency(self) -> float:
        """
        Wie gut wird Parallelität genutzt?
        1.0 = perfekt, < 0.5 = Bottleneck
        """
        theoretical_parallel_time = sum(t.duration for t in self.active_tasks)
        actual_elapsed = self.elapsed_time
        return theoretical_parallel_time / (actual_elapsed * self.max_parallel)
```

### Visualisierung

```
╔═════════════════════════════════════════════════════════════════╗
║  EPIC: Feature-X           Efficiency: 78%    Cost: $12.50     ║
╠═════════════════════════════════════════════════════════════════╣
║                                                                 ║
║  Timeline:                                                      ║
║  ├─ Wave 1 ─────────────────────────────────────────────────┤  ║
║  │  task-001 ████████████████████████░░░░░░ 80%             │  ║
║  │  task-002 ██████████████████████████████ ✓               │  ║
║  │  task-004 ████████████████░░░░░░░░░░░░░░ 50%             │  ║
║  ├─ Wave 2 ─────────────────────────────────────────────────┤  ║
║  │  task-003 ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ waiting         │  ║
║  ├─ Wave 3 ─────────────────────────────────────────────────┤  ║
║  │  task-005 ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ waiting         │  ║
║  │  task-006 ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ waiting         │  ║
║                                                                 ║
╚═════════════════════════════════════════════════════════════════╝
```
