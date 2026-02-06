# Post-Merge Cleanup Skill

Automates the cleanup process after a Pull Request has been merged, handling both git assets and task tracking updates.

## Features

- **Git Cleanup:** Removes worktrees, local branches, and remote branches
- **Multi-Source Task Tracking:** Supports both filesystem (STATUS.md) and Linear
- **Safe Defaults:** Dry-run mode, PR verification, confirmation prompts
- **Idempotent:** Safe to run multiple times
- **Smart Detection:** Auto-detects task source based on ID pattern

## Quick Start

```bash
# Basic usage - auto-detects task source
/git-workflow:post-merge-cleanup task-013

# Linear issue
/git-workflow:post-merge-cleanup PROJ-123

# Preview without making changes
/git-workflow:post-merge-cleanup task-013 --dry-run

# Only cleanup git, skip status update
/git-workflow:post-merge-cleanup task-013 --no-status-update
```

## What It Does

1. **Detects task source** (Linear or STATUS.md file)
2. **Finds associated git assets** (worktrees, branches)
3. **Verifies PR was merged** (safety check)
4. **Cleans up git assets:**
   - Removes worktree from `.worktrees/`
   - Deletes local feature branch
   - Deletes remote feature branch
   - Prunes stale references
5. **Updates task status:**
   - For STATUS.md: Updates table, recalculates progress
   - For Linear: Moves issue to "Done" state
6. **Commits changes** (filesystem only)

## Task Source Detection

| Pattern | Detected As | Example |
|---------|-------------|---------|
| `task-NNN` | Filesystem | `task-013` |
| `NNN` (numeric) | Filesystem | `013` |
| `PROJ-NNN` | Linear | `PROJ-123` |

Override with `--linear` or `--file` flags.

## Supported STATUS.md Formats

The skill supports various markdown table formats:

```markdown
# Format A: ID column
| ID  | Task        | Status         |
|-----|-------------|----------------|
| 013 | Dashboard   | 🔄 in_progress |

# Format B: Task identifier
| Task     | Status  |
|----------|---------|
| task-013 | pending |
```

## Options

| Flag | Description |
|------|-------------|
| `--dry-run` | Preview changes without executing |
| `--linear` | Force Linear as task source |
| `--file` | Force filesystem as task source |
| `--no-status-update` | Only cleanup git assets |
| `--keep-local` | Keep local branch, only delete remote |

## Safety Features

- **PR Verification:** Warns if no merged PR is found
- **Uncommitted Changes:** Warns if worktree has unsaved work
- **Unmerged Branch:** Asks before force-deleting unmerged branches
- **Dry-Run Mode:** Preview all actions before execution

## Requirements

- Git 2.0+
- GitHub CLI (`gh`) for PR verification
- Linear MCP server (for Linear integration)

## Related Skills

- [professional-commit-workflow](../professional-commit-workflow/) - Create commits
- [professional-pr-workflow](../professional-pr-workflow/) - Create pull requests
