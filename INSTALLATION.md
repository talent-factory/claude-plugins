# Installation Guide

Complete guide to installing and using Talent Factory Claude Code plugins.

## Prerequisites

- Claude Code installed ([Installation Guide](https://docs.claude.com/en/docs/claude-code))
- Git installed
- Active Anthropic account

## Installation Methods

### Method 1: Via Marketplace (Recommended)

This method automatically installs and updates plugins.

#### Step 1: Add Marketplace

In your project root, create or edit `.claude/settings.json`:

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

#### Step 2: Trust the Repository

When you open the project in Claude Code, you'll be prompted to trust the repository. Click "Trust" to enable the marketplace.

#### Step 3: Browse and Install

```bash
# Open Claude Code
claude

# In the Claude prompt:
/plugin

# Select "Browse Plugins"
# Choose "talent-factory" marketplace
# Select plugins to install
```

#### Step 4: Enable Plugins

After installation, enable the plugins you want to use:

```json
{
  "enabledPlugins": {
    "git-workflow@talent-factory": true,
    "education@talent-factory": true
  }
}
```

### Method 2: Local Development

For testing or contributing to plugins.

#### Step 1: Clone Repository

```bash
git clone https://github.com/talent-factory/claude-plugins.git
cd claude-plugins
```

#### Step 2: Test Single Plugin

```bash
# Test git-workflow plugin
claude --plugin-dir ./plugins/git-workflow

# In Claude:
/commit
```

#### Step 3: Test Entire Marketplace

```bash
# Load all plugins
claude --plugin-dir .

# Verify plugins loaded
/plugin
```

## Configuration

### User-Level Settings

Install plugins for all your projects:

`~/.claude/settings.json`:
```json
{
  "extraKnownMarketplaces": {
    "talent-factory": {
      "source": {
        "source": "github",
        "repo": "talent-factory/claude-plugins"
      }
    }
  },
  "enabledPlugins": {
    "git-workflow@talent-factory": true,
    "core@talent-factory": true
  }
}
```

### Project-Level Settings

Install plugins for a specific project:

`.claude/settings.json` (in project root):
```json
{
  "extraKnownMarketplaces": {
    "talent-factory": {
      "source": {
        "source": "github",
        "repo": "talent-factory/claude-plugins"
      }
    }
  },
  "enabledPlugins": {
    "git-workflow@talent-factory": true,
    "project-management@talent-factory": true
  }
}
```

### Team Settings

Share plugin configuration with your team by committing `.claude/settings.json` to version control.

Team members will be prompted to:

1. Trust the marketplace
2. Install suggested plugins

They can skip unwanted plugins while accepting others.

## Plugin Selection Guide

### For Students

Recommended plugins:
```json
{
  "enabledPlugins": {
    "education@talent-factory": true,
    "code-quality@talent-factory": true,
    "git-workflow@talent-factory": true
  }
}
```

### For Development Teams

Recommended plugins:
```json
{
  "enabledPlugins": {
    "git-workflow@talent-factory": true,
    "project-management@talent-factory": true,
    "code-quality@talent-factory": true,
    "core@talent-factory": true
  }
}
```

### For Educators

Recommended plugins:
```json
{
  "enabledPlugins": {
    "education@talent-factory": true,
    "code-quality@talent-factory": true,
    "core@talent-factory": true
  }
}
```

### For Individual Developers

Choose what you need:
```json
{
  "enabledPlugins": {
    "git-workflow@talent-factory": true,
    "code-quality@talent-factory": true
  }
}
```

## Verification

### Check Installed Plugins

```bash
/plugin
# Select "Manage Plugins"
# View installed and enabled plugins
```

### Test Commands

```bash
# Test git-workflow
/commit

# Test education
/explain-code

# Test core utilities
/check-commands
```

### View Plugin Details

```bash
/plugin
# Select "Manage Plugins"
# Click on a plugin to see:
# - Version
# - Commands
# - Agents
# - Description
```

## Updating Plugins

### Automatic Updates (Marketplace)

Claude Code checks for updates when you start a session. Updates are downloaded automatically.

### Manual Update (Local Development)

```bash
cd claude-plugins
git pull origin main
```

Then restart Claude Code.

## Uninstalling Plugins

### Disable Plugin

In `.claude/settings.json`:
```json
{
  "enabledPlugins": {
    "git-workflow@talent-factory": false
  }
}
```

### Remove Plugin

```bash
/plugin
# Select "Manage Plugins"
# Find plugin
# Click "Uninstall"
```

### Remove Marketplace

Remove from `.claude/settings.json`:
```json
{
  "extraKnownMarketplaces": {
    // Remove "talent-factory" entry
  }
}
```

## Troubleshooting

### Plugin Not Appearing

**Problem:** Marketplace added but plugins don't appear

**Solutions:**

1. Restart Claude Code
2. Verify `.claude/settings.json` syntax
3. Check you trusted the repository
4. Run `/plugin` and manually browse

### Commands Not Working

**Problem:** Commands appear but don't execute

**Solutions:**

1. Check plugin is enabled in settings
2. Verify plugin is compatible with your Claude Code version
3. Check command syntax: `/command-name` not `command-name`

### Marketplace Not Loading

**Problem:** Can't add marketplace

**Solutions:**

1. Verify GitHub repository exists and is public
2. Check internet connection
3. Verify JSON syntax in settings.json
4. Check repository URL is correct

### Plugin Validation Errors

**Problem:** Plugin fails validation

**Solutions:**

1. Run `/plugin validate .` in plugin directory
2. Check plugin.json for required fields
3. Verify commands have correct file extension (.md)
4. Ensure no syntax errors in markdown files

## Advanced Configuration

### Custom Plugin Directory

Test plugins from a different location:

```bash
claude --plugin-dir /path/to/plugins
```

### Multiple Marketplaces

Add multiple plugin sources:

```json
{
  "extraKnownMarketplaces": {
    "talent-factory": {
      "source": {
        "source": "github",
        "repo": "talent-factory/claude-plugins"
      }
    },
    "my-company": {
      "source": {
        "source": "github",
        "repo": "my-company/claude-plugins"
      }
    }
  }
}
```

### Managed Settings (Enterprise)

For organization-wide deployment, use managed settings:

`/etc/claude/managed-settings.json` (macOS/Linux)
or
`C:\ProgramData\claude\managed-settings.json` (Windows)

## Getting Help

- **Documentation:** [Talent Factory Claude Plugins](https://talent-factory.github.io/claude-plugins/)
- **Issues:** [GitHub Issues](https://github.com/talent-factory/claude-plugins/issues)
- **Discussions:** [GitHub Discussions](https://github.com/talent-factory/claude-plugins/discussions)
- **Email:** support@talent-factory.ch

## Next Steps

1. ✅ Install plugins
2. 📖 Read plugin documentation
3. 🎯 Try example commands
4. 🤝 Share with your team
5. 💡 Provide feedback

Happy coding with Claude! 🚀
