---
description: Analyze and resolve merge conflicts intelligently with automated test validation
category: develop
argument-hint: "[PR-Nr|Branch] [--target develop] [--dry-run] [--no-tests] [--strategy ours|theirs|smart]"
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Glob
  - Grep
---

# Claude Command: Resolve Merge Conflicts

Analyze and resolve merge conflicts intelligently with automatic root cause analysis, semantic code merging, and test validation.

**All output and commit messages are written in German.**

## Usage

Standard (merge current branch with target):

```bash
/git-workflow:resolve-conflicts
```

With options:

```bash
/git-workflow:resolve-conflicts --target develop          # Target branch (default: develop)
/git-workflow:resolve-conflicts --dry-run                 # Analysis only, no changes
/git-workflow:resolve-conflicts --no-tests                # Skip tests
/git-workflow:resolve-conflicts --strategy smart          # Strategy: smart (default), ours, theirs
/git-workflow:resolve-conflicts feature/task-009          # Specify branch
/git-workflow:resolve-conflicts 42                        # Specify PR number
```

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `[Branch\|PR-Nr]` | Branch to merge or PR number | Current branch |
| `--target` | Target branch to merge from | `develop` |
| `--dry-run` | Analyze only, no changes | `false` |
| `--no-tests` | Skip test execution | `false` |
| `--strategy` | Resolution strategy: `smart`, `ours`, `theirs` | `smart` |

## Workflow

### Step 1: Detect Environment

- Check if operating in a worktree: `git rev-parse --show-toplevel` and `git worktree list`
- Check for uncommitted changes: `git status --porcelain`
  - If present: **HALT** - user must commit or stash first
- Detect project type based on existing files:
  - `pyproject.toml` / `setup.py` -> Python
  - `package.json` -> Frontend/Node
  - `pom.xml` / `build.gradle` -> Java
- Record detected project type for steps 7-8

### Step 2: Parse Input

- **No argument**: Use current branch, merge from `--target` (default: `develop`)
- **Branch name** (e.g., `feature/task-009`): Check out this branch
- **PR number** (e.g., `42`): Determine branch via `gh pr view 42 --json headRefName -q .headRefName`
- Parse all flags: `--target`, `--dry-run`, `--no-tests`, `--strategy`

### Step 3: Detect Conflicts

```bash
# Update remote
git fetch origin

# Determine merge base
git merge-base HEAD origin/<target>

# Start non-destructive merge
git merge --no-commit --no-ff origin/<target>
```

- If **no conflicts**: Abort merge (`git merge --abort`), display message, done
- If **conflicts**: Collect conflict files via `git diff --name-only --diff-filter=U`
- Output: Table with all conflict files and their category

### Step 4: Analyze Conflict Causes

For each conflict file:

1. **Analyze merge base**: `git diff <merge-base>..HEAD -- <file>` (our changes)
2. **Target changes**: `git diff <merge-base>..origin/<target> -- <file>` (their changes)
3. **Identify cause**:
   - Same lines modified -> Content conflict
   - Adjacent changes -> Context conflict
   - Structural changes (imports, exports) -> Additive merge possible
4. **Identify PR/commit source**: `git log --oneline <merge-base>..origin/<target> -- <file>`

**Output**:

```
File                           | Cause               | Source           | Risk
-------------------------------|---------------------|------------------|--------
src/api/auth/__init__.py       | Import extension    | task-006 + 007   | Low
src/api/routes/v1/__init__.py  | Route registration  | task-006 + 007   | Low
alembic/versions/...           | Revision chain      | task-003         | Medium
src/services/email.py          | Logic change        | task-007         | High
```

**With `--dry-run`**: After this step, execute `git merge --abort` and display report. DONE.

### Step 5: Resolve Conflicts

Conflicts are resolved in the following order (simple -> complex):

#### 5a: Lock Files (`uv.lock`, `bun.lockb`, `package-lock.json`)

```bash
git checkout --theirs <lock-file>
```

Then regenerate the lock file:
- Python: `uv lock`
- Frontend: `bun install` or `npm install`

If regeneration fails: **HALT** and inform user.

#### 5b: Configuration Files (`pyproject.toml`, `package.json`, `tsconfig.json`)

- **Form union**: Merge both sides of dependency lists
- Remove duplicates, prefer higher version
- Read file, understand conflict markers, write merged version

#### 5c: Source Code Files

Depending on `--strategy`:

