# Changelog

All notable changes to the Talent Factory Claude Plugins project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project setup with OpenSource best practices
- Comprehensive documentation for contributors
- GitHub Actions workflows for CI/CD
- Branch protection guidelines and automation
- Security policy and vulnerability reporting process

### Plugins

#### git-workflow 2.0.0 (Major Update)
- ✨ Migrated comprehensive commands from dotfiles with full references
- ✨ Added `/pr-edit-history` command for PR description tracking
- ✨ Integrated professional-commit-workflow skill (~70% faster)
- ✨ Integrated professional-pr-workflow skill
- 📚 Added comprehensive reference documentation:
  - commit/best-practices.md - Commit quality guidelines
  - commit/commit-types.md - Complete emoji conventional commits
  - commit/pre-commit-checks.md - Automated validation details
  - commit/troubleshooting.md - Common issues and solutions
  - create-pr/code-formatting.md - Automatic formatting
  - create-pr/commit-workflow.md - Commit management in PRs
  - create-pr/pr-template.md - PR description structure
  - create-pr/troubleshooting.md - Common PR issues
- 🔧 Enhanced pre-commit checks for Java, Python, React, Documentation
- 🔧 Improved PR description generation from all commits
- 📖 Extensive README with examples, best practices, and troubleshooting

#### project-management 2.0.0 (Major Update)
- ✨ Added `/create-plan` command with Linear integration and task breakdown
- ✨ Added `/implement-task` command with git worktree workflow
- ✨ Enhanced `/create-prd` with comprehensive templates
- 📚 Added comprehensive reference documentation (13 files):
  - create-prd/best-practices.md - PRD quality guidelines
  - create-prd/sections-guide.md - Detailed section templates
  - create-prd/templates.md - Ready-to-use templates
  - create-plan/agent-mapping.md - Agent selection guidelines
  - create-plan/best-practices.md - Planning methodologies
  - create-plan/filesystem.md - File-based plan storage
  - create-plan/linear-integration.md - Linear API usage
  - create-plan/task-breakdown.md - Task decomposition
  - implement-task/best-practices.md - Implementation guidelines
  - implement-task/filesystem.md - Task file management
  - implement-task/linear.md - Linear integration
  - implement-task/troubleshooting.md - Common issues
  - implement-task/workflow.md - Complete workflow guide
- 🔗 Integrated Linear API for issue synchronization
- 🌲 Added git worktree support for isolated development
- 📖 Extensive README with workflow examples and Linear setup

### Infrastructure
- GitHub Issue templates (bug report, feature request)
- Pull Request template with comprehensive checklist
- Automated PR labeling based on content and size
- Stale issue and PR management
- First-time contributor greeting workflow
- Branch protection validation workflow
- Plugin validation and testing workflow
- Security scanning integration
- Markdown link checking

### Documentation
- CODE_OF_CONDUCT.md with contact information
- SECURITY.md with security policies and reporting
- CONTRIBUTING.md with detailed contribution guidelines
- Plugin Development Guide (docs/PLUGIN_DEVELOPMENT.md)
- Branch Protection Setup Guide (.github/BRANCH_PROTECTION_SETUP.md)
- Enhanced .gitignore for better exclusions

### Configuration
- GitHub labeler configuration
- Markdown link check configuration
- Funding configuration (prepared for future use)

## Version Format

Versions follow semantic versioning (MAJOR.MINOR.PATCH):
- **MAJOR:** Breaking changes
- **MINOR:** New features, backwards compatible
- **PATCH:** Bug fixes, backwards compatible

## Categories

Changes are grouped by category:
- **Added:** New features
- **Changed:** Changes to existing functionality
- **Deprecated:** Features that will be removed
- **Removed:** Removed features
- **Fixed:** Bug fixes
- **Security:** Security improvements
- **Infrastructure:** CI/CD, tooling, and infrastructure changes
- **Documentation:** Documentation updates

## Links

- [GitHub Releases](https://github.com/talent-factory/claude-plugins/releases)
- [GitHub Milestones](https://github.com/talent-factory/claude-plugins/milestones)
- [Roadmap](README.md#roadmap)

---

*For plugin-specific changelogs, see individual plugin README files.*
