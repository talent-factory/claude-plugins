# Troubleshooting: PR Creation

## Branch Issues

### Branch Already Exists

**Problem**: Branch name collides with an existing branch

**Symptom**:

```bash
fatal: A branch named 'feature/new-feature' already exists.
```

**Diagnosis**:

```bash
git branch -a                    # Show all branches
git branch -r | grep feature     # Remote feature branches
```

**Solutions**:

1. **Automatic suffix** (command does this automatically):

   ```
   feature/new-feature    → feature/new-feature-v2
   ```

2. **Use existing branch**:

   ```bash
   git checkout feature/new-feature
   /git-workflow:create-pr
   ```

3. **Delete old branch** (use with caution!):

   ```bash
   git branch -D feature/old-feature
   git push origin --delete feature/old-feature
   ```

### Branch Cannot Be Created

**Problem**: Uncommitted changes block branch switching

**Symptom**:

```bash
error: Your local changes would be overwritten by checkout
```

**Solutions**:

1. **Commit changes**:

   ```bash
   /git-workflow:commit
   /git-workflow:create-pr
   ```

2. **Stash changes**:

   ```bash
   git stash
   /git-workflow:create-pr
   git stash pop
   ```

### Wrong Base Branch

**Problem**: Branch was forked from the wrong branch

**Symptom**: PR contains unwanted commits

**Diagnosis**:

```bash
git log --oneline --graph
```

**Solution**: Rebase the branch

```bash
git rebase --onto main old-base feature-branch
```

## Formatting Issues

### Formatting Fails

**Problem**: Code formatter finds errors

**Symptom**:

```bash
Error: Biome formatting failed
Error: Black formatting failed
```

**Diagnosis**:

```bash
# JavaScript
npx biome check .

# Python
black --check .

# Java
mvn fmt:check
```

**Solutions**:

1. **Fix errors**:

   ```bash
   # Auto-fix
   npx biome format --write .
   black .
   mvn fmt:format
   ```

2. **Skip formatting**:

   ```bash
   /git-workflow:create-pr --no-format
   ```

3. **Exclude specific files**:

   ```toml
   # pyproject.toml
   [tool.black]
   extend-exclude = '''
   /(
     problematic_dir
   )/
   '''
   ```

### Formatting Too Slow

**Problem**: Formatting takes very long

**Diagnosis**:

```bash
time black .
time npx biome format .
```

**Solutions**:

1. **Only changed files**:

   ```bash
   black $(git diff --name-only --diff-filter=ACM "*.py")
   ```

2. **Parallel processing**:

   ```bash
   black --fast .
   ```

3. **Skip formatting**:

   ```bash
   /git-workflow:create-pr --no-format
   ```

### Formatting Conflicts

**Problem**: Different formatters contradict each other

**Symptom**: File is formatted differently multiple times

**Solution**: Establish tool priority

```ini
# .editorconfig
root = true

[*.py]
indent_style = space
indent_size = 4
max_line_length = 88

[*.js]
indent_style = space
indent_size = 2
```

## GitHub CLI (gh) Issues

### GitHub CLI Not Configured

**Problem**: `gh` commands do not work

**Symptom**:

```bash
gh: command not found
# Or
error: gh: To get started with GitHub CLI, please run: gh auth login
```

**Solution**:

```bash
# Installation (macOS)
brew install gh

# Installation (Linux)
sudo apt install gh

# Authentication
gh auth login
```

**Verify setup**:

```bash
gh auth status
gh repo view
```

### No Permission for Repository

**Problem**: Missing push permission

**Symptom**:

```bash
remote: Permission to user/repo.git denied
```

**Diagnosis**:

```bash
gh auth status
git remote -v
```

**Solutions**:

1. **Check token permissions**:

   ```bash
   gh auth refresh -s repo
   ```

2. **SSH instead of HTTPS**:

   ```bash
   git remote set-url origin git@github.com:user/repo.git
   ```

3. **Verify repository access**:
   - Create fork if necessary
   - Check team membership

### PR Cannot Be Created

**Problem**: `gh pr create` fails

**Symptom**:

```bash
error: could not create pull request
```

**Common causes**:

1. **Branch not pushed**:

   ```bash
   git push -u origin branch-name
   gh pr create
   ```

2. **No changes**:

   ```bash
   git diff origin/main...HEAD
   # If empty: No changes present
   ```

3. **PR already exists**:

   ```bash
   gh pr list
   gh pr view <number>
   ```

## Commit Integration Issues

### /git-workflow:commit Is Not Invoked

**Problem**: Uncommitted changes but no commit created

**Diagnosis**:

```bash
git status
git diff --stat
```

**Possible causes**:

1. **Only untracked files**:

   ```bash
   git add .
   /git-workflow:create-pr
   ```

2. **All changes already staged**:

   ```bash
   git reset HEAD
   /git-workflow:create-pr  # Now /git-workflow:commit will be invoked
   ```

### Commits in Wrong Order

**Problem**: Commit history is illogical

**Solution**: Interactive rebase

```bash
git rebase -i HEAD~5
# Reorder commits
```

**Or**: Squash commits

```bash
git rebase -i HEAD~3
# Mark with 'squash'
```

### Too Many Commits

**Problem**: PR has 30+ commits, difficult to review

**Solutions**:

1. **Squash commits**:

   ```bash
   git rebase -i origin/main
   # Mark commits as 'squash'
   ```

