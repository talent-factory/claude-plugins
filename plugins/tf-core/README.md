# TF Core Utilities Plugin

Comprehensive development utilities for plugin/command/agent development, validation, CI automation, and OpenSource project initialization.

## Version 2.0.0

**Major Update:** Now includes 8 commands and 3 expert agents for complete development workflow automation.

## Commands

### Development & Validation

#### `/check`

Run project checks and fix errors without committing.

**Features:**
- 🔍 Automatic project type detection
- ✅ Linting and formatting
- 🧪 Test execution
- 🏗️ Build verification
- ⚠️ Error reporting without commits

**Usage:**
```bash
/check              # Run all checks
/check --fix        # Auto-fix issues
```

#### `/check-commands`

Validate command files, documentation, and best practices.

**Features:**
- 📝 YAML frontmatter validation
- 🔍 Markdown syntax checking
- 📚 Documentation completeness
- ✅ Naming convention enforcement
- 🎯 Best practices verification

**Usage:**
```bash
/check-commands                  # Check all commands
/check-commands path/to/cmd.md   # Check specific command
```

#### `/check-agents`

Validate agent configurations and YAML frontmatter.

**Features:**
- 🤖 Agent structure validation
- 🎨 Color attribute checking
- 📋 Required field verification
- 🔍 Trigger pattern validation
- ✅ Best practices enforcement

**Usage:**
```bash
/check-agents                    # Check all agents
/check-agents path/to/agent.md   # Check specific agent
```

### Plugin & Skill Development

#### `/build-skill`

Create comprehensive Claude Code Skills through elicitation-driven development.

**Features:**
- 💬 Interactive requirements gathering
- 📋 Skill specification creation
- 🏗️ Automated skill generation
- ✅ Validation and testing
- 📚 Documentation generation

**Usage:**
```bash
/build-skill
```

**Workflow:**
1. Elicit requirements from user
2. Create skill specification
3. Generate skill structure
4. Validate implementation
5. Generate documentation

#### `/package-skill`

Validate and package Claude Code Skills into distributable zip files.

**Features:**
- ✅ Complete skill validation
- 📦 Zip package creation
- 📚 Documentation bundling
- 🔍 Dependency checking
- ✨ README generation

**Usage:**
```bash
/package-skill              # Package current directory
/package-skill path/to/skill  # Package specific skill
```

#### `/create-command`

Create new commands following existing patterns and organizational structure.

**Features:**
- 📝 Template-based generation
- 🎯 Pattern matching with existing commands
- ✅ Automatic validation
- 📚 Documentation scaffolding
- 🔧 Best practices enforcement

**Usage:**
```bash
/create-command
```

### Project & CI

#### `/init-project`

Initialize new OpenSource projects with GitHub best practices.

**Features:**
- 📋 Complete project structure
- 🔒 Security policy (SECURITY.md)
- 🤝 Contributing guidelines
- 📄 License files
- 🔧 CI/CD workflows
- 🏷️ Issue/PR templates

**Usage:**
```bash
/init-project
```

**Creates:**
- CODE_OF_CONDUCT.md
- CONTRIBUTING.md
- SECURITY.md
- LICENSE
- README.md
- .github/workflows/
- .github/ISSUE_TEMPLATE/
- .github/PULL_REQUEST_TEMPLATE.md

#### `/run-ci`

Execute CI checks locally and fix all errors until tests pass.

**Features:**
- 🔄 Complete CI simulation
- ✅ All checks execution
- 🔧 Automatic error fixing
- 🔁 Retry until success
- 📊 Detailed reporting

**Usage:**
```bash
/run-ci              # Run all CI checks
/run-ci --fix        # Auto-fix and retry
```

**Checks:**
- Linting
- Type checking
- Unit tests
- Integration tests
- Build verification
- Security scans

## Agents

### Agent Expert

Expert for creating and optimizing specialized Claude Code Agents.

**Expertise:**
- 🎯 Agent design and architecture
- ✨ Prompt engineering
- 🏗️ Domain modeling
- 📚 Best practices for agent development
- 🔧 claude-code-templates system

**Use proactively for:**
- Designing new agents
- Improving existing agents
- Agent optimization
- Prompt refinement

**Location:** `agents/agent-expert.md`

### Command Expert

Expert for creating CLI commands for automation and tooling.

**Expertise:**
- 🛠️ Command-line interface design
- 📋 Argument parsing
- 🔧 Task automation
- 💻 CLI best practices

**Use proactively for:**
- Designing command-line interfaces
- Argument parsing logic
- Task automation workflows
- CLI tool development

**Location:** `agents/command-expert.md`

### Skill Builder

Comprehensive agent system for building Claude Code Skills.

**Agents:**
- skill-elicitation-agent - Requirements gathering
- skill-generator-agent - Skill code generation
- skill-validator-agent - Testing and validation
- skill-documenter-agent - Documentation creation

**Use proactively for:**
- Building new skills
- Skill requirements elicitation
- Skill specification creation
- Skill validation and testing
- Documentation generation

**Location:** `agents/skill-builder/`

## Installation

This plugin is part of the Talent Factory marketplace.

**Add to `.claude/settings.json`:**
```json
{
  "enabledPlugins": {
    "tf-core@talent-factory": true
  }
}
```

## Project Structure

