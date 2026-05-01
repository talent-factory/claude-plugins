# Obsidian Integration Plugin

Integration with Obsidian: task management via the TaskNotes Plugin API, plus a curated LLM-Wiki workflow (ingest, lint, migrate, query) — directly from Claude Code.

## Version 1.2.0

This plugin combines two complementary workflows for Obsidian users:

1. **Task management** — through the TaskNotes Plugin HTTP API
2. **LLM-Wiki maintenance** — an opinionated workflow for curating a personal knowledge base from web clippings, AI chats, transcripts, and own notes

---

## Features

### Task Management

- **List tasks** — "show my tasks"
- **Create tasks** — "create a task for X"
- **Update tasks** — change status, add details
- **Delete tasks** — remove tasks
- **Work recommendations** — "what should I work on?"
- **Vault-wide scanning** — find all tasks in your entire vault with `--scan`

### LLM-Wiki Workflow

- **Ingest sources** — file web clippings, AI chats, transcripts, or raw notes under `_raw/` and distill them into curated `_wiki/` pages with bidirectional cross-references
- **Lint the wiki** — weekly health check for frontmatter integrity, asymmetric links, stale claims, tag discipline, migration backlog, and missing hub pages
- **Migrate legacy notes** — split hybrid legacy files into raw + wiki content with template-compliant frontmatter; cluster mode for thematic batches
- **Query the wiki** — index-first search with citations and optional filing-back of the synthesis as a new wiki page

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

See [Skills & Agents Activation Guide](https://talent-factory.github.io/claude-plugins/reference/skills-agents-activation/) for detailed activation instructions.

### tasknotes

Main skill for task management. Automatically activated for:

- Task-related requests
- Task management questions
- Productivity workflows

**Key Features:**

- `--scan` flag: scans the entire vault filesystem to find ALL tasks with the `#task` tag
- `--all` flag: includes completed and cancelled tasks in listings
- Automatic vault detection via `.obsidian` folder
- Smart sorting by scheduled and due dates

### wiki-ingest

Files a new source (web clipping, AI chat export, raw note, transcript) under `_raw/`, distills it into one or more `_wiki/` pages, updates the index and log, and pulls bidirectional cross-references. Activates on phrases such as "ingest this source" or "digest this clipping into the wiki".

### wiki-lint

Weekly structural and content health check across `_wiki/` and `_raw/`. Detects frontmatter issues, broken or asymmetric cross-references, stale claims, tag discipline violations, missing hub pages, and orphan content. Produces a structured lint report.

### wiki-migrate-file

Migrates legacy files from outside `_wiki/` and `_raw/` into the LLM-Wiki schema. Analyzes a file, proposes a split into raw + wiki content with proper frontmatter, pulls cross-references, updates index and log, and deletes the original. Cluster mode handles thematic groups in a single confirmation.

### wiki-query

Answers a question against the curated `_wiki/` via index-first search and full-text fallback. Returns a synthesized answer with citations and optionally files the synthesis back as a new wiki page.

## LLM-Wiki Configuration

The wiki skills expect the following vault layout (default paths shown):

- `<wiki-root>/_raw/` — raw source files, organized by type subfolder
- `<wiki-root>/_wiki/` — distilled wiki pages
- `<wiki-root>/_wiki/index.md` — section-based index of all wiki pages
- `<wiki-root>/_wiki/log.md` — append-only operation log
- `<wiki-root>/_wiki/templates/` — frontmatter templates per source/wiki type

Default `<wiki-root>` is `Wiki/`. Override via `wiki_root: <path>` in the vault's `CLAUDE.md`. The migration backlog soft cap (default: 50 files) is configurable via `wiki_migration_cap: <n>`.

## Project Structure

```text
obsidian/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── tasknotes/
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       └── tasks.py
│   ├── wiki-ingest/
│   │   └── SKILL.md
│   ├── wiki-lint/
│   │   └── SKILL.md
│   ├── wiki-migrate-file/
│   │   └── SKILL.md
│   └── wiki-query/
│       └── SKILL.md
└── README.md
```

---

## Changelog

### Version 1.2.0 (2026-05-01)

- Added LLM-Wiki workflow with four skills: `wiki-ingest`, `wiki-lint`, `wiki-migrate-file`, `wiki-query`
- Updated plugin description and keywords to cover both task management and wiki workflows

### Version 1.1.2 (2026-02-27)

- Added `keywords` and `license` fields to plugin.json
- Fixed author email to support@talent-factory.ch
- Improved tasknotes skill description

---

## Related Plugins

- **[Project Management](project-management.md)** - PRD and task planning
- **[Git Workflow](git-workflow.md)** - Commit and PR automation

---

## License

MIT License - see [LICENSE](https://github.com/talent-factory/claude-plugins/blob/main/LICENSE) for details.

---

**Made with care by Talent Factory GmbH**
