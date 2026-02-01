---
description: Implement task with worktree, branch creation, and PR (Filesystem or Linear)
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

Automated task implementation: Create worktree, create branch (including submodules), implement, and create pull request.

## Overview

This command orchestrates the complete workflow from task to pull request:

1. **Select Task** - From filesystem or Linear (via `--linear` flag)
2. **Create Worktree** - In `.worktrees/task-<task-id>/` for parallel work
3. **Create Branch** - In main repository and all submodules
4. **Prepare Draft PR** - Early PR creation for visibility and CI/CD
5. **Update Status** - Set task to "In Progress"
6. **Implementation** - Code changes based on task description
7. **Finalize PR** - Release draft PR for review
8. **Finalization** - Set task status to "Completed", update tracking

## Usage

```bash
# Filesystem-based (default)
/implement-task              # Interactive selection
/implement-task task-001     # With task ID
/implement-task --plan dark-mode task-003  # With plan context

# Linear-based
/implement-task --linear           # Interactive selection
/implement-task --linear PROJ-123  # With issue ID
```

## Provider Selection

### Filesystem (Default)

**When to use**: Tasks were created via `/create-plan` and reside in `.plans/*/tasks/`.

**Expected Structure**:

```text
.plans/[feature-name]/
├── EPIC.md
├── STATUS.md
└── tasks/
    ├── task-001-*.md
    ├── task-002-*.md
    └── ...
```

### Linear (`--linear`)

**When to use**: Tasks are managed in Linear.

**Prerequisite**: Linear MCP Server must be configured.

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

## Common Workflow

### 1. Task Identification

**With Argument**: Validate and retrieve task ID
**Without Argument**: List available tasks, user selects interactively

### 2. Read Task Data

Extract the following information:

- **Title and Description** - For branch name and context
- **Labels/Tags** - For commit type determination
- **Status** - Must be "pending" / "Backlog"
- **Acceptance Criteria** - As test plan checklist
- **Dependencies** - Verify before starting (filesystem only)

### 3. Worktree and Branch Creation

> **IMPORTANT**: Git worktrees are used for parallel work on multiple tasks!

#### Worktree Concept

Each task is processed in its own worktree:

- **Directory**: `.worktrees/task-<task-id>/`
- **Enables**: Parallel work on multiple tasks without branch switching
- **Isolated**: Each task has its own working copy

#### Workflow

```bash
# 1. Preparations in main repository
git fetch origin
git status  # Must be clean

# 2. Create worktree directory (if not present)
mkdir -p .worktrees

# 3. Determine branch name (based on issue type/labels)
# Labels → Branch prefix mapping:
# - bug, fix → bugfix/<task-id>-<description>
# - feature, enhancement → feature/<task-id>-<description>
# - docs, documentation → docs/<task-id>-<description>
# - refactor → refactor/<task-id>-<description>
# - performance → perf/<task-id>-<description>
# - test → test/<task-id>-<description>
# Default: feature/<task-id>-<description>
BRANCH_NAME="<type>/<task-id>-<description>"

# 4. Create worktree with new branch
git worktree add -b "$BRANCH_NAME" ".worktrees/task-<task-id>" origin/main

# 5. Switch to worktree
cd ".worktrees/task-<task-id>"
```

#### Submodule Handling

> **For projects with submodules**: These must also be checked out to their own branches!

```bash
# 1. In worktree: Initialize submodules
cd ".worktrees/task-<task-id>"
git submodule update --init --recursive

# 2. For each submodule: Create branch (same type as main repo)
git submodule foreach --recursive '
  git fetch origin
  git checkout -b "<type>/<task-id>-<description>" origin/main
'
```

**Submodule Check**:

```bash
# Check if submodules are present
git submodule status
```

#### Branch Naming

**Format based on issue type/labels**:

```
<type>/<ISSUE-ID>-<description>
```

**Labels → Branch Prefix Mapping**:

- `bug`, `fix` → `bugfix/`
- `feature`, `enhancement` → `feature/`
- `docs`, `documentation` → `docs/`
- `refactor` → `refactor/`
- `performance` → `perf/`
- `test` → `test/`
- Default: `feature/`

