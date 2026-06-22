# Obsidian Integration Plugin

Obsidian integration for Claude Code: task management via the TaskNotes Plugin API,
LLM-Wiki curation, and productivity intelligence — daily briefings, weekly retrospectives,
project-pulse dashboards, and opportunity mining — all from within Claude Code.

## Version 1.4.0

This plugin combines four complementary workflows for Obsidian users:

1. **Task management** — through the TaskNotes Plugin HTTP API
2. **LLM-Wiki maintenance** — curate a personal knowledge base from web clippings, AI chats, transcripts, and notes
3. **Daily & weekly intelligence** — aggregate tasks, calendar, email, Linear, and GitHub into structured briefings
4. **Opportunity mining** — surface product and project ideas from your knowledge base and repositories

---

## Configuration

All skills in this plugin share a common configuration mechanism. Add the relevant
keys to `~/.claude/CLAUDE.md` once, and every skill reads them automatically.
Environment variables take precedence over CLAUDE.md values.

```yaml
# ~/.claude/CLAUDE.md

# Obsidian plugin configuration
obsidian_vault: ~/Obsidian/MyVault        # Required for vault-writing skills
obsidian_daily_dir: Daily                 # Daily notes folder (relative to vault)
obsidian_template_daily: Templates/Daily Note.md  # Daily note template
obsidian_template_weekly: Templates/Weekly Review.md
obsidian_wiki_root: Wiki                  # Wiki root folder (relative to vault)
obsidian_companies_dir: Companies         # Stakeholder / customer notes folder
obsidian_ideas_dir: Ideas                 # Ideas output folder (relative to vault)
obsidian_context_dir:                     # Optional: strategic context notes folder
github_org: my-org                        # GitHub organisation (required for GitHub steps)
user_email: me@example.com               # Email for Gmail "needs reply" detection
```

**Environment variable overrides:**

| Variable | Corresponding key |
|---|---|
| `OBSIDIAN_VAULT` | `obsidian_vault` |
| `OBSIDIAN_DAILY_DIR` | `obsidian_daily_dir` |
| `OBSIDIAN_TEMPLATE_DAILY` | `obsidian_template_daily` |
| `OBSIDIAN_TEMPLATE_WEEKLY` | `obsidian_template_weekly` |
| `GITHUB_ORG` | `github_org` |
| `USER_EMAIL` | `user_email` |

**Vault auto-detection:** If `obsidian_vault` is not set, the plugin searches
`$HOME` up to five directory levels deep for a `.obsidian` folder. Set the key
explicitly to avoid ambiguity when multiple vaults are present.

---

## Features

### Task Management

- **List tasks** — "show my tasks"
- **Create tasks** — "create a task for X"
- **Update tasks** — change status, add details
- **Delete tasks** — remove tasks
- **Work recommendations** — "what should I work on?"
- **Vault-wide scanning** — find all tasks in the entire vault with `--scan`

### LLM-Wiki Workflow

- **Ingest sources** — file web clippings, AI chats, transcripts, or raw notes under `_raw/` and distil them into curated `_wiki/` pages with bidirectional cross-references; write-time validation gate blocks malformed frontmatter before it reaches the vault; contradiction detect-and-confirm workflow flags conflicting claims for user resolution
- **Lint the wiki** — weekly health check for frontmatter integrity, asymmetric links, stale claims, tag discipline, and missing hub pages; deterministic checks delegated to the shared validation module
- **Migrate legacy notes** — split hybrid legacy files into raw + wiki content with template-compliant frontmatter; write-time validation gate ensures all migrated pages meet the schema
- **Query the wiki** — index-first search with citations and optional filing-back of the synthesis
- **Think about the wiki** — structured deep reasoning with challenge, connect, or socratic modes; optionally writes a thinking-page to the vault
- **Maintain the wiki** — non-interactive lint + auto-fix pass with a written report; designed for unattended scheduling via cron or launchd

### Daily Briefing

- Aggregates tasks from TaskNotes, Google Calendar, Gmail, Linear, and GitHub
- Ranks items by urgency using a configurable priority scoring system
- Writes a structured briefing to today's daily note
- Creates the daily note from template if it does not exist

### Weekly Review

- Collects completed tasks, GitHub activity, calendar meetings, wiki learnings, and Linear progress
- Writes a structured retrospective with a preserved Reflection section
- Identifies open loops and proposes a prioritised focus list for the following week

### Project Pulse

- Categorises all GitHub repositories as Active / Dormant / Stalled
- Lists open pull requests and assigned issues
- Terminal output only — fast, no vault writes
- Supports `--stalled-only` flag for focused cleanup sessions

### Ideas — Opportunity Mining

- Analyses the knowledge wiki, GitHub portfolio, stakeholder notes, and live market trends
- Applies a cross-reference matrix to identify ideas where multiple signals align
- Rates ideas by effort (S/M/L) and value (High/Medium/Low)
- Writes a structured ideas document to the vault

---

## Prerequisites

