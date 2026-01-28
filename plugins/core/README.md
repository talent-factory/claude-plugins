# Core Utilities Plugin

Comprehensive development utilities for plugin/command/agent development, validation, CI automation, and text humanization.

## Version 3.0.0

**Breaking Change:** `init-project` command moved to `development` plugin. Now includes 7 commands, 1 skill, and 2 expert agents for development workflow automation.

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

### CI Automation

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

See [Skills & Agents Activation Guide](../reference/skills-agents-activation.md) for detailed activation instructions.

### Agent Expert

Expert for creating and optimizing specialized Claude Code Agents.

**Activation:**
- Automatic: Agent creation or improvement requests
- Manual: "Use agent-expert to design this agent"

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

**Activation:**
- Automatic: CLI command creation or design requests
- Manual: "Use command-expert to design this CLI"

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

## Skills

See [Skills & Agents Activation Guide](../reference/skills-agents-activation.md) for detailed activation instructions.

### Humanizer

Removes signs of AI-generated text to make content more natural and human.

**Activation:**
- Automatic: "Humanize this text", "remove AI patterns"
- Manual: "Make this text more natural"

**Features:**
- 🔍 Erkennung von 24 KI-Schreibmustern
- ✏️ Automatisches Umschreiben problematischer Abschnitte
- 🎯 Erhalt von Bedeutung und Stimme
- 💡 Hinzufügen von Persönlichkeit und Seele

**Erkannte Muster:**
- Aufgeblasene Symbolik und Bedeutung
- Werbesprache und übertriebene Betonung
- Oberflächliche Partizip-Analysen
- Vage Zuschreibungen und Wieselwörter
- KI-Vokabular (darüber hinaus, entscheidend, etc.)
- Gedankenstrich-Übernutzung
- Dreierregel-Übernutzung
- Negative Parallelismen
- Und 16 weitere Muster...

**Basiert auf:** [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)

**Verwendung:**
```
"Humanisiere diesen Text"
"Entferne KI-Schreibmuster aus diesem Dokument"
"Mach diesen Text menschlicher"
```

**Location:** `skills/humanizer/SKILL.md`

## Installation

This plugin is part of the Talent Factory marketplace.

**Add to `.claude/settings.json`:**
```json
{
  "enabledPlugins": {
    "core@talent-factory": true
  }
}
```

## Project Structure

```
core/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── check.md
│   ├── check-agents.md
│   ├── check-commands.md
│   ├── build-skill.md
│   ├── package-skill.md
│   ├── create-command.md
│   └── run-ci.md
├── agents/
│   ├── agent-expert.md
│   └── command-expert.md
├── skills/
│   └── humanizer/
│       └── SKILL.md
└── README.md
```

## Workflow Examples

### Example 1: Create New Plugin

```bash
# 1. Initialize project structure
/development:init-project

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

### Example 5: Text humanisieren

```bash
# Humanizer Skill verwenden

User: "Humanisiere diesen Text: Das neue Software-Update
dient als Zeugnis für das Engagement des Unternehmens
für Innovation. Darüber hinaus bietet es eine nahtlose,
intuitive und leistungsstarke Benutzererfahrung."

# Claude mit Humanizer Skill:
# - Identifiziert KI-Muster (aufgeblasene Symbolik,
#   KI-Vokabular, Dreierregel)
# - Schreibt Text natürlicher um
# - Fügt konkrete Details hinzu

# Ergebnis:
# "Das Software-Update fügt Stapelverarbeitung,
# Tastenkürzel und Offline-Modus hinzu."
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

### For Content Writers

- Remove AI writing patterns from text
- Make content more natural and human
- Improve text authenticity
- Editorial quality assurance

## Requirements

- **Claude Code:** Latest version
- **Git:** For version control
- **Node.js/Python:** For specific project types

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

### Version 3.0.0 (2026-01-28)

**Breaking Change:**
- Moved `/init-project` command to development plugin
- Removed skill-builder agent system (available via `/build-skill` command)
- Updated documentation to English

### Version 2.1.0 (2026-01-19)

- Added Humanizer skill for removing AI writing patterns
- Added `/build-skill` and `/package-skill` commands

### Version 2.0.0 (2026-01-10)

- Added `/check` command for project validation
- Added `/create-command` for pattern-based command generation
- Added `/run-ci` for local CI execution
- Added agent-expert agent for agent development
- Added command-expert agent for CLI development
- Enhanced `/check-commands` with best practices validation
- Enhanced `/check-agents` with color attribute checking

### Version 1.0.0

- Initial release with `/check-commands` and `/check-agents`

## Support

- **Issues:** [GitHub Issues](https://github.com/talent-factory/claude-plugins/issues)
- **Discussions:** [GitHub Discussions](https://github.com/talent-factory/claude-plugins/discussions)
- **Email:** support@talent-factory.ch

## Contributing

See [CONTRIBUTING.md](https://github.com/talent-factory/claude-plugins/blob/main/CONTRIBUTING.md) in the main repository.

## License

MIT License - see [LICENSE](https://github.com/talent-factory/claude-plugins/blob/main/LICENSE) file for details.

---

**Made with ❤️ by Talent Factory GmbH**
