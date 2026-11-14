# Plugin Catalog

Browse all available plugins in the Talent Factory marketplace. Each plugin provides specialized commands, agents, and skills for different workflows.

---

## All Plugins

| Plugin                                      | Version | Commands | Agents | Skills | Tags                                |
| ------------------------------------------- | ------- | -------- | ------ | ------ | ----------------------------------- |
| [Git Workflow](git-workflow.md)             | 3.0.0   | 1        | 0      | 5      | git, workflow, commits, PRs, merge  |
| [Project Management](project-management.md) | 3.0.0   | 0        | 0      | 6      | planning, PRD, Plane, EPIC, agile  |
| [Code Quality](code-quality.md)             | 4.0.0   | 0        | 0      | 1      | Python, Ruff, linting      |
| [Education](education.md)                   | 5.0.0   | 0        | 0      | 2      | markdown, PDF, Swiss German |
| [Core Utilities](core.md)                   | 6.0.0   | 2        | 0      | 4      | validation, PDF, ponytail, AntML  |
| [Obsidian Integration](obsidian.md)         | 2.0.2   | 0        | 0      | 9     | tasks, Obsidian, wiki, briefing, ideas |
| [Development](development.md)               | 3.0.0   | 0        | 0      | 1      | documentation, sync |

---

## By Category

### :material-git: Development Workflow

<div class="grid cards" markdown>

- **Git Workflow**

  ***

  Professional git automation with emoji conventional commits, pre-commit checks, PR management, and intelligent merge conflict resolution.

  **Commands:** `/git-workflow:pr-edit-history`
  **Skills:** `commit`, `create-pr`, `resolve-conflicts`, `post-merge-cleanup`, `hunk-review`

  [:octicons-arrow-right-24: Details](git-workflow.md)

- **Project Management**

  ***

  File-based project planning with PRD generation, task implementation in git worktrees, EPIC automation, and Plane support.

  **Skills:** `/project-management:create-prd`, `/project-management:create-plan`, `/project-management:init-task`, `/project-management:implement-task`, `/project-management:implement-epic`, `/project-management:document-handoff`

  [:octicons-arrow-right-24: Details](project-management.md)

</div>

---

### :material-code-braces: Code Quality & Development

<div class="grid cards" markdown>

- **Code Quality**

  ***

  Python linting and formatting with Ruff.

  **Skills:** `ruff-check`

  [:octicons-arrow-right-24: Details](code-quality.md)

- **Development**

  ***

  Documentation synchronisation between CLAUDE.md, README.md and docs/.

  **Skills:** `update-documents`

  [:octicons-arrow-right-24: Details](development.md)

- **Core Utilities**

  ***

  Validation of plugin commands and agents, PDF-to-Markdown conversion, the Ponytail minimalism suite, text humanisation, and AntML system-prompt authoring.

  **Commands:** `/core:check-commands`, `/core:check-agents`
    **Skills:** `humanizer`, `pdf-to-markdown`, `ponytail`, `antml-prompt-writer`

  [:octicons-arrow-right-24: Details](core.md)


</div>

---

### :material-school: Education & Productivity

<div class="grid cards" markdown>

- **Education**

  ***

  Markdown clean-up with Swiss German orthography and Markdown-to-PDF conversion for course material.

  **Skills:** `markdown-syntax-formatter`, `md-to-pdf`

  [:octicons-arrow-right-24: Details](education.md)

- **Obsidian Integration**

  ***

  Task management via the TaskNotes API, LLM-Wiki curation, and productivity briefings: daily briefing, weekly review, and idea mining.

  **Skills:** `tasknotes`, `today`, `weekly-review`, `ideas`, `wiki-ingest`, `wiki-query`, `wiki-lint`, `wiki-maintain`, `wiki-migrate-file`

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
| Task Management    |      No      |     Yes      |      No      |     No      |    No     |  No  |   Yes    |
| Daily Briefing     |      No      |      No      |      No      |     No      |    No     |  No  |   Yes    |
| Idea Mining        |      No      |      No      |      No      |     No      |    No     |  No  |   Yes    |
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
