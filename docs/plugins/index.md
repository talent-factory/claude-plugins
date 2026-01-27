# Plugin Catalog

Browse all available plugins in the Talent Factory marketplace. Each plugin provides specialized commands, agents, and skills for different workflows.

---

## All Plugins

| Plugin | Version | Commands | Agents | Skills | Tags |
|--------|---------|----------|--------|--------|------|
| [Git Workflow](git-workflow.md) | 2.0.0 | 3 | 0 | 2 | git, workflow, commits, PRs |
| [Project Management](project-management.md) | 2.2.0 | 4 | 0 | 2 | planning, PRD, Linear, agile |
| [Code Quality](code-quality.md) | 2.0.0 | 3 | 3 | 0 | review, quality, Python, Java |
| [Education](education.md) | 1.1.0 | 2 | 1 | 0 | teaching, learning, students |
| [Core Utilities](core.md) | 2.1.0 | 8 | 3 | 1 | validation, CI, development |
| [Obsidian Integration](obsidian.md) | 1.0.1 | 4 | 0 | 0 | tasks, Obsidian, productivity |

---

## By Category

### :material-git: Development Workflow

<div class="grid cards" markdown>

-   **Git Workflow**

    ---

    Professional git automation with emoji conventional commits, pre-commit checks, and PR management.

    **Commands:** `/commit`, `/create-pr`, `/pr-edit-history`

    [:octicons-arrow-right-24: Details](git-workflow.md)

-   **Project Management**

    ---

    Comprehensive project planning with PRD generation, Linear integration, and git worktree workflows.

    **Commands:** `/create-prd`, `/create-plan`, `/implement-task`, `/sync-linear`

    [:octicons-arrow-right-24: Details](project-management.md)

</div>

---

### :material-code-braces: Code Quality

<div class="grid cards" markdown>

-   **Code Quality**

    ---

    Expert code review and refactoring with specialized agents for Python, Java, and React.

    **Commands:** `/review`, `/refactor`, `/lint-python`  
    **Agents:** `python-expert`, `java-expert`, `frontend-expert`

    [:octicons-arrow-right-24: Details](code-quality.md)

-   **Core Utilities**

    ---

    Development utilities for plugin validation, CI automation, and project initialization.

    **Commands:** `/check`, `/check-commands`, `/check-agents`, `/build-skill`, `/create-command`, `/init-project`, `/run-ci`, `/humanize`

    [:octicons-arrow-right-24: Details](core.md)

</div>

---

### :material-school: Education & Productivity

<div class="grid cards" markdown>

-   **Education**

    ---

    Teaching aids and student support for IT education with Java Tutor agent.

    **Commands:** `/explain-code`, `/format-markdown`  
    **Agents:** `java-tutor`

    [:octicons-arrow-right-24: Details](education.md)

-   **Obsidian Integration**

    ---

    Task management via Obsidian TaskNotes Plugin API with natural language support (DE/EN).

    **Commands:** `/task`, `/tasks`, `/task-complete`, `/task-delete`

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

| Feature | Git Workflow | Project Mgmt | Code Quality | Education | Core | Obsidian |
|---------|:------------:|:------------:|:------------:|:---------:|:----:|:--------:|
| Git Integration | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Pre-commit Checks | ✅ | ❌ | ✅ | ❌ | ✅ | ❌ |
| Linear Integration | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Code Review | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| Expert Agents | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ |
| Task Management | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |
| CI Automation | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| Documentation | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ |

---

## Recommended Combinations

### For Software Development Teams

```json
{
  "enabledPlugins": {
    "git-workflow@talent-factory": true,
    "project-management@talent-factory": true,
    "code-quality@talent-factory": true,
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

