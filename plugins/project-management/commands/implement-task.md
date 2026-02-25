---
description: Implement task with context analysis, agent routing, worktree workflow, quality gate, and PR (Filesystem or Linear)
argument-hint: "[task-ID] [--linear] [--skip-brainstorm] [--skip-quality-gate]"
allowed-tools:
  - Read
  - Write
  - Edit
  - TodoWrite
  - AskUserQuestion
  - Glob
  - Grep
  - Bash
  - Task
---

# Implement Task

Automated task implementation with intelligent plugin orchestration: Context analysis, agent-routed implementation, quality gate, and pull request creation.

## Overview

This command orchestrates the complete workflow from task to pull request, leveraging the full plugin ecosystem:

1. **Select Task** - From filesystem or Linear (via `--linear` flag)
2. **Read Task Data** - Extract title, description, labels, acceptance criteria
3. **Context Analysis** - Brainstorm and analyze codebase before implementation
4. **Agent & Plugin Resolution** - Automatically select optimal agents and plugins
5. **Create Worktree** - In `.worktrees/task-<task-id>/` for parallel work
6. **Prepare Draft PR** - Early PR creation for visibility and CI/CD
7. **Update Status** - Set task to "In Progress"
8. **Implementation** - Agent-routed code changes based on context analysis
9. **Quality Gate** - Automated code review, linting, and commit standardization
10. **Finalization** - Set task status to "Completed", finalize PR, update tracking

## Usage

```bash
# Filesystem-based (default)
/implement-task              # Interactive selection
/implement-task task-001     # With task ID
/implement-task --plan dark-mode task-003  # With plan context

# Linear-based
/implement-task --linear           # Interactive selection
/implement-task --linear PROJ-123  # With issue ID

# Skip optional phases
/implement-task task-001 --skip-brainstorm     # Skip context analysis
/implement-task task-001 --skip-quality-gate   # Skip quality gate
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
- **Labels/Tags** - For commit type determination and agent routing
- **Status** - Must be "pending" / "Backlog"
- **Acceptance Criteria** - As test plan checklist
- **Dependencies** - Verify before starting (filesystem only)
- **Agent Recommendation** - From task file (if available from `/create-plan`)

### 3. Context Analysis (Brainstorm)

> **PURPOSE**: Understand the codebase deeply before writing any code. This phase replaces ad-hoc exploration with systematic analysis.

#### Superpowers Integration (Recommended)

If the **Superpowers** plugin (`obra/superpowers`) is available, invoke it for Socratic brainstorming:

```bash
/superpowers:brainstorm
```

This initiates an interactive design session that:

- Refines the task requirements through targeted questions
- Explores edge cases and technological alternatives
- Captures constraints before implementation begins
- Presents a refined design for validation

**Prerequisite**: Superpowers plugin installed via:

```bash
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

#### Built-in Context Analysis (Fallback)

If Superpowers is not available, perform context analysis directly:

**Step 1: Technology Stack Detection**

```bash
# Detect project type and technology stack
# Check for: package.json, pom.xml, build.gradle.kts, requirements.txt,
#            Cargo.toml, go.mod, pyproject.toml, etc.
```

**Step 2: Affected Code Analysis**

From the task description and acceptance criteria, identify:

- Which files need modification (use Grep/Glob to locate)
- Which modules/packages are affected
- What existing patterns to follow
- Which interfaces/contracts must be maintained

**Step 3: Architecture Pattern Recognition**

Analyze the existing codebase for:

- Project structure (MVC, Hexagonal, Layered, etc.)
- Naming conventions
- Test patterns and frameworks
- Configuration approaches

**Step 4: Dependency Impact Assessment**

- Which other tasks/features does this change affect?
- Are there shared utilities or services that must remain stable?
- What are the integration points?

**Step 5: Implementation Strategy**

Create a structured implementation plan using TodoWrite:

```
TodoWrite:
  - [ ] Identify affected files and modules
  - [ ] Define implementation approach
  - [ ] Plan test strategy
  - [ ] Estimate scope of changes
```

**Details**: [context-analysis.md](../references/implement-task/context-analysis.md)

### 4. Agent & Plugin Resolution

