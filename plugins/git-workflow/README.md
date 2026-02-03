# Git Workflow Plugin

Professional git workflow automation with pre-commit checks, emoji conventional commits, PR management, and comprehensive references.

## Version 2.1.0

**Minor Update:** Added `post-merge-cleanup` skill for automated branch cleanup after merge. Now includes 3 professional workflow skills.

## Commands

### `/commit`

Create professional git commits with automated pre-commit checks and emoji conventional commit format.

**Features:**

- 🎨 Emoji Conventional Commits (✨ feat, 🐛 fix, 📚 docs, etc.)
- ⚡ Automated pre-commit checks for Java, Python, React, and Documentation
- 🔍 Project type detection (Maven, Gradle, npm, pytest, etc.)
- 📋 Comprehensive commit message validation
- 🚀 Optional integration with professional-commit-workflow skill (~70% faster)
- ✅ Best practices enforcement
- 📖 Extensive reference documentation

**Usage:**
```bash
/commit                    # Standard workflow
/commit --no-verify        # Skip pre-commit checks
/commit --skip-tests       # Skip test execution
/commit --with-skills      # Use professional-commit-workflow skill
```

**Pre-Commit Checks:**

- **Java**: Maven/Gradle build, Checkstyle, JUnit tests
- **Python**: Ruff/Black formatting, pytest, mypy type checking
- **React/Node.js**: ESLint, Prettier, TypeScript compilation, Jest/Vitest
- **Documentation**: LaTeX compilation, Markdown linting

**Supported Commit Types:**

- ✨ `feat` - New features
- 🐛 `fix` - Bug fixes
- 📚 `docs` - Documentation changes
- 💎 `style` - Code formatting
- ♻️ `refactor` - Code restructuring
- ⚡ `perf` - Performance improvements
- 🧪 `test` - Testing
- 🔧 `chore` - Build/tools/config

