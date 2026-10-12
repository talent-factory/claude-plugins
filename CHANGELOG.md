# Changelog

All notable changes to the Talent Factory Claude Plugins project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **education 1.8.0**: `md-to-pdf` ConTeXt output — code blocks become a breakable framed table with grey background (replaces the shaded box, which overflowed the footer at page breaks); each code block gets a `Listing N: Titel` caption (title from the info string); table captions accept `: Titel` and `: Table: Titel` and render as `Tabelle N: Titel`, flush left; spacing around code blocks; unit tests for the transformations
- **education 1.7.0**: `md-to-pdf` profile `ffhs-thesis` for FFHS theses (ConTeXt) — layout after the FFHS thesis template (A4, 11 pt, Helvetica-compatible font, 1.5 line spacing, 3 cm side margins), title page from `[these]` in `md-to-pdf.toml`, roman front matter with arabic main text, table of contents and optional lists of figures and tables; validation of `[these]` and unit/end-to-end tests
- **education 1.6.0**: `md-to-pdf` skill — Markdown to PDF or ConTeXt source with configurable header/footer, font, and margins (CLI or `md-to-pdf.toml`), ConTeXt (default) or XeLaTeX engine, and automatic Mermaid rendering; adapted from the personal `md-to-pdf` skill and made plugin-relative via `${CLAUDE_PLUGIN_ROOT}`
- **dev-browser 1.0.0**: new plugin — browser automation on the Playwright Python API. Persistent-session profile (cookies/logins survive across runs), YAML accessibility-tree element discovery (`snapshot()`), screenshot capture, and network-interception scraping; honours an ambient `HTTPS_PROXY` and auto-detects a pre-installed Chromium, so it works out-of-the-box in Claude Code web. Self-contained `scripts/browser.py` helper with a network-free self-check. Reimplemented in Python (no Node/extension runtime); inspired by [SawyerHood/dev-browser](https://github.com/SawyerHood/dev-browser) (MIT)
- **core 3.2.0**: Ponytail minimalism suite — four skills adapted from [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) (MIT): `ponytail` (always-on lazy-coding discipline with a seven-rung YAGNI/stdlib-first ladder and `lite`/`full`/`ultra` intensity), `ponytail-review` (diff review for over-engineering), `ponytail-audit` (repo-wide bloat audit), and `ponytail-debt` (`ponytail:` shortcut-comment debt ledger); invocation hints namespaced to `/core:ponytail*`, prose cross-reference repointed to the `humanizer` skill, repo-standard frontmatter added
- **obsidian 1.4.0**: shared validation module (`skills/_shared/scripts/validate.py` + `validation-rules.md`) — deterministic frontmatter, kind/type, dead-link, and asymmetric-link checks used by all wiki skills
- **obsidian 1.4.0**: write-time validation gate in `wiki-ingest` and `wiki-migrate-file` — malformed pages are blocked with a structured error before any vault write
- **obsidian 1.4.0**: contradiction propose-and-confirm workflow in `wiki-ingest` — conflicting claims are surfaced for user resolution before the page is committed
- **obsidian 1.4.0**: `wiki-think` skill — structured deep reasoning against the knowledge base in challenge / connect / socratic mode; optional `type: thinking` page output
- **obsidian 1.4.0**: `wiki-maintain` skill — non-interactive lint + deterministic auto-fix pass with written report; cron/launchd scheduling recipes provided
- **obsidian 1.4.0**: `wiki-lint` refactored to delegate all deterministic checks to the shared validation module (behavior unchanged)
- **git-workflow 2.3.0**: `hunk-review` skill for interactive terminal diff review sessions via the Hunk CLI — session discovery, hunk navigation, and batch inline commenting (adapted from [modem-dev/hunk](https://github.com/modem-dev/hunk), MIT)
- **obsidian 1.3.0**: `today` skill — prioritised daily briefing from TaskNotes, Google Calendar, Gmail, Linear, and GitHub; writes to today's Obsidian daily note
- **obsidian 1.3.0**: `weekly-review` skill — structured weekly retrospective with completed tasks, shipped code, meetings, wiki learnings, and Linear progress; preserves user-written Reflection section on re-runs
- **obsidian 1.3.0**: `project-pulse` skill — GitHub repository status snapshot categorised as Active / Dormant / Stalled; terminal output only
- **obsidian 1.3.0**: `ideas` skill — opportunity mining across wiki, GitHub portfolio, stakeholder notes, and market trends; writes a structured ideas document to the vault
- **obsidian 1.3.0**: `update_daily_note.py` script — configurable note create/update utility with `--vault`, `--daily-dir`, `--template`, `--section-heading`, and `--anchor` CLI flags; resolves config from CLAUDE.md keys and environment variables with auto-detection fallback
- **obsidian 1.3.0**: all four new skills use a unified CLAUDE.md configuration system (`obsidian_vault`, `obsidian_daily_dir`, `github_org`, etc.) with environment variable overrides and vault auto-detection
- **education 1.5.0**: `explain-code` skill — patient programming instructor that explains code structure and design decisions, adapts to student level (Beginner / Intermediate / Advanced), and generates exercises
- **gemini-bridge 1.1.0**: `analyze` skill — delegates large-context or multimodal analysis to Gemini 2.5 Pro with automatic Claude-vs-Gemini routing guidance
- **gemini-bridge 1.1.0**: `compare` skill — independent two-approach comparison via Gemini implementing the "propose with Claude, validate with Gemini" pattern
- **gemini-bridge 1.1.0**: `vision` skill — transforms screenshots, mockups, diagrams, and PDFs into code or documentation using Gemini's multimodal capabilities
- **code-quality 3.1.0**: `ruff-check` skill — lints and formats Python files via Ruff; activates on natural-language requests such as "lint my Python"
- **git-workflow 2.4.0**: `resolve-conflicts` skill — semantic merge conflict resolution with 10-step workflow, test validation, and structured report; activates on "I have merge conflicts"
- **project-management 2.7.0**: `document-handoff` skill — creates comprehensive pre-compact handoff documentation; activates on "prepare a handoff" or "context is getting too large"

### Changed

- **Repository workflow**: switched to **trunk-based development**. Retired the `develop` integration branch — `main` is now the single long-lived branch and the live marketplace source; all work lands via short-lived branches and Pull Requests to `main`. Updated branch protection, CI triggers (`validate-plugins.yml`, `branch-protection.yml`), `CLAUDE.md`, `CONTRIBUTING.md`, and `.github/BRANCH_PROTECTION_SETUP.md`. Rationale: a dedicated `develop` only pays off with batched, staged releases against a consuming environment, which this marketplace does not have.

### Fixed

- **education 1.7.1**: `md-to-pdf` ConTeXt output — code blocks use a monospaced font (`tt`), so indentation is kept, and the shaded frame around code blocks is removed, so the last code line no longer overlaps the footer at a page break

## [1.5.0] - 2026-05-01

### Added

- **obsidian**: LLM-Wiki workflow with four new skills — `wiki-ingest`, `wiki-lint`, `wiki-migrate-file`, `wiki-query`
- **obsidian**: Configurable `<wiki-root>` placeholder (default `Wiki/`) with vault-level `CLAUDE.md` overrides for `wiki_root` and `wiki_migration_cap`
- **obsidian**: Keywords `wiki`, `knowledge-base`, `llm-wiki`

### Fixed

- **core**: `pdf-to-markdown` skill — `convert_vision_api` referenced an undefined `end_page` in the header f-string, raising `NameError` after every Vision API run; fixed by computing `end_page` from `start_page + pages_converted - 1`
- **core**: `pdf-to-markdown` skill — `total_pages` was reused for both the converted slice and the full PDF length; now derived separately via `pdfinfo_from_path` so the header reads "Pages: 5-10 of 247" instead of "5-10 of 6"
- **core**: `pdf-to-markdown` skill — default Vision API model updated from the retired `claude-sonnet-4-20250514` to `claude-opus-4-7` for high-resolution image handling

### Plugin Versions

| Plugin | Version |
|--------|---------|
| git-workflow | 2.2.2 |
| project-management | 2.6.2 |
| code-quality | 3.0.2 |
| education | 1.4.0 |
| core | 3.1.3 |
| obsidian | 1.2.0 |
| development | 1.3.2 |
| gemini-bridge | 1.0.1 |

---

## [1.4.0] - 2026-03-28

### Added

- **education**: FFHS Lecture Slides skill for reveal.js and PowerPoint presentation generation
- **education**: Keywords for FFHS, presentations, and slides

### Plugin Versions

| Plugin | Version |
|--------|---------|
| git-workflow | 2.2.2 |
| project-management | 2.6.2 |
| code-quality | 3.0.2 |
| education | 1.4.0 |
| core | 3.1.3 |
| obsidian | 1.1.2 |
| development | 1.3.2 |
| gemini-bridge | 1.0.1 |

---

## [1.3.1] - 2026-03-13

### Changed

- **Marketplace version**: 1.3.1
- **Frontmatter standardization**: Normalized YAML frontmatter across all 38 agent and command files (field ordering, missing fields, data type corrections)
- **Language policy enforcement**: Translated 13 German reference and skill documentation files to professional English
- **Agent tools format**: Converted comma-separated tool strings to proper YAML arrays in 4 skill-builder agents
- **Category taxonomy**: Unified `develop` → `development`, `project-task-management` → `project`
- **Version synchronization**: Updated all README.md and docs/ files to match plugin.json versions

### Plugin Versions

| Plugin | Version |
|--------|---------|
| git-workflow | 2.2.2 |
| project-management | 2.6.2 |
| code-quality | 3.0.2 |
| education | 1.3.3 |
| core | 3.1.3 |
| obsidian | 1.1.2 |
| development | 1.3.2 |
| gemini-bridge | 1.0.1 |

### Fixed

- Git identity configuration in auto-tag GitHub Actions workflow
- Gemini Bridge command and agent frontmatter errors
- Silent None return in Gemini Bridge status endpoint
- `java-developer` agent: Moved `<example>` blocks from frontmatter description to body

---

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
