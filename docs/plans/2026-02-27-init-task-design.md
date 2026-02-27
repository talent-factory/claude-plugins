# Design Document: `init-task` Command

**Date**: 2026-02-27
**Plugin**: project-management
**Status**: Approved
**Author**: Daniel Senften / Claude

## Problem Statement

The current project-management workflow requires a Product Requirements Document (PRD) and a full plan (`create-plan`) before any task can be created. There is no mechanism for:

- Creating a **single ad-hoc task** discovered during development (e.g., a bug or unexpected edge case)
- **Adding a task to an existing plan** mid-project without rebuilding the entire plan
- Creating a task **outside of a PRD context** entirely

This gap forces users into heavyweight processes even for lightweight task capture, resulting in either process abandonment or informal task tracking.

## Solution Overview

A new command, `/project-management:init-task`, that provides guided, interactive task creation with duplicate prevention, ATOMIC validation, and mandatory Definition of Done. It supports both filesystem and Linear providers, and can operate plan-attached or standalone.

## Architecture Decision

**Approach**: Command + Reference Files (Approach B)

The main command file orchestrates the workflow while reference files provide reusable templates and detailed logic. This follows the established pattern used by `implement-task` and other project-management commands.

```
plugins/project-management/
├── commands/
│   └── init-task.md                          # Main command (workflow orchestration)
└── references/
    └── init-task/
        ├── task-template.md                   # Standardized task structure template
        ├── duplicate-detection.md             # Search & matching logic
        └── validation-rules.md               # ATOMIC validation & DoD requirements
```

## Workflow Design

### 6-Phase Pipeline

```
Phase 1: Context Discovery
  → Detect project environment (existing plans, Linear configuration)
  → Identify available task sources

Phase 2: Duplicate Detection
  → Search filesystem (.plans/**/tasks/*.md)
  → Search Linear issues (if configured)
  → Present potential duplicates for user decision (interactive confirmation)

Phase 3: Task Data Collection
  → Interactive wizard (default) OR parse inline arguments
  → Mandatory fields: Title, Description, Acceptance Criteria, Definition of Done
  → Optional fields: Priority, Labels, Story Points, Dependencies, Agent Recommendation

Phase 4: ATOMIC Validation
  → Verify task meets ATOMIC criteria:
    - Actionable: Immediately implementable without further clarification
    - Testable: Clear acceptance criteria defined
    - Ownable: Assignable to one person/agent
    - Measurable: Story points estimated
    - Independent: Minimally dependent on other tasks
    - Complete: Self-contained
  → Flag issues for correction before creation

Phase 5: Task Creation
  → Filesystem: Write task-NNN-slug.md to .plans/[plan]/tasks/ or .plans/adhoc/tasks/
  → Linear: Create issue via MCP tools with proper hierarchy

Phase 6: Status Integration
  → Update STATUS.md if plan-attached (filesystem)
  → Confirm creation and display next steps
```

### Workflow Position

```
create-plan (bulk) → [existing tasks] → init-task (single) → implement-task (execute)
                                              ↑
                                    standalone (no plan) also supported
```

## Command Interface

### Usage Examples

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

### Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `[title]` | No | Interactive prompt | Task title (positional) |
| `--plan <name>` | No | Auto-detect or standalone | Attach to existing plan |
| `--linear` | No | Filesystem | Use Linear as provider |
| `--standalone` | No | false | Force standalone (skip plan detection) |
| `--type <type>` | No | feature | Task type (feature/bug/documentation/refactor/testing) |
| `--priority <p>` | No | Interactive prompt | Priority (must/should/could) |
| `--estimate <sp>` | No | Interactive prompt | Story points (1/2/3/5/8) |

### Interactive Wizard Flow

