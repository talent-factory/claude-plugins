---
description: Implement a complete EPIC automatically with parallel agents using native Claude Code autonomous loops
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

Automated, parallel implementation of all tasks within an EPIC using **native Claude Code autonomous loops** (Task tool with subagents) for self-directed development cycles.

## Overview

This command orchestrates the **fully automated implementation of an EPIC**:

1. **Load EPIC** - From `.plans/` or Linear
2. **Analyze Dependency Graph** - Identify parallelizable tasks
3. **Start Parallel Execution** - One agent per independent task in its own worktree
4. **Autonomous Implementation** - Subagent loop until completion
5. **Automatic Review** - Code review agent with iterative improvements
6. **Status Update** - Continuous updates to STATUS.md
7. **Next Round** - Start newly available tasks

## Usage

```bash
# Filesystem-based (default)
/project-management:implement-epic                           # Interactive selection
/project-management:implement-epic dark-mode-toggle          # Plan name
/project-management:implement-epic --plan .plans/feature/    # Explicit path

# Linear-based
/project-management:implement-epic --linear                  # Interactive selection
/project-management:implement-epic --linear PROJ-123         # EPIC ID

# With options
/project-management:implement-epic feature-x --max-parallel 5 --max-iterations 50
```

## Prerequisites

### Native Claude Code Task Tool

This command uses Claude Code's built-in **Task tool** to spawn subagents. No external plugins are required. The Task tool enables:

- Spawning isolated subagents with fresh context
- Parallel execution of independent work
- Automatic context management per agent

### Project Structure

The EPIC must have been created via `/project-management:create-plan`:

```text
.plans/[feature-name]/
├── EPIC.md          # Feature overview
├── STATUS.md        # Progress tracking
└── tasks/
    ├── task-001-*.md
    ├── task-002-*.md
    └── ...
```

## Workflow Details

### Phase 1: EPIC Analysis

```mermaid
graph LR
    A[Load EPIC] --> B[Read Tasks]
    B --> C[Dependency Graph]
    C --> D[Parallelizable Tasks]
```

**Dependency Analysis**:

- Read `Dependencies.Requires` from each task file
- Build directed graph
- Identify tasks without open blockers (entry points)

**Example Dependency Graph**:

```text
task-001 ──┬──► task-003 ──► task-005
           │
task-002 ──┘

task-004 (independent)
```

→ **Parallelizable**: task-001, task-002, task-004

### Phase 2: Parallel Implementation

For each independent task, a **separate subagent** is spawned:

```bash
# Per task in dedicated worktree:
Task Agent (fresh context):
│
├── 1. Create Worktree
│      git worktree add -b feature/task-001 .worktrees/task-001 origin/main
│
├── 2. Autonomous Implementation Loop (via Task tool)
│      The subagent receives:
│      - Task description and acceptance criteria
│      - Instructions to implement until all criteria are met
│      - Clear completion conditions
│
│      Subagent works autonomously:
│      - Analyzes requirements
│      - Implements solution
│      - Runs tests
│      - Iterates until acceptance criteria pass
│
├── 3. Commit & Push
│      git add . && git commit -m "feat(task-001): [description]"
│      git push -u origin feature/task-001
│
└── 4. Create Draft PR
       gh pr create --draft --title "[task-001] Task Title"
```

### Phase 3: Automatic Review

After implementation, the **review loop** starts automatically:

```bash
Review Agent (fresh context):
│
├── 1. Load PR Diff
│      gh pr diff [pr-number]
│
├── 2. Autonomous Review Loop (via Task tool)
│      The review subagent:
│      - Analyzes all changes
│      - Checks code quality (see code-reviewer checklist)
│      - Identifies issues
│      - Fixes ALL discovered issues autonomously
│      - Commits fixes with descriptive messages
│
│      Completion conditions:
│      - All issues resolved → Mark review complete
│      - Issues requiring user intervention → Document and flag
│
└── 3. Finalize PR
       gh pr ready [pr-number]  # When review complete
```

### Phase 4: Status Update and Next Round

After each completed task:

1. **Update STATUS.md**
   - Set task to `completed` / `needs_attention`
   - Recalculate progress statistics
   - Update Mermaid graph

2. **Re-evaluate Dependency Graph**
   - Which tasks are now unblocked?
   - Start new parallel agents

3. **Loop Until EPIC Complete**
   - Repeat until all tasks are completed
   - Or only blocked tasks remain

## Orchestrator Logic

```python
# Pseudocode for the EPIC orchestrator

def implement_epic(epic_id, max_parallel=3, max_iterations=30):
    epic = load_epic(epic_id)
    tasks = load_all_tasks(epic)

    while not all_tasks_complete(tasks):
        # Identify tasks ready to start
        ready_tasks = [t for t in tasks
                       if t.status == 'pending'
                       and all_dependencies_complete(t, tasks)]

        # Limit parallelism
        to_start = ready_tasks[:max_parallel - active_agents_count()]

        for task in to_start:
            # Spawn agent in dedicated worktree
            spawn_task_agent(
                task=task,
                max_iterations=max_iterations,
                on_complete=lambda: handle_task_complete(task),
                on_blocked=lambda: handle_task_blocked(task)
            )

        # Wait for next completion
        wait_for_any_completion()

        # Status update
        update_status_md(epic)

    # Finalization
    generate_epic_summary(epic)
    notify_user_completion(epic)
```

