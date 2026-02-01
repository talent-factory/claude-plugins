# Troubleshooting: Task Implementation

Common issues encountered during task implementation and their solutions.

## Task Identification

### Task Not Found

**Symptom**:

```
❌ Error: Task [ID] not found
```

**Solutions**:

**Filesystem**:

```bash
# List all tasks
find .plans -name "task-*.md"

# Search with plan context
/implement-task --plan dark-mode-toggle task-001
```

**Linear**:

```bash
# Validate issue ID (format: [A-Z]+-[0-9]+)
# Example: PROJ-123, not proj-123

# API test
curl -H "Authorization: Bearer $LINEAR_API_KEY" \
  https://api.linear.app/graphql \
  -d '{"query":"query{issue(id:\"PROJ-123\"){id title}}"}'
```

## Worktree Issues

### Worktree Already Exists

**Symptom**:

```
❌ fatal: '.worktrees/task-001' already exists
```

**Solutions**:

1. **Switch to the existing worktree**:

   ```bash
   cd .worktrees/task-001
   # Continue working
   ```

2. **Remove and recreate the worktree**:

   ```bash
   git worktree remove .worktrees/task-001
   git worktree add -b feature/task-001-desc .worktrees/task-001 origin/main
   ```

3. **Clean up orphaned worktree** (if directory was manually deleted):
   ```bash
   git worktree prune
   git worktree add -b feature/task-001-desc .worktrees/task-001 origin/main
   ```

### Worktree Directory Missing

**Symptom**:

```
❌ Error: .worktrees directory not found
```

**Solution**:

```bash
mkdir -p .worktrees
# Retry the operation
```

### Branch Already Checked Out in Another Worktree

**Symptom**:

```
❌ fatal: 'feature/task-001-...' is already checked out at '/path/to/.worktrees/...'
```

**Solutions**:

1. **Locate and use the other worktree**:

   ```bash
   git worktree list
   # Shows: .worktrees/task-001  abc1234 [feature/task-001-desc]
   cd .worktrees/task-001
   ```

2. **Remove the old worktree**:
   ```bash
   git worktree remove /path/to/old/worktree
   # Then recreate
   ```

### List All Worktrees

**Diagnosis**:

```bash
git worktree list
# Output:
# /path/to/main           abc1234 [main]
# /path/to/.worktrees/task-001  def5678 [feature/task-001-desc]
```

### Clean Up Orphaned Worktrees

**Symptom**: Worktree directory was manually deleted, but Git still references it

**Solution**:

```bash
git worktree prune
git worktree list  # Verify
```

### Clean Up Worktree After Merge

**After successful PR merge**:

```bash
# From the main repository (NOT from within the worktree)
cd /path/to/main/repo

# 1. Remove the worktree
git worktree remove .worktrees/task-001

# 2. Delete the local branch
git branch -d feature/task-001-desc

# 3. Delete the remote branch (optional, typically handled via PR)
git push origin --delete feature/task-001-desc
```

## Submodule Issues

### Submodule Not Initialized in Worktree

**Symptom**:

```
❌ Submodule path 'libs/shared' not initialized
```

**Solution**:

```bash
cd .worktrees/task-001
git submodule update --init --recursive
```

### Branch Conflict in Submodule

**Symptom**:

```
❌ fatal: A branch named 'feature/task-001-...' already exists in submodule
```

**Solutions**:

1. **Use the existing branch**:

   ```bash
   cd .worktrees/task-001/libs/shared
   git checkout feature/task-001-desc
   ```

2. **Delete and recreate the branch in the submodule**:
   ```bash
   cd .worktrees/task-001/libs/shared
   git branch -D feature/task-001-desc
   git checkout -b feature/task-001-desc origin/main
   ```

### Verify Submodule Status

**Diagnosis**:

```bash
cd .worktrees/task-001

# Display all submodules and their branches
git submodule foreach --recursive 'echo "=== $name ===" && git branch --show-current'

# Submodule status
git submodule status --recursive
```

### Clean Up Submodule Branches After Merge

**After successful PR merge**:

```bash
# From within the worktree
cd .worktrees/task-001

# Reset all submodules to main and delete branches
git submodule foreach --recursive '
  git checkout main
  git pull origin main
  git branch -d "feature/task-001-desc" 2>/dev/null || echo "Branch not found in $name"
'
```

### Submodule Shows "detached HEAD"

**Symptom**:

```
HEAD detached at abc1234
```

**Cause**: Submodule was not checked out to a branch

**Solution**:

```bash
cd .worktrees/task-001/libs/shared
git checkout -b feature/task-001-desc
# Or if the branch exists:
git checkout feature/task-001-desc
```

## Branch Issues

### Branch Already Exists

**Symptom**:

