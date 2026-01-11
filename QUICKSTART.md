# Quick Start Guide

Get started with Talent Factory Claude Code Plugins in 5 minutes.

## 1. Add Marketplace (30 seconds)

In your project, create `.claude/settings.json`:

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

## 2. Open Claude Code (10 seconds)

```bash
cd your-project
claude
```

Trust the repository when prompted.

## 3. Install Plugins (1 minute)

```
/plugin
→ Browse Plugins
→ talent-factory
→ Select plugins to install
```

## 4. Enable Plugins (30 seconds)

Add to `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": { /* ... */ },
  "enabledPlugins": {
    "git-workflow@talent-factory": true,
    "education@talent-factory": true
  }
}
```

## 5. Try It Out (2 minutes)

### Git Workflow
```
/commit
```
Follow prompts to create a professional commit.

### Education
```
/explain-code
```
Get detailed code explanations.

### Core Utilities
```
/check-commands
```
Validate your command files.

## Popular Configurations

### For Students
```json
{
  "enabledPlugins": {
    "education@talent-factory": true,
    "code-quality@talent-factory": true,
    "git-workflow@talent-factory": true
  }
}
```

### For Teams
```json
{
  "enabledPlugins": {
    "git-workflow@talent-factory": true,
    "project-management@talent-factory": true,
    "code-quality@talent-factory": true
  }
}
```

### For Solo Developers
```json
{
  "enabledPlugins": {
    "git-workflow@talent-factory": true,
    "code-quality@talent-factory": true,
    "core@talent-factory": true
  }
}
```

## Next Steps

- 📖 Read [Full Documentation](./README.md)
- 🔧 See [Installation Guide](./INSTALLATION.md)
- 📦 Explore individual plugin READMEs
- 🤝 Join [GitHub Discussions](https://github.com/talent-factory/claude-plugins/discussions)

## Need Help?

- [Installation Issues](./INSTALLATION.md#troubleshooting)
- [GitHub Issues](https://github.com/talent-factory/claude-plugins/issues)
- Email: support@talent-factory.ch

---

**Time invested: 5 minutes**  
**Productivity boost: Immediate** 🚀
