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