| Type     | Filesystem                             | Linear                        |
| -------- | -------------------------------------- | ----------------------------- |
| Feature  | `feature/task-001-ui-toggle-component` | `feature/proj-123-user-auth`  |
| Bug      | `bugfix/task-002-login-crash`          | `bugfix/proj-124-api-error`   |
| Docs     | `docs/task-003-api-documentation`      | `docs/proj-125-readme-update` |
| Refactor | `refactor/task-004-auth-module`        | `refactor/proj-126-db-layer`  |

#### Pre-Worktree Checks

- Working directory is clean (git status)
- Remote is up-to-date (git fetch)
- `.worktrees/` exists or will be created
- Worktree does not already exist for this task ID

### 3b. Draft PR Preparation (MANDATORY)

> **IMPORTANT**: A draft PR is created immediately after branch creation!

The draft PR serves as:

- **Early Visibility**: Team sees that work is in progress
- **CI/CD Integration**: Automatic checks run from the start
- **Review Preparation**: Reviewers can provide early feedback
- **Task Linking**: PR is linked to task from the beginning

#### Draft PR Workflow

```bash
# 1. In worktree: Create initial commit (if needed)
cd ".worktrees/task-<task-id>"
git commit --allow-empty -m "wip: Start work on <task-id>"

# 2. Push branch
git push -u origin "$BRANCH_NAME"

# 3. Create draft PR via /git-workflow:create-pr
/git-workflow:create-pr --draft --target main
```

#### Alternative: Manual Draft PR with gh CLI

If `/git-workflow:create-pr` is not available:

```bash
# Create draft PR with GitHub CLI
gh pr create --draft \
  --title "WIP: [<task-id>] <Task-Title>" \
  --body "$(cat <<'EOF'
## Description

Implementation of Task <task-id>: <Task-Title>

## Status

**Work in Progress** - This PR is not yet ready for review.

## Task Reference

- **Task ID**: <task-id>
- **Provider**: Filesystem / Linear
- **Link**: [Task Details](<link-to-task>)

## Planned Changes

- [ ] <Acceptance criterion 1>
- [ ] <Acceptance criterion 2>
- [ ] <Acceptance criterion 3>

## Test Plan

- [ ] Unit Tests
- [ ] Integration Tests
- [ ] Manual Verification

---
*This draft PR was automatically created via `/implement-task`*
EOF
)"
```

#### Submodule Draft PRs

> **For projects with submodules**: Draft PRs are also created for submodules!

```bash
# For each submodule with changes: Create draft PR
git submodule foreach --recursive '
  # Only if branch can be pushed
  git push -u origin "<type>/<task-id>-<description>" 2>/dev/null && \
  gh pr create --draft \
    --title "WIP: [<task-id>] <Task-Title> (Submodule: $(basename $PWD))" \
    --body "Part of parent PR for <task-id>"
'
```

#### Draft PR Checklist

- Branch is pushed (`git push -u origin`)
- Draft PR is created (`gh pr create --draft`)
- PR title contains task ID and WIP marker
- PR body contains task reference and acceptance criteria
- Submodules have their own draft PRs (if affected)

### 4. Status Update (CRITICAL for Parallel Work)

> **IMPORTANT**: The status update must occur **in the main branch** so other developers see that the task is in progress! This prevents overlap during parallel work.

| Provider   | Transition                                         | Location              |
| ---------- | -------------------------------------------------- | --------------------- |
| Filesystem | `pending` → `in_progress` in task file + STATUS.md | **Main branch**       |
| Linear     | `Backlog` → `In Progress` via MCP                  | Remote (auto-visible) |

#### Filesystem Status Update Workflow

> **MANDATORY**: These steps MUST be executed before starting implementation!

```bash
# 1. Return to main directory (main branch)
cd <project-root>

# 2. Ensure we are on the main branch (main/develop)
git checkout main  # or develop, depending on project
git pull origin main
```

**Update Task File** (with Edit tool):

