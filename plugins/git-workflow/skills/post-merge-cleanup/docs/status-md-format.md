# STATUS.md Format Guide

This document describes the STATUS.md formats supported by the post-merge-cleanup skill.

## Supported Table Structures

### Structure A: Explicit ID Column

The most common format with a dedicated ID column:

```markdown
| ID  | Task                    | Sprint | SP  | Status         | Blocked By |
|-----|-------------------------|--------|-----|----------------|------------|
| 001 | Database Schema         | 1      | 5   | ✅ completed   | -          |
| 002 | FastAPI Setup           | 1      | 3   | ✅ completed   | 001        |
| 013 | Admin Dashboard         | 6      | 8   | 🔄 in_progress | 011        |
```

**Detection:** Matches `| 013 |` or `| task-013 |` in the ID column.

### Structure B: Task Name as Identifier

Simpler format where the task name contains the identifier:

```markdown
| Task        | Status    | Notes           |
|-------------|-----------|-----------------|
| task-013    | pending   | Waiting for API |
| task-014    | doing     | In review       |
```

**Detection:** Matches `task-013` anywhere in the row.

### Structure C: Checkbox Format

GitHub-style task list format:

```markdown
## Tasks

- [x] task-001: Database Schema
- [x] task-002: FastAPI Setup
- [ ] task-013: Admin Dashboard
- [ ] task-014: E2E Tests
```

**Detection:** Matches `task-013` in checkbox lines.

## Status Values

The skill recognizes various status indicators:

| Category | Recognized Values |
|----------|-------------------|
| **Pending** | `pending`, `⬜`, `todo`, `open`, `backlog`, `not started` |
| **In Progress** | `in_progress`, `🔄`, `doing`, `active`, `started`, `wip` |
| **Review** | `review`, `👀`, `in review`, `pr open` |
| **Completed** | `completed`, `✅`, `done`, `closed`, `finished`, `merged` |
| **Blocked** | `blocked`, `❌`, `waiting`, `on hold` |

## Progress Summary Format

If your STATUS.md includes a progress summary, it will be automatically updated:

```markdown
## Progress Overview

| Sprint     | Tasks | Story Points | Status                    |
|------------|-------|--------------|---------------------------|
| Sprint 1-2 | 5     | 26           | ✅ Completed (26/26 SP)   |
| Sprint 5-6 | 5     | 29           | 🔄 In Progress (19/29 SP) |
| **Total**  | **18**| **88**       | **89%** (78/88 SP)        |
```

**Auto-calculation:**
- Counts completed tasks vs total
- Sums completed story points
- Updates percentage

## Next Steps Section

If present, the "Next Steps" or "Immediately Available" section is updated:

```markdown
## Next Steps

### Immediately Available (No Blockers)

1. **task-014**: E2E Tests
   - Blocked by: task-012 ✅, task-013 ✅
   - Ready to start
```

**Auto-update:**
- Removes completed tasks from the list
- Adds newly unblocked tasks (based on dependency column)

## Best Practices

1. **Use consistent ID format:** Either `NNN` or `task-NNN`
2. **Include Status column:** Makes parsing reliable
3. **Use emoji indicators:** Visual and parseable (✅, 🔄, ⬜)
4. **Keep dependencies up-to-date:** Enables accurate "Next Steps" updates
