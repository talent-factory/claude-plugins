# Troubleshooting Guide

Common issues and solutions for the post-merge-cleanup skill.

## Git Issues

### Worktree Cannot Be Removed

**Error:**
```
fatal: cannot remove directory '.worktrees/task-013': Directory not empty
```

**Cause:** The worktree directory contains untracked or modified files.

**Solutions:**
1. Check for uncommitted changes:
   ```bash
   cd .worktrees/task-013
   git status
   ```
2. Either commit/stash changes or use `--force`:
   ```bash
   git worktree remove .worktrees/task-013 --force
   ```

### Branch Not Fully Merged

**Warning:**
```
error: The branch 'feature/task-013-foo' is not fully merged.
```

**Cause:** This often happens with squash merges, as Git doesn't recognize the commits as merged.

**Solutions:**
1. Verify the PR was actually merged:
   ```bash
   gh pr view <pr-number> --json state
   ```
2. Force delete the branch:
   ```bash
   git branch -D feature/task-013-foo
   ```

### Remote Branch Already Deleted

**Error:**
```
error: unable to delete 'feature/task-013': remote ref does not exist
```

**Cause:** Branch was already deleted (e.g., via GitHub PR settings).

**Solution:** This is safe to ignore. The skill handles this gracefully.

### Stale Remote References

**Symptom:** `git branch -r` shows branches that no longer exist on remote.

**Solution:**
```bash
git fetch --prune
git remote prune origin
```

## Task Detection Issues

### Task Not Found in STATUS.md

**Error:**
```
Could not find task-013 in any STATUS.md file
```

**Causes:**
1. Task ID format mismatch (e.g., `013` vs `task-013`)
2. STATUS.md in unexpected location
3. Table format not recognized

**Solutions:**
1. Check the exact ID format in your STATUS.md:
   ```bash
   grep -r "013" .plans/
   ```
2. Use explicit file path:
   ```bash
   /git-workflow:post-merge-cleanup task-013 --file
   ```

### Linear Issue Not Found

**Error:**
```
Could not find Linear issue: PROJ-123
```

**Causes:**
1. Wrong issue identifier
2. Linear MCP server not configured
3. Insufficient permissions

**Solutions:**
1. Verify the issue exists:
   ```bash
   # Check via Linear MCP
   mcp__plugin_linear_linear__get_issue(id: "PROJ-123")
   ```
2. Check Linear MCP configuration in `.mcp.json`

## Status Update Issues

### STATUS.md Parse Error

**Error:**
```
Could not parse STATUS.md table structure
```

**Cause:** Unusual table format or malformed markdown.

**Solutions:**
1. Validate markdown table syntax
2. Ensure consistent column separators (`|`)
3. Check for merged cells or complex formatting

### Progress Calculation Wrong

**Symptom:** Updated percentage doesn't match expected value.

**Causes:**
1. Story points column not detected
2. Some rows have missing data
3. Header row mistaken for data

**Solution:** Verify table structure has clear headers:
```markdown
| ID | Task | SP | Status |
|----|------|----|--------|  <!-- This separator row is required -->
| 01 | Foo  | 5  | done   |
```

### Linear Update Failed

**Error:**
```
Error updating Linear issue: Insufficient permissions
```

**Cause:** API token doesn't have write access.

**Solutions:**
1. Check Linear API token permissions
2. Update manually and use `--no-status-update` flag
3. Verify team/project access

## Recovery

### Accidentally Deleted Branch

If you deleted a branch that shouldn't have been deleted:

**From local reflog (within ~90 days):**
```bash
git reflog | grep <branch-name>
git checkout -b <branch-name> <commit-sha>
```

**From remote (if still exists):**
```bash
git fetch origin
git checkout -b <branch-name> origin/<branch-name>
```

### Revert STATUS.md Changes

If the status update was incorrect:

```bash
git checkout HEAD~1 -- .plans/subscribeflow-mvp/STATUS.md
git commit -m "Revert status update"
```

## Getting Help

If you encounter an issue not covered here:

1. Run with `--dry-run` to see what would happen
2. Check git status and branch state manually
3. Open an issue with:
   - Command that was run
   - Full error message
   - Git status output
   - STATUS.md excerpt (if relevant)
