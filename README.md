# Talent Factory Claude Plugins

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Plugins-blue)](https://claude.ai)
[![Plugins](https://img.shields.io/badge/Plugins-6-green)](https://github.com/talent-factory/claude-plugins)

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
Professional git commands for commits, PRs, and branch management.

**Commands:**

- `/commit` - Conventional commits with validation
- `/create-pr` - Professional PR creation

[📖 Documentation](./plugins/git-workflow/README.md)

---

### 📋 Project Management

PRD generation, planning, and Linear integration.

**Commands:**

- `/create-prd` - Generate Product Requirements Documents
- `/create-plan` - Create project plans with Linear integration

[📖 Documentation](./plugins/project-management/README.md)

---

### ✨ Code Quality

Code review, refactoring, and quality checks.

**Commands:**

- `/review` - Comprehensive code reviews
- `/refactor` - Guided refactoring

[📖 Documentation](./plugins/code-quality/README.md)

---

### 🎓 Education Tools

Teaching aids and student support for IT education.

**Commands:**

- `/explain-code` - Educational code explanations

**Agents:**

- Java Tutor - Expert Java instructor

[📖 Documentation](./plugins/education/README.md)

---

### 🛠️ Core Utilities

Development utilities for plugin/command/agent development, validation, CI automation, project initialization, and text humanization.

**Commands:**

- `/check` - Project validation without commits
- `/check-commands` - Validate command files
- `/check-agents` - Validate agent configurations
- `/build-skill` - Create Claude Code Skills
- `/package-skill` - Package skills
- `/create-command` - Generate new commands
- `/init-project` - Initialize OpenSource projects
- `/run-ci` - Run CI checks locally

**Agents:**

- Agent Expert - Agent design and optimization
- Command Expert - CLI development
- Skill Builder - Complete skill-building system

**Skills:**

- Humanizer - Text humanization and AI writing improvement

[📖 Documentation](./plugins/core/README.md)

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

## 🛡️ Version Compatibility

| Plugin | Claude Code Version | Status |
|--------|---------------------|--------|
| All Plugins | 1.0.0+ | ✅ Supported |

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