- **`smart`** (default): Semantic analysis
  - **Import blocks**: Merge both import lists, sort
  - **Additive changes** (e.g., new functions, new routes): Keep both sides
  - **Same location modified**: Analyze context, prioritize our logic, integrate target changes
  - **Structural conflicts**: Understand architecture, merge correctly
- **`ours`**: Keep our version on conflicts (`git checkout --ours <file>`)
- **`theirs`**: Keep their version on conflicts (`git checkout --theirs <file>`)

#### 5d: Special Case Alembic Migrations

- Linearize `down_revision` chain
- Check if multiple heads result: `alembic heads`
- If multiple heads: Create merge migration

#### 5e: Special Case Architectural Conflicts

When a file has been **fundamentally restructured** (e.g., class split, API changed):
- **HALT**: Ask user how the merge should look
- Present options with code excerpts from both sides
- Proceed only after user decision

#### 5f: Test Files

- Merge both test suites
- Keep test imports and fixtures from both sides
- Detect duplicate test functions and ask user

### Step 6: Syntactic Validation

After resolving each file:

```bash
# No conflict markers remaining?
grep -rn "<<<<<<< \|======= \|>>>>>>> " <file>

# Python syntax valid?
python -c "import ast; ast.parse(open('<file>').read())"

# TypeScript/JavaScript syntax valid?
# (only check if tsc/node available)
```

If conflict markers found: Re-analyze and resolve the file.
If syntax invalid: Display error and re-edit the file.

### Step 7: Run Tests (unless `--no-tests`)

Based on detected project type:

```bash
# Python
uv run pytest

# Frontend
cd apps/web && bun run test:run

# Java
mvn test
```

- If **tests pass**: Proceed to step 8
- If **tests fail**: Analyze errors and attempt to fix
  - Maximum 2 repair attempts
  - After that: **HALT** and inform user with error report

### Step 8: Linting

```bash
# Python
uv run ruff check . --fix
uv run ruff format .

# Frontend
cd apps/web && bun run lint
```

If linting errors: Apply auto-fix; for remaining errors, inform user.

### Step 9: Generate Report

Output summary table:

```
Merge Conflict Report
=====================

Target:    origin/develop -> feature/task-009
Conflicts: 4 files
Strategy:  smart

File                           | Strategy     | Rationale                        | Risk
-------------------------------|--------------|----------------------------------|--------
uv.lock                       | regenerated  | Lock file regenerated            | None
src/api/auth/__init__.py       | smart/union  | Imports from both tasks merged   | Low
src/api/routes/v1/__init__.py  | smart/union  | Routes merged additively         | Low
src/services/email.py          | smart/ours   | Our logic prioritized            | Medium

Tests:  47 passed, 0 failed
Lint:   No errors
```

### Step 10: Commit and Push

1. **Stage all resolved files**: `git add <files>`
2. **Complete merge** with meaningful message:

```bash
git commit -m "$(cat <<'EOF'
🔀 merge: Integrate develop into feature/task-009

Resolved conflicts in 4 files:
- auth/__init__.py: Import union from task-006 + task-007
- routes/v1/__init__.py: Route registration merged
- services/email.py: Logic merge prioritizing our changes
- uv.lock: Regenerated
EOF
)"
```

3. **Offer push**: Ask user whether to push
   - On confirmation: `git push origin <branch>`

**IMPORTANT:** Commit messages do NOT contain automatic signatures (no Co-Authored-By, no Generated with Claude Code).

## Error Handling

### Merge Already Active

```
A merge is already active. Options:
1. Continue merge: git merge --continue
2. Abort merge: git merge --abort
```

Ask user which action is desired.

### No Remote Branch

```
Branch 'origin/<target>' not found.
   Available remote branches: git branch -r
```

### Worktree Without Remote Tracking

```
No tracking branch set.
   Set tracking: git branch --set-upstream-to=origin/<branch>
```

### Lock File Regeneration Failed

```
Lock file could not be regenerated.
   Please run manually: uv lock / bun install
   Then retry: /git-workflow:resolve-conflicts --no-tests
```

### Tests Failed After Resolution

```
Tests failed after 2 repair attempts.
   Failed tests:
   - test_email_send: AssertionError (expected 200, got 404)
   - test_auth_flow: ImportError (missing module)

   Please review manually and then commit.
   Merge status: All conflicts resolved, not committed.
```

## Additional Information

- **Resolution Strategies**: [strategies.md](../references/resolve-conflicts/strategies.md)
- **Best Practices**: [best-practices.md](../references/resolve-conflicts/best-practices.md)
- **Troubleshooting**: [troubleshooting.md](../references/resolve-conflicts/troubleshooting.md)
