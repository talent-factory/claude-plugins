# Troubleshooting

Common issues and solutions for EPIC implementation.

## Orchestrator Issues

### EPIC Not Found

**Symptom**:

```
Error: EPIC 'feature-x' not found
```

**Causes and Solutions**:

1. **Incorrect path**

   ```bash
   # Verify
   ls -la .plans/

   # Correct invocation
   /project-management:implement-epic --plan .plans/feature-x/
   ```

2. **Missing EPIC.md**

   ```bash
   # Recreate EPIC
   /project-management:create-plan --prd PRD.md
   ```

3. **Missing Linear flag**
   ```bash
   # For Linear EPICs
   /project-management:implement-epic --linear PROJ-123
   ```

### Circular Dependency Error

**Symptom**:

```
Error: Circular dependency detected: task-001 → task-003 → task-001
```

**Solution**:

```bash
# Inspect dependencies
grep -r "Requires:" .plans/feature-x/tasks/

# Resolve circular reference
# In task-001.md:
# - Requires: task-003  ← Remove or decompose task
```

### No Tasks Available to Start

**Symptom**:

```
Warning: No tasks ready to start (all blocked or completed)
```

**Causes**:

1. **All tasks have dependencies**

   ```bash
   # At least one task must have no requirements
   cat .plans/feature-x/tasks/task-001.md | grep "Requires"
   # Should be "Requires: None"
   ```

2. **Tasks already in progress**
   ```bash
   # Check status
   cat .plans/feature-x/STATUS.md
   ```

## Autonomous Loop Issues

### Loop Does Not Terminate

**Symptom**:
Loop runs indefinitely, reaches max-iterations.

**Solutions**:

1. **Verify completion promise**

   ```bash
   # Promise must appear exactly in output
   # Incorrect:
   Output: TASK_COMPLETE

   # Correct:
   <promise>TASK_COMPLETE</promise>
   ```

2. **Refine prompt**

   ```markdown
   # Clearer success criteria

   When these conditions are satisfied:

   1. npm test succeeds (exit code 0)
   2. npm run lint returns no errors

   Then output EXACTLY this text:
   <promise>TASK_COMPLETE</promise>
   ```

3. **Implement fallback**

   ```markdown
   After 25 iterations, if not completed:

   1. Document progress in PROGRESS.md
   2. List outstanding items
   3. <promise>TASK_PARTIAL</promise>
   ```

### Premature Completion

**Symptom**:
Loop terminates although task is incomplete.

**Causes**:

1. **Promise emitted prematurely**

   ```markdown
   # Refine prompt

   IMPORTANT: Output <promise>TASK_COMPLETE</promise> ONLY when:

   - All tests pass (npm test shows "X passing, 0 failing")
   - No ESLint errors
   - Changes committed
   ```

2. **Unintended match**
   ```bash
   # If code contains "TASK_COMPLETE"
   # Use more distinctive promise
   --completion-promise "EPIC_TASK_001_COMPLETE"
   ```

### Memory/Context Issues

**Symptom**:
Loop performance degrades, context overflow errors.

**Solutions**:

1. **Enable context rotation**

   ```python
   # In orchestrator
   spawn_subagent(
       fresh_context=True,
       memory_handoff='minimal'  # Transfer only essential data
   )
   ```

2. **Decompose tasks**

   ```bash
   # Instead of one large task
   task-001: Complete Auth System  # 13 SP ← Too large!

   # Multiple smaller tasks
   task-001a: Auth Service scaffold  # 3 SP
   task-001b: JWT integration        # 3 SP
   task-001c: Password hashing       # 2 SP
   task-001d: Auth tests             # 3 SP
   ```

## Worktree Issues

### Worktree Already Exists

**Symptom**:

```
fatal: '.worktrees/task-001' already exists
```

**Solutions**:

1. **Use existing worktree**

   ```bash
   cd .worktrees/task-001
   git status  # Inspect contents
   ```

2. **Cleanup and recreate**
   ```bash
   git worktree remove .worktrees/task-001 --force
   git worktree add -b feature/task-001 .worktrees/task-001 origin/main
   ```

### Branch Already Exists

**Symptom**:

```
fatal: A branch named 'feature/task-001' already exists
```

**Solutions**:

