# Parallelisation Strategies

Strategies for efficient parallel task execution.

## Dependency Analysis

### Graph Types

**Sequential (Chain)**:

```
task-001 → task-002 → task-003 → task-004
```

- Parallelisation: None
- Strategy: Process sequentially

**Broad (Many independent)**:

```
task-001 ─┐
task-002 ─┼→ task-005
task-003 ─┤
task-004 ─┘
```

- Parallelisation: High (4 parallel)
- Strategy: Start all, then merge

**Hybrid (Typical)**:

```
task-001 ──┬──→ task-003 ──┬──→ task-005
           │               │
task-002 ──┘               └──→ task-006

task-004 (independent)
```

- Parallelisation: Medium
- Strategy: Wave-based execution

## Scheduling Algorithms

### Topological Sorting

```python
def topological_sort(tasks: List[Task]) -> List[List[Task]]:
    """
    Groups tasks into waves based on dependencies.

    Returns:
        List of waves, each wave executable in parallel
    """
    waves = []
    remaining = set(t.id for t in tasks)
    completed = set()

    while remaining:
        # Tasks with no outstanding dependencies
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

**Example**:

```
Tasks: 001(none), 002(none), 003(001,002), 004(none), 005(003,004)

Wave 1: [001, 002, 004]  ← All parallel
Wave 2: [003]            ← Awaits 001, 002
Wave 3: [005]            ← Awaits 003, 004
```

### Critical Path

```python
def critical_path(tasks: List[Task]) -> List[str]:
    """
    Identifies the longest path through the dependency graph.
    This determines the minimum total execution time.
    """
    # Story point weighted longest path
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

    # Find task with longest path length
    lengths = {t.id: max_path_length(t.id) for t in tasks}
    return _reconstruct_path(lengths)
```

## Resource Management

### Worker Pool

```python
class WorkerPool:
    def __init__(self, max_workers: int):
        self.max_workers = max_workers
        self.active_workers = {}
        self.queue = asyncio.Queue()

    async def submit(self, task: Task) -> Future:
        """Enqueue task for execution."""
        future = asyncio.Future()
        await self.queue.put((task, future))
        return future

    async def _worker_loop(self, worker_id: int):
        """Worker loop."""
        while True:
            task, future = await self.queue.get()

            try:
                result = await self._execute_task(task)
                future.set_result(result)
            except Exception as e:
                future.set_exception(e)

            self.queue.task_done()
```

### Dynamic Scaling

```python
class AdaptiveScheduler:
    def __init__(self, min_parallel=1, max_parallel=5):
        self.min_parallel = min_parallel
        self.max_parallel = max_parallel
        self.current_parallel = min_parallel

    def adjust_parallelism(self, metrics: SystemMetrics):
        """
        Adjusts parallelism based on system metrics.
        """
        if metrics.cpu_usage > 80:
            # System overloaded, reduce parallelism
            self.current_parallel = max(
                self.min_parallel,
                self.current_parallel - 1
            )
        elif metrics.cpu_usage < 40 and metrics.memory_available > 2_000_000_000:
            # Capacity available, increase parallelism
            self.current_parallel = min(
                self.max_parallel,
                self.current_parallel + 1
            )
```

## Worktree Optimisation

### Worktree Reuse

Instead of recreating worktrees each time:

```python
class WorktreePool:
    def __init__(self, pool_size: int = 5):
        self.pool = []
        self._initialize_pool(pool_size)

    def _initialize_pool(self, size):
        """Creates pool of worktrees."""
        for i in range(size):
            path = f".worktrees/pool-{i}"
            subprocess.run([
                "git", "worktree", "add",
                "--detach", path
            ])
            self.pool.append(WorktreeSlot(path, available=True))

    def acquire(self, branch_name: str) -> str:
        """Acquire worktree from pool."""
        for slot in self.pool:
            if slot.available:
                slot.available = False
                # Switch branch
                subprocess.run([
                    "git", "checkout", "-b", branch_name
                ], cwd=slot.path)
                return slot.path
        raise NoWorktreeAvailable()

    def release(self, path: str):
        """Return worktree to pool."""
        for slot in self.pool:
            if slot.path == path:
                # Cleanup
                subprocess.run(["git", "reset", "--hard"], cwd=path)
                subprocess.run(["git", "checkout", "main"], cwd=path)
                slot.available = True
                return
```

### Shared Dependencies

For multiple tasks with identical dependencies:

```bash
# Base worktree with npm install
git worktree add .worktrees/base origin/main
cd .worktrees/base && npm ci

# For tasks: only switch branch
cd .worktrees/base
git checkout -b feature/task-001
# node_modules already present!
```

## Conflict Prevention

### File Locking

```python
class FileLockManager:
    def __init__(self):
        self.locks = {}  # file_path -> task_id

    def can_modify(self, task_id: str, files: List[str]) -> bool:
        """Checks whether task may modify files."""
        for file in files:
            if file in self.locks and self.locks[file] != task_id:
                return False
        return True

    def acquire_locks(self, task_id: str, files: List[str]):
        """Lock files for task."""
        for file in files:
            self.locks[file] = task_id

    def release_locks(self, task_id: str):
        """Release all locks held by task."""
        self.locks = {
            f: t for f, t in self.locks.items()
            if t != task_id
        }
```

### Conflict Detection

```python
def detect_potential_conflicts(tasks: List[Task]) -> List[Tuple[str, str, str]]:
    """
    Detects tasks that may modify the same files.

    Returns:
        List of (task1_id, task2_id, shared_file) tuples
    """
    conflicts = []

    for i, task1 in enumerate(tasks):
        for task2 in tasks[i+1:]:
            shared_files = set(task1.affected_files) & set(task2.affected_files)
            for file in shared_files:
                conflicts.append((task1.id, task2.id, file))

    return conflicts
```

### Conflict Resolution

For unavoidable conflicts:

```python
def resolve_conflict(task1: Task, task2: Task, file: str):
    """
    Strategies for conflict resolution.
    """
    # Strategy 1: Serialise
    task2.requires.append(task1.id)

    # Strategy 2: Split file (if feasible)
    # e.g., utils.py → utils/helpers.py + utils/formatters.py

    # Strategy 3: Defer merge
    # Execute both in parallel, with manual merge step
```

## Monitoring and Metrics

### Progress Tracking

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
        Measures parallelism utilisation.
        1.0 = optimal, < 0.5 = bottleneck
        """
        theoretical_parallel_time = sum(t.duration for t in self.active_tasks)
        actual_elapsed = self.elapsed_time
        return theoretical_parallel_time / (actual_elapsed * self.max_parallel)
```

### Visualisation

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
