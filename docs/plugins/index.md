# Plugin Catalog

Browse all available plugins in the Talent Factory marketplace. Each plugin provides specialized commands, agents, and skills for different workflows.

---

## All Plugins

| Plugin                                      | Version | Commands | Agents | Skills | Tags                                |
| ------------------------------------------- | ------- | -------- | ------ | ------ | ----------------------------------- |
| [Git Workflow](git-workflow.md)             | 2.4.0   | 4        | 0      | 5      | git, workflow, commits, PRs, merge  |
| [Project Management](project-management.md) | 2.7.0   | 6        | 1      | 1      | planning, PRD, Linear, EPIC, agile  |
| [Code Quality](code-quality.md)             | 3.1.0   | 1        | 3      | 1      | review, quality, Python, React      |
| [Education](education.md)                   | 1.6.0   | 1        | 2      | 3      | teaching, learning, markdown, FFHS  |
| [Core Utilities](core.md)                   | 3.2.0   | 7        | 2      | 6      | validation, CI, PDF, ponytail, dev  |
| [Obsidian Integration](obsidian.md)         | 1.4.0   | 0        | 0      | 11     | tasks, Obsidian, wiki, briefing, ideas |
| [Development](development.md)               | 1.3.2   | 1        | 1      | 2      | java, gradle, python, documentation |
| [Gemini Bridge](gemini-bridge.md)           | 1.1.0   | 3        | 2      | 4      | gemini, mcp, multi-model, vision    |
| [Dev Browser](dev-browser.md)               | 1.0.0   | 0        | 0      | 1      | browser, playwright, scraping, testing |

---

## By Category

### :material-git: Development Workflow

<div class="grid cards" markdown>

- **Git Workflow**

  ***

  Professional git automation with emoji conventional commits, pre-commit checks, PR management, and intelligent merge conflict resolution.

  **Commands:** `/git-workflow:commit`, `/git-workflow:create-pr`, `/git-workflow:pr-edit-history`, `/git-workflow:resolve-conflicts`
  **Skills:** `professional-commit-workflow`, `professional-pr-workflow`, `post-merge-cleanup`

  [:octicons-arrow-right-24: Details](git-workflow.md)

- **Project Management**

  ***

  Comprehensive project planning with PRD generation, single-task initialization, EPIC automation, Linear integration, and git worktree workflows.

  **Commands:** `/project-management:create-prd`, `/project-management:create-plan`, `/project-management:init-task`, `/project-management:implement-task`, `/project-management:implement-epic`, `/project-management:document-handoff`
  **Agents:** `epic-orchestrator`

  [:octicons-arrow-right-24: Details](project-management.md)

</div>

---

### :material-code-braces: Code Quality & Development

<div class="grid cards" markdown>

- **Code Quality**

  ***

  Expert code review and refactoring with specialized agents for Python and React/Frontend development.

  **Commands:** `/code-quality:ruff-check`
  **Agents:** `python-expert`, `frontend-developer`, `code-reviewer`

  [:octicons-arrow-right-24: Details](code-quality.md)

- **Development**

  ***

  Expert development agents, project initialization with Git branching, Java/Gradle, Python/uv, and documentation synchronization tools.

  **Commands:** `/development:init-project`
  **Agents:** `java-developer`
  **Skills:** `professional-init-project`, `update-documents`

  [:octicons-arrow-right-24: Details](development.md)

- **Gemini Bridge**

  ***

  Model-agnostic bridge to Google Gemini 2.5 Pro — long-context codebase analysis, multimodal vision, and independent model validation.

  **Commands:** `/gemini-bridge:analyze`, `/gemini-bridge:compare`, `/gemini-bridge:vision`
  **Agents:** `gemini-analyst`, `model-router`
  **Skills:** `gemini-analyst`

  [:octicons-arrow-right-24: Details](gemini-bridge.md)

- **Core Utilities**

  ***

  Development utilities for plugin validation, CI automation, plugin development, PDF-to-Markdown conversion, and the Ponytail minimalism suite.

  **Commands:** `/core:check`, `/core:check-commands`, `/core:check-agents`, `/core:build-skill`, `/core:package-skill`, `/core:create-command`, `/core:run-ci`
  **Agents:** `agent-expert`, `command-expert`
  **Skills:** `humanizer`, `pdf-to-markdown`, `ponytail`, `ponytail-review`, `ponytail-audit`, `ponytail-debt`

  [:octicons-arrow-right-24: Details](core.md)

- **Dev Browser**

  ***

  Browser automation on the Playwright Python API — navigate, fill forms, take screenshots, test web apps, and scrape data with short, incremental scripts and a persistent session profile.

  **Skills:** `dev-browser`

  [:octicons-arrow-right-24: Details](dev-browser.md)

</div>

---

### :material-school: Education & Productivity

<div class="grid cards" markdown>

