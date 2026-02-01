# Best Practices: Task Implementation

Best practices for implementing tasks (Filesystem or Linear).

## Branch Naming

### Standardized Format

**All providers utilize the same format**:

```
feature/<ISSUE-ID>-<description>
```

| Provider   | Example                                |
| ---------- | -------------------------------------- |
| Filesystem | `feature/task-001-ui-toggle-component` |
| Linear     | `feature/proj-123-oauth2-auth`         |

### Conventions

1. **Prefix `feature/`**: Required for all feature branches
2. **Lowercase**: Always use lowercase characters
3. **Kebab-case**: Separate words with hyphens
4. **Issue ID after prefix**: `feature/<ID>-...`
5. **Concise description**: Maximum 3-4 words following the ID
6. **No emojis**: Use ASCII characters only

### Examples

```bash
# Recommended
feature/task-001-ui-toggle-component
feature/proj-123-user-authentication

# Not Recommended
task-001-ui-toggle          # Missing feature/ prefix
feature/oauth               # Missing Issue ID
Feature/PROJ-123            # Not lowercase
daniels-branch              # Non-standard format
```

### Alternative Prefixes

For other branch types:

| Type    | Format              | Example                     |
| ------- | ------------------- | --------------------------- |
| Feature | `feature/<ID>-desc` | `feature/task-001-toggle`   |
| Bugfix  | `fix/<ID>-desc`     | `fix/task-002-button-crash` |
| Hotfix  | `hotfix/<ID>-desc`  | `hotfix/proj-999-security`  |

## Commit Messages

### Format

```
<emoji> <type>: <description>

[optional body]
```

### Commit Types Derived from Task Labels

| Task Label               | Commit Type | Emoji |
| ------------------------ | ----------- | ----- |
| `bug`, `fix`             | fix         | 🐛    |
| `feature`, `enhancement` | feat        | ✨    |
| `docs`, `documentation`  | docs        | 📚    |
| `refactor`               | refactor    | ♻️    |
| `performance`            | perf        | ⚡    |
| `test`                   | test        | 🧪    |
| `style`                  | style       | 💎    |
| `chore`                  | chore       | 🔧    |

### Examples

```bash
# Feature
git commit -m "✨ feat: Add ThemeToggle component"

# Bug Fix
git commit -m "🐛 fix: Correct theme persistence bug"

# Tests
git commit -m "🧪 test: Add ThemeToggle unit tests"

# Status Updates
git commit -m "🔄 chore: Start task-001 implementation"
git commit -m "✅ chore: Mark task-001 as completed"
```

### Atomic Commits

**Best Practice**: One commit per logical change

```bash
# Recommended
git commit -m "✨ feat: Add ThemeToggle component"
git commit -m "🧪 test: Add ThemeToggle tests"
git commit -m "📚 docs: Document ThemeToggle usage"

# Not Recommended
git commit -m "Implement everything"
```

## Pull Request Design

### PR Title

```bash
# Standardized Format
feat(task-001): UI Toggle Component
feat(proj-123): User Authentication via OAuth2
```

### PR Body Template

```markdown
## Task: [ID] - [Title]

**Description**:
<Task description>

**Changes**:

- <Change 1>
- <Change 2>

**Test Plan**:

- [x] Acceptance criterion 1
- [x] Acceptance criterion 2

**Status**: In Progress → Completed
```

### PR Size

| LOC     | Assessment                      |
| ------- | ------------------------------- |
| < 150   | Excellent, enables rapid review |
| 150-400 | Good, standard review time      |
| 400-800 | Acceptable, extended review     |
| > 800   | Excessive, consider splitting   |

## Testing

### Minimum Coverage Requirements

- **New Features**: 80%+
- **Bug Fixes**: 100% (both bug scenario and fix covered)
- **Refactoring**: No reduction in coverage
- **Critical Paths**: 100%

### Acceptance Criteria as Tests

```javascript
// Issue AC: "User can log in with Google"
// → Test:
it("should allow user to log in with Google", async () => {
  // Test implementation
});
```

### Test Pyramid

```
       / E2E \        ← 10% Few tests, critical flows only
     /Integration\   ← 20% Moderate, API tests
   /  Unit Tests   \ ← 70% Comprehensive, all functions
```

## Code Quality

### Pre-PR Checklist

- [ ] All acceptance criteria satisfied?
- [ ] Tests written and passing?
- [ ] Linting successful?
- [ ] Build successful?
- [ ] Debug code removed?
- [ ] Documentation updated?

### Self-Review

```bash
# Review the diff
git diff main...HEAD

# Consider:
# - Would I approve this code in a review?
# - Is the code comprehensible without additional context?
# - Are edge cases covered by tests?
```

## Task Organization

### Status Workflow

**Best Practice**: Maximum 1-2 tasks in progress concurrently

```
1. Select task (pending/Backlog)
2. Status → in_progress/In Progress
3. Implement
4. Create PR
5. Status → completed/Done
6. Select next task
```

### Dependency Awareness (Filesystem)

**Before starting a task**: Verify dependencies are resolved.

```markdown
## Dependencies

- **Requires**: task-001, task-003 ← Must be completed first
- **Blocks**: task-005
```

## Summary: Guidelines

### Recommended Practices

1. **Descriptive branch names**
2. **Atomic commits** following Emoji Conventional format
3. **Small PRs** (< 400 LOC)
4. **Write tests** (80%+ coverage)
5. **Verify dependencies** before starting tasks
6. **Maintain current status**
7. **Self-review** before PR submission

### Practices to Avoid

1. **Vague branch names** (`fix-stuff`)
2. **Large commits** (`Implement everything`)
3. **Oversized PRs** (> 800 LOC)
4. **Omitting tests**
5. **Ignoring dependencies**
6. **Outdated status information**
7. **Excessive parallel tasks** (limit to 1-2)

## See Also

- [workflow.md](./workflow.md) - Detailed workflow documentation
- [filesystem.md](./filesystem.md) - Filesystem-specific guidance
- [linear.md](./linear.md) - Linear-specific guidance
- [troubleshooting.md](./troubleshooting.md) - Problem resolution
