# marketplace.json Schema Reference

Complete technical reference for the `marketplace.json` configuration file that defines a Claude Code plugin marketplace.

---

## Overview

The `marketplace.json` file is the catalog for a Claude Code plugin marketplace. It lists all available plugins and provides marketplace metadata. Users add marketplaces to their Claude Code settings to discover and install plugins.

---

## Location

```
.claude-plugin/marketplace.json
```

**Required**: Yes (at repository root for marketplace)

---

## Schema

### Root Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Marketplace identifier (lowercase, hyphen-separated) |
| `version` | string | Yes | Marketplace schema version |
| `owner` | object | Yes | Marketplace owner information |
| `description` | string | Yes | Brief marketplace description |
| `plugins` | array | Yes | List of available plugins |

### Owner Object

```json
{
  "owner": {
    "name": "Talent Factory GmbH",
    "email": "support@talent-factory.ch",
    "url": "https://talent-factory.ch"
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Owner name or organization |
| `email` | string | Yes | Contact email address |
| `url` | string | No | Owner website URL |

### Plugin Entry

Each plugin in the `plugins` array:

```json
{
  "name": "git-workflow",
  "description": "Professional git workflow tools",
  "source": "./plugins/git-workflow",
  "version": "2.0.0",
  "tags": ["git", "workflow", "productivity"]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Plugin identifier (must match plugin.json) |
| `description` | string | Yes | Brief plugin description |
| `source` | string | Yes | Relative path to plugin directory |
| `version` | string | Yes | Plugin version (must match plugin.json) |
| `tags` | array | Yes | Search keywords for discoverability |

---

## Complete Example

```json
{
  "name": "talent-factory",
  "version": "1.0.0",
  "owner": {
    "name": "Talent Factory GmbH",
    "email": "support@talent-factory.ch",
    "url": "https://talent-factory.ch"
  },
  "description": "Professional Claude Code plugins for software development and education",
  "plugins": [
    {
      "name": "git-workflow",
      "description": "Professional git workflow with automated pre-commit checks, emoji conventional commits, PR management, and comprehensive references",
      "source": "./plugins/git-workflow",
      "version": "2.0.0",
      "tags": [
        "git",
        "workflow",
        "productivity",
        "commits",
        "pull-requests",
        "automation",
        "pre-commit",
        "conventional-commits"
      ]
    },
    {
      "name": "project-management",
      "description": "Comprehensive project management with PRD generation, project planning, task implementation, Linear integration, and git worktree workflow",
      "source": "./plugins/project-management",
      "version": "2.2.0",
      "tags": [
        "planning",
        "prd",
        "linear",
        "project-management",
        "agile",
        "worktree",
        "task-management"
      ]
    },
    {
      "name": "code-quality",
      "description": "Comprehensive code quality with Python linting and expert agents for Python, Java, and Frontend development",
      "source": "./plugins/code-quality",
      "version": "2.0.0",
      "tags": [
        "review",
        "quality",
        "refactoring",
        "best-practices",
        "python",
        "java",
        "react",
        "linting"
      ]
    }
  ]
}
```

---

## Validation Rules

### Marketplace Name

- **Format**: Lowercase letters, numbers, and hyphens only
- **Pattern**: `^[a-z0-9][a-z0-9-]*$`
- **Examples**:
    - ✅ `talent-factory`
    - ✅ `my-marketplace`
    - ✅ `company-plugins`
    - ❌ `Talent-Factory` (uppercase)
    - ❌ `talent_factory` (underscore)

### Version

- **Format**: Semantic versioning (MAJOR.MINOR.PATCH)
- **Current**: `1.0.0` (marketplace schema version)
- **Note**: This is the schema version, not the marketplace content version

### Plugin Entries

Each plugin entry must:

1. **Match plugin.json**: `name` and `version` must match the plugin's `plugin.json`
2. **Valid source**: Path must point to existing plugin directory
3. **Unique names**: No duplicate plugin names in the array
4. **Consistent tags**: Use standardized tag vocabulary

---

## Best Practices

### Marketplace Organization

✅ **Do**:

- Group related plugins together
- Use consistent tag vocabulary across plugins
- Keep descriptions concise but informative
- Maintain version consistency with plugin.json files
- Order plugins logically (by category or popularity)

❌ **Don't**:

- List plugins that don't exist in the repository
- Use inconsistent versioning between marketplace.json and plugin.json
- Duplicate plugin entries
- Use vague or marketing-heavy descriptions

### Plugin Descriptions

**Good descriptions** explain what the plugin does and its key features:

```json
{
  "description": "Professional git workflow with automated pre-commit checks, emoji conventional commits, and PR management"
}
```

**Poor descriptions** are vague or too brief:

```json
{
  "description": "Git tools"  // Too vague
}
```

### Tag Strategy

Use a consistent tag vocabulary across your marketplace:

**Development Tags**: `git`, `workflow`, `commits`, `pull-requests`, `automation`
**Language Tags**: `python`, `java`, `javascript`, `typescript`, `react`
**Feature Tags**: `linting`, `formatting`, `testing`, `review`, `refactoring`
**Domain Tags**: `education`, `project-management`, `productivity`, `integration`

**Example tag sets**:

```json
// Git plugin
"tags": ["git", "workflow", "commits", "automation"]

// Python quality plugin
"tags": ["python", "linting", "quality", "best-practices"]

// Education plugin
"tags": ["education", "teaching", "learning", "students"]
```

---

## User Installation

Users add your marketplace to their `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "talent-factory": {
      "source": {
        "source": "github",
        "repo": "talent-factory/claude-plugins"
      }
    }
  }
}
```

Then enable specific plugins:

```json
{
  "enabledPlugins": {
    "git-workflow@talent-factory": true,
    "code-quality@talent-factory": true
  }
}
```

---

## Marketplace Discovery Flow

```
1. User adds marketplace to settings
   └─> Claude Code fetches marketplace.json from GitHub

2. Claude Code indexes plugins
   └─> Reads each plugin's .claude-plugin/plugin.json
   └─> Validates structure and metadata

3. User browses marketplace
   └─> /plugin command shows available plugins
   └─> Filtered by tags and search terms

4. User installs plugin
   └─> Plugin added to enabledPlugins
   └─> Commands/agents become available
```

---

## Maintenance

### Adding a New Plugin

1. Create plugin directory structure
2. Add plugin.json with metadata
3. Add plugin entry to marketplace.json
4. Ensure version numbers match
5. Test locally with `claude --plugin-dir .`
6. Commit and push changes

### Updating Plugin Version

1. Update version in `plugins/NAME/.claude-plugin/plugin.json`
2. Update version in `.claude-plugin/marketplace.json`
3. Update CHANGELOG.md with changes
4. Commit with version bump message

### Removing a Plugin

1. Remove plugin entry from marketplace.json
2. (Optional) Archive plugin directory
3. Document removal in CHANGELOG.md
4. Notify users if plugin was widely used

---

## Troubleshooting

### Plugin Not Appearing

**Problem**: Plugin doesn't show in `/plugin` browse list

**Solutions**:

1. Verify plugin entry exists in marketplace.json
2. Check that `source` path is correct
3. Ensure plugin.json exists at `source/.claude-plugin/plugin.json`
4. Validate JSON syntax (no trailing commas, proper quotes)

### Version Mismatch Error

**Problem**: "Version mismatch between marketplace.json and plugin.json"

**Solution**: Ensure versions match exactly

```json
// marketplace.json
{
  "name": "git-workflow",
  "version": "2.0.0",  // Must match ↓
  ...
}

// plugins/git-workflow/.claude-plugin/plugin.json
{
  "name": "git-workflow",
  "version": "2.0.0",  // Must match ↑
  ...
}
```

### Invalid JSON Syntax

**Problem**: Marketplace fails to load

**Common issues**:

```json
// ❌ Trailing comma
{
  "plugins": [
    { "name": "plugin1" },
    { "name": "plugin2" },  // Remove this comma
  ]
}

// ✅ Correct
{
  "plugins": [
    { "name": "plugin1" },
    { "name": "plugin2" }
  ]
}
```

---

## Related Resources

- **[plugin.json](plugin-json.md)** - Plugin metadata schema
- **[Plugin Development](../development/plugin-development.md)** - Create plugins
- **[Installation Guide](../getting-started/installation.md)** - User installation
- **[Marketplace Setup](../getting-started/marketplace-setup.md)** - Add marketplace to Claude Code

