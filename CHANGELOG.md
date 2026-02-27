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

#### project-management 2.5.0 (Minor Update)

- 🧠 Added plugin orchestration to `/project-management:implement-task` (Superpowers brainstorm, agent routing, quality gate)
- ⚡ Added skip options: `--skip-brainstorm`, `--skip-quality-gate`
- 📚 Added reference documentation: agent-routing, context-analysis, quality-gate
- Now includes 5 commands, 1 agent

#### git-workflow 2.2.0 (Minor Update)

- ✨ Added `/resolve-conflicts` command for intelligent merge conflict resolution
- 📖 Added comprehensive reference documentation (strategies, best practices, troubleshooting)
- 🧠 Smart merge strategy with semantic code analysis
- 🔀 Support for `smart`, `ours`, and `theirs` strategies
- 🧪 Automated test and lint validation after resolution
- Now includes 4 commands and 3 professional workflow skills

#### development 1.3.0 (Minor Update)

- ✨ Added `update-documents` skill for documentation synchronization
- 📄 Syncs content between CLAUDE.md, README.md, and docs/
- 🔍 Code block awareness to avoid false section detection
- 📝 Auto-creation of missing sections in target files
- Now includes 1 command, 1 agent, and 2 skills

#### core 3.1.0 (Minor Update)

- ✨ Added `pdf-to-markdown` skill for PDF to Markdown conversion
- 📄 Dual-mode support: fast (PyMuPDF) and vision (Claude Code analysis)
- 🔍 LaTeX umlaut correction (¨a → ä, ¨o → ö, ¨u → ü)
- 🇨🇭 Swiss German orthography (ß → ss)
- 📊 Table recognition and code block detection
- 📚 Added comprehensive guide in docs/guides/pdf-to-markdown.md
- Now includes 7 commands, 2 skills, and 2 expert agents

#### git-workflow 2.1.0 (Minor Update)

- ✨ Added `post-merge-cleanup` skill for automated branch cleanup after merge
- Now includes 3 skills total

#### obsidian 1.1.1

- 🔧 Patch release with minor improvements

#### education 1.3.1

- 🔧 Patch release with minor improvements

#### development 1.2.1

- 🔧 Java projects now always use Gradle Kotlin DSL (not Maven)
- 🔧 Initial commit uses `/git-workflow:commit`
- 📚 Clearer step-by-step instructions in skill

#### development 1.1.0 (NEW)

- New plugin for expert development agents and project initialization
- Added `java-developer` agent (moved from code-quality plugin)
- Added `/init-project` command (moved from core plugin)
- All documentation in professional English

#### code-quality 3.0.0 (Breaking Change)

- Breaking: Moved `java-developer` agent to development plugin
- Updated description and documentation

#### core 3.0.0 (Breaking Change)

- Breaking: Moved `/init-project` command to development plugin
- Updated documentation to English
- Now includes 7 commands, 1 skill, and 2 expert agents

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

#### project-management 2.2.0 (Major Update)

- ✨ Added `/create-plan` command with Linear integration and task breakdown
- ✨ Added `/implement-task` command with git worktree workflow
- ✨ Added `/update-task` command for task status updates
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

#### core 2.1.0 (Major Update)

- ✨ Added `/check` command for project validation without commits
- ✨ Added `/create-command` for pattern-based command generation
- ✨ Added `/init-project` for OpenSource project initialization
- ✨ Added `/run-ci` for local CI execution with auto-fix
- 🤖 Added agent-expert agent for agent design and optimization
- 🤖 Added command-expert agent for CLI development
- 🤖 Added skill-builder agent system (4 specialized agents):
  - skill-elicitation-agent - Requirements gathering
  - skill-generator-agent - Code generation
  - skill-validator-agent - Testing and validation
  - skill-documenter-agent - Documentation creation
- 🎨 Added humanizer skill for text humanization and AI writing improvement
- 🔧 Enhanced `/check-commands` with best practices validation
- 🔧 Enhanced `/check-agents` with color attribute checking
- 🔧 Enhanced `/build-skill` with elicitation-driven development
- 🔧 Enhanced `/package-skill` with dependency checking
- 📖 Extensive README with 8 commands, 3 agents, and 1 skill

#### code-quality 2.0.0 (Major Update)

- ✨ Added `/ruff-check` command for Python linting with Ruff
- 🤖 Added code-reviewer agent for proactive code reviews
- 🤖 Added python-expert agent for idiomatic Python development
- 🤖 Added java-developer agent for modern Java/Spring Boot
- 🤖 Added frontend-developer agent for Next.js/React/Tailwind

#### education 1.1.0

- 🤖 Added markdown-syntax-formatter agent for Markdown formatting
- 📚 Converts visually formatted text to proper Markdown syntax
- ✅ Fixes formatting issues (lists, headings, code blocks, emphasis)

#### obsidian 1.0.1

- ✨ Initial release with TaskNotes Plugin API integration
- 🎯 Task management via natural language (German/English)
- 📝 List, create, update, and delete tasks in Obsidian
- 💡 Work recommendations based on task priorities
- 🔗 Direct integration with Obsidian vault via HTTP API
- 🛠️ CLI commands for task management
- 📖 Comprehensive documentation with setup guide

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

## [2.6.0] - 2026-02-27

### Added
- **project-management**: New `/project-management:init-task` command for single-task creation with duplicate detection, ATOMIC validation, and mandatory Definition of Done
- **project-management**: Task template reference with extended metadata fields (Type, Plan, Definition of Done)
- **project-management**: Duplicate detection reference with cross-provider search (filesystem + Linear)
- **project-management**: Validation rules reference with ATOMIC criteria enforcement

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
- [Roadmap](https://github.com/talent-factory/claude-plugins#roadmap)

---

*For plugin-specific changelogs, see individual plugin README files.*
