---
name: tasknotes
description: Use this skill when the user asks to "show my tasks", "create a task", "what should I work on", "mark as done", or wants to filter tasks by status/project.
---

# TaskNotes Skill

Task management in Obsidian via the TaskNotes Plugin HTTP API.

<example>
User: "show my tasks"
Action: Execute `list --scan --table` to display all tasks in the vault
</example>

<example>
User: "create a task to finish the landing page"
Action: Execute `create "Finish landing page"`
</example>

<example>
User: "what should I work on?"
Action: Execute `list --status in-progress --scan --table` to show active tasks
</example>

<example>
User: "mark task X as done"
Action: Execute `update "Tasks/task-x.md" --status done`
</example>

## Prerequisites

1. **TaskNotes Plugin** installed in Obsidian
2. **HTTP API enabled** in TaskNotes settings:
   - Open Obsidian Settings → TaskNotes
   - Enable "HTTP API" toggle
   - Set API port (default: 8080)
   - API Token: leave empty for no authentication, or set a token for security
3. **Environment variables** in `.env` file at vault root (if authentication is used):
   ```
   TASKNOTES_API_PORT=8080
   TASKNOTES_API_KEY=your_token_here
   ```
   If TaskNotes has no auth token configured, no `.env` file is required.

## CLI Commands

The script is located at `${CLAUDE_PLUGIN_ROOT}/skills/tasknotes/scripts/tasks.py`.

```bash
# List all tasks (API-monitored folders only)
uv run ${CLAUDE_PLUGIN_ROOT}/skills/tasknotes/scripts/tasks.py list

# Find all tasks in the ENTIRE vault (scans filesystem)
uv run ${CLAUDE_PLUGIN_ROOT}/skills/tasknotes/scripts/tasks.py list --scan --table

# All active tasks (excluding completed) in the entire vault
uv run ${CLAUDE_PLUGIN_ROOT}/skills/tasknotes/scripts/tasks.py list --scan --table

# ALL tasks including completed in the entire vault
uv run ${CLAUDE_PLUGIN_ROOT}/skills/tasknotes/scripts/tasks.py list --all --table

# Filter by status (use your configured status values)
uv run ${CLAUDE_PLUGIN_ROOT}/skills/tasknotes/scripts/tasks.py list --status "in-progress" --scan

# Filter by project
uv run ${CLAUDE_PLUGIN_ROOT}/skills/tasknotes/scripts/tasks.py list --project "My Project" --scan

# Create a task
uv run ${CLAUDE_PLUGIN_ROOT}/skills/tasknotes/scripts/tasks.py create "Task title" --project "My Project" --priority high

# Create a task with scheduled time
uv run ${CLAUDE_PLUGIN_ROOT}/skills/tasknotes/scripts/tasks.py create "Meeting preparation" --scheduled "2025-01-15T14:00:00"

# Update task status
uv run ${CLAUDE_PLUGIN_ROOT}/skills/tasknotes/scripts/tasks.py update "Tasks/task.md" --status done

# Add/update description
uv run ${CLAUDE_PLUGIN_ROOT}/skills/tasknotes/scripts/tasks.py update "Tasks/task.md" --details "Additional context here."

# Delete a task
uv run ${CLAUDE_PLUGIN_ROOT}/skills/tasknotes/scripts/tasks.py delete "Tasks/task.md"

# Retrieve available options (statuses, priorities, projects)
uv run ${CLAUDE_PLUGIN_ROOT}/skills/tasknotes/scripts/tasks.py options --table

# Human-readable output (add --table)
uv run ${CLAUDE_PLUGIN_ROOT}/skills/tasknotes/scripts/tasks.py list --table
```

## Task Properties

**Status and priority values:** Configured in TaskNotes plugin settings. Execute the `options` command to view available values:

```bash
uv run ${CLAUDE_PLUGIN_ROOT}/skills/tasknotes/scripts/tasks.py options --table
```

**Additional fields:**
- `projects` - Array of project links, e.g., `["[[ProjectName]]"]`
- `contexts` - Array such as `["office", "energy-high"]`
- `due` - Due date (YYYY-MM-DD)
- `scheduled` - Scheduled date/time (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)
- `timeEstimate` - Minutes (number)
- `tags` - Array of tags
- `details` - Task description (writes to Markdown body, not frontmatter)

## API Reference

Base URL: `http://localhost:8080/api`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /tasks | List tasks (supports filters) |
| POST | /tasks | Create task |
| GET | /tasks/{id} | Retrieve single task |
| PUT | /tasks/{id} | Update task |
| DELETE | /tasks/{id} | Delete task |
| GET | /filter-options | Available statuses, priorities, projects |

### Query Parameters for GET /tasks

- `status` - Filter by status
- `project` - Filter by project name
- `priority` - Filter by priority
- `tag` - Filter by tag
- `overdue` - true/false
- `sort` - Sort field
- `limit` - Maximum results
- `offset` - Pagination offset

## Usage Patterns

| User Request | Action |
|--------------|--------|
| "create a task for X" | Create task |
| "show my tasks" | list --scan --table (finds all tasks in vault) |
| "show in-progress tasks" | list --status in-progress --scan --table |
| "mark X as done" | Set task status to done |
| "what should I work on" | list --scan --table |

**IMPORTANT:** Always use `--scan` when listing to find ALL tasks in the entire vault, not just those in the configured TaskNotes folder.

## Example Workflow

```bash
# Morning: Check what to work on (all tasks in vault)
uv run ${CLAUDE_PLUGIN_ROOT}/skills/tasknotes/scripts/tasks.py list --scan --table
uv run ${CLAUDE_PLUGIN_ROOT}/skills/tasknotes/scripts/tasks.py list --status in-progress --scan --table

# Show top 5 tasks
uv run ${CLAUDE_PLUGIN_ROOT}/skills/tasknotes/scripts/tasks.py list --scan --limit 5 --table

# Create a task with project association
uv run ${CLAUDE_PLUGIN_ROOT}/skills/tasknotes/scripts/tasks.py create "Complete landing page" \
  --project "Website Redesign" \
  --priority high

# Complete a task
uv run ${CLAUDE_PLUGIN_ROOT}/skills/tasknotes/scripts/tasks.py update "Tasks/complete-landing-page.md" --status done
```

## Important Notes

- **JSON output** (default): Suitable for programmatic processing
- **Table output** (`--table`): For human-readable display
- **Vault path**: The script expects the `.env` file at the vault root or automatically locates the Obsidian vault
- **Error handling**: On connection errors, verify that Obsidian is running and the TaskNotes API is enabled
- **Scan mode** (`--scan`): Directly scans the filesystem and finds ALL tasks with the #task tag in the entire vault, regardless of the configured TaskNotes folder. **This is the recommended mode for listing tasks.**
- **API mode** (without `--scan`): Uses the TaskNotes HTTP API but only finds tasks in TaskNotes-monitored folders
