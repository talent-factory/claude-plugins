# Getting Started

Welcome to the Talent Factory Claude Plugins! This guide will help you install and start using professional plugins for Claude Code.

---

## Prerequisites

Before you begin, ensure you have:

- **Claude Code** installed ([Installation Guide](https://docs.claude.com/en/docs/claude-code))
- **Git** installed (for git-workflow plugin)
- Basic familiarity with command-line interfaces

---

## Installation Steps

### 1. Add the Marketplace

Add the Talent Factory marketplace to your Claude Code settings:

=== "Manual Configuration"

    Edit `.claude/settings.json` in your project:

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

=== "Using Claude Code"

    1. Open Claude Code: `claude`
    2. Use the plugin command: `/plugin`
    3. Select **"Add Marketplace"**
    4. Enter: `talent-factory/claude-plugins`

### 2. Browse & Install Plugins

Once the marketplace is added:

```bash
# Open Claude Code
claude

# Browse plugins
/plugin

# Select "Browse Plugins" → "talent-factory"
# Choose plugins to install
```

### 3. Verify Installation

Check that plugins are enabled in `.claude/settings.json`:

```json
{
  "enabledPlugins": {
    "git-workflow@talent-factory": true,
    "project-management@talent-factory": true,
    "code-quality@talent-factory": true
  }
}
```

---

## Quick Start Guides

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } **5-Minute Quick Start**

    ---

    Get up and running with your first plugin in 5 minutes.

    [:octicons-arrow-right-24: Quick Start](quickstart.md)

-   :material-git:{ .lg .middle } **Your First Commit**

    ---

    Learn how to use `/commit` for professional git commits.

    [:octicons-arrow-right-24: First Commit Guide](../guides/first-commit.md)

-   :material-pull-request:{ .lg .middle } **Create Your First PR**

    ---

    Use `/create-pr` to create professional pull requests.

    [:octicons-arrow-right-24: First PR Guide](../guides/create-first-pr.md)

-   :material-clipboard-text:{ .lg .middle } **PRD-Based Workflow**

    ---

    Generate Product Requirements Documents with `/create-prd`.

    [:octicons-arrow-right-24: PRD Workflow](../guides/prd-workflow.md)

</div>

---

## Next Steps

After installation, explore:

1. **[Plugin Catalog](../plugins/index.md)** - Browse all available plugins
2. **[Guides & Tutorials](../guides/index.md)** - Learn common workflows
3. **[Reference Documentation](../reference/index.md)** - Technical details

---

## Troubleshooting

### Marketplace Not Found

If Claude Code can't find the marketplace:

1. Verify `.claude/settings.json` syntax is valid JSON
2. Restart Claude Code
3. Check GitHub repository is accessible: [talent-factory/claude-plugins](https://github.com/talent-factory/claude-plugins)

### Plugin Commands Not Working

If commands like `/commit` don't work:

1. Verify plugin is enabled in `.claude/settings.json`
2. Restart Claude Code session
3. Check plugin version compatibility

### Need Help?

- **GitHub Issues**: [Report a problem](https://github.com/talent-factory/claude-plugins/issues)
- **Discussions**: [Ask questions](https://github.com/talent-factory/claude-plugins/discussions)
- **Security**: [Report vulnerabilities](../community/security.md)

---

## What's Next?

<div class="grid" markdown>

=== "For Users"

    - Explore the [Plugin Catalog](../plugins/index.md)
    - Follow [step-by-step guides](../guides/index.md)
    - Join the [community](../community/index.md)

=== "For Developers"

    - Read the [Development Guide](../development/index.md)
    - Learn [plugin architecture](../development/architecture.md)
    - Start [contributing](../development/contributing.md)

</div>