1. Scan for existing `.plans/` directories and present choice: attach to plan or standalone
2. Prompt for task title
3. Prompt for task type (multiple choice: feature, bug, documentation, refactor, testing)
4. Prompt for description
5. Prompt for acceptance criteria (iterative: "Add another criterion?")
6. Prompt for Definition of Done (pre-filled defaults + custom items)
7. Prompt for priority (must/should/could)
8. Prompt for story point estimate (1/2/3/5/8)
9. Execute duplicate detection and present results if any matches found
10. Confirm and create

## Task Template (Extended)

The existing task template is extended with a mandatory **Definition of Done** section:

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

### Changes from Existing Template

| Field | Change | Rationale |
|-------|--------|-----------|
| `Definition of Done` | **New section (mandatory)** | Ensures explicit completion criteria beyond acceptance criteria |
| `Type` in Metadata | **New field** | Enables categorization for agent routing and branch naming |
| `Plan` in Metadata | **New field** | Links task to parent plan or marks as standalone |

### Backward Compatibility

The extended template is fully compatible with `implement-task` — the additional fields (`Type`, `Plan`, `Definition of Done`) are additive. `implement-task` reads `Metadata`, `Description`, `Acceptance Criteria`, `Dependencies`, and `Agent Recommendation`, all of which remain unchanged.

## File Structure

### Standalone Task Storage

When no plan context exists, tasks are stored in an auto-created `adhoc` plan:

```
.plans/
└── adhoc/
    ├── STATUS.md                             # Tracks standalone tasks
    └── tasks/
        ├── task-001-fix-auth-timeout.md
        └── task-002-refactor-queries.md
```

The `adhoc` plan uses the standard STATUS.md format but omits EPIC.md (no PRD context required).

### Task ID Assignment

- **Plan-attached**: Next sequential ID within the plan (e.g., if task-003 exists, next is task-004)
- **Standalone (adhoc)**: Next sequential ID within `.plans/adhoc/tasks/`
- **Linear**: ID assigned by Linear (e.g., PROJ-456)

## Duplicate Detection Strategy

### Sources

1. **Filesystem**: Read all `task-*.md` files in `.plans/*/tasks/`, extract titles and descriptions
2. **Linear**: Use `mcp__linear__list_issues()` with title keyword matching (when `--linear` flag active)

### Matching Algorithm

- Title-based keyword overlap with simple similarity scoring
- Threshold: Present matches with >50% keyword overlap
- User decision options: Skip creation / Create anyway / View existing task details

### User Interaction

When potential duplicates are found, present them interactively:

```
Potential duplicates found:

1. task-003: "Fix authentication timeout" (.plans/auth-feature/tasks/)
   Similarity: 85% — Title closely matches your input

2. PROJ-234: "Authentication session timeout bug" (Linear)
   Similarity: 60% — Related keywords detected

Options:
  [Skip] — Do not create this task
  [Create anyway] — Create despite potential overlap
  [View #1] — Read the full task details before deciding
```

## Integration Matrix

| Existing Command | Integration with init-task | Changes Required |
|------------------|---------------------------|------------------|
| `implement-task` | Consumes tasks created by `init-task` | None (compatible template) |
| `implement-epic` | Picks up newly added tasks within a plan | None |
| `create-plan` | Independent — `init-task` adds to plans that `create-plan` created | None |
| `document-handoff` | References tasks created by `init-task` automatically | None |
| `create-prd` | Independent — `init-task` does not require a PRD | None |

## Non-Goals

- **Task editing**: This command creates tasks only. Editing existing tasks is out of scope.
- **Task deletion**: Not supported. Users manage task lifecycle manually or via Linear.
- **Bulk creation**: For bulk task creation, use `create-plan`. This command handles single tasks.
- **Skill acceleration**: A companion skill may be added in a future iteration but is not part of this design.

## Success Criteria

1. Tasks created by `init-task` are consumable by `implement-task` without modification
2. Duplicate detection catches >80% of obvious duplicates across both providers
3. Interactive wizard completes in under 2 minutes for a standard task
4. All tasks include a Definition of Done section
5. STATUS.md is correctly updated when tasks are added to existing plans