> **PURPOSE**: Automatically select the optimal agents and plugins based on the context analysis results.

#### Agent Selection Logic

Based on technology stack, task labels, and agent recommendations from the task file:

| Detected Context | Resolved Agent | Plugin Source |
| --- | --- | --- |
| Java / Spring Boot | `@java-developer` | `development` plugin |
| Python / Django / FastAPI | `@python-expert` | `code-quality` plugin |
| React / TypeScript / Frontend | `@frontend-developer` | `code-quality` plugin |
| Documentation / Markdown | `@markdown-syntax-formatter` | `education` plugin |
| AI / LLM Integration | `@ai-engineer` | Agent mapping |
| Agent Development | `@agent-expert` | Agent mapping |
| Security-Critical Changes | `@code-reviewer` (proactive) | `code-quality` plugin |

#### Resolution Priority

1. **Explicit Agent Recommendation** from task file (highest priority)
2. **Technology Stack Detection** from context analysis
3. **Task Label Matching** (labels → agent mapping)
4. **Default**: Generalist implementation (no specific agent)

#### Plugin Dependency Resolution

Based on resolved context, prepare the following plugin integrations:

| Phase | Plugin / Command | Condition |
| --- | --- | --- |
| Brainstorm | `/superpowers:brainstorm` | If Superpowers available |
| Implementation | `@<resolved-agent>` | Based on agent resolution |
| Commits | `/git-workflow:commit` | Always |
| Quality Gate | `@code-reviewer` | Unless `--skip-quality-gate` |
| Linting (Python) | `/code-quality:ruff-check` | If Python project detected |
| PR Creation | `/git-workflow:create-pr` | Always |

**Details**: [agent-routing.md](../references/implement-task/agent-routing.md)

### 5. Worktree and Branch Creation

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

### 5b. Draft PR Preparation (MANDATORY)

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

### 6. Status Update (CRITICAL for Parallel Work)

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

### 7. Implementation (Agent-Routed)

> **ENHANCED**: Implementation is now guided by the resolved agent and informed by the context analysis.

#### Agent-Guided Implementation

If an agent was resolved in Phase 4, the implementation follows that agent's methodology:

**Java Development** (`@java-developer`):
- Spring Boot patterns, JPA repositories, service layer
- Gradle Kotlin DSL (NOT Maven!)
- JUnit 5 tests

**Python Development** (`@python-expert`):
- PEP 8 compliance, type hints
- pytest for testing
- asyncio patterns where applicable

**Frontend Development** (`@frontend-developer`):
- Component-based architecture
- TypeScript strict mode
- Testing with appropriate framework

**General Implementation** (no specific agent):
- Follow existing project patterns from context analysis
- Acceptance criteria as implementation guide

#### Implementation Steps

1. **Apply Context Analysis Results** - Use the implementation strategy from Phase 3
2. **Acceptance Criteria as Checklist** - Work through step by step via TodoWrite
3. **Perform Code Changes** - Following resolved agent's methodology
4. **Write Tests** - Unit/integration tests for each acceptance criterion
5. **Standardized Commits** - Use `/git-workflow:commit` for each logical change

**Labels → Commit Type Mapping**:

- `bug`, `fix` → fix
- `feature`, `enhancement` → feat
- `docs`, `documentation` → docs
- `refactor` → refactor
- `performance` → perf
- `test` → test
- Default: feat

### 8. Quality Gate

> **PURPOSE**: Ensure code quality before PR finalization. Skippable with `--skip-quality-gate`.

#### Step 1: Automated Code Review

Invoke the `@code-reviewer` agent on all changes:

```bash
# Review all changes against main
git diff main...HEAD
```

The code reviewer checks:

- **Fundamental Quality**: Readability, naming, no duplication
- **Security**: No exposed secrets, input validation, OWASP compliance
- **Robustness**: Error handling, resource management
- **Maintainability**: Modular code, test coverage
- **Performance**: Algorithm efficiency, query optimization

#### Step 2: Language-Specific Linting

Based on detected technology stack:

| Language | Linting Command | Plugin |
| --- | --- | --- |
| Python | `/code-quality:ruff-check` | `code-quality` |
| JavaScript/TypeScript | Project-specific (eslint, biome) | Via Bash |
| Java | Project-specific (checkstyle, spotbugs) | Via Bash |

