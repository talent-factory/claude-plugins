# Code Quality Plugin

Comprehensive code quality tools with Python linting, code review, and expert agents for Python and Frontend development.

## Version 3.0.1

**Breaking Change:** Java developer agent moved to `development` plugin. Now includes `/code-quality:ruff-check` command and 3 expert agents for proactive code quality assistance.

## Commands

### `/code-quality:ruff-check`

Lint and format all Python files in the project with Ruff.

**Features:** 

- ⚡ Fast Python linting with Ruff
- 🔧 Automatic code formatting
- ✅ PEP 8 compliance checking
- 🐛 Common error detection
- 📊 Detailed error reporting

**Usage:**
```bash
/code-quality:ruff-check              # Lint all Python files
/code-quality:ruff-check --fix        # Auto-fix issues
```

**Checks:**
- PEP 8 style compliance
- Import sorting
- Unused imports
- Code complexity
- Type hints
- Docstring presence

## Agents

All agents activate automatically based on context. See [Skills & Agents Activation Guide](../reference/skills-agents-activation.md) for details.

### Code Reviewer

Expert for comprehensive code reviews with focus on quality, security, and maintainability.

**Activation:**
- Automatic: After writing/changing code, during PR reviews
- Manual: "Review this code for quality and security"

**Expertise:**
- 🔍 Code quality analysis
- 🔒 Security vulnerability detection
- ⚡ Performance optimization suggestions
- 📚 Best practices enforcement
- ♻️ Refactoring recommendations

**Use proactively:**
- Automatically after writing/changing code
- For pull request reviews
- Before commits
- During refactoring sessions

**Review Focus:**
- Code structure and organization
- Security vulnerabilities
- Performance bottlenecks
- Maintainability issues
- Test coverage
- Documentation quality

### Python Expert

Expert for writing idiomatic Python code with advanced features.

**Activation:**
- Automatic: Python refactoring, optimization, or architecture questions
- Manual: "Use python-expert to optimize this code"

**Expertise:**
- 🐍 Idiomatic Python patterns
- 🎨 Decorators, generators, async/await
- ⚡ Performance optimization
- 🎯 Design patterns
- ✅ Comprehensive testing
- 📋 Type hints and mypy

**Use proactively for:**
- Python refactoring
- Optimization tasks
- Complex Python features
- Architecture decisions
- Testing strategies

**Specializations:**
- Modern Python (3.10+)
- Async programming
- Context managers
- Metaclasses
- Performance tuning

### Frontend Developer

Expert for creating Next.js applications with React, shadcn/ui, and Tailwind CSS.

**Activation:**
- Automatic: React/Next.js development, UI component creation
- Manual: "Use frontend-developer to create this component"

**Expertise:**
- ⚛️ React components and hooks
- 🎨 shadcn/ui component library
- 🎯 Tailwind CSS styling
- 🚀 Next.js SSR/SSG
- 📱 App Router patterns
- ⚡ Modern frontend architecture

**Use proactively for:**
- Next.js development
- UI component creation
- Frontend architecture
- Performance optimization
- Responsive design

**Specializations:**
- Server components
- Client components
- App Router
- shadcn/ui integration
- Tailwind patterns

## Installation

```json
{
  "enabledPlugins": {
    "code-quality@talent-factory": true
  }
}
```

## Use Cases

### Python Development

```bash
# Lint Python code
/code-quality:ruff-check --fix

# Claude (with python-expert):
# - Reviews code proactively
# - Suggests idiomatic patterns
# - Optimizes performance
# - Adds type hints
```

### React/Next.js Development

```bash
# Claude (with frontend-developer):
# - Creates shadcn/ui components
# - Implements App Router patterns
# - Optimizes performance
# - Ensures responsive design
```

### Code Review Workflow

```bash
# After writing code, Claude (with code-reviewer):
# - Analyzes code quality automatically
# - Identifies security issues
# - Suggests refactoring
# - Checks test coverage
```

## Changelog

### Version 3.0.1 (2026-01-28)

- Breaking: Moved java-developer agent to development plugin
- Updated description to reflect current agent inventory

### Version 2.0.0 (2026-01-10)

- Added `/code-quality:ruff-check` command for Python linting
- Added code-reviewer agent for proactive reviews
- Added python-expert agent for Python development
- Added frontend-developer agent for Next.js/React development

### Version 1.0.0

- Initial release with `/code-quality:review` and `/code-quality:refactor` commands

## License

MIT License - see [LICENSE](https://github.com/talent-factory/claude-plugins/blob/main/LICENSE) file for details.

---

**Made with ❤️ by Talent Factory GmbH**
