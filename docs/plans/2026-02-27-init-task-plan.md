# `init-task` Command Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create the `/project-management:init-task` command for single-task creation with duplicate detection, ATOMIC validation, and mandatory Definition of Done.

**Architecture:** Command + Reference Files pattern (matching `implement-task`). Main command file orchestrates a 6-phase workflow, with three reference files providing reusable templates, duplicate detection logic, and validation rules. Supports both filesystem and Linear providers.

**Tech Stack:** Markdown command files with YAML frontmatter (Claude Code plugin system). No build/compile step — validation via `/core:check-commands`.

**Design Document:** `docs/plans/2026-02-27-init-task-design.md`

---

### Task 1: Create Task Template Reference File

**Files:**
- Create: `plugins/project-management/references/init-task/task-template.md`

**Step 1: Create the reference directory**

Run: `mkdir -p plugins/project-management/references/init-task`
Expected: Directory created without error

**Step 2: Write the task-template.md file**

Create `plugins/project-management/references/init-task/task-template.md` with the following complete content:

````markdown
# Task Template Reference

Standardized task structure for tasks created by `/project-management:init-task`. This template extends the existing task format from `/project-management:create-plan` with a mandatory Definition of Done section and additional metadata fields.

## Compatibility

This template is fully backward-compatible with `/project-management:implement-task`. The additional fields (`Type`, `Plan`, `Definition of Done`) are additive — `implement-task` consumes all existing sections without modification.

## Complete Template

```markdown
# Task-NNN: [Task-Title]

## Metadata

- **ID**: task-NNN
- **Status**: pending
- **Priority**: must | should | could
- **Type**: feature | bug | documentation | refactor | testing
- **Estimate**: [N] Story Points
- **Labels**: [label1, label2, ...]
- **Assignee**: [agent-name]
- **Created**: YYYY-MM-DD
- **Updated**: YYYY-MM-DD
- **Plan**: [plan-name] or standalone

## Description

[Detailed description of the task]

**User Story**: As a [Persona], I want to [Action] so that [Benefit].

## Acceptance Criteria

- [ ] Criterion 1 (testable, measurable)
- [ ] Criterion 2
- [ ] Criterion 3

## Definition of Done

- [ ] All acceptance criteria verified
- [ ] Code reviewed and approved
- [ ] Tests written and passing
- [ ] Documentation updated (if applicable)
- [ ] [Custom DoD items specific to this task]

## Dependencies

- **Requires**: [task-XXX or None]
- **Blocks**: [task-YYY or None]

## Agent Recommendation

**Recommended Agent**: `[agent-name]`
**Rationale**: [Why this agent is recommended]
```

## Field Descriptions

### Metadata Fields

| Field | Required | Values | Description |
|-------|----------|--------|-------------|
| ID | Yes | `task-NNN` | Sequential ID within the plan or adhoc context |
| Status | Yes | `pending` | Always `pending` on creation |
| Priority | Yes | `must`, `should`, `could` | MoSCoW priority level |
| Type | Yes | `feature`, `bug`, `documentation`, `refactor`, `testing` | Determines branch prefix and commit type |
| Estimate | Yes | `1`, `2`, `3`, `5`, `8` | Fibonacci story points |
| Labels | No | Comma-separated list | Categorization tags |
| Assignee | No | Agent name | Recommended agent for implementation |
| Created | Yes | `YYYY-MM-DD` | Auto-populated on creation |
| Updated | Yes | `YYYY-MM-DD` | Auto-populated on creation, updated on changes |
| Plan | Yes | Plan name or `standalone` | Parent plan context |

### Type to Branch Prefix Mapping

| Type | Branch Prefix | Commit Prefix |
|------|---------------|---------------|
| feature | `feature/` | `feat` |
| bug | `bugfix/` | `fix` |
| documentation | `docs/` | `docs` |
| refactor | `refactor/` | `refactor` |
| testing | `test/` | `test` |

### Definition of Done Defaults

Every task includes these standard DoD items by default. Custom items are appended during task creation:

1. **All acceptance criteria verified** — Each criterion has been implemented and tested
2. **Code reviewed and approved** — At least one code review completed
3. **Tests written and passing** — Unit and/or integration tests cover the changes
4. **Documentation updated** — Relevant documentation reflects the changes (if applicable)

### Agent Recommendation Mapping

Based on the task type and labels, suggest an appropriate agent:

| Context | Agent | Plugin |
|---------|-------|--------|
| Java / Spring Boot | `@java-developer` | development |
| Python / Django / FastAPI | `@python-expert` | code-quality |
| React / TypeScript / Frontend | `@frontend-developer` | code-quality |
| Documentation / Markdown | `@markdown-syntax-formatter` | education |

## Linear Mapping

When creating tasks in Linear (`--linear`), the template fields map as follows:

