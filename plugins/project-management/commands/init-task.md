---
description: Initialize a single task with duplicate detection, ATOMIC validation, and mandatory Definition of Done (Filesystem or Linear)
argument-hint: "[title] [--plan <name>] [--linear] [--standalone] [--type <type>] [--priority <p>] [--estimate <sp>]"
allowed-tools:
  - Read
  - Write
  - Edit
  - AskUserQuestion
  - Glob
  - Grep
  - Bash
  - Task
---

# Initialize Task

Create a single, well-structured task with duplicate prevention and quality validation. Supports both filesystem (`.plans/`) and Linear providers, with optional attachment to an existing plan.

## Overview

This command orchestrates a 6-phase workflow for guided task creation:

1. **Context Discovery** — Detect project environment, existing plans, and Linear configuration
2. **Duplicate Detection** — Search filesystem and Linear for potential duplicates
3. **Task Data Collection** — Interactive wizard or inline argument parsing
4. **ATOMIC Validation** — Verify task quality against ATOMIC criteria
5. **Task Creation** — Write task file (filesystem) or create issue (Linear)
6. **Status Integration** — Update STATUS.md or Linear project state

## Usage

```bash
# Interactive wizard (default)
/project-management:init-task

# With plan context
/project-management:init-task --plan dark-mode-toggle
/project-management:init-task --plan dark-mode-toggle --linear

# Quick inline creation
/project-management:init-task "Fix authentication timeout bug" --type bug --priority must
/project-management:init-task "Add user profile page" --plan user-management --type feature

# Linear provider
/project-management:init-task --linear
/project-management:init-task "Implement caching layer" --linear --priority should

# Standalone (no plan)
/project-management:init-task "Refactor database queries" --standalone
```

## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `[title]` | No | Interactive prompt | Task title (positional argument) |
| `--plan <name>` | No | Auto-detect or standalone | Attach to an existing plan in `.plans/` |
| `--linear` | No | Filesystem | Use Linear as the task provider |
| `--standalone` | No | false | Force standalone mode, skip plan detection |
| `--type <type>` | No | Interactive prompt | Task type: `feature`, `bug`, `documentation`, `refactor`, `testing` |
| `--priority <p>` | No | Interactive prompt | Priority: `must`, `should`, `could` |
| `--estimate <sp>` | No | Interactive prompt | Story points: `1`, `2`, `3`, `5`, `8` |

## Provider Selection

### Filesystem (Default)

**When to use**: Local project without Linear, rapid iteration, offline work.

**Output Location**:

- **Plan-attached**: `.plans/[plan-name]/tasks/task-NNN-[slug].md`
- **Standalone**: `.plans/adhoc/tasks/task-NNN-[slug].md`

### Linear (`--linear`)

**When to use**: Team collaboration, project tracking, integration with external tools.

**Prerequisite**: Linear MCP Server must be configured:

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

### Phase 1: Context Discovery

Detect the project environment to determine available options:

**Filesystem Detection**:

```bash
# Scan for existing plans
.plans/*/EPIC.md
.plans/*/STATUS.md
.plans/*/tasks/
```

**Linear Detection**: Verify Linear MCP server availability (when `--linear` is specified).

**Decision Logic**:

| Condition | Behavior |
|-----------|----------|
| `--plan <name>` provided | Validate plan exists, use it |
| `--standalone` provided | Skip plan detection, use `.plans/adhoc/` |
| `--linear` provided | Use Linear project selection |
| Plans found in `.plans/` | Present list, let user choose or select standalone |
| No plans found | Default to standalone (`.plans/adhoc/`) |

### Phase 2: Duplicate Detection

Before collecting task data (if title is provided inline) or after collecting the title (in wizard mode), search for potential duplicates:

**Filesystem Search**: Read all `task-*.md` files in `.plans/*/tasks/`, extract titles.

**Linear Search** (when `--linear` active): Query issues via `mcp__linear__list_issues()`.

**Matching**: Title-based keyword overlap with >50% similarity threshold.

**User Interaction**: Present potential duplicates via `AskUserQuestion` with options: Skip, Create anyway, View details.

**Details**: [duplicate-detection.md](../references/init-task/duplicate-detection.md)

### Phase 3: Task Data Collection

#### Interactive Wizard (Default)

When invoked without full inline arguments, guide the user through each field:

**Step 1**: Plan selection (if not specified via `--plan` or `--standalone`)

Use `AskUserQuestion` to present available plans:
- List detected plans from `.plans/*/`
- Include "Standalone (no plan)" option
- Include "Create new plan" option (defers to `/project-management:create-plan`)

**Step 2**: Task title

If not provided as positional argument, prompt for the task title.

**Step 3**: Task type

Use `AskUserQuestion` with options:
- Feature — New functionality or capability
- Bug — Defect correction or error resolution
- Documentation — Documentation creation or update
- Refactor — Code restructuring without behavior change
- Testing — Test creation or test infrastructure

**Step 4**: Description

Prompt for a detailed task description including context and scope.

**Step 5**: Acceptance criteria

Iteratively prompt for acceptance criteria:
- Ask for each criterion individually
- After each criterion, ask "Add another criterion?" (Yes/No)
- Minimum 1 criterion required

**Step 6**: Definition of Done

Present the four default DoD items and prompt for custom additions:

