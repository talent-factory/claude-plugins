# Filesystem-Based Project Planning

Detailed guide for filesystem-based project planning using the `.plans/` structure.

## Directory Structure

```
.plans/
├── [feature-name]/
│   ├── EPIC.md          # Feature overview
│   ├── STATUS.md        # Progress tracking
│   └── tasks/
│       ├── task-001-[slug].md
│       ├── task-002-[slug].md
│       └── ...
```

**Feature name in kebab-case**:

- "Dark Mode Toggle" → `dark-mode-toggle`
- "RAG-Based System" → `rag-based-system`
- "User Authentication" → `user-authentication`

## EPIC.md Template

```markdown
# [Feature-Name]

## Status

- **Created**: [Date]
- **Status**: planned | in_progress | completed
- **Priority**: high | medium | low

## Executive Summary

[3-5 sentences from PRD Executive Summary]

## Business Value

**Problem**: [Core problem]

**Solution**: [Solution approach]

**Impact**:

- **Time**: [Time savings]
- **Cost**: [Cost savings]
- **Quality**: [Quality improvement]

## Success Metrics

| Metric     | Baseline   | Target   | Timeline   |
| ---------- | ---------- | -------- | ---------- |
| [Metric 1] | [Baseline] | [Target] | [Timeline] |

## Timeline and Milestones

| Milestone | Target Date | Description   |
| --------- | ----------- | ------------- |
| [Phase 1] | [Date]      | [Description] |

## Dependencies

### External Dependencies

- [Dependency 1]

### Internal Dependencies

- [Dependency 1]

## Key Risks

| Risk     | Impact   | Mitigation   |
| -------- | -------- | ------------ |
| [Risk 1] | [Impact] | [Mitigation] |

## MVP Scope

### MUST-HAVE Features

1. [Feature 1]

### SHOULD-HAVE (Post-MVP)

- [Feature 1]

### WON'T-HAVE (Out of Scope)

- [Feature 1]

## Link to PRD

[Full PRD Document](../../[prd-file].md)
```

## STATUS.md Template

```markdown
# Project Status: [Feature-Name]

**Last Updated**: [Date]

## Progress Overview

- **Total Tasks**: [N]
- **Completed**: [N] ([%]%)
- **In Progress**: [N] ([%]%)
- **Pending**: [N] ([%]%)
- **Blocked**: [N] ([%]%)

## Tasks by Priority

### Must-Have (MVP)

- [ ] **task-NNN**: [Task-Name] ([SP] SP) - [status]

### Should-Have (Post-MVP)

- [ ] **task-NNN**: [Task-Name] ([SP] SP) - [status]

## Tasks by Status

### Completed

[None yet or list]

### In Progress

[None yet or list]

### Pending

- **task-NNN-[slug].md** ([SP] SP) [[agent]]

### Blocked

[None or list with blocking reason]

## Story Points Summary

- **Total SP**: [N]
- **Must-Have SP**: [N] ([%]%)
- **Should-Have SP**: [N] ([%]%)

## Dependencies Graph

graph TD
task001[Task 001: Name] --> task002[Task 002: Name]
task002 --> task003[Task 003: Name]

## Critical Path

[Task 1] → [Task 2] → [Task 3] → Launch

## Next Steps

### Immediate (Week 0-1)

1. [Step 1]

### Short-Term (Week 2-4)

1. [Step 1]

## Team Assignments

| Agent/Role  | Primary Tasks      | Workload |
| ----------- | ------------------ | -------- |
| **[agent]** | task-NNN, task-NNN | ~[N] SP  |
```

## Task File Template

**Filename**: `task-NNN-[slug].md`

```markdown
# Task-NNN: [Task-Title]

## Metadata

- **ID**: task-NNN
- **Status**: pending | in_progress | completed | blocked
- **Priority**: must | should | could | wont
- **Estimate**: [N] Story Points
- **Labels**: [label1, label2, ...]
- **Assignee**: [agent-name]
- **Created**: [Date]
- **Updated**: [Date]

## Description

[Detailed description of the task]

**User Story**: As a [Persona], I want to [Action] so that [Benefit].

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Dependencies

- **Requires**: [task-XXX or None]
- **Blocks**: [task-YYY or None]

## Agent Recommendation

**Recommended Agent**: `[agent-name]`

**Rationale**: [Why this agent is recommended]
```