- **Education**

  ***

  Teaching aids and student support for IT education with Java Tutor agent and Markdown formatting skill.

  **Commands:** `/education:explain-code`
  **Agents:** `java-tutor`, `markdown-syntax-formatter`
  **Skills:** `markdown-syntax-formatter`, `md-to-pdf`

  [:octicons-arrow-right-24: Details](education.md)

- **Obsidian Integration**

  ***

  Task management via TaskNotes API, LLM-Wiki curation, and productivity intelligence — daily briefings, weekly retrospectives, project-pulse dashboards, and opportunity mining.

  **Skills:** `tasknotes`, `today`, `weekly-review`, `project-pulse`, `ideas`, `wiki-ingest`, `wiki-lint`, `wiki-migrate-file`, `wiki-query`, `wiki-think`, `wiki-maintain`

  [:octicons-arrow-right-24: Details](obsidian.md)

</div>

---

## Installation

To install plugins from this marketplace:

1. **Add the marketplace** to `.claude/settings.json`:

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

2. **Browse and install** plugins:

   ```bash
   claude
   /plugin
   # Select "Browse Plugins" → "talent-factory"
   ```

3. **Enable plugins** in settings:
   ```json
   {
     "enabledPlugins": {
       "git-workflow@talent-factory": true,
       "project-management@talent-factory": true
     }
   }
   ```

[:octicons-arrow-right-24: Detailed Installation Guide](../getting-started/installation.md)

---

## Plugin Comparison

### Feature Matrix

| Feature            | Git Workflow | Project Mgmt | Code Quality | Development | Education | Core | Obsidian | Gemini Bridge | Dev Browser |
| ------------------ | :----------: | :----------: | :----------: | :---------: | :-------: | :--: | :------: | :-----------: | :---------: |
| Git Integration    |     Yes      |     Yes      |      No      |     Yes     |    No     |  No  |    No    |      No       |     No      |
| Merge Conflicts    |     Yes      |      No      |      No      |     No      |    No     |  No  |    No    |      No       |     No      |
| Pre-commit Checks  |     Yes      |      No      |     Yes      |     No      |    No     | Yes  |    No    |      No       |     No      |
| Linear Integration |      No      |     Yes      |      No      |     No      |    No     |  No  |    No    |      No       |     No      |
| Code Review        |      No      |      No      |     Yes      |     No      |    No     |  No  |    No    |      No       |     No      |
| Expert Agents      |      No      |     Yes      |     Yes      |     Yes     |    Yes    | Yes  |    No    |     Yes       |     No      |
| Task Management    |      No      |     Yes      |      No      |     No      |    No     |  No  |   Yes    |      No       |     No      |
| Daily Briefing     |      No      |      No      |      No      |     No      |    No     |  No  |   Yes    |      No       |     No      |
| GitHub Pulse       |      No      |      No      |      No      |     No      |    No     |  No  |   Yes    |      No       |     No      |
| Idea Mining        |      No      |      No      |      No      |     No      |    No     |  No  |   Yes    |      No       |     No      |
| CI Automation      |      No      |      No      |      No      |     No      |    No     | Yes  |    No    |      No       |     No      |
| Project Init       |      No      |      No      |      No      |     Yes     |    No     |  No  |    No    |      No       |     No      |
| EPIC Automation    |      No      |     Yes      |      No      |     No      |    No     |  No  |    No    |      No       |     No      |
| Long-Context (1M)  |      No      |      No      |      No      |     No      |    No     |  No  |    No    |     Yes       |     No      |
| Multimodal Vision  |      No      |      No      |      No      |     No      |    No     |  No  |    No    |     Yes       |     No      |
| MCP Tools          |      No      |      No      |      No      |     No      |    No     |  No  |    No    |     Yes       |     No      |
| Browser Automation |      No      |      No      |      No      |     No      |    No     |  No  |    No    |      No       |     Yes     |
| Web Scraping       |      No      |      No      |      No      |     No      |    No     |  No  |    No    |      No       |     Yes     |

---

## Recommended Combinations

### For Software Development Teams

```json
{
  "enabledPlugins": {
    "git-workflow@talent-factory": true,
    "project-management@talent-factory": true,
    "code-quality@talent-factory": true,
    "development@talent-factory": true,
    "core@talent-factory": true,
    "gemini-bridge@talent-factory": true
  }
}
```

**Workflow**: PRD → Planning → Implementation → Review → Commit → PR

---

### For Educators & Students

```json
{
  "enabledPlugins": {
    "education@talent-factory": true,
    "git-workflow@talent-factory": true,
    "core@talent-factory": true
  }
}
```

**Workflow**: Learn → Code → Commit → Review

---

### For Individual Developers

```json
{
  "enabledPlugins": {
    "git-workflow@talent-factory": true,
    "development@talent-factory": true,
    "obsidian@talent-factory": true,
    "core@talent-factory": true
  }
}
```

**Workflow**: Task → Code → Commit → Track

---

## Next Steps

- **[Getting Started](../getting-started/index.md)** - Install and configure plugins
- **[Guides](../guides/index.md)** - Learn common workflows
- **[Development](../development/index.md)** - Create your own plugins
