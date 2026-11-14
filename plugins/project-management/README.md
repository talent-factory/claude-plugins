# Project Management Plugin

## Version 3.0.0

Planning and implementation workflow for features: from a PRD to a file-based plan, to tasks implemented in isolated git worktrees with a pull request each.

## Skills

All skills are invoked as `/project-management:<name>` and also activate from natural language.

| Skill | What it does |
|---|---|
| `create-prd` | Writes a Product Requirements Document: problem, SMART objectives, stories with acceptance criteria, prioritised requirements, scope, risks. |
| `create-plan` | Turns the PRD into `.plans/<feature>/` with `EPIC.md`, `STATUS.md` (dependency graph) and atomic task files (Story Points 1 to 8). |
| `init-task` | Adds one task: duplicate detection, ATOMIC validation, mandatory Definition of Done. |
| `implement-task` | One task end to end: context analysis, worktree and branch, draft PR, status update on the default branch, implementation with tests, quality gate, PR. Source: `.plans/` or Plane (`--plane`). |
| `implement-epic` | A whole plan in dependency waves with parallel subagents in separate worktrees. Many tokens: it shows the waves and asks first. |
| `document-handoff` | Writes a handoff document before `/compact` or the end of a session. |

Formats of the plan files: [references/formats.md](references/formats.md). Plane setup and state handling: [references/plane.md](references/plane.md).

## Typical flow

```text
/project-management:create-prd "Dark mode toggle"
/project-management:create-plan
/project-management:implement-task task-001
/git-workflow:post-merge-cleanup task-001
```

## Conventions

- **Plans** live in `.plans/<feature>/` (EPIC, STATUS, `tasks/task-NNN-<slug>.md`).
- **One worktree per task** in `.worktrees/task-<id>/`, branch `<type>/<task-id>-<slug>`.
- **Status changes happen on the default branch**, so parallel workers see which tasks are taken.
- **Closing keyword** in the PR text: `Closes <ID>` when the PR finishes a task, `Refs <ID>` when it stays open on purpose.
- **Plane:** the repository's `CLAUDE.md` names the workspace and the project identifier; see [references/plane.md](references/plane.md).

## Works with

- `git-workflow` for commits (`/git-workflow:commit`), PRs and cleanup.
- The `superpowers` plugin (optional): `implement-task` uses its `brainstorming` skill for design questions.

## Installation

```json
{
  "extraKnownMarketplaces": {
    "talent-factory": {
      "source": { "source": "github", "repo": "talent-factory/claude-plugins" }
    }
  },
  "enabledPlugins": { "project-management@talent-factory": true }
}
```

## Changelog

### Version 3.0.0 (2026-11-14)

**Breaking:**

- All commands are skills now with the same invocations (`/project-management:create-prd`, `create-plan`, `init-task`, `implement-task`, `implement-epic`, `document-handoff`).
- Removed the Linear provider (`--linear`, `--linear-issue`): Linear is archived. Plane and `.plans/` remain.
- Removed the `epic-orchestrator` agent; `implement-epic` orchestrates directly with subagents.
- Removed the generic reference guides for PRDs, plans, estimation, agent mapping, quality gate and troubleshooting (about 10.7k lines). The plan file formats and the Plane guide remain.
- The plugin shrank from about 14k to about 0.5k lines.

### Version 2.8.2 (2026-11-14)

- Examples and defaults are generic: ticket identifiers `PROJ-123` instead of company ticket IDs, no company Plane URL, and the document-handoff example no longer draws on a customer product

### Version 2.8.1 (2026-11-14)

- Plane guide and `implement-task` use the single `plane` MCP server with a `workspace` parameter instead of the retired `plane-tf` server; example identifiers genericised

### Version 2.7.0 (2026-05-08)

**Minor Update:**

- ✨ Added `document-handoff` skill for natural-language pre-compact handoff documentation activation

### Version 2.6.2 (2026-02-27)

**Single-Task Creation:**

- 📋 Added `/project-management:init-task` command for single-task creation
- 🔍 Duplicate detection across filesystem and Linear with Jaccard similarity
- ✅ ATOMIC validation with hard requirements and soft warnings
- 📄 Extended task template with Type, Plan, and Definition of Done fields
- 📚 Added 3 reference documents: task-template, duplicate-detection, validation-rules

### Version 2.5.0 (2026-02-26)

**Plugin Orchestration:**

- 🧠 Added plugin orchestration to `/project-management:implement-task` (Superpowers brainstorm, agent routing, quality gate)
- ⚡ Added skip options: `--skip-brainstorm`, `--skip-quality-gate`
- 📚 Added reference documentation: agent-routing, context-analysis, quality-gate

### Version 2.4.0 (2026-02-01)

**Documentation & Architecture:**

- 🌐 Complete documentation translation to professional English (academic level)
- 🔧 Removed external plugin dependency (ralph-wiggum)
- 🔄 Uses native Claude Code autonomous loops via Stop hooks
- 📚 Renamed `ralph-integration.md` to `autonomous-loop-integration.md`

### Version 2.3.0 (2026-02-01)

**Autonomous EPIC Implementation:**

- 🤖 Added `/project-management:implement-epic` command with autonomous loop integration
- 🔀 Parallel task execution with isolated worktrees
- 👥 Added `epic-orchestrator` agent for coordination
- 🔄 Autonomous implementation and review loops
- 📊 Real-time progress tracking and status updates
- 📚 Added 4 new reference documents for EPIC implementation

### Version 2.0.0 (2026-01-10)

**Major Update:**

- ✨ Added `/project-management:create-plan` command with Linear integration
- ✨ Added `/project-management:implement-task` command with worktree workflow
- 📚 Added comprehensive reference documentation (13 files)
- 🔗 Integrated Linear API for issue management
- 🌲 Added git worktree support for isolated development
- 📋 Enhanced PRD templates and best practices

**Migration from 1.0.0:**

- `/project-management:create-prd` remains compatible
- New commands optional but recommended
- Linear integration opt-in

### Version 1.0.0

- Initial release with `/project-management:create-prd`

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