```python
# In task file: Change status
old_string = "- **Status**: pending"
new_string = "- **Status**: in_progress"

# Update Updated date
from datetime import date
today = date.today().isoformat()
# - **Updated**: <old-date> → - **Updated**: <today>
```

**Regenerate STATUS.md**:

The STATUS.md in the plan directory must also be updated:

- Expand "In Progress" section with the task
- Reduce "Pending" section accordingly
- Adjust progress overview (percentages)

**Commit Changes**:

```bash
# 3. Stage and commit changes
git add .plans/<feature-name>/tasks/task-<id>-*.md
git add .plans/<feature-name>/STATUS.md
git commit -m "chore: Start task-<id> implementation"

# 4. Push to remote (so others can see!)
git push origin main  # or develop
```

**Then switch to worktree**:

```bash
# 5. Switch to worktree for actual implementation
cd ".worktrees/task-<task-id>"
```

#### Filesystem Status Update Checklist

- Working in main branch (not worktree)
- Task file: `pending` → `in_progress`
- Task file: `Updated` date updated
- STATUS.md: Task moved under "In Progress"
- STATUS.md: Progress overview updated
- Changes committed: `chore: Start task-<id> implementation`
- Changes pushed to remote
- Only then switch to worktree

#### Linear Status Update

With Linear, the update is simpler since status is stored centrally:

```python
# Via MCP tool
linear_update_issue(
    issue_id="PROJ-123",
    state="In Progress"
)

# Optional: Add comment
linear_create_comment(
    issue_id="PROJ-123",
    body="Implementation started\n- Branch: `feature/proj-123-...`\n- Worktree: `.worktrees/task-proj-123/`"
)
```

### 5. Implementation

1. **Analyze Task Description** - Identify affected files
2. **Acceptance Criteria as Checklist** - Work through step by step
3. **Perform Code Changes** - Based on task description
4. **Write Tests** - Unit/integration tests for acceptance criteria

**Labels → Commit Type Mapping**:

- `bug`, `fix` → fix
- `feature`, `enhancement` → feat
- `docs`, `documentation` → docs
- `refactor` → refactor
- `performance` → perf
- `test` → test
- Default: feat

### 6. PR Creation

Create PR with task linking:

- Title: Task title
- Body: Description, changes, test plan
- Labels: Based on task labels

### 7. Finalization (MANDATORY)

> **IMPORTANT**: This step is NOT optional!

| Provider   | Actions                                      |
| ---------- | -------------------------------------------- |
| Filesystem | Task status → `completed`, update STATUS.md  |
| Linear     | Issue status → `In Review` or `Done` via MCP |

#### Worktree Cleanup (After PR Merge)

After successful merge, the worktree can be cleaned up:

```bash
# From main repository
git worktree remove .worktrees/task-<task-id>
git branch -d <type>/<task-id>-<description>  # local branch

# For submodules: Delete branches there too (if not merged)
```

## Error Handling

- **Task Not Found**: Validation, suggest alternatives
- **Worktree Already Exists**: Warning, option to switch to existing worktree
- **Branch Already Exists**: Warning, option to switch
- **Submodule Branch Conflict**: Offer interactive resolution
- **Dependencies Not Met** (FS): Display list, user decision
- **Linear MCP Not Available**: Error message with setup instructions

## Detailed Documentation

### General

- **[workflow.md](../references/implement-task/workflow.md)** - Detailed workflow with examples
- **[best-practices.md](../references/implement-task/best-practices.md)** - Branch naming, commits, PR design
- **[troubleshooting.md](../references/implement-task/troubleshooting.md)** - Common problems and solutions

### Provider-Specific

- **[filesystem.md](../references/implement-task/filesystem.md)** - Filesystem tasks, STATUS.md
- **[linear.md](../references/implement-task/linear.md)** - Linear MCP setup, API details

## See Also

- **[/project-management:create-plan](./create-plan.md)** - Project planning (Filesystem/Linear)
- **[/git-workflow:commit](../../git-workflow/commands/commit.md)** - Professional Git commits
- **[/git-workflow:create-pr](../../git-workflow/commands/create-pr.md)** - Pull request creation

---

**Arguments**: $ARGUMENTS
