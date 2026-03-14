# Talent Factory Claude Plugins

<div class="grid cards" markdown>

-   :rocket:{ .lg .middle } **Getting Started**

    ---

    Install the marketplace and start using professional plugins in minutes.

    [:octicons-arrow-right-24: Quick Start](getting-started/quickstart.md)

-   :package:{ .lg .middle } **Browse Plugins**

    ---

    Explore 8 professional plugins for git, project management, code quality, development, education, and more.

    [:octicons-arrow-right-24: Plugin Catalog](plugins/index.md)

-   :books:{ .lg .middle } **Guides & Tutorials**

    ---

    Learn workflows with step-by-step tutorials for common tasks.

    [:octicons-arrow-right-24: View Guides](guides/index.md)

-   :hammer_and_wrench:{ .lg .middle } **Develop Plugins**

    ---

    Create your own plugins or contribute to existing ones.

    [:octicons-arrow-right-24: Development Guide](development/index.md)

</div>

---

## What are Claude Code Plugins?

**Claude Code Plugins** extend [Claude Code](https://claude.ai/code) with custom commands, agents, and skills tailored to your workflow. The **Talent Factory Marketplace** provides professional, production-ready plugins for:

- **Software Development**: Git workflows, code quality, project management
- **Education**: Teaching aids, student support, Java tutoring
- **Productivity**: Task management, documentation, automation

---

## Featured Plugins

### :material-git: Git Workflow

Professional git automation with emoji conventional commits, pre-commit checks, and PR management.

**Commands:** `/git-workflow:commit`, `/git-workflow:create-pr`, `/git-workflow:pr-edit-history`, `/git-workflow:resolve-conflicts`
**Skills:** `professional-commit-workflow`, `professional-pr-workflow`, `post-merge-cleanup`

[:octicons-arrow-right-24: Learn more](plugins/git-workflow.md){ .md-button }

---

### :material-clipboard-text: Project Management

Comprehensive project planning with PRD generation, Linear integration, and git worktree workflows.

**Commands:** `/project-management:create-prd`, `/project-management:create-plan`, `/project-management:init-task`, `/project-management:implement-task`, `/project-management:implement-epic`, `/project-management:document-handoff`
**Agents:** `epic-orchestrator`

[:octicons-arrow-right-24: Learn more](plugins/project-management.md){ .md-button }

---

### :material-code-braces: Code Quality

Expert code review and refactoring with specialized agents for Python, Java, and React.

**Commands:** `/code-quality:ruff-check`
**Agents:** `code-reviewer`, `python-expert`, `frontend-developer`

[:octicons-arrow-right-24: Learn more](plugins/code-quality.md){ .md-button }

---

### :material-school: Education

Teaching aids and student support for IT education with Java Tutor agent.

**Commands:** `/education:explain-code`
**Agents:** `java-tutor`, `markdown-syntax-formatter`
**Skills:** `markdown-syntax-formatter`

[:octicons-arrow-right-24: Learn more](plugins/education.md){ .md-button }

---

### :material-tools: Core Utilities

Development utilities for plugin validation, CI automation, and project initialization.

**Commands:** `/core:check`, `/core:check-commands`, `/core:check-agents`, `/core:build-skill`, `/core:package-skill`, `/core:create-command`, `/core:run-ci`
**Agents:** `agent-expert`, `command-expert`
**Skills:** `humanizer`, `pdf-to-markdown`

[:octicons-arrow-right-24: Learn more](plugins/core.md){ .md-button }

---

### :material-note-text: Obsidian Integration

Task management via Obsidian TaskNotes Plugin API with natural language support (DE/EN).

**Skills:** `tasknotes`

[:octicons-arrow-right-24: Learn more](plugins/obsidian.md){ .md-button }

---

### :material-laptop: Development

Expert development agents, project initialization with Git branching, Gradle Kotlin DSL, Python/uv support, and documentation synchronization.

**Commands:** `/development:init-project`
**Agents:** `java-developer`
**Skills:** `professional-init-project`, `update-documents`

[:octicons-arrow-right-24: Learn more](plugins/development.md){ .md-button }

---

### :material-bridge: Gemini Bridge

Model-agnostic bridge to Google Gemini 2.5 Pro for long-context codebase analysis (1M tokens), multimodal vision, and independent model validation.

**Commands:** `/gemini-bridge:analyze`, `/gemini-bridge:compare`, `/gemini-bridge:vision`
**Agents:** `gemini-analyst`, `model-router`
**Skills:** `gemini-analyst`

[:octicons-arrow-right-24: Learn more](plugins/gemini-bridge.md){ .md-button }

---

## Quick Installation

=== "Step 1: Add Marketplace"

    Add the Talent Factory marketplace to your `.claude/settings.json`:

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

=== "Step 2: Browse Plugins"

    Open Claude Code and use the plugin command:

    ```bash
    claude
    /plugin
    ```

    Select **"Browse Plugins"** → **"talent-factory"**

=== "Step 3: Install & Use"

    Choose plugins to install, then use commands like:

    ```bash
    /commit
    /create-pr
    /create-prd
    /review
    ```


---

## Community & Support

<div class="grid cards" markdown>

-   :material-github:{ .lg .middle } **GitHub**

    ---

    Report issues, request features, or contribute code.

    [:octicons-arrow-right-24: GitHub Repository](https://github.com/talent-factory/claude-plugins)

-   :material-shield-check:{ .lg .middle } **Security**

    ---

    Report security vulnerabilities responsibly.

    [:octicons-arrow-right-24: Security Policy](community/security.md)

-   :material-book-open-variant:{ .lg .middle } **Contributing**

    ---

    Learn how to contribute plugins, commands, or documentation.

    [:octicons-arrow-right-24: Contributing Guide](development/contributing.md)

-   :material-license:{ .lg .middle } **License**

    ---

    All plugins are open source under MIT License.

    [:octicons-arrow-right-24: View License](https://github.com/talent-factory/claude-plugins/blob/main/LICENSE)

</div>

---

## About Talent Factory

**Talent Factory GmbH** is a Swiss company specializing in software development education and professional tooling. We create high-quality educational resources and development tools for students, educators, and professional developers.

[:material-web: talent-factory.xyz](https://talent-factory.xyz){ .md-button .md-button--primary }