```
⚠️ Branch feature/proj-123-... already exists
```

**Solutions**:

1. **Locate the existing worktree using this branch**:

   ```bash
   git worktree list | grep "feature/proj-123"
   ```

2. **Delete and recreate the branch** (if no worktree exists):

   ```bash
   git branch -D feature/proj-123-user-auth
   git worktree add -b feature/proj-123-user-auth .worktrees/task-proj-123 origin/main
   ```

3. **Select a different task**

### Working Directory Not Clean

**Symptom**:

```
❌ Error: Working directory not clean
```

**Solutions**:

```bash
# Option 1: Commit changes
/commit

# Option 2: Stash changes
git stash save "WIP before implementing task"

# Option 3: Discard changes (use with caution)
git reset --hard HEAD
```

> **Note**: When using worktrees, the main repository is typically clean since changes are isolated within the worktree.

### Remote Not Up-to-Date

**Symptom**:

```
⚠️ Local branch is behind remote
```

**Solution**:

```bash
git fetch origin
git pull --rebase origin main
```

## Status Update Issues

### Filesystem: Status Update Fails

**Symptom**:

```
❌ Could not update task status
Old string not found: "- **Status**: pending"
```

**Cause**: Format in task file deviates from expected format

**Solution**: Manually correct the task file:

```markdown
- **Status**: pending
```

### Linear: MCP Server Unavailable

**Symptom**:

```
❌ Linear MCP server not available
```

**Diagnosis**:

```bash
# Verify MCP configuration
cat ~/.config/claude/mcp_config.json

# Test API key
echo $LINEAR_API_KEY
curl -H "Authorization: Bearer $LINEAR_API_KEY" \
  https://api.linear.app/graphql \
  -d '{"query":"{ viewer { id } }"}'
```

**Solution**: Create MCP configuration:

```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-linear"],
      "env": { "LINEAR_API_KEY": "${LINEAR_API_KEY}" }
    }
  }
}
```

### Linear: Invalid API Key

**Symptom**:

```
❌ Error 401: Unauthorized
```

**Solution**:

1. Generate a new key: https://linear.app → Settings → API
2. Update in `~/.env`:
   ```bash
   export LINEAR_API_KEY="lin_api_NEW_KEY"
   source ~/.env
   ```

## PR Creation Issues

### GitHub CLI Not Authenticated

**Symptom**:

```
❌ gh: Not authenticated
```

**Solution**:

```bash
gh auth login
# Follow the browser login flow
gh auth status  # Verify
```

### No Commits for PR

**Symptom**:

```
❌ No commits between main and feature-branch
```

**Solution**:

```bash
# Commit changes
git add .
git commit -m "✨ feat: Implement feature"

# Then create PR
/create-pr
```

## Finalization Issues

### Task Remains in_progress After PR

**Symptom**: Task status remains `in_progress` despite PR creation

**Solution**:

**Filesystem**:

```bash
# Manually set task status
# Edit: - **Status**: completed
# Edit: - **Updated**: <today>

# Regenerate STATUS.md
git add .plans/*/tasks/*.md .plans/*/STATUS.md
git commit -m "✅ chore: Mark task as completed"
```

**Linear**:

```bash
# Set issue status in Linear to "In Review" or "Done"
```

## Performance Issues

### Command Hangs

**Symptom**: No output for >5 minutes

**Solutions**:

1. `Ctrl+C` to abort
2. Check rate limit (Linear: 1,200 requests/hour)
3. Restart with debug logging: `export DEBUG=*`

### Search Too Slow (Filesystem)

**Symptom**: Task search takes >5 seconds

**Solution**: Specify plan context

```bash
# Instead of
/implement-task task-001

# Use
/implement-task --plan dark-mode task-001
```

## Quick Reference: Worktree Commands

```bash
# === CREATE WORKTREE ===
mkdir -p .worktrees
git worktree add -b feature/task-001-desc .worktrees/task-001 origin/main
cd .worktrees/task-001

# === INITIALIZE SUBMODULES ===
git submodule update --init --recursive
git submodule foreach --recursive 'git checkout -b feature/task-001-desc origin/main'

# === LIST WORKTREES ===
git worktree list

# === REMOVE WORKTREE ===
git worktree remove .worktrees/task-001
git branch -d feature/task-001-desc

# === CLEAN UP ORPHANED WORKTREES ===
git worktree prune

# === SUBMODULE STATUS ===
git submodule foreach --recursive 'echo "=== $name ===" && git branch --show-current'
```

## See Also

- [workflow.md](./workflow.md) - Detailed workflow documentation
- [best-practices.md](./best-practices.md) - Best practices
- [filesystem.md](./filesystem.md) - Filesystem-specific guidance
- [linear.md](./linear.md) - Linear-specific guidance
