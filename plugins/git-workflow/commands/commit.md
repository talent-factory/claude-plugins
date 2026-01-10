# Git Commit Command

Create professional git commits with conventional commit format and pre-commit validation.

## Context

You are helping create a git commit following these guidelines:

### Conventional Commit Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation only
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **perf**: Performance improvements
- **test**: Adding or updating tests
- **build**: Build system changes
- **ci**: CI/CD changes
- **chore**: Maintenance tasks

### Rules
1. Subject line max 50 characters
2. Body wrapped at 72 characters
3. Use imperative mood ("add" not "added")
4. Separate subject from body with blank line
5. Include breaking changes in footer if applicable

## Pre-Commit Checks

Before committing, verify:

1. **Code Quality**
   - Run linters if configured
   - Check for console.logs, debugger statements
   - Verify no TODO/FIXME without tracking

2. **Tests**
   - Run relevant test suite
   - Ensure all tests pass
   - Check code coverage if applicable

3. **Files**
   - Review staged files: `git diff --cached`
   - Ensure no sensitive data (API keys, passwords)
   - Check .gitignore is properly configured

## Workflow

1. **Analyze Changes**
   ```bash
   git status
   git diff --cached
   ```

2. **Generate Commit Message**
   - Determine commit type
   - Write clear, concise subject
   - Add detailed body if needed
   - Include issue references

3. **Execute Commit**
   ```bash
   git commit -m "type(scope): subject" -m "body"
   ```

## Example

```
feat(auth): add OAuth2 login support

- Implement OAuth2 authentication flow
- Add Google and GitHub providers
- Update user model with OAuth fields
- Add migration for new columns

Closes #123
```

## Interactive Mode

Ask the user:
1. What changes are being committed?
2. What is the primary type of change?
3. What scope is affected?
4. Are there breaking changes?

Then generate and present the commit message for approval.