#### Step 3: Acceptance Criteria Verification

Systematically verify each acceptance criterion:

```
For each acceptance criterion:
  1. Is it implemented?
  2. Is it tested?
  3. Does the test pass?
  → If any fails: Flag for attention before proceeding
```

#### Step 4: Commit Standardization

Use `/git-workflow:commit` for the final commit set:

- Ensure all commits follow Emoji Conventional Commits format
- Atomic commits: one logical change per commit
- Clear, descriptive messages

#### Quality Gate Checklist

- [ ] Code review completed (no critical issues)
- [ ] Language-specific linting passed
- [ ] All acceptance criteria verified
- [ ] Tests written and passing
- [ ] Commits follow project conventions

**Details**: [quality-gate.md](../references/implement-task/quality-gate.md)

### 9. PR Finalization

Finalize the draft PR for review:

- Update title: Remove "WIP:" prefix
- Update body: Add description of actual changes, test results
- Labels: Based on task labels
- Mark PR as ready: `gh pr ready`

### 10. Finalization (MANDATORY)

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

## Plugin Ecosystem Integration

### Required Plugins

| Plugin | Commands / Agents Used | Phase |
| --- | --- | --- |
| **git-workflow** | `/git-workflow:commit`, `/git-workflow:create-pr` | 5b, 7, 9 |

### Optional Plugins (Auto-Detected)

| Plugin | Commands / Agents Used | Condition |
| --- | --- | --- |
| **superpowers** (obra) | `/superpowers:brainstorm` | Phase 3, if installed |
| **code-quality** | `@code-reviewer`, `@python-expert`, `@frontend-developer`, `/ruff-check` | Phase 4, 7, 8 |
| **development** | `@java-developer` | Phase 7, if Java detected |
| **education** | `@markdown-syntax-formatter` | Phase 7, if docs task |

### Plugin Availability Check

If an optional plugin is not available, the workflow continues gracefully:

- **Superpowers not installed**: Built-in context analysis (Phase 3 fallback)
- **Code-quality not installed**: Quality gate uses basic diff review
- **Development not installed**: General implementation without Java agent

## Error Handling

- **Task Not Found**: Validation, suggest alternatives
- **Worktree Already Exists**: Warning, option to switch to existing worktree
- **Branch Already Exists**: Warning, option to switch
- **Submodule Branch Conflict**: Offer interactive resolution
- **Dependencies Not Met** (FS): Display list, user decision
- **Linear MCP Not Available**: Error message with setup instructions
- **Plugin Not Available**: Graceful fallback, inform user
- **Quality Gate Failures**: Report issues, let user decide to proceed or fix

## Detailed Documentation

### General

- **[workflow.md](../references/implement-task/workflow.md)** - Detailed workflow with examples
- **[context-analysis.md](../references/implement-task/context-analysis.md)** - Brainstorm and context analysis guide
- **[agent-routing.md](../references/implement-task/agent-routing.md)** - Agent selection logic and mapping
- **[quality-gate.md](../references/implement-task/quality-gate.md)** - Quality gate checks and configuration
- **[best-practices.md](../references/implement-task/best-practices.md)** - Branch naming, commits, PR design
- **[troubleshooting.md](../references/implement-task/troubleshooting.md)** - Common problems and solutions

### Provider-Specific

- **[filesystem.md](../references/implement-task/filesystem.md)** - Filesystem tasks, STATUS.md
- **[linear.md](../references/implement-task/linear.md)** - Linear MCP setup, API details

## See Also

- **[/project-management:create-plan](./create-plan.md)** - Project planning (Filesystem/Linear)
- **[/git-workflow:commit](../../git-workflow/commands/commit.md)** - Professional Git commits
- **[/git-workflow:create-pr](../../git-workflow/commands/create-pr.md)** - Pull request creation
- **[/superpowers:brainstorm](https://github.com/obra/superpowers)** - Socratic brainstorming (Superpowers plugin)
- **[/code-quality:ruff-check](../../code-quality/commands/ruff-check.md)** - Python linting

---

**Arguments**: $ARGUMENTS
