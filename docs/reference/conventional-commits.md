# Emoji Conventional Commits Reference

Complete reference for emoji conventional commit format used in the git-workflow plugin.

---

## Format

```
<emoji> <type>: <description>

[optional body]

[optional footer]
```

---

## Commit Types

| Emoji | Type | Description | Example |
|-------|------|-------------|---------|
| ✨ | `feat` | New features | `✨ feat: Add user authentication` |
| 🐛 | `fix` | Bug fixes | `🐛 fix: Resolve login timeout issue` |
| 📚 | `docs` | Documentation | `📚 docs: Update installation guide` |
| 💎 | `style` | Code formatting | `💎 style: Format with Prettier` |
| ♻️ | `refactor` | Code restructuring | `♻️ refactor: Simplify auth logic` |
| ⚡ | `perf` | Performance | `⚡ perf: Optimize database queries` |
| 🧪 | `test` | Testing | `🧪 test: Add login tests` |
| 🔧 | `chore` | Build/tools | `🔧 chore: Update dependencies` |
| 🎉 | `init` | Initial commit | `🎉 init: Initialize project` |
| 🔒 | `security` | Security fixes | `🔒 security: Patch XSS vulnerability` |
| 🌐 | `i18n` | Internationalization | `🌐 i18n: Add German translations` |
| ♿ | `a11y` | Accessibility | `♿ a11y: Improve screen reader support` |
| 🚀 | `deploy` | Deployment | `🚀 deploy: Release v2.0.0` |
| 🔀 | `merge` | Merge branches | `🔀 merge: Merge feature/auth into main` |
| ⏪ | `revert` | Revert changes | `⏪ revert: Revert "Add feature X"` |

---

## Best Practices

### ✅ Do

- **Use imperative mood**: "Add feature" not "Added feature"
- **Be specific**: Explain what and why
- **Keep it concise**: 50 characters or less for description
- **Use correct type**: Choose the most appropriate type
- **Add body for complex changes**: Explain the reasoning

### ❌ Don't

- **Mix changes**: One logical change per commit
- **Use vague descriptions**: "Fix stuff" is not helpful
- **Skip the emoji**: It provides visual context
- **Ignore conventions**: Follow the format consistently

---

## Examples

### Feature Addition

```
✨ feat: Add password reset functionality

Implements email-based password reset with:
- Token generation and validation
- Email notification service
- Secure password update endpoint

Closes #123
```

### Bug Fix

```
🐛 fix: Resolve memory leak in WebSocket connection

The WebSocket connection was not properly closed on component
unmount, causing memory leaks in long-running sessions.

Fixes #456
```

### Documentation

```
📚 docs: Add API authentication guide

Comprehensive guide covering:
- JWT token generation
- Token refresh workflow
- Error handling
```

### Refactoring

```
♻️ refactor: Extract validation logic into separate module

Improves code organization and reusability by moving
validation functions from controllers to dedicated module.
```

---

## Scope (Optional)

Add scope for more context:

```
✨ feat(auth): Add OAuth2 support
🐛 fix(api): Resolve CORS issue
📚 docs(readme): Update installation steps
```

---

## Breaking Changes

Mark breaking changes in footer:

```
✨ feat: Redesign authentication API

BREAKING CHANGE: Authentication endpoint changed from
/api/login to /api/v2/auth/login. Update all client code.
```

---

## Related Resources

- **[Git Workflow Plugin](../plugins/git-workflow.md)** - Use `/commit` command
- **[Your First Commit](../guides/first-commit.md)** - Tutorial
- **[Contributing](../development/contributing.md)** - Contribution guidelines