### 1. TaskNotes Plugin in Obsidian (for task skills)

1. Open Obsidian Community Plugins
2. Search for "TaskNotes" and install
3. Enable the plugin
4. Enable HTTP API in plugin settings (default port: 8080)

### 2. GitHub CLI (for GitHub-dependent skills)

```bash
brew install gh && gh auth login
```

### 3. MCP integrations (optional, for full briefing capability)

The `today`, `weekly-review`, and `ideas` skills can use the following MCP
connections when available: Google Calendar, Gmail, Linear. Each integration
degrades gracefully when not configured — only that data source is skipped.

### 4. PyYAML (for wiki validation)

The shared validation module (`skills/_shared/scripts/validate.py`) requires
**PyYAML** to perform deterministic frontmatter checks at write time:

```bash
pip install pyyaml
```

Without PyYAML the wiki-ingest and wiki-migrate-file skills fall back to the
prose validation rules in `skills/_shared/validation-rules.md` and continue to
operate, but structural checks are less strict.

---

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

---

## Usage

### Natural Language

```
show my tasks
create a task to finish the landing page
what should I work on?
what's on my plate today?
prepare weekly review
show my GitHub project status
what could I build next?
```

### Direct Skill Invocation

```
/obsidian:tasknotes
/obsidian:today
/obsidian:weekly-review
/obsidian:project-pulse
/obsidian:project-pulse --stalled-only
/obsidian:ideas
/obsidian:wiki-ingest
/obsidian:wiki-query
/obsidian:wiki-lint
/obsidian:wiki-migrate-file
/obsidian:wiki-think
/obsidian:wiki-maintain
```

---

## Skills

### tasknotes

Main skill for task management via the TaskNotes HTTP API. Activates on phrases
such as "show my tasks", "create a task", "what should I work on", or "mark as done".

Key features:
- `--scan` flag: scans the entire vault filesystem to find all tasks
- `--all` flag: includes completed and cancelled tasks in listings
- Automatic vault detection via the `.obsidian` folder
- Smart sorting by scheduled and due dates

### today

Produces a prioritised daily briefing from all configured sources and writes it
to today's Obsidian daily note. Activates on "what's on my plate today", "daily
briefing", or "morning briefing".

Sources: TaskNotes · Google Calendar · Gmail · Linear · GitHub

### weekly-review

Writes a structured weekly retrospective to the vault. Collects completed tasks,
shipped code, meetings, wiki learnings, and Linear progress. Preserves the
Reflection section on subsequent runs. Activates on "weekly review",
"what did I accomplish this week", or "summarise my week".

Sources: TaskNotes · GitHub · Google Calendar · Linear · Wiki log

### project-pulse

Quick status snapshot of all GitHub repositories in the configured organisation.
Categorises repos as Active / Dormant / Stalled. Terminal output only. Activates
on "show me my repos", "project overview", "GitHub pulse", or "which projects are active".

Requires: `github_org` configuration key.

### ideas

Mines the knowledge wiki, GitHub portfolio, stakeholder notes, and market trends
to surface new product and project ideas. Writes a structured document to the vault.
Activates on "what could I build next", "give me project ideas", or "opportunity mining".

### wiki-ingest

Files a new source (web clipping, AI chat export, raw note, transcript) under
`_raw/`, distils it into one or more `_wiki/` pages, updates the index and log,
and pulls bidirectional cross-references. Activates on "ingest this source" or
"digest this clipping into the wiki".

### wiki-lint

Weekly structural and content health check across `_wiki/` and `_raw/`. Detects
frontmatter issues, broken or asymmetric cross-references, stale claims, tag
discipline violations, missing hub pages, and orphan content.

### wiki-migrate-file

Migrates legacy files from outside `_wiki/` and `_raw/` into the LLM-Wiki schema.
Cluster mode handles thematic groups in a single confirmation.

### wiki-query

Answers a question against the curated `_wiki/` via index-first search and
full-text fallback. Returns a synthesised answer with citations and optionally
files the synthesis back as a new wiki page.

### wiki-think

Engages in deep, structured reasoning against the curated `_wiki/`. Supports
three thinking modes:

- **challenge** — stress-tests a claim by surfacing contradicting evidence and
  underexplored assumptions from the knowledge base
- **connect** — maps lateral connections between ideas across disparate wiki pages
- **socratic** — guides iterative inquiry by generating and answering follow-up
  questions until a synthesis emerges

Pass `type: thinking` to write the result as a new thinking-page in the vault.
Activates on "think about", "challenge this idea", "connect ideas", or "explore".

### wiki-maintain

Non-interactive maintenance pass that runs lint checks, applies deterministic
auto-fixes, and writes a structured report — designed for scheduled execution via
cron or launchd. Unlike `wiki-lint`, it does not pause for user confirmation;
all fixable issues are resolved automatically and the remainder are logged.

Scheduling recipes (cron/launchd) are provided in
`skills/wiki-maintain/references/cron-recipes.md`.

---