1. **Use existing branch**

   ```bash
   git worktree add .worktrees/task-001 feature/task-001
   ```

2. **Delete branch (if no longer needed)**
   ```bash
   git branch -D feature/task-001
   git worktree add -b feature/task-001 .worktrees/task-001 origin/main
   ```

### Submodules Not Initialised

**Symptom**:

```
Error: Submodule 'libs/shared' not initialized
```

**Solution**:

```bash
cd .worktrees/task-001
git submodule update --init --recursive
```

## Git Issues

### Merge Conflicts

**Symptom**:

```
CONFLICT (content): Merge conflict in src/utils.ts
```

**Automated Resolution (in autonomous loop)**:

```markdown
For merge conflicts:

1. git fetch origin
2. git rebase origin/main
3. For conflicts:
   - Analyse both versions
   - Select optimal solution
   - git add <file>
   - git rebase --continue
4. If unresolvable: <promise>TASK_BLOCKED</promise>
```

**Manual Resolution**:

```bash
cd .worktrees/task-001
git status  # View conflict files
# Resolve manually
git add .
git rebase --continue
```

### Push Rejected

**Symptom**:

```
! [rejected] feature/task-001 -> feature/task-001 (non-fast-forward)
```

**Solution**:

```bash
cd .worktrees/task-001
git fetch origin
git rebase origin/feature/task-001
git push --force-with-lease
```

## Pull Request Issues

### Draft PR Creation Failure

**Symptom**:

```
Error: Failed to create pull request
```

**Causes and Solutions**:

1. **gh not authenticated**

   ```bash
   gh auth status
   gh auth login
   ```

2. **Branch not pushed**

   ```bash
   git push -u origin feature/task-001
   ```

3. **Insufficient repository permissions**
   ```bash
   # Fork instead of pushing to original
   gh repo fork
   git remote add fork <fork-url>
   git push fork feature/task-001
   gh pr create --repo original/repo --head fork:feature/task-001
   ```

### Review Changes Not Detected

**Symptom**:
Review loop resolves issues, but PR shows no changes.

**Solution**:

```bash
# In worktree
cd .worktrees/task-001
git status  # Check for unstaged changes
git add .
git commit -m "fix: Addressed review comments"
git push
```

## Performance Issues

### Excessive CPU/Memory Utilisation

**Symptom**:
System becomes slow, agents crash.

**Solutions**:

1. **Reduce parallelism**

   ```bash
   /project-management:implement-epic feature-x --max-parallel 2
   ```

2. **Limit iterations**

   ```bash
   /project-management:implement-epic feature-x --max-iterations 20
   ```

3. **Introduce pauses**
   ```python
   # In orchestrator
   after_each_task_complete:
       await asyncio.sleep(5)  # 5 second pause
   ```

### Excessive API Costs

**Symptom**:
Costs escalate rapidly.

**Solutions**:

1. **Execute dry run first**

   ```bash
   /project-management:implement-epic feature-x --dry-run
   # Displays estimated costs
   ```

2. **Smaller tasks**

   ```bash
   # Instead of 5 tasks at 8 SP
   # Better: 10 tasks at 3-4 SP
   ```

3. **More efficient prompts**

   ```markdown
   # Shorter, more focused prompts

   # Less context = fewer tokens
   ```

## Recovery

### Resume After Crash

```bash
# Check orchestrator state
cat .plans/feature-x/.orchestrator/state.json

# Resume
/project-management:implement-epic feature-x --resume

# Or: Continue specific task
/project-management:implement-task task-001 --continue
```

### Cleanup After Abort

```bash
# List all worktrees
git worktree list

# Remove unused worktrees
git worktree remove .worktrees/task-001 --force

# Delete orphaned branches
git branch -D feature/task-001

# Reset orchestrator state
rm -rf .plans/feature-x/.orchestrator/
```

## Debugging

### Verbose Mode

```bash
/project-management:implement-epic feature-x --verbose
# Displays detailed logs
```

### Debug Individual Task

```bash
# Start task manually
cd .worktrees/task-001

# Without autonomous loop, interactively
claude
> Implement Task task-001...
```

### Log Analysis

```bash
# Orchestrator logs
tail -f .plans/feature-x/.orchestrator/logs/orchestrator.log

# Task-specific logs
cat .plans/feature-x/.orchestrator/logs/task-001.log
```
