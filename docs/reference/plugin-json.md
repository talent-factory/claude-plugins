# plugin.json Schema Reference

Complete technical reference for the `plugin.json` configuration file used in Claude Code plugins.

---

## Overview

The `plugin.json` file contains essential metadata and configuration for a Claude Code plugin. It is required for every plugin and must be located in the `.claude-plugin/` directory.

---

## Location

```
plugins/your-plugin/.claude-plugin/plugin.json
```

**Required**: Yes (every plugin must have this file)

---

## Schema

### Required Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `name` | string | Plugin identifier (lowercase, hyphen-separated) | `"git-workflow"` |
| `version` | string | Semantic version number | `"2.0.0"` |
| `description` | string | Brief plugin description | `"Professional git workflow tools"` |
| `author` | object | Author information | See below |

### Optional Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `displayName` | string | Human-readable plugin name | `"Git Workflow"` |
| `keywords` | array | Search tags for discoverability | `["git", "workflow"]` |
| `license` | string | License identifier | `"MIT"` |
| `homepage` | string | Plugin homepage URL | `"https://example.com"` |
| `repository` | string | Source code repository URL | `"https://github.com/..."` |

### Author Object

```json
{
  "author": {
    "name": "Talent Factory GmbH",
    "email": "support@talent-factory.ch",
    "url": "https://talent-factory.ch"
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Author or organization name |
| `email` | string | No | Contact email address |
| `url` | string | No | Author website URL |

---

## Complete Example

```json
{
  "name": "git-workflow",
  "version": "2.0.0",
  "displayName": "Git Workflow",
  "description": "Professional git commands with automated pre-commit checks, emoji conventional commits, PR management, and comprehensive references",
  "keywords": [
    "git",
    "workflow",
    "productivity",
    "commits",
    "pull-requests",
    "automation"
  ],
  "author": {
    "name": "Talent Factory GmbH",
    "email": "support@talent-factory.ch",
    "url": "https://talent-factory.ch"
  },
  "license": "MIT",
  "homepage": "https://github.com/talent-factory/claude-plugins",
  "repository": "https://github.com/talent-factory/claude-plugins"
}
```

---

## Validation Rules

### Name Field

- **Format**: Lowercase letters, numbers, and hyphens only
- **Pattern**: `^[a-z0-9][a-z0-9-]*$`
- **Examples**:
    - ✅ `git-workflow`
    - ✅ `code-quality`
    - ✅ `project-management`
    - ❌ `Git-Workflow` (uppercase)
    - ❌ `git_workflow` (underscore)
    - ❌ `-git-workflow` (starts with hyphen)

### Version Field

- **Format**: Semantic versioning (MAJOR.MINOR.PATCH)
- **Pattern**: `^\d+\.\d+\.\d+$`
- **Examples**:
    - ✅ `1.0.0`
    - ✅ `2.1.3`
    - ❌ `1.0` (missing patch)
    - ❌ `v2.0.0` (prefix not allowed)
    - ❌ `2.0.0-beta` (pre-release not supported)

### Description Field

- **Length**: 10-200 characters recommended
- **Content**: Clear, concise explanation of plugin purpose
- **Style**: Sentence case, no period at end

### Keywords Array

- **Count**: 3-10 keywords recommended
- **Format**: Lowercase, hyphen-separated
- **Purpose**: Improves plugin discoverability
- **Examples**: `["git", "workflow", "commits", "automation"]`

---

## Best Practices

### Naming

✅ **Do**:

- Use descriptive, memorable names
- Follow kebab-case convention
- Keep names short (2-3 words max)
- Use common terminology

❌ **Don't**:

- Use generic names like `utils` or `tools`
- Include "plugin" in the name
- Use abbreviations unless widely known
- Mix naming conventions

### Versioning

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR** (1.0.0 → 2.0.0): Breaking changes
- **MINOR** (1.0.0 → 1.1.0): New features (backward compatible)
- **PATCH** (1.0.0 → 1.0.1): Bug fixes (backward compatible)

**Examples**:

```
1.0.0 → Initial release
1.1.0 → Add new command (backward compatible)
1.1.1 → Fix bug in existing command
2.0.0 → Change command interface (breaking)
```

### Description

✅ **Good descriptions**:

- "Professional git workflow with automated pre-commit checks"
- "Comprehensive project management with PRD generation and Linear integration"
- "Code quality tools with Python linting and expert agents"

❌ **Poor descriptions**:

- "Git stuff" (too vague)
- "This plugin helps you with git workflows and commits and PRs" (too long)
- "The best git plugin ever!" (marketing language)

### Keywords

Choose keywords that users would search for:

**Development**: `git`, `workflow`, `commits`, `pull-requests`, `automation`
**Languages**: `python`, `java`, `javascript`, `typescript`
**Tools**: `linting`, `formatting`, `testing`, `review`
**Domains**: `education`, `project-management`, `productivity`

---

## Common Patterns

### Minimal Plugin

```json
{
  "name": "simple-plugin",
  "version": "1.0.0",
  "description": "A simple example plugin",
  "author": {
    "name": "Your Name"
  }
}
```

### Full-Featured Plugin

```json
{
  "name": "advanced-plugin",
  "version": "2.1.0",
  "displayName": "Advanced Plugin",
  "description": "Comprehensive toolset with multiple features",
  "keywords": [
    "productivity",
    "automation",
    "development",
    "tools"
  ],
  "author": {
    "name": "Your Organization",
    "email": "support@example.com",
    "url": "https://example.com"
  },
  "license": "MIT",
  "homepage": "https://example.com/plugins/advanced",
  "repository": "https://github.com/org/advanced-plugin"
}
```

---

## Troubleshooting

### Validation Errors

**Error**: "Invalid plugin name format"

**Solution**: Ensure name uses only lowercase letters, numbers, and hyphens

```json
// ❌ Wrong
"name": "My_Plugin"

// ✅ Correct
"name": "my-plugin"
```

**Error**: "Invalid version format"

**Solution**: Use semantic versioning (MAJOR.MINOR.PATCH)

```json
// ❌ Wrong
"version": "1.0"

// ✅ Correct
"version": "1.0.0"
```

**Error**: "Missing required field: author"

**Solution**: Add author object with at least a name

```json
"author": {
  "name": "Your Name"
}
```

---

## Related Resources

- **[marketplace.json](marketplace-json.md)** - Marketplace catalog schema
- **[Command Format](command-format.md)** - Command definition format
- **[Agent Format](agent-format.md)** - Agent definition format
- **[Plugin Development](../development/plugin-development.md)** - Complete development guide

