# Commit Workflow Integration

The `/git-workflow:create-pr` command integrates with the `/git-workflow:commit` command for professional commits.

## Workflow Overview

```text
Check current branch
        │
        ├─ Protected (main/master/develop)?
        │       │
        │       └─ YES → New branch MUST be created
        │
        └─ Feature branch?
                │
                └─ NO → Use current branch
                          │
Uncommitted changes?      │
        │                 │
        ├─ YES → Invoke /git-workflow:commit
        │           │
        │           ├─ Pre-commit checks
        │           ├─ Staging
        │           ├─ Commit message
        │           └─ Commit created
        │
        └─ NO  → Use existing commits
                      │
                      └─ Create branch (if necessary)
                         Push to remote
                         Create PR
```

## Branch Status Check ⚠️ IMPORTANT

**FIRST STEP** before any PR creation!

### Detecting Protected Branches

```bash
# Determine current branch
current_branch=$(git branch --show-current)

# Define protected branches
protected_branches=("main" "master" "develop")

# Check if current branch is protected
if [[ " ${protected_branches[*]} " =~ " ${current_branch} " ]]; then
  echo "⚠️ On protected branch: $current_branch"
  echo "➡️ New feature branch will be created"
else
  echo "✅ On feature branch: $current_branch"
  echo "➡️ Using current branch"
fi
```

### Why This Check?

**Protected branches** (`main`, `master`, `develop`):

- ❌ Direct commits are prohibited
- ❌ PRs targeting themselves are not possible
- ✅ A new branch MUST be created
- ✅ PR is created against the protected branch

**Feature branches** (e.g., `feature/xyz`, `bugfix/abc`):

- ✅ Already on a separate branch
- ✅ No new branch necessary
- ✅ PR can be created directly

### Example Scenarios

**On `main` branch:**

```bash
$ git branch --show-current
main

# /git-workflow:create-pr detects: protected branch!
# → Creates: feature/new-feature-2024-12-12
# → PR: feature/new-feature → main
```

**On `feature/login` branch:**

```bash
$ git branch --show-current
feature/login

# /git-workflow:create-pr detects: feature branch!
# → No new branch necessary
# → PR: feature/login → main
```

## Integration with /git-workflow:commit

### Prerequisites

The `/git-workflow:create-pr` command:

- **Checks for uncommitted changes**
- **Invokes `/git-workflow:commit`** if necessary
- **Uses existing commits** for PR
- **Does NOT create its own commits**

### Why This Integration?

**Consistency**: One command for commits = consistent quality

**No duplication**: Commit logic only in `/git-workflow:commit`

**Flexibility**: You can create commits manually or automatically

## Workflow Scenarios

### Scenario 1: No Commits Present

**Situation**: You have changes but no commit yet

```bash
$ git status
modified: src/app.py
modified: tests/test_app.py
```

**Workflow**:

```bash
/git-workflow:create-pr
```

1. **Detects uncommitted changes**
2. **Invokes `/git-workflow:commit`**
   - Pre-commit checks
   - Staging
   - Commit creation
3. **Creates branch**: `feature/new-feature-2024-10-30`
4. **Pushes branch**
5. **Creates PR**

### Scenario 2: Commits Already Present

**Situation**: You have already created commits

```bash
$ git log --oneline -3
abc1234 (HEAD -> main) ✨ feat: Add new feature
def5678 🧪 test: Add tests for new feature
ghi9012 📚 docs: Update documentation
```

**Workflow**:

```bash
/git-workflow:create-pr
```

1. **Detects existing commits**
2. **Skips commit creation**
3. **Creates branch**: `feature/new-feature-2024-10-30`
4. **Pushes branch with all commits**
5. **Creates PR** based on commit history

### Scenario 3: Mixed Situation

**Situation**: Commits present + new changes

```bash
$ git log --oneline -1
abc1234 (HEAD -> main) ✨ feat: Add new feature

$ git status
modified: src/app.py  # Additional changes
```

**Workflow**:

```bash
/git-workflow:create-pr
```

1. **Detects uncommitted changes**
2. **Invokes `/git-workflow:commit`** for new changes
3. **Creates branch** with all commits
4. **Pushes and creates PR**

## Commit Splitting

The `/git-workflow:commit` command can automatically split changes into logical commits.

### Automatic Detection

**Example**: Multiple independent changes

```bash
$ git status
modified: src/auth/login.py       # Auth feature
modified: src/dashboard/ui.py     # UI update
modified: tests/test_auth.py      # Auth tests
modified: tests/test_dashboard.py # UI tests
modified: README.md               # Docs
```

**Workflow**:

```bash
/git-workflow:commit
```

Can split into separate commits:

```text
✨ feat: Improve login functionality
├─ src/auth/login.py
└─ tests/test_auth.py

💎 style: Update dashboard UI
├─ src/dashboard/ui.py
└─ tests/test_dashboard.py

📚 docs: Update README with new features
└─ README.md
```

### Why Commit Splitting?

**Advantages**:

- **Atomic commits**: Each commit is independent
- **Better review**: Reviewers see clear structure
- **Easier debugging**: git bisect works better
- **Cherry-picking**: Individual features can be isolated

### Single-Commit Option

**If you want everything in one commit**:

```bash
/git-workflow:create-pr --single-commit
```

