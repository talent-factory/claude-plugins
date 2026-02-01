# Workflow: Task Implementation

Detailed workflow for implementing tasks (Filesystem or Linear).

## Overview

The workflow comprises 8 phases:

```
1. Task Identification
   ↓
2. Task Data Retrieval
   ↓
3. Worktree Creation
   ↓
4. Branch Creation (including Submodules)
   ↓
5. Task Status Update
   ↓
6. Implementation
   ↓
7. PR Creation
   ↓
8. Finalization and Cleanup
```

## Phase 1: Task Identification

### With Task ID Argument

**Filesystem**: `/implement-task task-001`
**Linear**: `/implement-task --linear PROJ-123`

**Workflow**:

1. Parse and validate task ID
2. Retrieve task (Filesystem: `.plans/*/tasks/`, Linear: MCP)
3. If multiple matches: Interactive selection

### Without Argument (Interactive)

**Filesystem**: `/implement-task`
**Linear**: `/implement-task --linear`

**Workflow**:

1. List available tasks
2. User selects task
3. Load task data

### Validation Checks

- Task exists
- Task is not already completed
- Task has valid status (pending/Backlog)
- Dependencies satisfied (Filesystem only)

## Phase 2: Task Data Retrieval

### Common Data Fields

| Field               | Filesystem               | Linear                  |
| ------------------- | ------------------------ | ----------------------- |
| Title               | From Markdown            | `issue.title`           |
| Description         | `## Description`         | `issue.description`     |
| Labels              | `**Labels**:`            | `issue.labels.nodes`    |
| Status              | `**Status**:`            | `issue.state.name`      |
| Acceptance Criteria | `## Acceptance Criteria` | Parsed from description |

### Data Structure

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

## Phase 3: Worktree Creation

> **IMPORTANT**: Git worktrees are used for parallel work on multiple tasks.

### Worktree Concept

Each task is processed in its own worktree:

- **Directory**: `.worktrees/task-<task-id>/`
- **Enables**: Parallel work on multiple tasks without branch switching
- **Isolation**: Each task has its own working copy

### Pre-Worktree Checks

```bash
# 1. Working directory clean?
git status --porcelain

# 2. Remote up-to-date?
git fetch origin

# 3. Worktree directory exists?
mkdir -p .worktrees

# 4. Worktree for this task does not already exist?
git worktree list | grep "task-<task-id>"
```

### Create Worktree

```bash
# Determine branch name
TASK_ID="task-001"  # or "proj-123" for Linear
DESCRIPTION="ui-toggle-component"
BRANCH_NAME="feature/${TASK_ID}-${DESCRIPTION}"

# Create worktree with new branch
git worktree add -b "$BRANCH_NAME" ".worktrees/task-${TASK_ID}" origin/main

# Switch to worktree
cd ".worktrees/task-${TASK_ID}"
```

## Phase 4: Branch Creation (including Submodules)

### Branch Naming

**Standardized format for all providers**:

```
feature/<ISSUE-ID>-<description>
```

| Provider   | Example                                |
| ---------- | -------------------------------------- |
| Filesystem | `feature/task-001-ui-toggle-component` |
| Linear     | `feature/proj-123-user-authentication` |

### Submodule Handling

> **For projects with submodules**: These must also be checked out to their own branches.

```bash
# 1. Check if submodules exist
git submodule status

# 2. If present: Initialize submodules
git submodule update --init --recursive

# 3. For each submodule: Create branch
git submodule foreach --recursive '
  echo "Creating branch in submodule: $name"
  git fetch origin
  git checkout -b "feature/<task-id>-<description>" origin/main
'
```

### Submodule Validation

```bash
# Verify all submodules are on the correct branch
git submodule foreach --recursive 'git branch --show-current'
```

## Phase 5: Task Status Update (CRITICAL)

> **IMPORTANT**: The status update must occur **BEFORE** switching to the worktree and must be committed **in the main branch**. This is essential for parallel work - other developers must be able to see that the task is already in progress.

### Filesystem

> **MANDATORY**: These steps prevent two developers from working on the same task.

#### Step 1: Remain in the Main Directory

