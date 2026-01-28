# Plugin Development Guide

A comprehensive guide to creating Claude Code plugins for the Talent Factory marketplace.

---

## Overview

Claude Code plugins are modular extensions that add commands, agents, and skills to Claude Code. They are distributed through marketplaces and installed by users via settings configuration.

### What You'll Learn

- How to structure a plugin
- Creating commands, agents, and skills
- Writing effective plugin documentation
- Testing and validation
- Publishing to the marketplace

### Prerequisites

- Claude Code installed
- Git for version control
- Basic understanding of Markdown and JSON
- Familiarity with YAML frontmatter

---

## Plugin Structure

### Required Files

Every plugin needs at minimum:

```
plugins/your-plugin/
├── .claude-plugin/
│   └── plugin.json      # Plugin metadata (required)
├── commands/
│   └── my-command.md    # At least one command
└── README.md            # Plugin documentation (required)
```

### Optional Components

```
plugins/your-plugin/
├── .claude-plugin/
│   └── plugin.json
├── commands/            # User-invocable commands
│   ├── command1.md
│   └── command2.md
├── agents/              # Specialized AI assistants
│   └── my-agent.md
├── skills/              # Reusable capabilities
│   └── my-skill/
│       ├── SKILL.md
│       └── scripts/
├── references/          # Supporting documentation
│   └── command1/
│       ├── details.md
│       └── examples.md
└── README.md
```

---

## Creating plugin.json

The `plugin.json` file defines your plugin's metadata:

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "displayName": "My Plugin",
  "description": "Brief description of what your plugin does",
  "keywords": ["tag1", "tag2", "tag3"],
  "author": "Your Name",
  "license": "MIT"
}
```

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Unique identifier (kebab-case) |
| `version` | string | Semantic version (e.g., `1.0.0`) |

### Recommended Fields

| Field | Type | Description |
|-------|------|-------------|
| `displayName` | string | Human-readable name |
| `description` | string | Brief description (1-2 sentences) |
| `keywords` | string[] | Searchable tags |
| `author` | string | Creator name or organization |
| `license` | string | License identifier (e.g., `MIT`) |

---

## Writing Commands

Commands are the primary way users interact with your plugin. They are invoked with `/command-name`.

### Command File Structure

Create a Markdown file in `commands/`:

```markdown
---
description: Brief description of the command
category: develop
argument-hint: "<required-arg> [optional-arg]"
allowed-tools:
  - "Bash(git *)"
  - Read
  - Write
  - Glob
---

# Command Title

Clear instructions for Claude to follow when this command is invoked.

## Purpose

Explain what this command does and when to use it.

## Usage

/my-command <argument>
/my-command --option value

## Instructions

1. First, analyze the user's input
2. Then, perform the main operation
3. Show results to the user
4. Handle any errors gracefully

## Examples

### Basic Usage

/my-command "hello world"

### With Options

/my-command --verbose "detailed output"
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `description` | Yes | Brief command description |
| `category` | No | Command category (e.g., `develop`, `project`) |
| `argument-hint` | No | Hint for argument format |
| `allowed-tools` | No | Tools the command may use |

### Tool Permissions

Use `allowed-tools` to restrict what a command can do:

```yaml
allowed-tools:
  - "Bash(git *)"          # Only git commands
  - "Bash(gh *)"           # GitHub CLI commands
  - Read                    # Read files
  - Write                   # Write files
  - Edit                    # Edit files
  - Glob                    # Find files
  - Grep                    # Search files
  - AskUserQuestion         # Ask user for input
  - TodoWrite               # Track progress
  - mcp__linear__*          # Linear MCP tools
```

### Using Arguments

Reference user-provided arguments with `$ARGUMENTS`:

```markdown
---
argument-hint: "<feature description>"
---

# Create PRD

Generate a Product Requirements Document for the described feature.

**Feature description**: $ARGUMENTS
```

### Referencing External Documentation

Keep commands concise by linking to reference files:

```markdown
## Commit Types

See [commit-types.md](../references/commit/commit-types.md) for the full list.

## Best Practices

Details: [best-practices.md](../references/commit/best-practices.md)
```

---

## Writing Agents

Agents are specialized AI assistants with domain-specific expertise.

### Agent File Structure

Create a Markdown file in `agents/`:

