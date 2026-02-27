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
   → If no warnings: Proceed to task creation
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
