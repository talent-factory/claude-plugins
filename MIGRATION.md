# Migration Guide: From Dotfiles to Plugins

Guide for migrating from [talent-factory/dotfiles](https://github.com/talent-factory/dotfiles) to the new plugin system.

## Why Migrate?

### Benefits of Plugins

✅ **Modular Installation**: Install only what you need  
✅ **Automatic Updates**: Get new features automatically  
✅ **Team Consistency**: Easy to share across teams  
✅ **Better Discovery**: Browse available plugins  
✅ **Version Control**: Track plugin versions  
✅ **No Manual Copying**: Installation is automated  

### What Changes?

**Before (Dotfiles):**
```bash
# Clone entire repo
git clone https://github.com/talent-factory/dotfiles ~/.dotfiles

# Run installer
cd ~/.dotfiles
./install.sh --interactive

# Select AI agents
# Manually symlink or copy files
```

**After (Plugins):**
```json
// .claude/settings.json
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

Then: `/plugin` → Browse → Install

## Migration Path

### Option 1: Fresh Start (Recommended)

Best for most users.

#### Step 1: Backup Current Setup
```bash
# Backup your current Claude configs
cp -r ~/.claude ~/.claude.backup
cp -r .claude .claude.backup
```

#### Step 2: Remove Old Symlinks
```bash
# Check current symlinks
ls -la ~/.claude/commands
ls -la ~/.claude/agents

# Remove old symlinks
rm ~/.claude/commands/*
rm ~/.claude/agents/*
```

#### Step 3: Install Plugins
Follow the [Quick Start Guide](https://talent-factory.github.io/claude-plugins/getting-started/quickstart/)

#### Step 4: Verify
```bash
claude
/plugin
# Check that plugins are loaded
```

### Option 2: Gradual Migration

Keep both systems during transition.

#### Step 1: Install Plugins
Add marketplace and install plugins (see Quick Start).

#### Step 2: Test Side-by-Side
Keep dotfiles symlinks active while testing plugins.

Commands will be namespaced:
- Dotfiles: `/commit`
- Plugin: `git-workflow:commit`

#### Step 3: Switch When Ready
```bash
# Disable dotfiles commands
rm ~/.claude/commands/*

# Plugins become default
# /commit now uses plugin version
```

### Option 3: Keep Both

Use dotfiles for non-Claude agents, plugins for Claude.

**Dotfiles**: Augment, Windsurf, Copilot  
**Plugins**: Claude Code only

```bash
# Keep dotfiles installed
# They manage other AI agents

# Add plugins for Claude
# Best of both worlds
```

## Command Mapping

### Git Workflow

| Dotfiles | Plugin | Notes |
|----------|--------|-------|
| `~/.claude/commands/commit.md` | `git-workflow:commit` | Enhanced with more checks |
| `~/.claude/commands/create-pr.md` | `git-workflow:create-pr` | Same functionality |

### Project Management

| Dotfiles | Plugin | Notes |
|----------|--------|-------|
| `~/.claude/commands/create-prd.md` | `project-management:create-prd` | Improved template |
| `~/.claude/commands/create-plan.md` | `project-management:create-plan` | Enhanced Linear integration |

### Education

| Dotfiles | Plugin | Notes |
|----------|--------|-------|
| Custom explain commands | `education:explain-code` | New unified command |
| N/A | `education:java-tutor` (agent) | New agent system |

### Core Utilities

| Dotfiles | Plugin | Notes |
|----------|--------|-------|
| `~/.claude/commands/check-agents.md` | `core:check-agents` | Same functionality |
| `~/.claude/commands/check-commands.md` | `core:check-commands` | Enhanced validation |

## Feature Parity

All commands from dotfiles are available in plugins with improvements:

### Git Workflow Plugin
✅ All git commands  
✅ Pre-commit validation  
✅ PR templates  
**New:** Better error handling  
**New:** More validation checks  

### Education Plugin
✅ Code explanation  
**New:** Java Tutor agent  
**New:** Student level adaptation  
**New:** Practice exercises  

### Core Plugin
✅ Command validation  
✅ Agent checking  
**New:** Automated reports  
**New:** Fix suggestions  

## Configuration Transfer

### Settings Migration

**Dotfiles `.env`** → **Plugin Settings**

```bash
# Old: dotfiles/.env
GITHUB_TOKEN=xxx
LINEAR_API_KEY=yyy

# New: .claude/settings.json
{
  "env": {
    "GITHUB_TOKEN": "xxx",
    "LINEAR_API_KEY": "yyy"
  }
}
```

### Custom Commands

If you created custom commands in dotfiles:

#### Step 1: Extract Command
```bash
# Copy your custom command
cp ~/.dotfiles/agents/claude/commands/my-custom-command.md ~/my-command.md
```

#### Step 2: Create Local Plugin
```bash
mkdir -p my-plugins/custom/.claude-plugin/commands
cp ~/my-command.md my-plugins/custom/commands/
```

#### Step 3: Load Local Plugin
```bash
claude --plugin-dir ~/my-plugins/custom
```

Or add to marketplace for team use.

## Troubleshooting

### Commands Not Found

**Problem:** Can't find commands after migration

**Solution:**
1. Verify plugins are enabled: `/plugin`
2. Check `.claude/settings.json` syntax
3. Restart Claude Code

### Duplicate Commands

**Problem:** Commands from both dotfiles and plugins

**Solution:**
1. Remove dotfiles symlinks
2. Or use namespaced commands: `plugin-name:command`

### Custom Scripts Broken

**Problem:** Custom scripts reference old paths

**Solution:**
Update scripts to use new plugin system or keep dotfiles for those scripts.

## Rollback Plan

If you need to rollback:

```bash
# Restore backup
rm -rf ~/.claude
mv ~/.claude.backup ~/.claude

# Reinstall dotfiles
cd ~/.dotfiles
./install.sh
```

## Team Migration

For teams using dotfiles:

### Phase 1: Pilot (Week 1)
- 2-3 team members test plugins
- Gather feedback
- Document issues

### Phase 2: Gradual Rollout (Week 2-3)
- Share marketplace config
- Team members install at their pace
- Support available

### Phase 3: Full Migration (Week 4)
- All team members on plugins
- Remove dotfiles from workflow
- Update documentation

## Best Practices

### During Migration

1. ✅ Keep backups
2. ✅ Test in non-critical project first
3. ✅ Document custom commands
4. ✅ Communicate with team
5. ✅ Plan rollback if needed

### After Migration

1. ✅ Remove old symlinks
2. ✅ Update documentation
3. ✅ Share team configuration
4. ✅ Provide feedback
5. ✅ Contribute improvements

## Getting Help

- **Migration Issues:** [Open Issue](https://github.com/talent-factory/claude-plugins/issues)
- **Questions:** [GitHub Discussions](https://github.com/talent-factory/claude-plugins/discussions)
- **Email:** support@talent-factory.ch

## Next Steps

1. ✅ Complete migration
2. 📖 Read plugin documentation
3. 🎯 Customize for your workflow
4. 🤝 Share with team
5. 💡 Contribute back

---

**Migration Difficulty:** Easy  
**Time Required:** 30 minutes  
**Risk Level:** Low (reversible)  
**Reward:** Immediate productivity boost 🚀