| Template Field | Linear Field | Notes |
|----------------|--------------|-------|
| Title | `issue.title` | Direct mapping |
| Description + User Story | `issue.description` | Combined in description body |
| Priority | `issue.priority` | `must` → Urgent, `should` → High, `could` → Medium |
| Type | Label | Applied as label |
| Estimate | `issue.estimate` | Direct story point mapping |
| Labels | `issue.labels` | Applied as Linear labels |
| Acceptance Criteria | Part of `issue.description` | Rendered as checklist in description |
| Definition of Done | Part of `issue.description` | Rendered as checklist in description |
| Dependencies | `issue.relations` | Created via `create_issue_relation` |
| Agent Recommendation | Part of `issue.description` | Included in description body |
````

**Step 3: Commit**

```bash
git add plugins/project-management/references/init-task/task-template.md
git commit -m "📚 docs(project-management): Add task template reference for init-task"
```

---

### Task 2: Create Duplicate Detection Reference File

**Files:**
- Create: `plugins/project-management/references/init-task/duplicate-detection.md`

**Step 1: Write the duplicate-detection.md file**

Create `plugins/project-management/references/init-task/duplicate-detection.md` with the following complete content:

````markdown
# Duplicate Detection Reference

Strategy and procedures for preventing duplicate task creation across filesystem and Linear providers.

## Detection Sources

### Filesystem

Scan all task files in `.plans/*/tasks/` directories:

```bash
# Glob pattern
.plans/*/tasks/task-*.md
```

For each task file, extract:
- **Title**: From the `# Task-NNN: [Title]` heading
- **Description**: From the `## Description` section
- **Status**: From the `**Status**:` metadata field (skip completed tasks)

### Linear

Query existing issues via MCP tools:

```
mcp__linear__list_issues(teamId, first: 50)
```

For each issue, extract:
- **Title**: `issue.title`
- **Description**: `issue.description`
- **Status**: `issue.state.name` (skip done issues)

## Matching Algorithm

### Title-Based Keyword Overlap

1. **Normalize** both titles: lowercase, remove stop words, split into keyword set
2. **Compute overlap**: `|intersection| / |union|` (Jaccard similarity)
3. **Threshold**: Present matches with similarity > 50%

### Stop Words

Common words excluded from comparison:
`the`, `a`, `an`, `is`, `are`, `was`, `were`, `be`, `been`, `being`, `have`, `has`, `had`, `do`, `does`, `did`, `will`, `would`, `shall`, `should`, `may`, `might`, `must`, `can`, `could`, `to`, `of`, `in`, `for`, `on`, `with`, `at`, `by`, `from`, `as`, `into`, `through`, `during`, `before`, `after`, `and`, `or`, `but`, `not`, `no`, `nor`, `so`, `yet`, `both`, `either`, `neither`, `each`, `every`, `all`, `any`, `few`, `more`, `most`, `other`, `some`, `such`, `only`, `own`, `same`, `than`, `too`, `very`, `just`, `because`, `if`, `when`, `while`, `where`, `how`, `what`, `which`, `who`, `whom`, `this`, `that`, `these`, `those`, `it`, `its`, `implement`, `add`, `create`, `update`, `fix`, `task`

### Similarity Scoring Example

**New task**: "Fix authentication timeout bug"
**Existing task**: "Fix authentication session timeout"

1. Normalize: `{fix, authentication, timeout, bug}` vs `{fix, authentication, session, timeout}`
2. After stop word removal: `{authentication, timeout, bug}` vs `{authentication, session, timeout}`
3. Intersection: `{authentication, timeout}` = 2
4. Union: `{authentication, timeout, bug, session}` = 4
5. Similarity: 2/4 = **50%** → Matches threshold, present to user

## User Interaction

When potential duplicates are detected, present them using `AskUserQuestion`:

### Presentation Format

```
Potential duplicates found for "[New Task Title]":

1. task-003: "Fix authentication timeout" (.plans/auth-feature/tasks/)
   Similarity: 85%

2. PROJ-234: "Authentication session timeout bug" (Linear)
   Similarity: 60%
```

### Decision Options

| Option | Action |
|--------|--------|
| **Skip** | Abort task creation entirely |
| **Create anyway** | Proceed with creation despite overlap |
| **View details** | Display full content of the potential duplicate before deciding |

### No Duplicates Found

If no matches exceed the 50% threshold, proceed directly to task creation without user interaction.

## Cross-Provider Detection

When `--linear` is specified, check **both** providers:
1. Search filesystem tasks in `.plans/*/tasks/`
2. Search Linear issues via MCP

This ensures comprehensive coverage even when switching between providers.

When `--linear` is **not** specified, search only filesystem tasks (Linear MCP may not be available).
````

**Step 2: Commit**

