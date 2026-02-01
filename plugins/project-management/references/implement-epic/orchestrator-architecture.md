# EPIC Orchestrator Architecture

Technical specifications for the implementation of the EPIC Orchestrator system.

## Architectural Overview

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
│ │   Auto    │ │  │ │   Auto    │ │  │ │   Auto    │ │
│ │   Loop    │ │  │ │   Loop    │ │  │ │   Loop    │ │
│ └───────────┘ │  │ └───────────┘ │  │ └───────────┘ │
│               │  │               │  │               │
│ ┌───────────┐ │  │ ┌───────────┐ │  │ ┌───────────┐ │
│ │Review Loop│ │  │ │Review Loop│ │  │ │Review Loop│ │
│ └───────────┘ │  │ └───────────┘ │  │ └───────────┘ │
└───────────────┘  └───────────────┘  └───────────────┘
```

## Components

### 1. EPIC Loader

The EPIC Loader retrieves EPIC data from either the filesystem or Linear.

```python
class EPICLoader:
    def load_from_filesystem(self, plan_path: str) -> EPIC:
        """
        Loads an EPIC from .plans/[feature]/

        Returns:
            EPIC containing:
            - metadata (from EPIC.md)
            - tasks (from tasks/*.md)
            - status (from STATUS.md)
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
        Loads an EPIC from Linear via MCP.

        Uses:
            - mcp__linear__get_issue(id=epic_id)
            - mcp__linear__list_issues(parentId=epic_id)
        """
        # Linear API calls via MCP
        pass
```

### 2. Dependency Resolver

The Dependency Resolver analyses task dependencies and determines the execution order.

```python
from dataclasses import dataclass
from typing import List, Set, Dict

@dataclass
class Task:
    id: str
    status: str  # pending, in_progress, completed, blocked
    requires: List[str]  # Task IDs that must be completed first
    blocks: List[str]    # Task IDs that depend on this task

class DependencyResolver:
    def __init__(self, tasks: List[Task]):
        self.tasks = {t.id: t for t in tasks}
        self.graph = self._build_graph()

    def _build_graph(self) -> Dict[str, Set[str]]:
        """Constructs the dependency graph."""
        graph = {t.id: set() for t in self.tasks.values()}
        for task in self.tasks.values():
            for req in task.requires:
                graph[task.id].add(req)
        return graph

    def get_ready_tasks(self) -> List[Task]:
        """
        Returns tasks that are ready for execution:
        - Status = pending
        - All dependencies are completed
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
        """Detects circular dependencies."""
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
        Computes the critical path (longest chain).
        Useful for time estimation.
        """
        # Topological sorting + longest path algorithm
        pass
```

### 3. Agent Coordinator

The Agent Coordinator manages Task Agents and their lifecycle.

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
        Spawns a new Task Agent.

        1. Create worktree
        2. Spawn agent with fresh context
        3. Start autonomous loop for implementation
        """
        # Wait for available slot
        while len(self.active_agents) >= self.max_parallel:
            await self._wait_for_completion()

        agent = TaskAgent(task, config)
        self.active_agents[task.id] = agent

        # Start agent in separate thread
        future = self.executor.submit(agent.run)
        agent.future = future

        return agent

    async def _wait_for_completion(self):
        """Waits until an agent completes."""
        while True:
            for task_id, agent in list(self.active_agents.items()):
                if agent.is_complete():
                    del self.active_agents[task_id]
                    return agent
            await asyncio.sleep(5)

    def get_status(self) -> Dict:
        """Returns the current status of all agents."""
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

Individual agent responsible for task implementation.

```python
class TaskAgent:
    def __init__(self, task: Task, config: AgentConfig):
        self.task = task
        self.config = config
        self.worktree_path = f".worktrees/task-{task.id}"
        self.status = "initializing"
        self.current_iteration = 0

    def run(self):
        """Main loop of the Task Agent."""
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

            # Phase 3: Finalisation
            self.status = "finalizing"
            self._finalize_pr()
            self._update_task_status("completed")

        except Exception as e:
            self._handle_error(e)

    def _setup_worktree(self):
        """Creates the Git worktree."""
        branch_name = f"feature/task-{self.task.id}"

        # Create worktree
        subprocess.run([
            "git", "worktree", "add",
            "-b", branch_name,
            self.worktree_path,
            "origin/main"
        ], check=True)

        # Initialise submodules
        subprocess.run([
            "git", "submodule", "update",
            "--init", "--recursive"
        ], cwd=self.worktree_path, check=True)

    def _run_implementation_loop(self) -> str:
        """
        Autonomous loop for implementation.

        Returns:
            "TASK_COMPLETE" or "TASK_BLOCKED"
        """
        prompt = self._build_implementation_prompt()

        # Use Task tool with fresh context
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
        Autonomous loop for review.

        Returns:
            "REVIEW_COMPLETE" or "REVIEW_NEEDS_ATTENTION"
        """
        prompt = self._build_review_prompt()

        result = spawn_subagent(
            type="review",
            prompt=prompt,
            working_dir=self.worktree_path,
            max_iterations=15,  # Reviews require fewer iterations
            completion_promise="REVIEW_COMPLETE|REVIEW_NEEDS_ATTENTION"
        )

        return result.completion_promise

    def _build_implementation_prompt(self) -> str:
        """Constructs the implementation prompt."""
        return f"""
