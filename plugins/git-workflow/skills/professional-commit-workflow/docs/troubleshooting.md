# Troubleshooting: Commit Issues

## Build Errors

### Java Build Fails

**Problem**: Maven/Gradle build errors

**Diagnosis**:

```bash
mvn clean compile          # Maven
./gradlew clean build      # Gradle
```

**Common causes**:

1. **Compilation errors in code**
   - Syntax errors
   - Missing imports
   - Type mismatches

   **Solution**: Fix errors from compiler output

2. **Missing dependencies**

   ```bash
   mvn dependency:resolve    # Maven
   ./gradlew dependencies    # Gradle
   ```

3. **Stale build artifacts**

   ```bash
   mvn clean                 # Maven
   ./gradlew clean          # Gradle
   ```

### Python Build Errors

**Problem**: Linting or test errors

**Diagnosis**:

```bash
ruff check .              # Linting
pytest -v                # Tests with details
```

**Common causes**:

1. **Ruff/Flake8 violations**

   ```bash
   ruff check --fix .     # Auto-fix
   black .               # Formatting
   ```

2. **Import errors**

   ```bash
   pip install -e .      # Editable install
   pip install -r requirements.txt
   ```

3. **Missing test dependencies**

   ```bash
   pip install -e ".[test]"
   ```

### React/Node Build Errors

**Problem**: TypeScript or ESLint errors

**Diagnosis**:

```bash
npm run lint             # ESLint
tsc --noEmit            # TypeScript check
npm run build           # Full build
```

**Common causes**:

1. **ESLint errors**

   ```bash
   npm run lint -- --fix  # Auto-fix
   ```

2. **TypeScript errors**
   - Missing type definitions
   - Type mismatches

   **Solution**:

   ```bash
   npm install --save-dev @types/[package]
   ```

3. **Outdated node modules**

   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

## Test Errors

### Tests Fail

**Problem**: Unit tests or integration tests failed

**Options**:

1. **Skip tests** (for debugging only):

   ```bash
   /git-workflow:commit --skip-tests
   ```

2. **Debug individual tests**:

   ```bash
   # Java
   mvn test -Dtest=ClassName#methodName

   # Python
   pytest tests/test_file.py::test_function -v

   # JavaScript
   npm test -- --testNamePattern="test name"
   ```

3. **Analyze test output**:
   - Stack traces
   - Assertion errors
   - Setup/teardown issues

### Flaky Tests

**Problem**: Tests fail intermittently

**Diagnosis**:

```bash
# Run multiple times
for i in {1..10}; do npm test; done
```

**Common causes**:

- Race conditions
- Non-isolated tests
- External dependencies (time, network)
- Shared state between tests

**Solutions**:

- Use mocking
- Ensure test isolation
- Deterministic seeds for random values

## Linting Issues

### Automatic Fixes Do Not Work

**Problem**: Linter reports errors that are not auto-fixable

**Strategies**:

1. **Fix incrementally**:

   ```bash
   # Python
   black .              # Formatting first
   isort .             # Then imports
   ruff check --fix .  # Then linting

   # JavaScript
   prettier --write .  # Formatting first
   eslint --fix .     # Then linting
   ```

2. **Temporarily disable individual rules**:

   ```python
   # noqa: E501  (only when truly necessary)
   ```

   ```javascript
   // eslint-disable-next-line rule-name
   ```

3. **Review configuration**:
   - `.eslintrc`, `pyproject.toml`, etc.
   - Conflicts between tools

### Formatting Overwrites Code

**Problem**: Auto-formatter destroys intentional formatting

**Solution**:

```python
# fmt: off
special_formatting = [
    1,  2,  3,
    4,  5,  6,
]
# fmt: on
```

```javascript
// prettier-ignore
const matrix = [
  1, 0, 0,
  0, 1, 0,
  0, 0, 1,
];
```

## Merge Conflicts

### Conflicts Before Committing

**Problem**: Merge conflicts detected

**Solution**:

1. **Save current state**:

   ```bash
   git stash                    # Stash changes
   git pull --rebase origin main # Update
   git stash pop               # Restore changes
   ```