```bash
git add plugins/project-management/references/init-task/duplicate-detection.md
git commit -m "📚 docs(project-management): Add duplicate detection reference for init-task"
```

---

### Task 3: Create Validation Rules Reference File

**Files:**
- Create: `plugins/project-management/references/init-task/validation-rules.md`

**Step 1: Write the validation-rules.md file**

Create `plugins/project-management/references/init-task/validation-rules.md` with the following complete content:

````markdown
# Validation Rules Reference

ATOMIC validation criteria and mandatory field requirements for task creation via `/project-management:init-task`.

## Mandatory Fields

Every task created by `init-task` must include all of the following:

| Field | Validation Rule | Error Message |
|-------|----------------|---------------|
| Title | Non-empty, max 120 characters | "Task title is required and must not exceed 120 characters." |
| Description | Non-empty, min 20 characters | "Task description must contain at least 20 characters." |
| Acceptance Criteria | At least 1 criterion | "At least one acceptance criterion is required." |
| Definition of Done | At least the 4 default items | "Definition of Done must include standard completion criteria." |
| Priority | One of: `must`, `should`, `could` | "Priority must be one of: must, should, could." |
| Type | One of: `feature`, `bug`, `documentation`, `refactor`, `testing` | "Type must be one of: feature, bug, documentation, refactor, testing." |
| Estimate | One of: `1`, `2`, `3`, `5`, `8` | "Story point estimate must be a Fibonacci value: 1, 2, 3, 5, or 8." |

## ATOMIC Validation

After collecting all task data, validate against the ATOMIC criteria before creation:

### A — Actionable

**Check**: Description is specific enough to begin implementation without additional questions.

**Indicators of failure**:
- Description contains only a title restatement
- No technical context or scope boundaries
- Vague language: "improve", "optimize", "enhance" without specific targets

**Prompt on failure**: "The task description may be too vague for immediate implementation. Consider adding specific scope boundaries or technical context."

### T — Testable

**Check**: At least one acceptance criterion exists and each criterion is verifiable.

**Indicators of failure**:
- No acceptance criteria defined
- Criteria use subjective language: "looks good", "works well", "is fast"
- Criteria lack measurable outcomes

**Prompt on failure**: "Acceptance criteria should be testable and measurable. Consider rephrasing subjective criteria into specific, verifiable conditions."

### O — Ownable

**Check**: Task scope is appropriate for a single developer or agent.

**Indicators of failure**:
- Description mentions multiple unrelated components
- More than 5 acceptance criteria (may indicate scope creep)
- Estimate exceeds 8 story points

**Prompt on failure**: "This task may be too large for a single assignee. Consider decomposing it into smaller, focused tasks."

### M — Measurable

**Check**: Story point estimate is provided and reasonable.

**Indicators of failure**:
- No estimate provided
- Estimate exceeds 8 (too large)

**Prompt on failure**: "Tasks exceeding 8 story points should be decomposed into smaller units."

### I — Independent

**Check**: Dependencies are explicitly documented.

**Indicators of failure**:
- Description references other tasks without declaring dependencies
- Implicit assumptions about system state

**Prompt on failure**: "This task appears to reference other work. Declare explicit dependencies in the Dependencies section."

### C — Complete

**Check**: Task contains all required sections and the Definition of Done is populated.

**Indicators of failure**:
- Missing required sections
- Definition of Done contains only defaults without task-specific items

**Prompt on failure**: "Consider adding task-specific items to the Definition of Done beyond the standard defaults."

## Validation Workflow

```
1. Check mandatory fields (hard requirements — block creation if missing)
   ↓
2. Run ATOMIC checks (soft requirements — warn and prompt for improvement)
   ↓
3. If all mandatory fields present:
   → If ATOMIC warnings exist: Present warnings, ask user to improve or proceed
   → If no warnings: Proceed to duplicate detection
```

## Definition of Done Enforcement

### Default Items (Always Included)

These four items are automatically added to every task and cannot be removed:

1. `- [ ] All acceptance criteria verified`
2. `- [ ] Code reviewed and approved`
3. `- [ ] Tests written and passing`
4. `- [ ] Documentation updated (if applicable)`

### Custom Items

The interactive wizard prompts the user to add task-specific DoD items. Examples by task type:

| Type | Example Custom DoD Items |
|------|-------------------------|
| feature | "API endpoint documented in OpenAPI spec", "Feature flag configured" |
| bug | "Regression test added", "Root cause documented" |
| documentation | "Screenshots updated", "Links verified" |
| refactor | "No public API changes", "Performance benchmarks unchanged" |
| testing | "Coverage threshold met", "CI pipeline green" |

### Inline Mode Handling

When using inline arguments (no wizard), the four default DoD items are included automatically. Users can add custom items by editing the task file after creation.
````

**Step 2: Commit**