Implement Task {self.task.id}: {self.task.title}

## Description
{self.task.description}

## Acceptance Criteria
{self._format_acceptance_criteria()}

## Working Directory
You are working in: {self.worktree_path}

## Instructions
1. Analyse the task
2. Implement step by step
3. Write tests for each acceptance criterion
4. Execute tests and resolve failures
5. Commit regularly with descriptive messages

## Completion
When all acceptance criteria are satisfied:
Output: <promise>TASK_COMPLETE</promise>

For insurmountable blockers (missing dependencies, unclear requirements):
- Document the blocker
- Output: <promise>TASK_BLOCKED</promise>
"""

    def _build_review_prompt(self) -> str:
        """Constructs the review prompt."""
        return f"""
Review PR for Task {self.task.id}

## Task
1. Load PR diff: gh pr diff
2. Evaluate against code review checklist:
   - Fundamental quality (readability, naming, duplication)
   - Security (no secrets, input validation)
   - Robustness (error handling, logging)
   - Maintainability (tests, documentation)
   - Performance (algorithm efficiency)

3. For each identified issue:
   - Resolve it directly
   - Commit with clear message

## Completion
When all issues are resolved:
Output: <promise>REVIEW_COMPLETE</promise>

For issues requiring user intervention:
- Document in PR comment
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
        """Generates STATUS.md content."""
        # Template-based generation
        pass

    @classmethod
    def from_status_md(cls, content: str) -> 'EPICState':
        """Parses STATUS.md."""
        pass
```

### Persistence

The orchestrator persists its state in the following structure:

```
.plans/[feature]/
├── .orchestrator/
│   ├── state.json       # Current orchestrator state
│   ├── agents.json      # Active agent states
│   └── logs/
│       ├── task-001.log
│       └── task-002.log
```

This enables:

- **Crash recovery**: Orchestrator can resume from last checkpoint
- **Status queries**: `/implement-epic --status feature-x`
- **Debugging**: Per-task log files

## Event System

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

### Event Handlers

```python
# Status updates
orchestrator.events.on('task_progress', lambda task_id, iteration:
    update_progress_display(task_id, iteration)
)

# Slack notifications (optional)
orchestrator.events.on('epic_completed', lambda epic_id:
    send_slack_notification(f"EPIC {epic_id} completed!")
)
```

## Error Recovery

### Checkpoint System

```python
class CheckpointManager:
    def save_checkpoint(self, state: EPICState):
        """Saves checkpoint for recovery."""
        checkpoint = {
            'state': state.to_dict(),
            'timestamp': datetime.now().isoformat(),
            'active_agents': self._serialize_agents()
        }
        self._write_checkpoint(checkpoint)

    def restore_from_checkpoint(self) -> EPICState:
        """Restores state from most recent checkpoint."""
        checkpoint = self._read_latest_checkpoint()
        return EPICState.from_dict(checkpoint['state'])
```

### Recovery Strategies

| Error              | Recovery                             |
| ------------------ | ------------------------------------ |
| Agent crash        | Retain worktree, spawn new agent     |
| Orchestrator crash | Resume from checkpoint               |
| Git conflict       | Set task status to `needs_attention` |
| API rate limit     | Exponential backoff, then resume     |
