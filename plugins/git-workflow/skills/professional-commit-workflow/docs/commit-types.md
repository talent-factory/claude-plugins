# Commit Types with Emojis

Emoji Conventional Commit format for a consistent Git history.

## Standard Types

### ✨ feat: New Functionality

**Usage**: Entirely new features or functionality

**Examples**:

```text
✨ feat: Add user dashboard with metrics
✨ feat: Implement OAuth2 authentication
✨ feat: Add dark mode toggle to settings
```

### 🐛 fix: Bug Fix

**Usage**: Bug fixes and corrections

**Examples**:

```text
🐛 fix: Resolve memory leak in database connection
🐛 fix: Correct erroneous response code for 404 errors
🐛 fix: Resolve race condition in async handler
```

### 📚 docs: Documentation

**Usage**: Documentation changes only

**Examples**:

```text
📚 docs: Update API documentation for v2 endpoints
📚 docs: Supplement README with installation guide
📚 docs: Add JSDoc comments for core modules
```

### 💎 style: Code Formatting

**Usage**: Formatting without logic changes (whitespace, indentation)

**Examples**:

```text
💎 style: Apply Prettier formatting to entire project
💎 style: Correct indentation in config files
💎 style: Remove trailing whitespace
```

### ♻️ refactor: Code Restructuring

**Usage**: Code changes without new features or fixes

**Examples**:

```text
♻️ refactor: Split User Service into smaller modules
♻️ refactor: Introduce dependency injection for improved testability
♻️ refactor: Replace deprecated API with modern alternative
```

### ⚡ perf: Performance

**Usage**: Performance improvements

**Examples**:

```text
⚡ perf: Optimize database queries with indexing
⚡ perf: Implement lazy loading for large components
⚡ perf: Add caching layer for API responses
```

### 🧪 test: Tests

**Usage**: Adding or correcting tests

**Examples**:

```text
🧪 test: Add unit tests for Authentication Service
🧪 test: Extend E2E tests for checkout flow
🧪 test: Stabilize flaky test in CI/CD pipeline
```

### 🔧 chore: Maintenance

**Usage**: Build, tools, configuration

**Examples**:

```text
🔧 chore: Update dependencies to latest versions
🔧 chore: Tighten ESLint configuration
🔧 chore: Optimize build script for production
```

## Special Types

### 🚀 ci: Continuous Integration

**Usage**: CI/CD pipeline changes

**Examples**:

```text
🚀 ci: Add GitHub Actions workflow for automatic deployment
🚀 ci: Add test coverage report to pipeline
🚀 ci: Optimize Docker build stage
```

### 🔒 security: Security

**Usage**: Security improvements and fixes

**Examples**:

```text
🔒 security: Resolve SQL injection vulnerability
🔒 security: Implement CSRF protection for forms
🔒 security: Update dependencies with known CVEs
```

### 🌐 i18n: Internationalization

**Usage**: Translations and localization

**Examples**:

```text
🌐 i18n: Add German translation for UI components
🌐 i18n: Implement date formatting for various locales
🌐 i18n: Implement language selection dropdown
```

### ♿ a11y: Accessibility

**Usage**: Accessibility improvements

**Examples**:

```text
♿ a11y: Add ARIA labels for screen readers
♿ a11y: Implement keyboard navigation for dropdown menus
♿ a11y: Adjust color contrasts to WCAG 2.1 AA compliance
```

### 📦 deps: Dependencies

**Usage**: Dependency updates (as an alternative to chore)

**Examples**:

```text
📦 deps: Update React from 18.2 to 18.3
📦 deps: Apply security update for lodash
📦 deps: Update development dependencies
```

## Best Practices

### Commit Message Format

```text
<emoji> <type>: <brief description>

[optional body with details]

[optional footer: breaking changes, issues]
```

### Use Imperative Mood

✅ **Correct**:

```text
✨ feat: Add user dashboard
🐛 fix: Resolve memory leak in API
```

❌ **Incorrect**:

```text
✨ feat: Added dashboard
🐛 fix: Fixed memory leak
```

### Observe Length Constraints

- **Subject Line**: ≤ 72 characters
- **Body**: Wrap lines at a maximum of 72 characters

### Mark Breaking Changes

```text
♻️ refactor: Introduce API v2 endpoints

BREAKING CHANGE: Legacy v1 endpoints are deprecated.
See docs/migration.md for the migration guide.
```
