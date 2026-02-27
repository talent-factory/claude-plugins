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