```markdown
---
name: my-agent
description: Expert in specific domain
color: blue
---

# My Agent

You are an expert in [specific domain].

## Expertise

- Area of expertise 1
- Area of expertise 2
- Area of expertise 3

## Approach

When helping users, you:

1. **Understand** the user's needs
2. **Plan** a solution approach
3. **Execute** step by step
4. **Verify** the results

## Communication Style

- Be clear and concise
- Provide code examples
- Explain reasoning
- Ask clarifying questions when needed

## Examples

### Example: User asks about X

User: "How do I implement X?"

You should:
1. Explain the concept
2. Show a minimal example
3. Point out common pitfalls
```

### Agent Frontmatter

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique agent identifier |
| `description` | Yes | Brief agent description |
| `color` | No | UI color (`blue`, `green`, `purple`, `orange`, `red`) |

### Color Convention

| Color | Domain | Examples |
|-------|--------|----------|
| `blue` | Development | java-developer, python-expert |
| `green` | Testing/quality | code-reviewer |
| `purple` | Architecture | agent-expert |
| `orange` | Education | java-tutor |
| `red` | Security | security-auditor |

---

## Writing Skills

Skills are reusable capabilities that can include scripts and configuration.

### Skill Structure

```text
skills/my-skill/
├── SKILL.md              # Skill definition (required)
├── config/               # Configuration files
│   └── settings.json
├── scripts/              # Supporting scripts
│   ├── main.py
│   └── utils.py
└── docs/                 # Skill documentation
    └── usage.md
```

### SKILL.md Format

```markdown
---
name: my-skill
description: What this skill does
---

# My Skill

Instructions for how Claude should use this skill.

## When to Use

Describe the scenarios where this skill applies.

## How It Works

Step-by-step process the skill follows.

## Configuration

Reference configuration files if needed.
```

---

## Testing Your Plugin

### Local Testing

```bash
# Test your plugin in isolation
claude --plugin-dir ./plugins/my-plugin

# Test all plugins together
claude --plugin-dir .
```

### Validation

```bash
# Use core plugin validation
/check-commands    # Validate command files
/check-agents      # Validate agent definitions
/run-ci            # Run full CI checks locally
```

See the [Testing Guide](testing.md) for comprehensive testing strategies.

---

## Publishing

### 1. Update Marketplace

Add your plugin to `.claude-plugin/marketplace.json`:

```json
{
  "name": "my-plugin",
  "description": "What your plugin does",
  "source": "./plugins/my-plugin",
  "version": "1.0.0",
  "tags": ["relevant", "keywords"]
}
```

### 2. Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- **Major** (1.0.0): Breaking changes
- **Minor** (0.1.0): New features, backwards compatible
- **Patch** (0.0.1): Bug fixes

### 3. Submission Checklist

- [ ] Plugin structure follows conventions
- [ ] `plugin.json` has all required fields
- [ ] README is comprehensive
- [ ] All commands tested and working
- [ ] Agents tested (if applicable)
- [ ] No secrets or credentials in files
- [ ] Version numbers aligned (plugin.json, marketplace.json)
- [ ] CHANGELOG updated
- [ ] PR created with detailed description

### 4. Review Process

1. Fork the repository
2. Create a feature branch: `feature/add-my-plugin`
3. Add your plugin files
4. Test locally
5. Submit a PR
6. CI validates automatically
7. Maintainer reviews
8. Merge and deploy

---

## Common Patterns

### Command with Pre-Checks

```markdown
## Instructions

1. **Pre-checks**
   - Verify git repository exists
   - Check for uncommitted changes
   - Validate prerequisites

2. **Main Operation**
   - Perform the core action
   - Handle errors at each step

3. **Post-actions**
   - Show summary to user
   - Suggest next steps
```

### Command Delegating to Another Command

```markdown
## Instructions

If uncommitted changes are detected:
1. Call `/commit` to create a commit first
2. Then proceed with PR creation
```

### Multi-Provider Command

```markdown
## Usage

/my-command                  # Default (filesystem)
/my-command --linear         # Linear integration

## Provider Selection

### Filesystem (Default)
When no flags are specified, use local filesystem.

### Linear (`--linear`)
When `--linear` is specified, use Linear MCP tools.
```

---

## Related Resources

- **[Architecture](architecture.md)** - Marketplace architecture
- **[Testing](testing.md)** - Test your plugins
- **[Best Practices](best-practices.md)** - Quality guidelines
- **[CI/CD](ci-cd.md)** - Automated validation
- **[Contributing](contributing.md)** - Submission process
- **[Command Format Reference](../reference/command-format.md)** - Command specification
- **[Agent Format Reference](../reference/agent-format.md)** - Agent specification
