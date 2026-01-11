# Contributing to Talent Factory Claude Plugins

Thank you for your interest in contributing to our Claude Code plugins! We welcome contributions from the community and are grateful for your support.

## 🎯 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the [existing issues](https://github.com/talent-factory/claude-plugins/issues) to avoid duplicates.

**When filing a bug report, please include:**
- A clear and descriptive title
- Steps to reproduce the issue
- Expected behavior vs. actual behavior
- Claude Code version
- Operating system and version
- Plugin version(s) affected
- Any relevant error messages or logs

### Suggesting Enhancements

We love to hear your ideas! Enhancement suggestions are tracked as GitHub issues.

**When suggesting an enhancement, please include:**
- A clear and descriptive title
- Detailed description of the proposed feature
- Use cases and benefits
- Any relevant examples or mockups
- Which plugin(s) would be affected

### Pull Requests

We actively welcome your pull requests! Here's how to contribute code:

## 🔧 Development Setup

### Prerequisites

- Claude Code installed ([Installation Guide](https://docs.claude.com/en/docs/claude-code))
- Git installed
- Basic understanding of Claude Code plugin structure

### Getting Started

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub, then clone your fork
   git clone https://github.com/YOUR-USERNAME/claude-plugins.git
   cd claude-plugins
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

3. **Test your changes locally**
   ```bash
   # Test a specific plugin
   claude --plugin-dir ./plugins/PLUGIN-NAME
   
   # Test all plugins
   claude --plugin-dir .
   ```

## 📝 Contribution Guidelines

### Branch Naming Convention

- `feature/` - New features (e.g., `feature/add-python-tutor`)
- `fix/` - Bug fixes (e.g., `fix/commit-validation-error`)
- `docs/` - Documentation updates (e.g., `docs/update-installation-guide`)
- `refactor/` - Code refactoring (e.g., `refactor/simplify-pr-template`)

### Commit Message Format

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
type(scope): subject

body (optional)

footer (optional)
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(education): add Python tutor agent
fix(git-workflow): resolve commit validation error
docs(readme): update installation instructions
```

### Code Style

- Use clear, descriptive names for commands and agents
- Follow existing plugin structure and conventions
- Include comprehensive documentation in command/agent files
- Add examples where appropriate
- Keep commands focused and single-purpose

### Plugin Structure

When creating or modifying plugins, follow this structure:

```
plugins/your-plugin/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata
├── commands/
│   └── your-command.md      # Command definitions
├── agents/
│   └── your-agent.md        # Agent definitions (optional)
└── README.md                # Plugin documentation
```

### Testing Your Changes

Before submitting a PR:

1. **Test the plugin locally**
   ```bash
   claude --plugin-dir ./plugins/YOUR-PLUGIN
   ```

2. **Verify all commands work**
   - Test each command in Claude Code
   - Check for errors or unexpected behavior
   - Verify documentation is accurate

3. **Run validation** (if available)
   ```bash
   /check-commands  # Using core plugin
   /check-agents    # Using core plugin
   ```

4. **Check documentation**
   - Ensure README is updated
   - Verify examples are correct
   - Check for typos and clarity

## 🚀 Submitting a Pull Request

1. **Push your changes**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a Pull Request**
   - Go to the [repository](https://github.com/talent-factory/claude-plugins)
   - Click "New Pull Request"
   - Select your fork and branch
   - Fill out the PR template completely

3. **PR Requirements**
   - Clear description of changes
   - Reference related issues (e.g., "Fixes #123")
   - All tests pass (if CI/CD is configured)
   - Documentation is updated
   - Follows code style guidelines

4. **Review Process**
   - A maintainer will review your PR
   - Address any requested changes
   - Once approved, your PR will be merged

## 🔒 Branch Protection

**Important:** The `main` and `develop` branches are protected to ensure code quality and maintain a clean history.

### Branch Access Rules

#### Main Branch
- **Purpose:** Production-ready code, stable releases
- **Access:** Pull Requests only (no direct commits)
- **Requirements:**
  - At least 1 approval from a maintainer
  - All CI/CD checks must pass
  - Must be up-to-date with base branch
  - No merge conflicts

#### Develop Branch
- **Purpose:** Integration branch for ongoing development
- **Access:**
  - **Maintainer (Daniel Senften) only:** Direct commits allowed
  - **All other contributors:** Pull Requests required
- **Requirements for PRs:**
  - At least 1 approval from a maintainer
  - All CI/CD checks must pass
  - Must be up-to-date with base branch
  - Branch naming convention must be followed

### Why These Rules?

1. **Code Quality:** All changes are reviewed before merging
2. **Traceability:** Every change has a documented reason (PR description)
3. **CI/CD Integration:** Automated tests catch issues early
4. **Collaboration:** PRs facilitate discussion and knowledge sharing
5. **Reversibility:** Easy to revert changes if needed

### Automated Protection

Our CI/CD pipeline enforces these rules automatically:
- Validates branch naming conventions
- Checks commit message format
- Runs plugin validation tests
- Scans for security issues
- Ensures documentation is updated

**Note:** Even if you have write access to the repository, please respect these rules. They exist to protect the project and maintain quality for all users.

## 📚 Additional Resources

- [Plugin Development Guide](./docs/PLUGIN_DEVELOPMENT.md)
- [Claude Code Documentation](https://docs.claude.com)
- [Conventional Commits](https://www.conventionalcommits.org/)

## 💬 Questions?

- Open a [Discussion](https://github.com/talent-factory/claude-plugins/discussions)
- Ask in your Pull Request
- Email: support@talent-factory.ch

## 🙏 Thank You!

Your contributions make this project better for everyone. We appreciate your time and effort!

---

**Maintained by:** Talent Factory GmbH  
**License:** MIT

