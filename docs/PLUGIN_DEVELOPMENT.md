# Plugin Development Guide

This guide provides comprehensive instructions for developing Claude Code plugins for the Talent Factory marketplace.

## Table of Contents

1. [Overview](#overview)
2. [Plugin Structure](#plugin-structure)
3. [Creating a New Plugin](#creating-a-new-plugin)
4. [Commands](#commands)
5. [Agents](#agents)
6. [Testing](#testing)
7. [Documentation](#documentation)
8. [Publishing](#publishing)
9. [Best Practices](#best-practices)

## Overview

Claude Code plugins are modular extensions that add commands and agents to Claude Code. They are distributed through marketplaces and can be easily installed by users.

### What You'll Need

- Claude Code installed
- Basic understanding of Markdown
- Familiarity with YAML frontmatter
- Git for version control

## Plugin Structure

A typical plugin has the following structure:

```
plugins/your-plugin/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata
├── commands/
│   ├── command-1.md         # Command definition
│   └── command-2.md         # Another command
├── agents/
│   └── agent-1.md           # Agent definition (optional)
├── scripts/                 # Helper scripts (optional)
│   └── helper.sh
└── README.md                # Plugin documentation
```

### File Descriptions

**`.claude-plugin/plugin.json`**
- Required metadata file
- Defines plugin name, version, description
- Lists commands and agents

**`commands/*.md`**
- Command definitions in Markdown
- YAML frontmatter for metadata
- Command prompt in Markdown body

**`agents/*.md`**
- Agent definitions in Markdown
- YAML frontmatter for metadata
- Agent system prompt in Markdown body

**`README.md`**
- User-facing documentation
- Installation instructions
- Usage examples

## Creating a New Plugin

### Step 1: Plan Your Plugin

Before coding, define:
- **Purpose:** What problem does this solve?
- **Target Users:** Who will use this plugin?
- **Commands:** What commands will it provide?
- **Agents:** Does it need specialized agents?

### Step 2: Create Directory Structure

```bash
cd plugins
mkdir -p your-plugin/.claude-plugin
mkdir -p your-plugin/commands
mkdir -p your-plugin/agents  # if needed
```

### Step 3: Create plugin.json

Create `.claude-plugin/plugin.json`:

```json
{
  "name": "your-plugin",
  "version": "1.0.0",
  "description": "Brief description of your plugin",
  "author": "Your Name or Organization",
  "license": "MIT",
  "homepage": "https://github.com/talent-factory/claude-plugins",
  "repository": {
    "type": "git",
    "url": "https://github.com/talent-factory/claude-plugins.git"
  },
  "keywords": ["claude", "plugin", "your-category"],
  "commands": [
    {
      "name": "your-command",
      "description": "What this command does",
      "file": "commands/your-command.md"
    }
  ],
  "agents": [
    {
      "name": "your-agent",
      "description": "What this agent does",
      "file": "agents/your-agent.md"
    }
  ]
}
```

### Step 4: Create README.md

```markdown
# Your Plugin Name

Brief description of what your plugin does.

## Installation

Add to `.claude/settings.json`:

\`\`\`json
{
  "enabledPlugins": {
    "your-plugin@talent-factory": true
  }
}
\`\`\`

## Commands

### /your-command

Description of what this command does.

**Usage:**
\`\`\`
/your-command
\`\`\`

**Example:**
\`\`\`
/your-command --option value
\`\`\`

## License

MIT License - see LICENSE file for details
```

## Commands

Commands are user-invocable through the `/command-name` syntax.

### Command File Structure

Create `commands/your-command.md`:

```markdown
---
name: your-command
description: Brief description
parameters:
  - name: arg1
    description: First argument
    required: true
  - name: arg2
    description: Second argument
    required: false
    default: "default-value"
examples:
  - /your-command value1
  - /your-command value1 --arg2 value2
---

# Command Prompt

You are executing the `your-command` command.

## Purpose

Explain what this command does and when to use it.

## Instructions

1. First, do this
2. Then, do that
3. Finally, output results

## Output Format

Describe the expected output format.

## Example

Show an example of what the command produces.
```

### Command Best Practices

1. **Clear Purpose:** Each command should have a single, clear purpose
2. **Good Names:** Use descriptive, action-oriented names
3. **Documentation:** Include examples and usage instructions
4. **Error Handling:** Guide Claude on handling errors gracefully
5. **User Feedback:** Provide clear, actionable feedback to users

### Command Naming Conventions

- Use kebab-case: `create-pr`, `check-code`
- Start with a verb: `validate-`, `generate-`, `check-`
- Be descriptive: Avoid vague names like `do-thing`
- Keep it short: Aim for 2-3 words maximum

## Agents

Agents are specialized AI assistants with specific expertise.

### Agent File Structure

Create `agents/your-agent.md`:

```markdown
---
name: your-agent
description: Expert in specific domain
color: blue
model: sonnet
trigger:
  type: auto
  keywords:
    - keyword1
    - keyword2
  patterns:
    - "pattern to match"
---

# Your Agent Name

You are an expert in [specific domain]. You specialize in [specific tasks].

## Expertise

- Area 1
- Area 2
- Area 3

## Approach

When helping users, you:

1. **Understand:** First, understand the user's needs
2. **Plan:** Create a clear plan of action
3. **Execute:** Implement the solution step by step
4. **Verify:** Test and validate the results

## Communication Style

- Be clear and concise
- Provide examples
- Explain your reasoning
- Ask clarifying questions when needed

## Tools and Capabilities

You have access to:
- Tool 1: For doing X
- Tool 2: For doing Y

## Examples

### Example 1: [Scenario]

User: "How do I..."

You should:
1. Step 1
2. Step 2
3. Step 3

### Example 2: [Scenario]

User: "Can you help with..."

You should:
1. Step 1
2. Step 2
3. Step 3

## Limitations

Be aware of:
- Limitation 1
- Limitation 2

Always be honest when something is beyond your capabilities.
```

### Agent Best Practices

1. **Focused Expertise:** Each agent should have a clear domain
2. **Consistent Personality:** Maintain a consistent tone and approach
3. **Proactive:** Guide users even when they're not sure what they need
4. **Examples:** Include concrete examples of interactions
5. **Self-Aware:** Know and communicate limitations

### Agent Colors

Use consistent colors for agent types:
- `blue` - Development/coding agents
- `green` - Testing/quality agents
- `purple` - Architecture/design agents
- `orange` - Education/learning agents
- `red` - Security/critical agents

## Testing

### Local Testing

Test your plugin locally before committing:

```bash
# Test single plugin
claude --plugin-dir ./plugins/your-plugin

# Test with existing plugins
claude --plugin-dir .

# In Claude, try your commands
/your-command

# Test agents (if applicable)
# Trigger agent with keywords or explicitly
```

### Validation

Run validation checks (if tf-core is available):

```bash
# Validate command structure
/check-commands

# Validate agent configuration
/check-agents
```

### Manual Testing Checklist

- [ ] Plugin loads without errors
- [ ] All commands are accessible
- [ ] Commands execute as expected
- [ ] Agents trigger correctly
- [ ] Documentation is clear and accurate
- [ ] Examples work as shown
- [ ] Error cases are handled gracefully

## Documentation

### Plugin README Template

Your plugin README should include:

1. **Title and Description**
2. **Installation Instructions**
3. **Quick Start**
4. **Commands Reference**
5. **Agents Reference** (if applicable)
6. **Examples**
7. **Configuration** (if applicable)
8. **Troubleshooting**
9. **Contributing**
10. **License**

### Inline Documentation

- Use clear, descriptive comments
- Explain WHY, not just WHAT
- Include examples for complex scenarios
- Keep documentation up-to-date with code

### Screenshots and Examples

When appropriate, include:
- Command output examples
- Agent interaction examples
- Configuration screenshots
- Use case diagrams

## Publishing

### Pre-Release Checklist

Before publishing your plugin:

- [ ] All files follow naming conventions
- [ ] plugin.json has correct metadata
- [ ] Version number follows semantic versioning
- [ ] README is complete and accurate
- [ ] Commands tested and working
- [ ] Agents tested and working
- [ ] No sensitive data in files
- [ ] License file included
- [ ] CHANGELOG updated

### Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- **Major (1.0.0):** Breaking changes
- **Minor (0.1.0):** New features, backwards compatible
- **Patch (0.0.1):** Bug fixes, backwards compatible

### Creating a Release

1. Update version in `plugin.json`
2. Update `CHANGELOG.md`
3. Create a git tag: `git tag plugin/your-plugin-v1.0.0`
4. Push tags: `git push --tags`
5. Create GitHub release

### Submission Process

1. **Fork Repository**
2. **Create Feature Branch:** `feature/add-your-plugin`
3. **Add Plugin Files**
4. **Test Thoroughly**
5. **Create Pull Request**
6. **Address Review Comments**
7. **Merge and Publish**

## Best Practices

### Code Quality

1. **Simplicity:** Keep commands and agents focused and simple
2. **Consistency:** Follow existing patterns in the repository
3. **Documentation:** Document everything clearly
4. **Testing:** Test all scenarios, including edge cases
5. **Feedback:** Provide clear user feedback

### User Experience

1. **Clear Commands:** Make command names intuitive
2. **Good Defaults:** Provide sensible default values
3. **Error Messages:** Show helpful error messages
4. **Examples:** Include plenty of examples
5. **Progressive Disclosure:** Start simple, offer advanced options

### Security

1. **Input Validation:** Validate all user input
2. **No Secrets:** Never hardcode secrets
3. **Safe Defaults:** Default to safe operations
4. **User Consent:** Ask before destructive operations
5. **Least Privilege:** Request minimum necessary permissions

### Performance

1. **Efficient Prompts:** Keep prompts concise but clear
2. **Lazy Loading:** Only load what's needed
3. **Caching:** Cache when appropriate
4. **Resource Limits:** Respect system resources
5. **Feedback:** Show progress for long operations

### Maintenance

1. **Version Control:** Use semantic versioning
2. **Changelog:** Maintain a detailed changelog
3. **Issues:** Track and respond to issues promptly
4. **Updates:** Keep dependencies updated
5. **Deprecation:** Give users time to migrate

## Common Patterns

### Command with Arguments

```markdown
---
name: example-command
description: Example with arguments
parameters:
  - name: input
    description: Input value
    required: true
  - name: output
    description: Output file
    required: false
    default: "result.txt"
---

# Example Command

Parse arguments from the command invocation.

The user provided: {input} as input.
Save results to: {output}.
```

### Multi-Step Command

```markdown
---
name: multi-step
description: Command with multiple steps
---

# Multi-Step Command

Execute the following steps:

1. **Gather Information**
   - Read current state
   - Validate prerequisites

2. **Process**
   - Perform main operation
   - Handle errors gracefully

3. **Report Results**
   - Show clear summary
   - Suggest next steps
```

### Interactive Agent

```markdown
---
name: interactive-helper
description: Interactive assistance
trigger:
  type: auto
  keywords: [help, assist]
---

# Interactive Helper

You help users through complex tasks interactively.

## Interaction Pattern

1. **Understand:** Ask clarifying questions
2. **Guide:** Provide step-by-step guidance
3. **Verify:** Check results at each step
4. **Adapt:** Adjust based on user feedback
```

## Resources

### Official Documentation

- [Claude Code Documentation](https://docs.claude.com)
- [Claude API Documentation](https://docs.anthropic.com)
- [Markdown Guide](https://www.markdownguide.org/)

### Community

- [GitHub Discussions](https://github.com/talent-factory/claude-plugins/discussions)
- [Issue Tracker](https://github.com/talent-factory/claude-plugins/issues)

### Examples

Look at existing plugins for inspiration:
- `git-workflow` - Git operations
- `education` - Teaching and learning
- `code-quality` - Code review

## Support

Need help with plugin development?

- **Questions:** [GitHub Discussions](https://github.com/talent-factory/claude-plugins/discussions)
- **Bugs:** [GitHub Issues](https://github.com/talent-factory/claude-plugins/issues)
- **Email:** support@talent-factory.ch

## Contributing

Contributions are welcome! Please see:
- [Contributing Guidelines](../CONTRIBUTING.md)
- [Code of Conduct](../CODE_OF_CONDUCT.md)
- [Security Policy](../SECURITY.md)

---

**Happy Plugin Development!** 🚀

*Last Updated: January 2026*
*Maintained by: Talent Factory GmbH*
