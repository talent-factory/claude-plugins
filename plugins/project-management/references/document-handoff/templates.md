# Handoff Templates

## Comprehensive Template

```markdown
# Handoff: [Task Title]

**Date**: [YYYY-MM-DD HH:MM]
**Branch**: [branch-name]
**Linear Issue**: [TF-XXX] - [Issue Title] (if applicable)

## Original Task

[Description of the original requirement]

**Business Value**: [Business value / Context]

## Completed Work

### Changes

| File                | Modification  | Status                  |
| ------------------- | ------------- | ----------------------- |
| `path/to/file1.py`  | [Description] | Committed / Uncommitted |
| `path/to/file2.tsx` | [Description] | Committed / Uncommitted |

### Successful Approaches

1. **[Approach 1]**
   - Implementation: [Description]
   - Rationale for success: [Justification]
   - Relevant files: `path/to/file.py:123`

2. **[Approach 2]**
   - Implementation: [Description]
   - Rationale for success: [Justification]

## Failed Attempts

### Attempt 1: [Brief Description]

**Approach**: [Detailed description]

**Error Message**:
```

[Relevant error message or log output]

````

**Failure Analysis**: [Analysis of the cause]

**Lessons Learned**: [Insights derived from this attempt]

### Attempt 2: [Brief Description]

[Same structure as above]

## Current State

### Git Status

```bash
[Output of git status]
````

### Uncommitted Changes

```bash
[Output of git diff --stat]
```

### Modified Files

| File                | Description of Changes |
| ------------------- | ---------------------- |
| `path/to/file1.py`  | [Brief description]    |
| `path/to/file2.tsx` | [Brief description]    |

### Environment

- **Services**: [Which are running / not running]
- **Database**: [Status, relevant data]
- **Dependencies**: [Relevant packages, versions]
- **Configuration**: [Important configurations]

## Subsequent Steps

### Priority 1: [Title]

**Objective**: [Detailed description of the task]

**Location**: `path/to/file.py:123-145`

**Approach**:

1. [Step 1]
2. [Step 2]
3. [Step 3]

**Acceptance Criteria**:

- [ ] [Criterion 1]
- [ ] [Criterion 2]

### Priority 2: [Title]

[Same structure as above]

### Priority 3: [Title]

[Same structure as above]

## Important References

### Relevant Files

| File                | Lines   | Relevance        |
| ------------------- | ------- | ---------------- |
| `path/to/main.py`   | 712-750 | [Description]    |
| `path/to/config.ts` | 45-60   | [Description]    |
| `.env.example`      | -       | [Considerations] |

### Documentation

- [Link to relevant documentation]
- [Link to similar resolved issue]
- [Link to API documentation]

### Code Patterns

```python
# Example of an important pattern in this project
def example_pattern():
    # This demonstrates how X is typically implemented in this project
    pass
```

## Important Notes

- [Warning 1: e.g., "Do not perform X because Y"]
- [Warning 2: e.g., "Environment variable Z must be configured"]
- [Special consideration: e.g., "Tests must be executed with --flag"]

## For the Subsequent Agent

[Summary in 2-3 sentences: What must the subsequent agent know to begin immediately? Most critical insight and next concrete step.]

````

## Minimal Template

For rapid handovers of less complex tasks:

```markdown
# Handoff: [Task Title]

**Date**: [YYYY-MM-DD HH:MM]
**Branch**: [branch-name]

## Original Task

[1-2 sentences describing the task]

## Completed Work

- [Change 1]
- [Change 2]

## Current State

**Modified Files**: [List or "git status" output]

## Subsequent Steps

1. **[Step 1]**: `path/to/file.py:123`
2. **[Step 2]**: `path/to/file.tsx:45`

## For the Subsequent Agent

[1-2 sentence summary]
````

## Template Selection Guidelines

| Situation                   | Template      | Rationale                                     |
| --------------------------- | ------------- | --------------------------------------------- |
| Complex feature development | Comprehensive | Multiple files, dependencies, failed attempts |
| Bug fix with investigation  | Comprehensive | Documentation of failed attempts is essential |
| Simple modification         | Minimal       | Limited context required                      |
| End of work session         | Minimal       | Status documentation only                     |
| Team handover               | Comprehensive | Maximum clarity for another individual        |

## Placeholder Reference

| Placeholder               | Description                       |
| ------------------------- | --------------------------------- |
| `[YYYY-MM-DD HH:MM]`      | Date and time of handoff creation |
| `[branch-name]`           | Current Git branch                |
| `[TF-XXX]`                | Linear issue ID (if applicable)   |
| `path/to/file.py:123`     | File path with line number        |
| `path/to/file.py:123-145` | File path with line range         |