See [commit-types.md](https://github.com/talent-factory/claude-plugins/blob/main/plugins/git-workflow/references/commit/commit-types.md) for complete list.

**References:**
- [Best Practices](https://github.com/talent-factory/claude-plugins/blob/main/plugins/git-workflow/references/commit/best-practices.md) - Commit quality guidelines
- [Commit Types](https://github.com/talent-factory/claude-plugins/blob/main/plugins/git-workflow/references/commit/commit-types.md) - Complete emoji conventional commit types
- [Pre-Commit Checks](https://github.com/talent-factory/claude-plugins/blob/main/plugins/git-workflow/references/commit/pre-commit-checks.md) - Automated validation details
- [Troubleshooting](https://github.com/talent-factory/claude-plugins/blob/main/plugins/git-workflow/references/commit/troubleshooting.md) - Common issues and solutions

### `/create-pr`

Create pull requests with automated branch management, commit analysis, and professional PR descriptions.

**Features:**

- 📝 Automatic PR description generation from commits
- 🔍 Branch status verification and validation
- 💪 Related issue linking and references
- ⚡ Breaking changes documentation
- 👥 Reviewer suggestions
- 🎯 Test plan generation
- 🔄 Code formatting integration (Biome, Black, Prettier)
- 🚀 Optional integration with professional-pr-workflow skill

**Usage:**
```bash
/create-pr                 # Standard PR creation
/create-pr --no-format     # Skip code formatting
/create-pr --with-skills   # Use professional-pr-workflow skill
```

**PR Description Includes:**

- Summary of changes from all commits (not just latest!)
- Technical implementation details
- Breaking changes (if any)
- Related issues and references
- Comprehensive test plan checklist
- Generated with Claude Code attribution

**References:**

- [Code Formatting](https://github.com/talent-factory/claude-plugins/blob/main/plugins/git-workflow/references/create-pr/code-formatting.md) - Automatic code formatting
- [Commit Workflow](https://github.com/talent-factory/claude-plugins/blob/main/plugins/git-workflow/references/create-pr/commit-workflow.md) - Commit management in PRs
- [PR Template](https://github.com/talent-factory/claude-plugins/blob/main/plugins/git-workflow/references/create-pr/pr-template.md) - PR description structure
- [Troubleshooting](https://github.com/talent-factory/claude-plugins/blob/main/plugins/git-workflow/references/create-pr/troubleshooting.md) - Common PR issues

### `/pr-edit-history`

Display the edit history of a GitHub Pull Request description.

**Features:**

- 📜 View all edits made to PR description
- 👤 See who made each edit
- ⏰ Timestamps for all changes
- 🔍 Diff view between versions

**Usage:**
```bash
/pr-edit-history           # For current branch's PR
/pr-edit-history 123       # For PR #123
```

## Skills

This plugin includes two powerful skills for enhanced performance. See [Skills & Agents Activation Guide](../reference/skills-agents-activation.md) for details.

### professional-commit-workflow

**~70% faster** than standard command with reduced token consumption.

**Activation:**

- Via command: `/commit --with-skills`

**Features:**

- Automatic project type detection
- Pre-commit validation (Java, Python, React, Docs)
- Emoji Conventional Commit generation
- JSON-based configuration
- Python module extensibility

**Location:** `./skills/professional-commit-workflow/`

**Documentation:** [professional-commit-workflow/README.md](https://github.com/talent-factory/claude-plugins/blob/main/plugins/git-workflow/skills/professional-commit-workflow/README.md)

### professional-pr-workflow

Automated PR creation with branch management and code formatting.

**Activation:**

- Via command: `/create-pr --with-skills`

**Features:**

- Branch creation and management
- Automatic commit splitting
- Code formatter integration (Biome, Black, Prettier)
- PR description generation
- GitHub CLI integration

**Location:** `./skills/professional-pr-workflow/`

**Documentation:** [professional-pr-workflow/README.md](https://github.com/talent-factory/claude-plugins/blob/main/plugins/git-workflow/skills/professional-pr-workflow/README.md)

## Installation

This plugin is part of the Talent Factory marketplace.

**Add marketplace to `.claude/settings.json`:**
```json
{
  "extraKnownMarketplaces": {
    "talent-factory": {
      "source": {
        "source": "github",
        "repo": "talent-factory/claude-plugins"
      }
    }
  },
  "enabledPlugins": {
    "git-workflow@talent-factory": true
  }
}
```

**Install via Claude Code:**
```bash
claude
/plugin
# Select "Browse Plugins" → "talent-factory" → "Git Workflow"
```

## Project Structure

```
git-workflow/
├── .claude-plugin/
│   └── plugin.json           # Plugin metadata
├── commands/
│   ├── commit.md             # Commit command
│   ├── create-pr.md          # PR creation command
│   └── pr-edit-history.md    # PR edit history
├── references/
│   ├── commit/
│   │   ├── best-practices.md
│   │   ├── commit-types.md
│   │   ├── pre-commit-checks.md
│   │   └── troubleshooting.md
│   └── create-pr/
│       ├── code-formatting.md
│       ├── commit-workflow.md
│       ├── pr-template.md
│       └── troubleshooting.md
├── skills/
│   ├── professional-commit-workflow/
│   └── professional-pr-workflow/
└── README.md
```

## Best Practices

### Commit Workflow

1. **Always use `/commit`** instead of direct `git commit`
2. **Let automated checks run** - they catch issues early
3. **Write descriptive messages** - explain the "why", not just the "what"
4. **Keep commits atomic** - one logical change per commit
5. **Use imperative mood** - "Add feature" not "Added feature"
6. **No tool signatures** - commits should not include "Generated with Claude Code"

### PR Workflow

1. **Use `/create-pr`** for consistency across team
2. **Review PR description** before creating
3. **Keep PRs small** - ideally < 400 lines changed
4. **Link related issues** - use "Fixes #123" syntax
5. **Document breaking changes** clearly
6. **Include test plan** - how to verify changes

### Code Quality

- ✅ Run linters before committing
- ✅ Ensure all tests pass
- ✅ Update documentation
- ✅ Remove debug statements
- ✅ Check for secrets/API keys
- ✅ Review your own diff first

## Examples

### Creating a Feature Commit

```bash
/commit

# Claude analyzes changes and generates:
✨ feat: Benutzer-Authentifizierung mit OAuth2 hinzugefügt

Implementiert OAuth2-Flow für Google und GitHub Login.
Erweitert User-Model mit OAuth-Feldern.

- Google OAuth2 Provider konfiguriert
- GitHub OAuth2 Provider konfiguriert
- Token-Refresh-Mechanismus implementiert
- Session-Management aktualisiert

Closes #123
```

### Creating a Pull Request

```bash
/create-pr

# Claude:
# 1. Analyzes all commits in branch
# 2. Checks branch status
# 3. Runs code formatters (if enabled)
# 4. Generates comprehensive PR description
# 5. Creates PR with `gh pr create`
# 6. Returns PR URL
```

### Checking PR Edit History

```bash
/pr-edit-history 456

# Claude displays:
# - All edits to PR #456
# - Who made each edit
# - When edits were made
# - Diff between versions
```

## Advanced Usage

### Commit with Skill Integration

```bash
/commit --with-skills

# Uses professional-commit-workflow skill:
# - ~70% faster execution
# - Lower token consumption (~300 lines vs ~1400)
# - Same quality output
# - Global configuration
```

### Skip Pre-Commit Checks

```bash
/commit --no-verify

# Use when:
# - Checks are failing due to infrastructure issues
# - Emergency hotfix needed
# - Working on non-code files only
```

### PR with Custom Formatting

```bash
/create-pr --no-format

# Skips automatic code formatting
# Useful when formatters conflict with team style
```

## Troubleshooting

### Commit Command Issues

**Problem:** Pre-commit checks fail
- **Solution:** See [commit/troubleshooting.md](https://github.com/talent-factory/claude-plugins/blob/main/plugins/git-workflow/references/commit/troubleshooting.md)

**Problem:** Commit message too long
- **Solution:** Keep subject line ≤ 72 characters, use body for details

**Problem:** Wrong commit type detected
- **Solution:** Claude analyzes changes, but you can override in message

### PR Creation Issues

**Problem:** GitHub CLI not found
- **Solution:** Install with `brew install gh` or download from github.com/cli/cli

**Problem:** Branch not pushed to remote
- **Solution:** `/create-pr` will push automatically with `-u` flag

**Problem:** PR description truncated
- **Solution:** Large diffs may truncate; commit more frequently

See [create-pr/troubleshooting.md](https://github.com/talent-factory/claude-plugins/blob/main/plugins/git-workflow/references/create-pr/troubleshooting.md) for more solutions.

## Requirements

- **Git:** Version 2.23+ recommended
- **GitHub CLI:** Optional but recommended for `/create-pr`
- **Working directory:** Must be inside a git repository

**Project-Specific:**
- **Java:** Maven or Gradle
- **Python:** Ruff/Black, pytest, mypy (optional)
- **React/Node.js:** ESLint, Prettier, TypeScript (optional)

## Changelog

### Version 2.1.0 (2026-02-03)

**Minor Update:**

- ✨ Added `post-merge-cleanup` skill for automated branch cleanup after merge
- Now includes 3 professional workflow skills

### Version 2.0.0 (2026-01-10)

**Major Update:**

- ✨ Added comprehensive reference documentation
- ✨ Integrated professional-commit-workflow skill
- ✨ Integrated professional-pr-workflow skill
- ✨ Added `/pr-edit-history` command
- 📚 Expanded commit types with emoji support
- 📚 Added troubleshooting guides
- 🔧 Enhanced pre-commit checks
- 🔧 Improved PR description generation

**Migration from 1.0.0:**

- All existing commands remain compatible
- New `--with-skills` flag optional
- References available for enhanced guidance

### Version 1.0.0

- Initial release with `/commit` and `/create-pr`

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
