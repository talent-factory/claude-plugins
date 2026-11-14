---
name: tasknotes
description: Manages tasks in Obsidian via the TaskNotes Plugin HTTP API. Provides task creation, status updates, filtering by project or status, and vault-wide scanning. Triggers when the user asks to "show my tasks", "create a task", "what should I work on", "mark as done", or wants to filter tasks by status/project.
---

# TaskNotes

Task management in Obsidian through the TaskNotes plugin and its HTTP API, wrapped by `${CLAUDE_PLUGIN_ROOT}/skills/tasknotes/scripts/tasks.py`. Run it as `uv run <script> <command>`; the output is JSON by default, `--table` makes it readable.

## Prerequisites

1. The TaskNotes plugin is installed in Obsidian and its **HTTP API** is enabled (Settings, TaskNotes; default port 8080).
2. If an API token is set, put `TASKNOTES_API_PORT` and `TASKNOTES_API_KEY` in a `.env` file at the vault root. Without a token no `.env` is needed.

## Commands

| Request | Command |
|---|---|
| Show my tasks, what should I work on | `list --scan --table` |
| Only in progress | `list --status in-progress --scan --table` |
| One project | `list --project "My Project" --scan --table` |
| Including completed tasks | `list --all --table` |
| Top five | `list --scan --limit 5 --table` |
| Create | `create "Title" --project "My Project" --priority high [--scheduled "2026-01-15T14:00:00"]` |
| Mark as done | `update "Tasks/task.md" --status done` |
| Add a description | `update "Tasks/task.md" --details "Context"` |
| Delete | `delete "Tasks/task.md"` |
| Valid statuses, priorities, projects | `options --table` |

**Always use `--scan` when listing.** It reads the vault's files and finds every task tagged `#task`; without it only the folders TaskNotes monitors are searched (API mode).

Status and priority values come from the TaskNotes settings; read them with `options` instead of guessing. Further fields: `projects` (`["[[Name]]"]`), `contexts`, `due` (YYYY-MM-DD), `scheduled`, `timeEstimate` (minutes), `tags`, and `details` (written to the note body, not the frontmatter).

## Errors

On a connection error check that Obsidian is running and the HTTP API is enabled. The script finds the vault from the `.env` location or by detecting the `.obsidian` folder.

## API

Base URL `http://localhost:8080/api`: `GET/POST /tasks`, `GET/PUT/DELETE /tasks/{id}`, `GET /filter-options`. `GET /tasks` accepts `status`, `project`, `priority`, `tag`, `overdue`, `sort`, `limit`, `offset`.