Default items (always included):
1. All acceptance criteria verified
2. Code reviewed and approved
3. Tests written and passing
4. Documentation updated (if applicable)

Prompt: "Add task-specific Definition of Done items? (e.g., 'Regression test added', 'API docs updated')"

**Step 7**: Priority

Use `AskUserQuestion` with options:
- Must — Critical for the current milestone
- Should — Important but not blocking
- Could — Desirable if time permits

**Step 8**: Story point estimate

Use `AskUserQuestion` with options:
- 1 SP — Trivial, under 2 hours
- 2 SP — Simple, 2-4 hours
- 3 SP — Standard, 4-8 hours
- 5 SP — Complex, 1-2 days
- 8 SP — Very complex, 2-3 days

**Step 9**: Dependencies (optional)

If plan-attached, prompt for dependency relationships:
- **Requires**: Tasks that must complete before this one
- **Blocks**: Tasks that depend on this one

**Step 10**: Agent recommendation (optional)

Based on task type and labels, suggest an appropriate agent. User may accept, change, or skip.

#### Inline Mode

When arguments are provided, skip the wizard for those fields. Missing mandatory fields trigger individual prompts.

### Phase 4: ATOMIC Validation

Validate the collected task data against the ATOMIC criteria:

| Criterion | Check | Severity |
|-----------|-------|----------|
| **A**ctionable | Description is specific and implementable | Warning |
| **T**estable | Acceptance criteria are verifiable | Warning |
| **O**wnable | Scope fits a single assignee (estimate ≤ 8 SP) | Warning |
| **M**easurable | Story points estimated | Hard requirement |
| **I**ndependent | Dependencies explicitly documented | Warning |
| **C**omplete | All mandatory sections populated, DoD present | Hard requirement |

**On hard requirement failure**: Block creation, prompt for correction.

**On warning**: Present warning, let user choose to improve or proceed.

**Details**: [validation-rules.md](../references/init-task/validation-rules.md)

### Phase 5: Task Creation

#### Filesystem

**Task ID Assignment**: Determine the next sequential ID:

```bash
# Scan existing task files in the target directory
.plans/[plan-name]/tasks/task-*.md
# If last file is task-003-*.md, next ID is task-004
```

**Filename**: `task-NNN-[slug].md` where `[slug]` is the title in kebab-case.

**Adhoc Plan Bootstrap**: If standalone and `.plans/adhoc/` does not exist:
1. Create `.plans/adhoc/tasks/` directory
2. Create `.plans/adhoc/STATUS.md` with initial structure

**Write Task File**: Populate the template from [task-template.md](../references/init-task/task-template.md) with collected data and write to the target directory.

#### Linear

**Create Issue**: Use `mcp__linear__save_issue()` with:
- Title from task data
- Description composed from: Description + Acceptance Criteria + Definition of Done + Agent Recommendation
- Priority mapping: `must` → Urgent, `should` → High, `could` → Medium
- Estimate from story points
- Labels from type and custom labels

**Link Dependencies**: If dependencies specified, use `mcp__linear__create_issue_relation()`.

### Phase 6: Status Integration

#### Filesystem

**Plan-Attached**: Update the plan's `STATUS.md`:
- Increment "Total Tasks" count
- Add task to "Pending" section
- Update progress percentages
- Recalculate story point totals

**Standalone (Adhoc)**: Update `.plans/adhoc/STATUS.md` with the same structure.

#### Linear

No additional status integration required — Linear tracks state automatically.

#### Confirmation

Display a summary of the created task:

```
Task created successfully:

  ID:       task-004
  Title:    Fix authentication timeout bug
  Type:     bug
  Priority: must
  Estimate: 3 SP
  Plan:     auth-feature
  Location: .plans/auth-feature/tasks/task-004-fix-authentication-timeout-bug.md

Next steps:
  → /project-management:implement-task task-004
  → /project-management:implement-task --plan auth-feature task-004
```

## Template

Tasks follow the extended template format with mandatory Definition of Done:

**Details**: [task-template.md](../references/init-task/task-template.md)

## Error Handling

| Error | Response |
|-------|----------|
| Plan not found | List available plans, prompt for selection |
| Linear MCP unavailable | Display setup instructions, suggest filesystem fallback |
| Duplicate detected | Interactive confirmation (Skip / Create anyway / View details) |
| ATOMIC validation failure (hard) | Block creation, prompt for correction |
| ATOMIC validation failure (soft) | Warning with option to improve or proceed |
| Directory creation fails | Report error with path details |
| Task ID conflict | Auto-increment to next available ID |

## Detailed Documentation

- **[task-template.md](../references/init-task/task-template.md)** — Standardized task structure and field descriptions
- **[duplicate-detection.md](../references/init-task/duplicate-detection.md)** — Search strategy and matching algorithm
- **[validation-rules.md](../references/init-task/validation-rules.md)** — ATOMIC validation and DoD enforcement

## See Also

- **[/project-management:create-plan](./create-plan.md)** — Bulk task creation from PRD
- **[/project-management:implement-task](./implement-task.md)** — Task implementation workflow
- **[/project-management:implement-epic](./implement-epic.md)** — Autonomous parallel EPIC implementation
- **[/project-management:create-prd](./create-prd.md)** — Product Requirements Document creation

---

**Arguments**: $ARGUMENTS
