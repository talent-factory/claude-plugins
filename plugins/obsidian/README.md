# Obsidian Integration Plugin

Integration with Obsidian via the TaskNotes Plugin API - task management directly from Claude Code.

## Version 1.1.1

This plugin enables seamless task management between Claude Code and Obsidian using the TaskNotes Plugin API.

---

## Features

- **List tasks** - "show my tasks"
- **Create tasks** - "create a task for X"
- **Update tasks** - Change status, add details
- **Delete tasks** - Remove tasks
- **Work recommendations** - "what should I work on?"
- **Vault-wide scanning** - Find all tasks in your entire vault with `--scan`

## Prerequisites

### 1. TaskNotes Plugin in Obsidian

1. Open Obsidian Community Plugins
2. Search for "TaskNotes" and install
3. Enable the plugin

### 2. Enable HTTP API

1. Obsidian Settings → TaskNotes
2. Enable "HTTP API" toggle
3. Set port (default: 8080)
4. Optional: Set API token for security

### 3. Environment Variables (optional)

If using authentication, create a `.env` file in your Obsidian vault:

```env
TASKNOTES_API_PORT=8080
TASKNOTES_API_KEY=your_secret_token
```

Alternatively, set `OBSIDIAN_VAULT_PATH` as an environment variable to specify the vault path.

## Installation

### Via Marketplace

```json
{
  "enabledPlugins": {
    "obsidian@talent-factory": true
  }
}
```

### Local Testing

```bash
claude --plugin-dir ./plugins/obsidian
```

## Usage

### Natural Language

```
show my tasks
create a task to finish the landing page
what should I work on?
mark "Tasks/landing-page.md" as done
```

### CLI Commands

The plugin also provides direct CLI commands:

```bash
# List all tasks in the vault (recommended)
uv run tasks.py list --scan --table

# List all tasks including completed
uv run tasks.py list --all --table

# Create a task
uv run tasks.py create "Prepare meeting" --project "Work" --priority high

# Update status
uv run tasks.py update "Tasks/meeting.md" --status done

# Filter by status
uv run tasks.py list --status in-progress --scan --table
```

## Skills

See [Skills & Agents Activation Guide](../reference/skills-agents-activation.md) for detailed activation instructions.

### tasknotes

Main skill for task management. Automatically activated for:

- Task-related requests
- Task management questions
- Productivity workflows

**Key Features:**

- `--scan` flag: Scans the entire vault filesystem to find ALL tasks with the #task tag
- `--all` flag: Includes completed and cancelled tasks in listings
- Automatic vault detection via `.obsidian` folder
- Smart sorting by scheduled/due dates

## Project Structure

```text
obsidian/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── tasknotes/
│       ├── SKILL.md
│       └── scripts/
│           └── tasks.py
└── README.md
```

---

## Related Plugins

- **[Project Management](project-management.md)** - PRD and task planning
- **[Git Workflow](git-workflow.md)** - Commit and PR automation

---

## License

MIT License - see [LICENSE](https://github.com/talent-factory/claude-plugins/blob/main/LICENSE) for details.

---

**Made with care by Talent Factory GmbH**
