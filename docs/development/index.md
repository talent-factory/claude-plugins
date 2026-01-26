# Plugin Development

Welcome to the Talent Factory Claude Plugins development guide! This section helps you create, test, and contribute plugins to the marketplace.

---

## Quick Links

<div class="grid cards" markdown>

-   :material-book-open-variant:{ .lg .middle } **Plugin Development Guide**

    ---

    Comprehensive guide to creating Claude Code plugins.

    [:octicons-arrow-right-24: Read Guide](plugin-development.md)

-   :material-git:{ .lg .middle } **Contributing**

    ---

    Learn how to contribute to existing plugins or submit new ones.

    [:octicons-arrow-right-24: Contributing Guide](contributing.md)

-   :material-sitemap:{ .lg .middle } **Architecture**

    ---

    Understand the marketplace and plugin architecture.

    [:octicons-arrow-right-24: Architecture Overview](architecture.md)

-   :material-test-tube:{ .lg .middle } **Testing**

    ---

    Test your plugins locally before submission.

    [:octicons-arrow-right-24: Testing Guide](testing.md)

-   :material-robot:{ .lg .middle } **CI/CD**

    ---

    Automated validation and deployment workflows.

    [:octicons-arrow-right-24: CI/CD Guide](ci-cd.md)

-   :material-star:{ .lg .middle } **Best Practices**

    ---

    Follow best practices for high-quality plugins.

    [:octicons-arrow-right-24: Best Practices](best-practices.md)

</div>

---

## Getting Started

### Prerequisites

- **Claude Code** installed
- **Git** for version control
- Basic understanding of Markdown
- Familiarity with JSON

### Development Workflow

```mermaid
graph LR
    A[Fork Repository] --> B[Create Plugin]
    B --> C[Write Commands]
    C --> D[Test Locally]
    D --> E[Validate]
    E --> F[Submit PR]
    F --> G[CI Validation]
    G --> H[Review]
    H --> I[Merge]
    I --> J[Deploy]
```

---

## Plugin Structure

A typical plugin has this structure:

```
plugins/your-plugin/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata
├── commands/
│   ├── command1.md          # Command definitions
│   └── command2.md
├── agents/                  # Optional
│   └── agent1.md            # Agent definitions
├── skills/                  # Optional
│   └── skill1/              # Skill definitions
├── references/              # Optional
│   └── docs.md              # Reference documentation
└── README.md                # Plugin documentation
```

---

## Quick Start: Create Your First Plugin

### 1. Fork the Repository

```bash
git clone https://github.com/YOUR-USERNAME/claude-plugins.git
cd claude-plugins
git checkout -b feature/add-my-plugin
```

### 2. Create Plugin Structure

```bash
mkdir -p plugins/my-plugin/.claude-plugin
mkdir -p plugins/my-plugin/commands
```

### 3. Create `plugin.json`

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "displayName": "My Plugin",
  "description": "Brief description of your plugin",
  "keywords": ["tag1", "tag2"],
  "author": "Your Name",
  "license": "MIT"
}
```

### 4. Create a Command

Create `plugins/my-plugin/commands/my-command.md`:

```markdown
# My Command

Brief description of what this command does.

## Usage

/my-command [options]

## Purpose

Explain when and why to use this command.

## Instructions

1. Step-by-step instructions
2. What the command should do
3. Expected outcomes

## Examples

### Example 1: Basic Usage

/my-command

### Example 2: With Options

/my-command --option value
```

### 5. Create README

Create `plugins/my-plugin/README.md`:

```markdown
# My Plugin

Description of your plugin.

## Commands

### `/my-command`

Brief description.

**Usage:**
/my-command [options]

## Installation

See [Installation Guide](../../docs/getting-started/installation.md)
```

### 6. Update Marketplace

Add your plugin to `.claude-plugin/marketplace.json`:

```json
{
  "plugins": [
    {
      "name": "my-plugin",
      "description": "Brief description",
      "source": "./plugins/my-plugin",
      "version": "1.0.0",
      "tags": ["tag1", "tag2"]
    }
  ]
}
```

### 7. Test Locally

```bash
# Test your plugin
claude --plugin-dir ./plugins/my-plugin

# In Claude Code session
/my-command
```

### 8. Validate

```bash
# Use core plugin validation
/check-commands
/check-agents
```

### 9. Submit PR

```bash
git add .
git commit -m "✨ feat: Füge my-plugin hinzu"
git push origin feature/add-my-plugin
```

Create a pull request on GitHub.

---

## Development Tools

### Core Plugin Commands

The `core` plugin provides development utilities:

- `/check-commands` - Validate command markdown files
- `/check-agents` - Validate agent definitions
- `/create-command` - Generate new command templates
- `/build-skill` - Create Claude Code Skills
- `/run-ci` - Run CI checks locally

### Local Testing

```bash
# Test single plugin
claude --plugin-dir ./plugins/your-plugin

# Test entire marketplace
claude --plugin-dir .
```

---

## Next Steps

<div class="grid" markdown>

=== "New to Plugin Development"

    1. Read [Plugin Development Guide](plugin-development.md)
    2. Study [Architecture](architecture.md)
    3. Follow [Best Practices](best-practices.md)
    4. Create your first plugin

=== "Ready to Contribute"

    1. Review [Contributing Guide](contributing.md)
    2. Check [open issues](https://github.com/talent-factory/claude-plugins/issues)
    3. Fork and create feature branch
    4. Submit pull request

=== "Need Help"

    1. Check [Testing Guide](testing.md)
    2. Review [CI/CD documentation](ci-cd.md)
    3. Ask in [Discussions](https://github.com/talent-factory/claude-plugins/discussions)
    4. Report issues on [GitHub](https://github.com/talent-factory/claude-plugins/issues)

</div>

