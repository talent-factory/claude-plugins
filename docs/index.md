# Talent Factory Claude Plugins

<div class="grid cards" markdown>

-   :rocket:{ .lg .middle } **Getting Started**

    ---

    Install the marketplace and start using professional plugins in minutes.

    [:octicons-arrow-right-24: Quick Start](getting-started/quickstart.md)

-   :package:{ .lg .middle } **Browse Plugins**

    ---

    Explore 6 professional plugins for git, project management, code quality, and education.

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

**Commands:** `/commit`, `/create-pr`, `/pr-edit-history`
**Skills:** `professional-commit-workflow`, `professional-pr-workflow`

[:octicons-arrow-right-24: Learn more](plugins/git-workflow.md){ .md-button }

---

### :material-clipboard-text: Project Management

Comprehensive project planning with PRD generation, Linear integration, and git worktree workflows.

**Commands:** `/create-prd`, `/create-plan`, `/implement-task`, `/sync-linear`
**Skills:** `prd-workflow`, `linear-workflow`

[:octicons-arrow-right-24: Learn more](plugins/project-management.md){ .md-button }

---

### :material-code-braces: Code Quality

Expert code review and refactoring with specialized agents for Python, Java, and React.

**Commands:** `/review`, `/refactor`, `/lint-python`
**Agents:** `python-expert`, `java-expert`, `frontend-expert`

[:octicons-arrow-right-24: Learn more](plugins/code-quality.md){ .md-button }

---

### :material-school: Education

Teaching aids and student support for IT education with Java Tutor agent.

**Commands:** `/explain-code`, `/format-markdown`
**Agents:** `java-tutor`

[:octicons-arrow-right-24: Learn more](plugins/education.md){ .md-button }

---

### :material-tools: Core Utilities

Development utilities for plugin validation, CI automation, and project initialization.

**Commands:** `/check`, `/check-commands`, `/check-agents`, `/build-skill`, `/create-command`, `/init-project`, `/run-ci`, `/humanize`
**Agents:** `plugin-developer`, `command-developer`, `agent-developer`

[:octicons-arrow-right-24: Learn more](plugins/core.md){ .md-button }

---

### :material-note-text: Obsidian Integration

Task management via Obsidian TaskNotes Plugin API with natural language support (DE/EN).

**Commands:** `/task`, `/tasks`, `/task-complete`, `/task-delete`

[:octicons-arrow-right-24: Learn more](plugins/obsidian.md){ .md-button }

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

[:material-web: talent-factory.ch](https://talent-factory.ch){ .md-button .md-button--primary }