2. **Resolve conflicts**:

   ```bash
   git status                   # View conflicted files
   # Edit files manually
   git add <resolved-files>
   git rebase --continue       # Or git merge --continue
   ```

3. **Use merge tool**:

   ```bash
   git mergetool
   ```

### Pre-Commit Hook Blocks

**Problem**: Pre-commit hook prevents commit

**Diagnosis**:

```bash
git commit -v              # Verbose output
```

**Options**:

1. **Fix hook errors** (recommended)
2. **Temporarily skip hook**:

   ```bash
   git commit --no-verify
   # Or
   /git-workflow:commit --no-verify
   ```

**Warning**: Only use `--no-verify` when you know what you are doing!

## Staging Issues

### Wrong Files Staged

**Problem**: Unwanted files in staging area

**Solution**:

```bash
git reset HEAD <file>          # Unstage individual file
git reset HEAD                # Unstage everything
```

### Files Being Ignored

**Problem**: `.gitignore` blocks desired files

**Diagnosis**:

```bash
git check-ignore -v <file>    # Which rule is blocking?
```

**Solution**:

```bash
git add -f <file>             # Force add
# Or adjust .gitignore
```

### Too Many Untracked Files

**Problem**: Hundreds of files, difficult to overview

**Solution**:

```bash
# Add only relevant files
git add src/                  # Only src directory
git add *.py                 # Only Python files
git add -p                   # Interactive staging
```

## Performance Issues

### Commit Takes Too Long

**Problem**: Pre-commit checks are slow

**Causes**:

1. **Too many tests**
   - Option: `--skip-tests`
   - Or: Only relevant tests

2. **Large number of files**
   - Linters scan too many files

   **Solution**: Check only staged files

   ```bash
   # Python
   ruff check $(git diff --staged --name-only | grep .py$)

   # JavaScript
   eslint $(git diff --staged --name-only | grep .js$)
   ```

3. **Dependency checks**
   - Slow network operations

### Repository Too Large

**Problem**: Large binary files in history

**Diagnosis**:

```bash
git count-objects -vH
```

**Solution**: Use Git LFS for large files

```bash
git lfs install
git lfs track "*.pdf"
git lfs track "*.zip"
```

## Commit Message Issues

### Editor Does Not Open

**Problem**: Git opens the wrong editor

**Solution**:

```bash
# System-wide
export EDITOR=vim
export VISUAL=vim

# Git-specific
git config --global core.editor "code --wait"  # VS Code
git config --global core.editor "nano"        # Nano
git config --global core.editor "vim"         # Vim
```

### Commit Message Validation Fails

**Problem**: commitlint or similar tools block the commit

**Diagnosis**: Review validation rules

**Solution**: Adjust format or modify rules

```bash
# .commitlintrc.json
{
  "extends": ["@commitlint/config-conventional"],
  "rules": {
    "subject-max-length": [2, "always", 100]
  }
}
```

## Authentication Issues

### Push After Commit Fails

**Problem**: Authentication failed

**Solutions**:

1. **Use SSH key**:

   ```bash
   ssh-add ~/.ssh/id_rsa
   ssh -T git@github.com      # Test connection
   ```

2. **Token authentication**:

   ```bash
   git config credential.helper store
   # Enter token on next push
   ```

3. **SSH instead of HTTPS**:

   ```bash
   git remote set-url origin git@github.com:user/repo.git
   ```

## Special Cases

### Undo a Commit

**After commit, before push**:

```bash
git reset HEAD~1              # Soft reset (preserves changes)
git reset --hard HEAD~1       # Hard reset (discards changes)
```

**After push**:

```bash
git revert HEAD               # Creates a new revert commit
```

### Modify Commit Message

**Last commit**:

```bash
git commit --amend
```

**Older commit**:

```bash
git rebase -i HEAD~5
# Mark commit with 'reword'
```

### Squash Multiple Commits

```bash
git rebase -i HEAD~5
# Mark commits with 'squash'
```

## Getting Help

When nothing works:

```bash
git status                    # Current state
git log --oneline -10        # Recent commits
git reflog                   # All operations
```

**Analyze logs**:

- Build logs
- Test output
- Linter reports
- Git output