## Branch Creation

### Automatic Branch Names

**Format**: `<type>/<description>-<date>`

**Examples**:

```text
feature/user-authentication-2024-10-30
bugfix/memory-leak-fix-2024-10-30
refactor/api-restructure-2024-10-30
```

### Branch Naming Based on Commits

The branch name is derived from the commit messages:

**Commits**:

```text
✨ feat: Add user dashboard
🧪 test: Implement dashboard tests
```

**Branch**: `feature/user-dashboard-2024-10-30`

### Avoiding Collisions

**Problem**: Branch already exists

**Solution**: Automatic suffix

```text
feature/new-feature-2024-10-30
feature/new-feature-2024-10-30-v2
feature/new-feature-2024-10-30-v3
```

## Push Strategy

### First-Time Push

**First push of a new branch**:

```bash
git push -u origin feature/new-feature
```

**The `-u` flag**:

- Sets upstream branch
- Allows simple `git push` later
- Tracks remote branch

### Presenting Commit History

**All commits are pushed**:

```bash
git log --oneline origin/main..HEAD
```

### Avoiding Force Push

**Principle**: Never use `--force` without necessity

**Exception**: Only upon explicit request

```bash
/git-workflow:create-pr --force-push  # ⚠️ Use with caution!
```

## PR Creation Based on Commits

### Commit Analysis

The command analyzes all commits:

```bash
git log --oneline origin/main..HEAD
```

### PR Title Generation

**Single commit**: Commit message as title

```text
✨ feat: Add user dashboard
```

→ PR title: **"Add user dashboard"**

**Multiple commits**: Create summary

```text
✨ feat: Implement login system
🧪 test: Add login tests
📚 docs: Create login documentation
```

→ PR title: **"Login system with tests and documentation"**

### PR Description Generation

**Based on commits**:

```markdown
## Description

This PR implements a new login system with OAuth2 support.

## Changes

- ✨ Implement login system
- 🧪 Add login tests
- 📚 Create login documentation

## Test Plan

- [ ] Manual tests performed
- [ ] Unit tests pass (18 new tests)
- [ ] Integration tests successful

## Breaking Changes

None
```

## Best Practices

### Commit Hygiene Before PR

**Checklist**:

- [ ] All commits have descriptive messages
- [ ] Commits are logically divided
- [ ] No "WIP" or "fix" commits
- [ ] Commit history is clean

**If necessary**: Clean up commits before `/git-workflow:create-pr`

```bash
git rebase -i HEAD~5
# Squash, reword, etc.
```

### Commit Messages as Documentation

**Commits document the "why"**:

```text
✨ feat: Rate limiting for API endpoints

Implement token bucket algorithm for API rate limiting.
Limit: 100 requests per minute per user.

Reason: Protection against API abuse and DoS attacks.
```

### Atomic Feature Branches

**One branch = one feature**

```text
✅ feature/user-authentication
✅ bugfix/login-memory-leak
❌ feature/multiple-unrelated-things
```

## Troubleshooting

### /git-workflow:commit Is Not Invoked

**Problem**: Changes are detected but `/git-workflow:commit` is not called

**Diagnosis**:

```bash
git status
git diff
```

**Possible causes**:

- All changes already committed
- Working directory is clean
- Only untracked files

### Commits Are in Wrong Order

**Problem**: Commit history is disordered

**Solution**: Rebase before PR

```bash
git rebase -i origin/main
# Reorder commits
```

### Branch Name Does Not Fit

**Problem**: Automatic branch name is inappropriate

**Solution**: Create branch manually

```bash
git checkout -b feature/better-name
/git-workflow:create-pr
# Uses existing branch name
```

### Too Many Commits

**Problem**: PR has 20+ commits, difficult to review

**Solution**: Squash commits

```bash
git rebase -i origin/main
# Mark commits as 'squash'
```

Or use:

```bash
/git-workflow:create-pr --single-commit
```

## Integration with Git Hooks

### Pre-Push Hook

**Automatic validation before push**:

```bash
#!/bin/bash
# .git/hooks/pre-push

# Check all commits
for commit in $(git rev-list origin/main..HEAD); do
  msg=$(git log -1 --format=%s $commit)
  if ! echo "$msg" | grep -E "^(feat|fix|docs|style|refactor|test|chore):"; then
    echo "❌ Commit $commit does not have a conventional message"
    exit 1
  fi
done
```

### Commit Message Hook

**Validation during committing**:

```bash
#!/bin/bash
# .git/hooks/commit-msg

msg=$(cat "$1")
if ! echo "$msg" | grep -E "^(✨|🐛|📚|💎|♻️|⚡|🧪|🔧)"; then
  echo "❌ Commit message requires emoji prefix"
  exit 1
fi
```

## Workflow Examples

### Simple Feature Workflow

```bash
# 1. Make changes
vim src/feature.py

# 2. Create PR (including commit)
/git-workflow:create-pr

# Done! Branch, commits, and PR created
```

### Complex Multi-Commit Workflow

```bash
# 1. Implement feature
vim src/auth.py
/git-workflow:commit

# 2. Add tests
vim tests/test_auth.py
/git-workflow:commit

# 3. Update docs
vim README.md
/git-workflow:commit

# 4. Create PR
/git-workflow:create-pr

# Branch with 3 clean commits + PR
```
