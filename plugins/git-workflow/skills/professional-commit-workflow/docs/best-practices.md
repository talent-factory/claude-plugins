# Best Practices for Git Commits

## Commit Quality

### Atomic Commits

**Principle**: Each commit should represent a logical, independent unit

✅ **Good atomic commits**:

```text
✨ feat: Add user authentication
🧪 test: Add tests for authentication
📚 docs: Create auth API documentation
```

❌ **Poor monolithic commit**:

```text
✨ feat: Auth, tests, docs, bugfixes, and refactoring
```

**Advantages**:

- Simplified code review
- Improved debugging (git bisect)
- Selective cherry-picking possible
- Clear Git history

### Descriptive Messages

**What constitutes a good commit message?**

1. **Describe the "what" and "why"**, not the "how"
2. **Provide context** for future developers
3. **Include technical details** when relevant

✅ **Good**:

```text
🐛 fix: Resolve memory leak in WebSocket connections

WebSocket connections were not properly closed when clients
terminated the connection abruptly. This led to memory leaks
under high load.

Solution: Implement explicit cleanup in finally block.
```

❌ **Poor**:

```text
fix: bug
```

### Imperative Mood

**Rule**: Write as though you are commanding the code to perform an action

✅ **Correct (imperative)**:

- Add feature
- Fix bug
- Update documentation
- Remove deprecated code

❌ **Incorrect (past tense)**:

- Added feature
- Fixed bug
- Updated documentation
- Removed deprecated code

**Rationale**: Git itself uses the imperative mood (e.g., "Merge branch", "Revert commit")

### First Line ≤ 72 Characters

**Reason**: Improved readability in Git tools

```text
✨ feat: User dashboard with metrics                    # ✅ 48 characters
✨ feat: Implementation of a comprehensive...           # ❌ too long
```

**Tools for verification**:

```bash
git log --oneline          # Shows only the first line
git log --format="%s"      # Subject lines
```

### No Automatic Signatures

**IMPORTANT**: Commit messages must NOT contain automatic additions:

❌ **Not permitted**:
```text
🤖 Generated with [Claude Code](https://claude.com/claude-code)
Co-Authored-By: Claude <noreply@anthropic.com>
```

✅ **Correct**: Only the actual commit content without tool signatures

## Code Quality Before Committing

### Checklist

Before committing:

- [ ] **Linting passed**: Code adheres to project standards
- [ ] **Tests successful**: All tests pass
- [ ] **Build successful**: Project compiles without errors
- [ ] **Documentation current**: README, comments, docs are up to date
- [ ] **No debug output**: console.log, print() removed
- [ ] **No commented-out code blocks**
- [ ] **Secrets removed**: API keys, passwords not committed

### Automatic Checks

**Setting up pre-commit hooks**:

```bash
# For all projects
git config --global core.hooksPath ~/.git-hooks

# Project-specific
# .git/hooks/pre-commit
```

### Code Review Before Committing

**Perform self-review**:

```bash
git diff --staged          # Review staged changes
git diff HEAD             # All changes
git add -p               # Interactive staging
```

## Project-Specific Standards

### Java

**Standards**:

- ✅ No compiler warnings
- ✅ Checkstyle conformity
- ✅ JavaDoc for public APIs
- ✅ Unit tests for new methods

**Verification**:

```bash
mvn clean compile -Werror
mvn checkstyle:check
```

### Python

**Standards**:

- ✅ PEP 8 compliance
- ✅ Type hints where possible
- ✅ Docstrings for functions
- ✅ Maximum line length: 88 (Black) or 79 (PEP 8)

**Verification**:

```bash
black --check .
ruff check .
mypy .
```

### React/TypeScript

**Standards**:

- ✅ No ESLint errors
- ✅ TypeScript strict mode
- ✅ Component tests present
- ✅ Props with TypeScript interfaces

**Verification**:

```bash
npm run lint
tsc --noEmit
npm test
```

## Avoiding Common Mistakes

### ❌ "WIP" Commits

**Problem**: "Work in Progress" commits in history

**Solution**: Squash before pushing

```bash
git rebase -i HEAD~3
# Mark commits as 'squash'
```

### ❌ Overly Large Commits

**Problem**: 50+ files in a single commit

**Solution**: Divide logically

```bash
git add -p                    # Interactive staging
git add path/to/feature/      # Only feature files
```

### ❌ Merge Commit Clutter

**Problem**: Unnecessary merge commits in feature branch

**Solution**: Use rebase

```bash
git pull --rebase origin main
# instead of
git pull origin main
```

### ❌ Missing Context Information

**Problem**: "fix typo", "update file"

**Solution**: Add context

```text
📚 docs: Correct typo in API documentation

The endpoint name was incorrectly documented (/api/user instead of /api/users),
which caused confusion among external API consumers.
```

## Maintaining a Clean Git History

### Before Pushing

**Review commits**:

```bash
git log --oneline -10         # Last 10 commits
git log --graph --oneline     # With branch visualization
```

**Clean up commits**:

```bash
git rebase -i HEAD~5          # Interactive rebase
# Options: pick, squash, reword, edit, drop
```

### Branch Hygiene

**Feature branches**:

```text
feature/user-authentication # ✅ Descriptive
feat/auth                   # ✅ Shorter, but clear
user-auth-123               # ✅ With ticket number
fix-login                   # ❌ Too generic
new-stuff                   # ❌ Not descriptive
```

**Clean up regularly**:

```bash
git branch --merged | grep -v main | xargs git branch -d
```

## Team Collaboration

### Consistent Conventions

**Establish team agreement**:

- Commit message format
- Branch naming schema
- PR requirements
- Review process

### Commit Message Templates

**Create**:

```bash
git config commit.template ~/.gitmessage
```

**Template** (`~/.gitmessage`):

```text
# <emoji> <type>: <subject>

# [optional body]

# [optional footer]

# Types: feat, fix, docs, style, refactor, perf, test, chore
# Emojis: ✨ 🐛 📚 💎 ♻️ ⚡ 🧪 🔧
```

## Tools and Automation

### Commit Message Linting

```bash
npm install -g @commitlint/cli @commitlint/config-conventional
```

### Pre-Commit Framework

```bash
pip install pre-commit
pre-commit install
```

### Git Aliases

```bash
# Useful shortcuts
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.lg "log --graph --oneline --decorate"
```
