# Talent Factory Claude Plugins

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Plugins-blue)](https://claude.ai)
[![Plugins](https://img.shields.io/badge/Plugins-7-green)](https://github.com/talent-factory/claude-plugins)

Professional Claude Code plugins for software development and education by Talent Factory GmbH.

## 🚀 Quick Start

### Add Marketplace

In your project's `.claude/settings.json`:

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

### Install Plugins

```bash
# Open Claude Code
claude

# Use the plugin command
/plugin

# Select "Browse Plugins" → "talent-factory"
# Choose plugins to install
```

## 📦 Available Plugins

### 🔧 Git Workflow
Professional git commands with automated pre-commit checks, emoji conventional commits, PR management, and intelligent merge conflict resolution.

**Commands:**

- `/git-workflow:commit` - Professional commits with automated checks
- `/git-workflow:create-pr` - Branch creation, commit splitting, and PR opening
- `/git-workflow:pr-edit-history` - Display PR description edit history
- `/git-workflow:resolve-conflicts` - Intelligent merge conflict resolution

**Skills:**

- Professional Commit Workflow - Automated commit creation with project-type detection
- Professional PR Workflow - Branch management and PR automation
- Post-Merge Cleanup - Worktree and branch cleanup after merge

[📖 Documentation](./plugins/git-workflow/README.md)

---

### 📋 Project Management

Comprehensive project management with PRD generation, project planning, task initialization, implementation orchestration, EPIC automation, and Linear integration.

**Commands:**

- `/project-management:create-prd` - Generate Product Requirements Documents
- `/project-management:create-plan` - Create project plans (Filesystem or Linear)
- `/project-management:init-task` - Initialize tasks with duplicate detection and ATOMIC validation
- `/project-management:implement-task` - Implement tasks with agent routing and quality gate
- `/project-management:implement-epic` - Autonomous EPIC implementation with parallel agents
- `/project-management:document-handoff` - Create handoff documentation before /compact

**Agents:**

- Epic Orchestrator - Parallel task implementation within EPICs

[📖 Documentation](./plugins/project-management/README.md)

---

### ✨ Code Quality

Comprehensive code quality tools with Python linting and expert agents for Python and Frontend development.

**Commands:**

- `/code-quality:ruff-check` - Lint and format Python files with Ruff

**Agents:**

- Code Reviewer - Proactive code review for quality, security, and maintainability
- Python Expert - Idiomatic Python with decorators, generators, and async/await
- Frontend Developer - Next.js applications with React, shadcn/ui, and Tailwind CSS

[📖 Documentation](./plugins/code-quality/README.md)

---

### 🎓 Education

Teaching aids with Java Tutor agent, Markdown syntax formatter, and code explanation for IT education.

**Commands:**

- `/education:explain-code` - Educational code explanations

**Agents:**

- Java Tutor - Expert Java programming instructor for students
- Markdown Syntax Formatter - Converts text to proper Markdown syntax

**Skills:**

- Markdown Syntax Formatter - Formatting, heading hierarchies, and Swiss German orthography

[📖 Documentation](./plugins/education/README.md)

---

### 🛠️ Core Utilities

Comprehensive development utilities for plugin/command/agent development, validation, CI automation, text humanization, and PDF-to-Markdown conversion.

**Commands:**

- `/core:check` - Project validation without commits
- `/core:check-commands` - Validate command files
- `/core:check-agents` - Validate agent configurations
- `/core:build-skill` - Create Claude Code Skills
- `/core:package-skill` - Package skills as distributable archives
- `/core:create-command` - Generate new commands
- `/core:run-ci` - Run CI checks locally

**Agents:**

- Agent Expert - Agent design and optimization
- Command Expert - CLI command development

**Skills:**

- Humanizer - Removes AI writing patterns from text
- PDF to Markdown - Converts PDF files with dual-mode support (fast/vision)

[📖 Documentation](./plugins/core/README.md)

---

### 💻 Development

Expert development agents, project initialization with Git branching, Gradle Kotlin DSL, Python/uv support, and documentation synchronization.

**Commands:**

- `/development:init-project` - Initialize open source projects with GitHub best practices

**Agents:**

- Java Developer - Modern Java with Streams, Concurrency, and JVM optimization

**Skills:**

- Professional Init-Project - Skill-based project initialization with automation
- Update Documents - Documentation synchronization between CLAUDE.md, README.md, and docs/

[📖 Documentation](./plugins/development/README.md)

---

### 📝 Obsidian Integration

Task management via TaskNotes Plugin API with natural language support (DE/EN).

**Skills:**

- TaskNotes - Obsidian task management integration

**Features:**

- List, create, update, and delete tasks
- Work recommendations
- Natural language interface (German/English)
- Direct integration with Obsidian vault

[📖 Documentation](./plugins/obsidian/README.md)

## 🎯 Who Is This For?

### Students

- BSc Computer Science students
- Self-learners

### Developers

- Software engineers
- Team leads
- Code reviewers

### Educators

- Programming instructors
- Course developers
- Teaching assistants

## 💡 Use Cases

### For Development Teams

**Standardize Git Workflow**
```json
{
  "enabledPlugins": {
    "git-workflow@talent-factory": true
  }
}
```

**Improve Code Quality**
```json
{
  "enabledPlugins": {
    "code-quality@talent-factory": true
  }
}
```

### For Educational Institutions

**Educational Course Setup**
```json
{
  "enabledPlugins": {
    "education@talent-factory": true,
    "code-quality@talent-factory": true
  }
}
```

### For Individual Developers

**Full Productivity Stack**
```json
{
  "enabledPlugins": {
    "git-workflow@talent-factory": true,
    "project-management@talent-factory": true,
    "code-quality@talent-factory": true,
    "core@talent-factory": true,
    "development@talent-factory": true,
    "obsidian@talent-factory": true
  }
}
```

## 📚 Documentation

### For Users

- [Installation Guide](#quick-start)
- [Plugin Overview](#available-plugins)
- Individual Plugin READMEs

### For Contributors

- [Contributing Guidelines](./CONTRIBUTING.md)
- [Plugin Development Guide](./docs/PLUGIN_DEVELOPMENT.md)
- [Code of Conduct](./CODE_OF_CONDUCT.md)

## 🔄 Migration from Dotfiles

If you're currently using [talent-factory/dotfiles](https://github.com/talent-factory/dotfiles):

1. **Keep dotfiles** for Augment, Windsurf, Copilot configurations
2. **Switch to plugins** for Claude Code commands and agents
3. **Benefits:**
   - Modular installation
   - Easy updates
   - Team-wide consistency
   - Better discoverability

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](./CONTRIBUTING.md).

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch
3. Add/modify plugins
4. Test locally with `claude --plugin-dir ./plugins/[name]`
5. Submit a Pull Request

## 📋 Roadmap

### Q1 2026

- [ ] Additional education agents (Python Tutor, Algorithm Coach)
- [ ] More project management integrations
- [ ] Advanced code quality checks

### Q2 2026

- [ ] CI/CD integration plugins
- [ ] Team collaboration tools
- [ ] Performance analysis plugins

## 🐛 Issues & Support

- **Bug Reports:** [Open an issue](https://github.com/talent-factory/claude-plugins/issues)
- **Feature Requests:** [Open an issue](https://github.com/talent-factory/claude-plugins/issues)
- **Questions:** [GitHub Discussions](https://github.com/talent-factory/claude-plugins/discussions)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built for students, developers and beyond
- Inspired by professional development workflows
- Community contributions welcome!

## 📞 Contact

**Talent Factory GmbH**

- Website: [talent-factory.ch](https://talent-factory.xyz)
- GitHub: [@talent-factory](https://github.com/talent-factory)
- Maintainer: Daniel Senften

---

**⭐ If these plugins help you, consider giving us a star!**

Made with ❤️ by Talent Factory GmbH
