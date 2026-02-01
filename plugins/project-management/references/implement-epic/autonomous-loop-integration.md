# Autonomous Loop Integration

Configuration and best practices for integrating autonomous execution loops in Claude Code.

## Overview

Autonomous loops enable Claude Code to execute iterative workflows without manual intervention. This document describes the native mechanisms for implementing persistent execution loops using Claude Code's built-in hook system and subagent capabilities.

## Core Concepts

### Stop Hook Mechanism

Claude Code supports Stop hooks that intercept exit attempts and enable conditional continuation:

```
┌─────────────────────────────────────────────────────────┐
│                     Claude Session                      │
│                                                         │
│  1. Prompt input                                        │
│           ▼                                             │
│  2. Claude executes...                                  │
│           ▼                                             │
│  3. Claude attempts to exit                             │
│           ▼                                             │
│  ┌─────────────────────────────────────────────────┐   │
│  │              STOP HOOK                          │   │
│  │                                                 │   │
│  │  Completion promise found?                      │   │
│  │     ├── YES → Allow exit                        │   │
│  │     └── NO → Re-inject prompt                   │   │
│  └─────────────────────────────────────────────────┘   │
│           ▼                                             │
│  4. Return to step 2 (with files as context)           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Completion Promise

The hook verifies exact string matches to determine loop termination:

```bash
# Simple promise
# Loop continues until output contains "COMPLETE"

# Multiple termination conditions
# Loop terminates on "SUCCESS", "FAILED", or "BLOCKED"
```

## Integration with EPIC Workflow

### Implementation Loop Configuration

The autonomous loop for task implementation uses a structured prompt with explicit termination conditions:

```markdown
Implement Task {task_id}: {title}

## Description

{description}

## Acceptance Criteria

{acceptance_criteria}

## Success Conditions

When ALL criteria are satisfied:

1. All tests pass
2. Code is committed
3. PR is created

Output: <promise>TASK_COMPLETE</promise>

## Failure Conditions

For insurmountable blockers:

- Document in BLOCKER.md
- Describe what is missing

Output: <promise>TASK_BLOCKED</promise>
```

Configuration parameters:

- Maximum iterations: 30
- Completion promise: `TASK_COMPLETE|TASK_BLOCKED`

### Review Loop Configuration

The review loop operates with fewer iterations and focuses on code quality:

```markdown
Review PR #{pr_number} for Task {task_id}

## Task

1. Load gh pr diff
2. Conduct code review
3. Resolve all issues independently
4. Commit fixes

## Success Conditions

When all issues are resolved:
Output: <promise>REVIEW_COMPLETE</promise>

## User Intervention Required

For issues requiring human decision:

- Document in PR comment
  Output: <promise>REVIEW_NEEDS_ATTENTION</promise>
```

Configuration parameters:

- Maximum iterations: 15
- Completion promise: `REVIEW_COMPLETE|REVIEW_NEEDS_ATTENTION`

## Prompt Engineering for Autonomous Loops

### Effective Prompts

**Clear Structure**:

```
# Task
[What needs to be done]

# Context
[Relevant information]

# Steps
1. [Step 1]
2. [Step 2]
...

# Success Criteria
[When is the task complete?]

# Completion
Output: <promise>DONE</promise>
```

**Testable Criteria**:

```
## Acceptance Criteria
- [ ] Unit tests pass (npm test)
- [ ] Lint checks pass (npm run lint)
- [ ] Coverage > 80%
- [ ] No TypeScript errors
```

**Escape Hatch**:

```
## Fallback
If not completed after 20 iterations:
1. Document current state
2. List outstanding items
3. Output: <promise>PARTIAL_COMPLETE</promise>
```

### Ineffective Prompts

**Vague Objectives**:

```
❌ "Improve the code"
✅ "Refactor AuthService: Extract JWT logic into separate class"
```

**Missing Exit Condition**:

```
❌ "Implement Feature X"
✅ "Implement Feature X. Output <promise>DONE</promise> when all tests pass"
```

**Excessive Scope**:

```
❌ "Build complete e-commerce system"
✅ "Implement user registration with email verification"
```

## Iteration Limits

### Recommended Values

| Task Type            | Max Iterations | Rationale                       |
| -------------------- | -------------- | ------------------------------- |
| Small task (1-2 SP)  | 15-20          | Should complete quickly         |
| Medium task (3-5 SP) | 25-35          | Additional complexity permitted |
| Large task (8+ SP)   | 40-50          | Consider decomposition          |
| Review               | 10-15          | Reviews are focused             |

### Cost Calculation

```
Cost ≈ Iterations × Tokens_per_Iteration × API_Price

Example (Sonnet):
- 30 iterations
- ~4000 tokens/iteration
- $0.003/1K input + $0.015/1K output

≈ 30 × 4000 × ($0.003 + $0.015) / 1000
≈ $2.16 per task
```

## Parallel Autonomous Loops

### Architecture

```
Terminal 1                Terminal 2                Terminal 3
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│ Worktree     │         │ Worktree     │         │ Worktree     │
│ task-001     │         │ task-002     │         │ task-004     │
│              │         │              │         │              │
│ Auto Loop    │         │ Auto Loop    │         │ Auto Loop    │
│ (impl)       │         │ (impl)       │         │ (impl)       │
└──────────────┘         └──────────────┘         └──────────────┘
       │                        │                        │
       └────────────────────────┼────────────────────────┘
                                │
                         ┌──────┴──────┐
                         │ Shared Git  │
                         │ Repository  │
                         └─────────────┘
```

### Conflict Avoidance

1. **Separate worktrees**: Each task in its own directory
2. **Separate branches**: No branch sharing
3. **Avoid shared files**: Tasks should modify distinct areas
4. **Regular rebase**: `git fetch && git rebase origin/main`

## Memory Management

### Context Rotation

Long-running loops can accumulate substantial context:

```python
# Orchestrator spawns Task Agents with fresh context
spawn_subagent(
    type="implementation",
    fresh_context=True,  # No history bloat
    memory_handoff={     # Essential data only
        'task': task.to_dict(),
        'worktree': worktree_path,
        'iteration': current_iteration
    }
)
```

### File-Based Communication

Instead of passing large contexts:

```
.worktrees/task-001/
├── .claude/
│   ├── context.json    # Current state
│   ├── progress.md     # Completed work
│   └── blockers.md     # Known issues
```

## Debugging

### Loop Status Verification

```bash
# View active processes (in another terminal)
claude process list

# View task logs
cat .plans/feature/.orchestrator/logs/task-001.log
```

### Manual Intervention

```bash
# Stop loop
# Use Ctrl+C or terminate the Claude session

# Continue manually
cd .worktrees/task-001
# ... apply fixes ...
git add . && git commit -m "fix: manual intervention"

# Restart loop with reduced iterations
# Spawn new Claude session with continuation prompt
```

### Common Issues

| Issue                   | Solution                                    |
| ----------------------- | ------------------------------------------- |
| Loop does not terminate | Verify completion promise, adjust prompt    |
| Excessive iterations    | Make prompt more specific                   |
| Incorrect completion    | Verify promise string exactly (whitespace!) |
| Memory overflow         | Decompose task, utilise context rotation    |
