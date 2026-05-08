---
name: resolve-conflicts
description: >
  Analyses and resolves Git merge conflicts intelligently using semantic code
  merging, automated test validation, and root-cause analysis of each conflict.
  Activate when the user says "I have merge conflicts", "help me resolve these
  conflicts", "there are conflicts after merging", "git merge failed", or
  "conflicts between my branch and develop". Supports --dry-run, --no-tests,
  and --strategy options.
---

# Resolve Merge Conflicts

Analyse and resolve Git merge conflicts with semantic merging, automatic test
validation, and a structured report. Uses strategy `smart` by default.

## Parameters

| Parameter | Default | Description |
|---|---|---|
| `[branch\|PR-number]` | current branch | Branch to merge or PR number to resolve |
| `--target <branch>` | `develop` | Target branch to merge from |
| `--dry-run` | false | Analyse only — no file changes |
| `--no-tests` | false | Skip test execution |
| `--strategy smart\|ours\|theirs` | `smart` | Resolution strategy |

## Workflow

### Step 1 — Environment check

- Detect if running inside a git worktree (`git worktree list`)
- Check for uncommitted changes (`git status --porcelain`)
  - **Halt** if present — ask the user to commit or stash first
- Detect project type from existing files: `pyproject.toml` → Python; `package.json` → Frontend; `pom.xml` / `build.gradle` → Java

### Step 2 — Parse input

- No argument → current branch, merge from `--target`
- Branch name → check out that branch
- PR number → resolve branch via `gh pr view <N> --json headRefName -q .headRefName`

### Step 3 — Detect conflicts

```bash
git fetch origin
git merge-base HEAD origin/<target>
git merge --no-commit --no-ff origin/<target>
```

If no conflicts → abort merge, report "No conflicts found", done.

Collect conflicting files: `git diff --name-only --diff-filter=U`

Output a table: file | conflict type | risk level.

### Step 4 — Analyse causes (per file)

For each conflict file:
1. `git diff <merge-base>..HEAD -- <file>` (our changes)
2. `git diff <merge-base>..origin/<target> -- <file>` (their changes)
3. Classify: content conflict · adjacent change · additive change · structural change
4. Identify source commit: `git log --oneline <merge-base>..origin/<target> -- <file>`

**With `--dry-run`**: abort merge here and display analysis report. Done.

### Step 5 — Resolve (ordered simple → complex)

**5a — Lock files** (`uv.lock`, `package-lock.json`, `bun.lockb`):
```bash
git checkout --theirs <lock-file>
# Then regenerate:  uv lock  |  bun install  |  npm install
```
Halt if regeneration fails.

**5b — Configuration files** (`pyproject.toml`, `package.json`):
Merge dependency lists as a union; remove duplicates; prefer higher version.

**5c — Source code** (depends on `--strategy`):
- `smart`: Merge import blocks as union; keep additive changes from both sides; for same-location edits, prioritise our logic and integrate their changes
- `ours`: `git checkout --ours <file>`
- `theirs`: `git checkout --theirs <file>`

**5d — Alembic migrations**: Linearise `down_revision` chain; create a merge migration if multiple heads result.

**5e — Architectural conflicts** (file fundamentally restructured):
Halt and ask the user how to proceed. Show both versions. Continue only after explicit decision.

**5f — Test files**: Merge both suites; keep fixtures from both sides; ask on duplicate test names.

### Step 6 — Syntactic validation (per resolved file)

```bash
grep -n "<<<<<<< \|======= \|>>>>>>> " <file>   # must be empty
python -c "import ast; ast.parse(open('<file>').read())"  # Python only
```

Re-analyse and re-resolve any file that still has markers or syntax errors.

### Step 7 — Run tests (skip with `--no-tests`)

| Project type | Command |
|---|---|
| Python | `uv run pytest` |
| Frontend | `bun run test:run` (or `npm test`) |
| Java | `mvn test` (or `./gradlew test`) |

If tests fail: attempt up to 2 repair cycles. After that, halt and report failing tests with full error output.

### Step 8 — Linting

```bash
# Python
uv run ruff check . --fix && uv run ruff format .

# Frontend
bun run lint  (or npm run lint)
```

### Step 9 — Report

```
Merge Conflict Report
=====================
Target:    origin/develop → feature/my-branch
Conflicts: N files
Strategy:  smart

File                     | Strategy     | Rationale              | Risk
-------------------------|--------------|------------------------|------
uv.lock                  | regenerated  | Lock file regenerated  | None
src/api/auth/__init__.py | smart/union  | Import lists merged    | Low
src/services/email.py    | smart/ours   | Logic conflict, manual | Med

Tests:  47 passed, 0 failed
Lint:   No errors
```

### Step 10 — Commit and offer push

```bash
git add <resolved-files>
git commit -m "🔀 merge: Integrate <target> into <branch>

Resolved conflicts in N files:
- <file>: <brief rationale>
..."
```

Offer to push (`git push origin <branch>`) and wait for the user's confirmation.

## Error Messages

| Situation | Message |
|---|---|
| Uncommitted changes present | Halt: "Please commit or stash your changes first." |
| Merge already active | "A merge is already in progress. Continue (`git merge --continue`) or abort (`git merge --abort`)?" |
| No remote branch | "Branch `origin/<target>` not found. Available: `git branch -r`" |
| Lock regeneration failed | "Lock file regeneration failed. Run manually: `uv lock` / `bun install`" |
| Tests failed after 2 attempts | Show failing test names, exit without committing |

## Additional Resources

- **`../references/resolve-conflicts/strategies.md`** — Strategy comparison and when to choose each
- **`../references/resolve-conflicts/best-practices.md`** — Best practices for conflict-free branching
- **`../references/resolve-conflicts/troubleshooting.md`** — Common failure modes and fixes