```
tf-core/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── check.md
│   ├── check-agents.md
│   ├── check-commands.md
│   ├── build-skill.md
│   ├── package-skill.md
│   ├── create-command.md
│   ├── init-project.md
│   └── run-ci.md
├── agents/
│   ├── agent-expert.md
│   ├── command-expert.md
│   └── skill-builder/
│       ├── skill-elicitation-agent.md
│       ├── skill-generator-agent.md
│       ├── skill-validator-agent.md
│       └── skill-documenter-agent.md
└── README.md
```

## Workflow Examples

### Example 1: Create New Plugin

```bash
# 1. Initialize project structure
/init-project

# 2. Create first command
/create-command

# 3. Validate command
/check-commands

# 4. Run all checks
/check
```

### Example 2: Build Custom Skill

```bash
# 1. Build skill interactively
/build-skill

# Claude (with skill-elicitation-agent):
# - Gathers requirements
# - Creates specification
# - Generates skill structure

# 2. Validate skill
/package-skill

# Claude:
# - Validates structure
# - Checks dependencies
# - Creates distributable package
```

### Example 3: Pre-Commit Workflow

```bash
# 1. Run checks before commit
/check

# Claude:
# - Detects project type (Java/Python/React)
# - Runs appropriate linters
# - Executes tests
# - Reports issues

# 2. Fix issues automatically
/check --fix

# 3. Run CI locally
/run-ci

# Claude:
# - Simulates complete CI pipeline
# - Fixes errors iteratively
# - Ensures all checks pass
```

### Example 4: Agent Development

```bash
# Working with agent-expert proactively

User: "I need an agent for React component optimization"

# Claude automatically uses agent-expert:
# - Designs agent architecture
# - Defines domain model
# - Creates prompt structure
# - Applies best practices

# Agent-expert generates:
# - Agent specification
# - Trigger patterns
# - System prompt
# - Example interactions
```

## Best Practices

### Command Development

1. **Follow conventions** - Use existing patterns
2. **Validate early** - Run `/check-commands` frequently
3. **Document thoroughly** - Include examples and usage
4. **Test locally** - Use `claude --plugin-dir`

### Agent Development

1. **Clear purpose** - Each agent has single responsibility
2. **Trigger patterns** - Define when agent activates
3. **Color coding** - Consistent color scheme
4. **Example interactions** - Show real usage patterns

### Skill Development

1. **Elicit requirements** - Use `/build-skill` workflow
2. **Validate structure** - Run `/package-skill` checks
3. **Test thoroughly** - Verify all functionality
4. **Document completely** - README, SKILL.md, examples

### CI/CD

1. **Run locally first** - Use `/run-ci` before push
2. **Fix errors iteratively** - Don't ignore warnings
3. **Automate checks** - `/check` in pre-commit hooks
4. **Keep builds green** - Address failures immediately

## Use Cases

### For Plugin Developers

- Create and validate new commands
- Build custom skills
- Ensure code quality
- Automate CI checks

### For Project Maintainers

- Initialize OpenSource projects
- Enforce best practices
- Automate validation
- Maintain code quality

### For Skill Builders

- Interactive skill creation
- Requirements elicitation
- Validation and packaging
- Documentation generation

### For Educators

- Create teaching agents
- Build educational skills
- Initialize course projects
- Validate student submissions

## Requirements

- **Claude Code:** Latest version
- **Git:** For project initialization
- **Node.js/Python:** For specific project types
- **GitHub CLI:** Optional for `/init-project`

## Troubleshooting

### Command Validation Issues

**Problem:** `/check-commands` fails
- **Solution:** Check YAML frontmatter syntax
- **Solution:** Ensure required fields present
- **Solution:** Validate markdown structure

### Agent Validation Issues

**Problem:** `/check-agents` reports errors
- **Solution:** Verify color attribute is valid
- **Solution:** Check trigger patterns syntax
- **Solution:** Ensure required metadata present

### Skill Packaging Issues

**Problem:** `/package-skill` fails
- **Solution:** Validate SKILL.md structure
- **Solution:** Check for missing dependencies
- **Solution:** Ensure README.md exists

### CI Issues

**Problem:** `/run-ci` gets stuck
- **Solution:** Check for infinite loops in tests
- **Solution:** Verify all dependencies installed
- **Solution:** Review error logs carefully

## Changelog

### Version 2.0.0 (2026-01-10)

**Major Update:**
- ✨ Added `/check` command for project validation without commits
- ✨ Added `/create-command` for pattern-based command generation
- ✨ Added `/init-project` for OpenSource project initialization
- ✨ Added `/run-ci` for local CI execution
- 🤖 Added agent-expert agent for agent development
- 🤖 Added command-expert agent for CLI development
- 🤖 Added skill-builder agent system (4 specialized agents)
- 🔧 Enhanced `/check-commands` with best practices validation
- 🔧 Enhanced `/check-agents` with color attribute checking
- 🔧 Enhanced `/build-skill` with elicitation workflow
- 🔧 Enhanced `/package-skill` with dependency checking

**Migration from 1.0.0:**
- All existing commands remain compatible
- New commands optional but recommended
- Agents provide proactive assistance

### Version 1.0.0

- Initial release with `/check-commands` and `/check-agents`

## Support

- **Issues:** [GitHub Issues](https://github.com/talent-factory/claude-plugins/issues)
- **Discussions:** [GitHub Discussions](https://github.com/talent-factory/claude-plugins/discussions)
- **Email:** support@talent-factory.ch

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) in the main repository.

## License

MIT License - see [LICENSE](../../LICENSE) file for details.

---

**Made with ❤️ by Talent Factory GmbH**
