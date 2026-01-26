# Marketplace Setup

This guide explains how to add the Talent Factory marketplace to Claude Code and configure plugin settings.

---

## Adding the Marketplace

### Method 1: Manual Configuration (Recommended)

1. **Locate your settings file**:
   ```bash
   # In your project directory
   .claude/settings.json
   ```

2. **Add marketplace configuration**:
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

3. **Restart Claude Code**:
   ```bash
   # Exit current session (Ctrl+D or /exit)
   # Start new session
   claude
   ```

### Method 2: Using Claude Code UI

1. Open Claude Code: `claude`
2. Use plugin command: `/plugin`
3. Select **"Add Marketplace"**
4. Enter repository: `talent-factory/claude-plugins`
5. Confirm addition

---

## Enabling Plugins

After adding the marketplace, enable specific plugins:

### Via Settings File

Edit `.claude/settings.json`:

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
    "project-management@talent-factory": true,
    "code-quality@talent-factory": true,
    "education@talent-factory": true,
    "core@talent-factory": true,
    "obsidian@talent-factory": true
  }
}
```

### Via Claude Code UI

1. Use `/plugin` command
2. Select **"Browse Plugins"**
3. Choose **"talent-factory"** marketplace
4. Select plugins to enable
5. Confirm installation

---

## Verifying Installation

### Check Enabled Plugins

```bash
# In Claude Code session
/plugin

# Select "Manage Plugins"
# View enabled plugins list
```

### Test Plugin Commands

```bash
# Test git-workflow
/commit

# Test project-management
/create-prd

# Test code-quality
/review

# Test core utilities
/check
```

---

## Configuration Options

### Plugin-Specific Settings

Some plugins support additional configuration:

```json
{
  "enabledPlugins": {
    "git-workflow@talent-factory": true
  },
  "pluginSettings": {
    "git-workflow@talent-factory": {
      "defaultCommitType": "feat",
      "skipPreCommitChecks": false,
      "useSkills": true
    }
  }
}
```

!!! note "Plugin Settings"
    Not all plugins support custom settings. Check individual plugin documentation for available options.

---

## Updating Plugins

Claude Code automatically checks for plugin updates. To manually update:

1. Use `/plugin` command
2. Select **"Update Plugins"**
3. Choose plugins to update
4. Confirm update

---

## Troubleshooting

### Marketplace Not Found

**Problem**: Claude Code can't find the talent-factory marketplace.

**Solutions**:

1. Verify JSON syntax in `.claude/settings.json`
2. Check GitHub repository is accessible: [talent-factory/claude-plugins](https://github.com/talent-factory/claude-plugins)
3. Ensure you have internet connection
4. Restart Claude Code

### Plugins Not Loading

**Problem**: Enabled plugins don't appear in Claude Code.

**Solutions**:

1. Verify plugin names match exactly (case-sensitive)
2. Check `enabledPlugins` syntax:
   ```json
   "plugin-name@talent-factory": true
   ```
3. Restart Claude Code session
4. Check Claude Code version compatibility

### Commands Not Working

**Problem**: Plugin commands like `/commit` don't work.

**Solutions**:

1. Verify plugin is enabled in settings
2. Check command syntax (commands start with `/`)
3. Ensure you're in a valid project context
4. Review plugin-specific requirements (e.g., git repository for `/commit`)

---

## Advanced Configuration

### Multiple Marketplaces

You can add multiple marketplaces:

```json
{
  "extraKnownMarketplaces": {
    "talent-factory": {
      "source": {
        "source": "github",
        "repo": "talent-factory/claude-plugins"
      }
    },
    "other-marketplace": {
      "source": {
        "source": "github",
        "repo": "other-org/other-plugins"
      }
    }
  }
}
```

### Selective Plugin Loading

Enable only specific plugins you need:

```json
{
  "enabledPlugins": {
    "git-workflow@talent-factory": true,
    "core@talent-factory": true
  }
}
```

---

## Next Steps

- **[Quick Start Guide](quickstart.md)** - Start using plugins
- **[Plugin Catalog](../plugins/index.md)** - Explore available plugins
- **[Guides](../guides/index.md)** - Learn common workflows