```bash
# DO NOT switch to the worktree
# We are still in the main directory on main/develop
pwd  # should be <project-root>, NOT .worktrees/...
git branch --show-current  # should be main or develop
```

#### Step 2: Update the Task File

```markdown
# Before

- **Status**: pending
- **Updated**: 2024-11-15

# After

- **Status**: in_progress
- **Updated**: 2024-11-18
```

#### Step 3: Update STATUS.md

The STATUS.md in the plan directory must also be updated:

```markdown
## Progress Overview

- **In Progress**: 1 (10%) ← increased from 0
- **Pending**: 9 (90%) ← reduced from 10

## Tasks by Status

### In Progress

- task-001: UI Toggle (3 SP) ← add here

### Pending

<!-- remove task-001 from here -->
```

#### Step 4: Commit and Push Changes

```bash
# Stage changes
git add .plans/<feature-name>/tasks/task-001-*.md
git add .plans/<feature-name>/STATUS.md

# Commit
git commit -m "🔄 chore: Start task-001 implementation"

# PUSH TO REMOTE (so others can see it)
git push origin main  # or develop
```

#### Step 5: Only Now Switch to Worktree

```bash
cd ".worktrees/task-001"
# Implementation may now begin
```

#### Filesystem Checklist

- Work in main branch (not worktree)
- Task file: `pending` → `in_progress`
- Task file: `Updated` date updated
- STATUS.md: Task moved to "In Progress"
- STATUS.md: Progress overview updated
- Changes committed
- Changes pushed to remote
- Only then switch to worktree

### Linear

Via MCP: `linear_update_issue_state()` → "In Progress"

Linear stores status centrally, making it automatically visible to all team members.

**Optional Comment**:

```markdown
Implementation started in worktree: `.worktrees/task-proj-123/`
Branch: `feature/proj-123-...`
```

## Phase 6: Implementation

### Strategy

1. **Analyze task description** - Identify affected files
2. **Use acceptance criteria as checklist** - Utilize TodoWrite
3. **Implement code changes** - Based on description
4. **Write tests** - Unit/Integration tests

### Label to Commit Type Mapping

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

### Atomic Commits

```bash
# Commit 1: Feature
git commit -m "✨ feat: Add ThemeToggle component"

# Commit 2: Tests
git commit -m "🧪 test: Add ThemeToggle tests"
```

## Phase 7: PR Creation

### PR Body Template

```markdown
## Task: [ID] - [Title]

**Description**:
<Task description>

**Changes**:

- <Change 1>
- <Change 2>

**Test Plan**:

- [x] <Acceptance criterion 1>
- [x] <Acceptance criterion 2>

**Status**: In Progress → Completed/In Review
```

### Create PR

```bash
# From within the worktree
cd .worktrees/task-<task-id>
git push -u origin <branch-name>
gh pr create --title "[ID]: [Title]" --body "..."
```

## Phase 8: Finalization and Cleanup

### Task Status Update

#### Filesystem

1. Task status → `completed`
2. Update STATUS.md
3. Commit: `✅ chore: Mark task-001 as completed`

#### Linear

1. Issue status → `In Review` or `Done`
2. Optional: Add PR link as comment

### Worktree Cleanup (After PR Merge)

After successful merge, the worktree may be removed:

```bash
# From the main repository (not from within the worktree)
cd <project-root>

# 1. Remove the worktree
git worktree remove .worktrees/task-<task-id>

# 2. Delete the local branch (if desired)
git branch -d feature/<task-id>-<description>

# 3. For submodules: Delete branches there as well
git submodule foreach --recursive '
  git checkout main
  git branch -d "feature/<task-id>-<description>" 2>/dev/null || true
'
```

### Worktree Overview

```bash
# Display all active worktrees
git worktree list

# Clean up orphaned worktrees
git worktree prune
```

## See Also

- [filesystem.md](./filesystem.md) - Filesystem-specific details
- [linear.md](./linear.md) - Linear-specific details
- [best-practices.md](./best-practices.md) - Best practices
- [troubleshooting.md](./troubleshooting.md) - Problem resolution
