# Plugin Catalog

Browse all available plugins in the Talent Factory marketplace. Each plugin provides specialized commands, agents, and skills for different workflows.

---

## All Plugins

| Plugin                                      | Version | Commands | Agents | Skills | Tags                                |
| ------------------------------------------- | ------- | -------- | ------ | ------ | ----------------------------------- |
| [Git Workflow](git-workflow.md)             | 2.2.0   | 4        | 0      | 3      | git, workflow, commits, PRs, merge  |
| [Project Management](project-management.md) | 2.4.0   | 5        | 1      | 0      | planning, PRD, Linear, EPIC, agile  |
| [Code Quality](code-quality.md)             | 3.0.0   | 1        | 3      | 0      | review, quality, Python, React      |
| [Education](education.md)                   | 1.3.1   | 1        | 2      | 1      | teaching, learning, markdown        |
| [Core Utilities](core.md)                   | 3.1.0   | 7        | 2      | 2      | validation, CI, PDF, development    |
| [Obsidian Integration](obsidian.md)         | 1.1.1   | 0        | 0      | 1      | tasks, Obsidian, productivity       |
| [Development](development.md)               | 1.3.0   | 1        | 1      | 2      | java, gradle, python, documentation |

---

## By Category

### :material-git: Development Workflow

<div class="grid cards" markdown>

- **Git Workflow**

  ***

  Professional git automation with emoji conventional commits, pre-commit checks, PR management, and intelligent merge conflict resolution.

  **Commands:** `/commit`, `/create-pr`, `/pr-edit-history`, `/resolve-conflicts`
  **Skills:** `professional-commit-workflow`, `professional-pr-workflow`, `post-merge-cleanup`

  [:octicons-arrow-right-24: Details](git-workflow.md)

- **Project Management**

  ***

  Comprehensive project planning with PRD generation, EPIC automation, Linear integration, and git worktree workflows.

  **Commands:** `/create-prd`, `/create-plan`, `/implement-task`, `/implement-epic`, `/document-handoff`
  **Agents:** `epic-orchestrator`

  [:octicons-arrow-right-24: Details](project-management.md)

</div>

---

### :material-code-braces: Code Quality & Development

<div class="grid cards" markdown>

- **Code Quality**

  ***

  Expert code review and refactoring with specialized agents for Python and React/Frontend development.

  **Commands:** `/ruff-check`
  **Agents:** `python-expert`, `frontend-developer`, `code-reviewer`

  [:octicons-arrow-right-24: Details](code-quality.md)

- **Development**

  ***

  Expert development agents, project initialization with Git branching, Java/Gradle, Python/uv, and documentation synchronization tools.

  **Commands:** `/init-project`
  **Agents:** `java-developer`
  **Skills:** `professional-init-project`, `update-documents`

  [:octicons-arrow-right-24: Details](development.md)

- **Core Utilities**

  ***

  Development utilities for plugin validation, CI automation, plugin development, and PDF-to-Markdown conversion.

  **Commands:** `/check`, `/check-commands`, `/check-agents`, `/build-skill`, `/package-skill`, `/create-command`, `/run-ci`
  **Agents:** `agent-expert`, `command-expert`
  **Skills:** `humanizer`, `pdf-to-markdown`

  [:octicons-arrow-right-24: Details](core.md)

</div>

---

### :material-school: Education & Productivity

<div class="grid cards" markdown>

- **Education**

  ***

  Teaching aids and student support for IT education with Java Tutor agent and Markdown formatting skill.

  **Commands:** `/explain-code`
  **Agents:** `java-tutor`, `markdown-syntax-formatter`
  **Skills:** `markdown-syntax-formatter`

  [:octicons-arrow-right-24: Details](education.md)

- **Obsidian Integration**

  ***

  Task management via Obsidian TaskNotes Plugin API with natural language support (DE/EN).

  **Skills:** `tasknotes`

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

| Feature            | Git Workflow | Project Mgmt | Code Quality | Development | Education | Core | Obsidian |
| ------------------ | :----------: | :----------: | :----------: | :---------: | :-------: | :--: | :------: |
| Git Integration    |     Yes      |     Yes      |      No      |     Yes     |    No     |  No  |    No    |
| Merge Conflicts    |     Yes      |      No      |      No      |     No      |    No     |  No  |    No    |
| Pre-commit Checks  |     Yes      |      No      |     Yes      |     No      |    No     | Yes  |    No    |
| Linear Integration |      No      |     Yes      |      No      |     No      |    No     |  No  |    No    |
| Code Review        |      No      |      No      |     Yes      |     No      |    No     |  No  |    No    |
| Expert Agents      |      No      |     Yes      |     Yes      |     Yes     |    Yes    | Yes  |    No    |
| Task Management    |      No      |     Yes      |      No      |     No      |    No     |  No  |   Yes    |
| CI Automation      |      No      |      No      |      No      |     No      |    No     | Yes  |    No    |
| Project Init       |      No      |      No      |      No      |     Yes     |    No     |  No  |    No    |
| EPIC Automation    |      No      |     Yes      |      No      |     No      |    No     |  No  |    No    |

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
    "core@talent-factory": true
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