2. **Single-commit option**:

   ```bash
   /git-workflow:create-pr --single-commit
   ```

## Push Issues

### Push Rejected

**Problem**: Remote has newer commits

**Symptom**:

```bash
! [rejected] feature-branch -> feature-branch (non-fast-forward)
```

**Solution**:

```bash
git pull --rebase origin feature-branch
git push
```

### Push Too Large

**Problem**: Push limit exceeded

**Symptom**:

```bash
remote: error: GH001: Large files detected
```

**Solution**: Use Git LFS

```bash
git lfs install
git lfs track "*.psd" "*.zip"
git add .gitattributes
git commit -m "Add Git LFS"
```

### Protected Branch

**Problem**: Cannot push directly to main/master

**Symptom**:

```bash
remote: error: GH006: Protected branch update failed
```

**Solution**: This is intentional! Always use feature branches:

```bash
git checkout -b feature/new-feature
/git-workflow:create-pr
```

## PR Description Issues

### PR Description Is Empty

**Problem**: No meaningful description generated

**Cause**: No meaningful commit messages

**Solution**: Improve commit messages

```bash
# Reword commits
git rebase -i HEAD~3
# Mark with 'reword'
```

### Breaking Changes Not Detected

**Problem**: Breaking changes not documented in PR

**Solution**: Add manually

```bash
gh pr edit <number> --body "$(cat <<EOF
## Breaking Changes

- API v1 deprecated
- Database Schema Changed

$(gh pr view <number> --json body -q .body)
EOF
)"
```

## Test Issues

### Tests Fail in CI

**Problem**: Tests pass locally but fail in CI

**Diagnosis**:

```bash
gh pr checks <number>
gh run view <run-id>
```

**Common causes**:

1. **Environment differences**:
   - Different Node/Python versions
   - Missing dependencies
   - Environment variables

2. **Timing issues**:
   - Flaky tests
   - Race conditions

3. **Resource limits**:
   - Memory limits
   - Timeout settings

**Solutions**:

```yaml
# .github/workflows/test.yml
- name: Run Tests
  run: pytest -v --timeout=300
  timeout-minutes: 10
```

### Coverage Too Low

**Problem**: Code coverage below minimum threshold

**Diagnosis**:

```bash
pytest --cov --cov-report=term-missing
```

**Solution**: Add tests

```bash
# Write new tests
vim tests/test_new_feature.py
/git-workflow:commit
git push
```

## Network Issues

### Timeout During Push

**Problem**: Push operation timeout

**Solution**:

```bash
# Increase timeout
git config --global http.postBuffer 524288000

# Or: Use SSH
git remote set-url origin git@github.com:user/repo.git
```

### SSL Errors

**Problem**: SSL certificate errors

**Temporary solution** (not recommended for production):

```bash
git config --global http.sslVerify false
```

**Proper solution**: Update CA certificates

```bash
# macOS
brew install ca-certificates

# Linux
sudo update-ca-certificates
```

## Draft vs. Ready

### PR Created as Draft, Should Be Ready

**Problem**: PR is still marked as draft

**Solution**:

```bash
gh pr ready <number>
```

### PR Created as Ready, Should Be Draft

**Problem**: PR is ready but still work in progress

**Solution**:

```bash
gh pr ready <number> --undo
```

## Merge Conflicts in PR

### Merge Conflicts After PR Creation

**Problem**: Base branch has changed

**Diagnosis**:

```bash
gh pr view <number>
# Shows "Merge conflicts" warning
```

**Solution**:

```bash
git checkout feature-branch
git pull origin main --rebase
# Resolve conflicts
git add .
git rebase --continue
git push --force-with-lease
```

## Special Cases

### Monorepo with Multiple Projects

**Problem**: PR contains changes to multiple projects

**Solution**: Create PRs per project

```bash
# Backend PR
git add backend/
/git-workflow:commit
/git-workflow:create-pr

# Frontend PR
git add frontend/
/git-workflow:commit
/git-workflow:create-pr
```

### Force Push Required

**Problem**: History was rewritten

**Solution** (use with caution!):

```bash
/git-workflow:create-pr --force-push
```

**Warning**: Only use when:

- You are the only one working on the branch
- You know what you are doing
- Never on main/master

### Creating PR from Fork

**Problem**: No push permission to original repository

**Workflow**:

```bash
# 1. Create fork (via GitHub UI)

# 2. Clone fork
git clone git@github.com:youruser/repo.git

# 3. Add upstream
git remote add upstream git@github.com:original/repo.git

# 4. Create branch and push
git checkout -b feature/new
/git-workflow:commit
git push origin feature/new

# 5. Create PR (to upstream)
gh pr create --repo original/repo
```

## Debugging

### Verbose Output

**Show more details**:

```bash
GIT_TRACE=1 git push
GH_DEBUG=1 gh pr create
```

### Analyzing Logs

```bash
# Git logs
git log --oneline --graph --all

# GitHub Actions logs
gh run list
gh run view <run-id> --log

# PR status
gh pr view <number> --json statusCheckRollup
```

### Common Sources of Error

**Checklist**:

- [ ] Git/GitHub CLI correctly installed and configured
- [ ] Authentication works
- [ ] Repository permissions correct
- [ ] Branch name is unique
- [ ] Working directory is clean
- [ ] Tests pass locally
- [ ] No large files (>100MB)