## Worktree Management

> **CRITICAL**: Each task operates in an **isolated worktree**!

### Why Worktrees?

- **Parallel Work**: Multiple tasks simultaneously without branch conflicts
- **Isolation**: No mutual overwriting
- **Clean History**: Clear commit separation per task

### Worktree Structure

```text
project/
├── .worktrees/
│   ├── task-001/          # Worktree for Task 001
│   │   ├── src/
│   │   └── ...
│   ├── task-002/          # Worktree for Task 002
│   │   ├── src/
│   │   └── ...
│   └── task-004/          # Worktree for Task 004
│       ├── src/
│       └── ...
├── src/                   # Main repo (main branch)
└── .plans/
    └── feature/
        ├── EPIC.md
        └── tasks/
```

### Worktree Lifecycle

```bash
# 1. Create (per task)
git worktree add -b feature/task-001 .worktrees/task-001 origin/main

# 2. Work (in worktree directory)
cd .worktrees/task-001
# ... implementation ...

# 3. After PR merge: Cleanup
git worktree remove .worktrees/task-001
git branch -d feature/task-001
```

## Status Tracking

### STATUS.md Updates

The orchestrator continuously updates:

```markdown
## Tasks by Status

### Completed

- **task-001**: UI Toggle Component (3 SP) - PR #12 merged

### In Progress

- **task-002**: Theme State Management (5 SP) - PR #13 in review
- **task-004**: Settings Integration (2 SP) - implementing...

### Pending

- **task-003**: LocalStorage Persistence (3 SP) - waiting for task-002
- **task-005**: E2E Tests (5 SP) - waiting for task-003

### Needs Attention

[Empty or tasks requiring user intervention]
```

### Real-Time Progress

```
╔═══════════════════════════════════════════════════════════╗
║  EPIC: Dark Mode Toggle                                   ║
╠═══════════════════════════════════════════════════════════╣
║  Progress: ████████░░░░░░░░░░░░░░░░░░░░░░  40% (2/5)      ║
║                                                           ║
║  Active Agents:                                           ║
║  • task-002 (Theme State)     [████████░░] 80% iter 24/30 ║
║  • task-004 (Settings)        [██████░░░░] 60% iter 18/30 ║
║                                                           ║
║  Completed: task-001                                      ║
║  Waiting:   task-003 → task-002                           ║
║             task-005 → task-003                           ║
╚═══════════════════════════════════════════════════════════╝
```

## Error Handling

### Task Blocked

When a task cannot be completed:

1. **Set Status**: `blocked` or `needs_attention`
2. **Documentation**: Reason in task file and PR comment
3. **User Notification**: Summary of what is missing
4. **Other Tasks**: Continue with independent tasks

### Agent Timeout

When `--max-iterations` is reached:

1. **Save Progress**: Commit all changes
2. **Status**: `in_progress` with note
3. **User Option**: Continue manually or skip

### Merge Conflicts

If main changes while EPIC is running:

```bash
# In worktree
git fetch origin
git rebase origin/main

# On conflicts: Set task to 'needs_attention'
```

## Best Practices

### DO

- **Clear Acceptance Criteria**: Testable and measurable
- **Small Tasks**: Ideally 1-5 Story Points
- **Proper Dependencies**: Correct sequence
- **Realistic Iterations**: 20-50 for complex tasks
- **Adjust Max-Parallel**: Based on CPU/Memory

### DON'T

- **Huge Tasks**: > 8 SP difficult to automate
- **Circular Dependencies**: Leads to deadlock
- **Vague Criteria**: "Code should be good"
- **Too Many Parallel**: > 5 can overload system
- **Without Tests**: Automatic validation missing

## Options

| Option             | Default | Description                  |
| ------------------ | ------- | ---------------------------- |
| `--max-parallel`   | 3       | Maximum concurrent agents    |
| `--max-iterations` | 30      | Max iterations per task loop |
| `--linear`         | false   | Linear instead of filesystem |
| `--skip-review`    | false   | Skip review phase            |
| `--dry-run`        | false   | Analysis only, no execution  |

## Cost Estimation

> **NOTE**: Autonomous loops can incur significant API costs!

**Rule of Thumb**:

- ~$0.50-2.00 per task (depending on complexity)
- Review: ~$0.20-0.50 per task
- EPIC with 10 tasks: ~$10-30

**Cost Control**:

```bash
# Conservative
/project-management:implement-epic feature-x --max-iterations 20 --max-parallel 2

# Fast but more expensive
/project-management:implement-epic feature-x --max-iterations 50 --max-parallel 5
```

## Detailed Documentation

- **[orchestrator-architecture.md](../references/implement-epic/orchestrator-architecture.md)** - Technical details
- **[parallel-strategies.md](../references/implement-epic/parallel-strategies.md)** - Parallelization patterns
- **[troubleshooting.md](../references/implement-epic/troubleshooting.md)** - Common problems

## See Also

- **[/project-management:create-plan](./create-plan.md)** - Create EPIC/tasks
- **[/project-management:implement-task](./implement-task.md)** - Individual tasks
- **[/code-quality:code-reviewer](../../code-quality/agents/code-reviewer.md)** - Review agent

---

**Arguments**: $ARGUMENTS