## LLM-Wiki Vault Layout

The wiki skills expect the following structure (default paths shown):

- `<wiki-root>/_raw/` — raw source files, organised by type subfolder
- `<wiki-root>/_wiki/` — distilled wiki pages
- `<wiki-root>/_wiki/index.md` — section-based index
- `<wiki-root>/_wiki/log.md` — append-only operation log
- `<wiki-root>/_wiki/templates/` — frontmatter templates

Default `<wiki-root>` is `Wiki/` relative to the vault root. Override via
`obsidian_wiki_root:` in `~/.claude/CLAUDE.md`. The migration backlog soft cap
(default: 50 files) is configurable via `wiki_migration_cap: <n>`.

---

## Project Structure

```text
obsidian/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── _shared/
│   │   ├── scripts/
│   │   │   └── validate.py          # shared deterministic validation (requires PyYAML)
│   │   └── validation-rules.md      # prose fallback rules
│   ├── tasknotes/
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       └── tasks.py
│   ├── today/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   └── priority-guide.md
│   │   └── scripts/
│   │       └── update_daily_note.py
│   ├── weekly-review/
│   │   ├── SKILL.md
│   │   └── references/
│   │       └── weekly-cadence.md
│   ├── ideas/
│   │   ├── SKILL.md
│   │   └── references/
│   │       └── idea-signals.md
│   ├── project-pulse/
│   │   └── SKILL.md
│   ├── wiki-ingest/
│   │   └── SKILL.md
│   ├── wiki-lint/
│   │   └── SKILL.md
│   ├── wiki-maintain/
│   │   ├── SKILL.md
│   │   └── references/
│   │       └── cron-recipes.md      # cron and launchd scheduling examples
│   ├── wiki-migrate-file/
│   │   └── SKILL.md
│   ├── wiki-query/
│   │   └── SKILL.md
│   └── wiki-think/
│       └── SKILL.md
└── README.md
```

---

## Changelog

### Version 1.4.0 (2026-06-22)

- Added shared validation module (`skills/_shared/scripts/validate.py` + `validation-rules.md`) providing a deterministic, reusable frontmatter and link-integrity checker
- Added write-time validation gate to `wiki-ingest` and `wiki-migrate-file`: malformed pages are blocked with a clear error before any vault write occurs
- Added contradiction detect-and-confirm workflow to `wiki-ingest`: conflicting claims are surfaced for user review before the ingested page is committed
- Added `wiki-think` skill: deep structured reasoning against the knowledge base in challenge / connect / socratic mode; optional `type: thinking` page output
- Added `wiki-maintain` skill: non-interactive lint + deterministic auto-fix pass with a written report, designed for unattended cron/launchd scheduling; recipes provided in `skills/wiki-maintain/references/cron-recipes.md`
- Refactored `wiki-lint` to delegate all deterministic checks to the shared validation module (behaviour unchanged; prose fallback retained for environments without PyYAML)
- Plugin now ships 11 skills (tasknotes, today, weekly-review, project-pulse, ideas, wiki-ingest, wiki-query, wiki-lint, wiki-migrate-file, wiki-think, wiki-maintain)

### Version 1.3.1 (2026-06-18)

- `wiki-lint`: exempt the append-only `_wiki/log.md` from the frontmatter-completeness check
- `wiki-lint`: accept `## Direktvergleich` **or** `## Options` as the comparison-table heading for `wiki-compare` pages; treat a missing `## Setup` on hosted/hardware tools as informational rather than critical
- `wiki-lint`: resolve dead links against `_raw/` sources and vault media too, normalize aliased/escaped/full-path links, and skip links inside code spans and generated `lint-report-*.md`/`log.md` bodies — eliminates the prior false positives

### Version 1.3.0 (2026-05-08)

- Added `today` skill: daily briefing from TaskNotes, Calendar, Gmail, Linear, GitHub
- Added `weekly-review` skill: structured weekly retrospective to vault
- Added `project-pulse` skill: GitHub repository status snapshot
- Added `ideas` skill: opportunity mining from wiki, GitHub, stakeholders, and market
- Added `update_daily_note.py` script: configurable note create/update utility
- All new skills use CLAUDE.md configuration keys with env var overrides and auto-detection
- Version bump to 1.3.0

### Version 1.2.0 (2026-05-01)

- Added LLM-Wiki workflow: `wiki-ingest`, `wiki-lint`, `wiki-migrate-file`, `wiki-query`
- Updated plugin description and keywords

### Version 1.1.2 (2026-02-27)

- Added `keywords` and `license` fields to plugin.json
- Fixed author email to support@talent-factory.ch
- Improved tasknotes skill description

---

## Related Plugins

- **[Project Management](project-management.md)** — PRD and task planning
- **[Git Workflow](git-workflow.md)** — Commit and PR automation

---

## License

MIT License — see [LICENSE](https://github.com/talent-factory/claude-plugins/blob/main/LICENSE) for details.

---

**Made with care by Talent Factory GmbH**