```bash
git add plugins/project-management/references/init-task/validation-rules.md
git commit -m "📚 docs(project-management): Add validation rules reference for init-task"
```

---

### Task 4: Create the Main Command File

**Files:**
- Create: `plugins/project-management/commands/init-task.md`

**Step 1: Write the init-task.md command file**

Create `plugins/project-management/commands/init-task.md` with the following complete content:

````markdown
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
````

**Step 2: Commit**

```bash
git add plugins/project-management/commands/init-task.md
git commit -m "✨ feat(project-management): Add init-task command for single-task creation"
```

---

### Task 5: Validate Command Structure

**Files:**
- Verify: `plugins/project-management/commands/init-task.md`
- Verify: `plugins/project-management/references/init-task/*.md`

**Step 1: Run command validation**

Run: `/core:check-commands`
Expected: `init-task.md` passes all validation checks (frontmatter present, description field, argument-hint field, allowed-tools array)

**Step 2: Verify reference file structure**

Run: `ls -la plugins/project-management/references/init-task/`
Expected: Three files listed: `task-template.md`, `duplicate-detection.md`, `validation-rules.md`

**Step 3: Verify cross-references**

Check that all relative links in `init-task.md` resolve correctly:
- `../references/init-task/task-template.md` — exists
- `../references/init-task/duplicate-detection.md` — exists
- `../references/init-task/validation-rules.md` — exists
- `./create-plan.md` — exists
- `./implement-task.md` — exists
- `./implement-epic.md` — exists
- `./create-prd.md` — exists

**Step 4: Fix any validation errors**

If `/core:check-commands` reports issues, resolve them before proceeding.

---

### Task 6: Update Plugin Metadata

**Files:**
- Modify: `plugins/project-management/.claude-plugin/plugin.json`
- Modify: `.claude-plugin/marketplace.json`

**Step 1: Update plugin.json version**

In `plugins/project-management/.claude-plugin/plugin.json`, change:

```json
"version": "2.5.0"
```

to:

```json
"version": "2.6.0"
```

Update the description to mention init-task:

```json
"description": "Comprehensive project management with PRD generation, project planning, single-task initialization with duplicate detection and ATOMIC validation, intelligent task implementation with plugin orchestration (Superpowers brainstorm, agent routing, quality gate), autonomous EPIC automation, Linear integration, and git worktree workflow for agile development"
```

**Step 2: Update marketplace.json**

In `.claude-plugin/marketplace.json`, update the project-management entry:

Change `"version": "2.5.0"` to `"version": "2.6.0"`.

Update the description to match plugin.json.

**Step 3: Commit**

```bash
git add plugins/project-management/.claude-plugin/plugin.json .claude-plugin/marketplace.json
git commit -m "🔖 chore(project-management): Bump version to 2.6.0 for init-task command"
```

---

### Task 7: Update Documentation

**Files:**
- Modify: `plugins/project-management/README.md` (add init-task to command list)
- Modify: `CHANGELOG.md` (add version 2.6.0 entry)

**Step 1: Update README.md**

Add `/project-management:init-task` to the commands section of the project-management README, positioned between `create-plan` and `implement-task` in the command list. Include a brief description matching the command's description field.

**Step 2: Update CHANGELOG.md**

Add a new entry at the top of the changelog:

```markdown
## [2.6.0] - 2026-02-27

### Added
- **project-management**: New `/project-management:init-task` command for single-task creation with duplicate detection, ATOMIC validation, and mandatory Definition of Done
- **project-management**: Task template reference with extended metadata fields (Type, Plan, Definition of Done)
- **project-management**: Duplicate detection reference with cross-provider search (filesystem + Linear)
- **project-management**: Validation rules reference with ATOMIC criteria enforcement
```

**Step 3: Commit**

```bash
git add plugins/project-management/README.md CHANGELOG.md
git commit -m "📚 docs(project-management): Update README and CHANGELOG for init-task 2.6.0"
```

---

### Task 8: Final Validation and Summary

**Step 1: Run full validation suite**

Run: `/core:check-commands`
Run: `/core:check-agents`
Expected: All checks pass

**Step 2: Verify git log**

Run: `git log --oneline -8`
Expected: Clean commit history with all init-task commits visible

**Step 3: Summary**

Confirm that the following files were created/modified:

| Action | File |
|--------|------|
| Created | `plugins/project-management/commands/init-task.md` |
| Created | `plugins/project-management/references/init-task/task-template.md` |
| Created | `plugins/project-management/references/init-task/duplicate-detection.md` |
| Created | `plugins/project-management/references/init-task/validation-rules.md` |
| Modified | `plugins/project-management/.claude-plugin/plugin.json` |
| Modified | `.claude-plugin/marketplace.json` |
| Modified | `plugins/project-management/README.md` |
| Modified | `CHANGELOG.md` |
