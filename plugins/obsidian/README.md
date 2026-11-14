# Obsidian Plugin

## Version 2.0.2

Task management through TaskNotes, LLM-Wiki curation, and productivity briefings for an Obsidian vault.

## Skills

Invoke as `/obsidian:<skill>`; all skills also activate from natural language.

| Skill | What it does |
|---|---|
| `tasknotes` | Lists, creates and updates tasks through the TaskNotes HTTP API (`tasks.py`, vault-wide `--scan`). |
| `today` | Daily briefing from TaskNotes, Apple Reminders, Google Calendar, Gmail, Plane and GitHub, ranked by urgency and written to today's daily note. |
| `weekly-review` | Weekly retrospective: completed tasks, commits and PRs, meetings, wiki learnings, Plane progress. Keeps your own Reflection section on re-runs. |
| `ideas` | Surfaces product and project ideas from the wiki, GitHub, customer notes and market trends. |
| `wiki-ingest` | Files a source (clipping, chat export, transcript, note) under `_raw/` and distils it into `_wiki/` pages with index, log and cross-references. Validates before writing. |
| `wiki-query` | Answers a question from the curated wiki with citations, optionally filing the answer back as a page. |
| `wiki-lint` | Health check: frontmatter, cross-references, contradictions, stale claims, tags, migration backlog. |
| `wiki-maintain` | `wiki-lint` unattended with optional auto-fix, for cron or launchd (`references/cron-recipes.md`). |
| `wiki-migrate-file` | Moves a legacy note, or a cluster of notes, into the wiki schema. |

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
plane_workspace: my-workspace            # Plane workspace slug (Plane steps are skipped if unset)
plane_url: https://plane.example.com     # Plane base URL for deep links (optional)
reminders_lists: Inbox,Work               # Apple Reminders lists (default: all)
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
| `PLANE_WORKSPACE` | `plane_workspace` |
| `PLANE_URL` | `plane_url` |
| `REMINDERS_LISTS` | `reminders_lists` |

**Vault auto-detection:** If `obsidian_vault` is not set, the plugin searches
`$HOME` up to five directory levels deep for a `.obsidian` folder. Set the key
explicitly to avoid ambiguity when multiple vaults are present.

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
connections when available: Google Calendar, Gmail, Plane (self-hosted, MCP server `plane`). Each integration
degrades gracefully when not configured — only that data source is skipped.

### 4. Apple Reminders (optional, macOS only, for `today`)

```bash
brew install steipete/tap/remindctl && remindctl authorize
```

Without `remindctl` the `today` skill skips Reminders silently. Restrict the lists
with `reminders_lists` / `REMINDERS_LISTS`.

### 5. PyYAML (for wiki validation)

The shared validation module (`skills/_shared/scripts/validate.py`) requires
**PyYAML** to perform deterministic frontmatter checks at write time:

```bash
pip install pyyaml
```

Without PyYAML the wiki-ingest and wiki-migrate-file skills fall back to the
prose validation rules in `skills/_shared/validation-rules.md` and continue to
operate, but structural checks are less strict.

---

## LLM-Wiki Vault Layout

The wiki skills expect the following structure (default paths shown):

- `<wiki-root>/_raw/` — raw source files, organised by type subfolder
- `<wiki-root>/_wiki/` — distilled wiki pages
- `<wiki-root>/_wiki/index.md` — section-based index
- `<wiki-root>/_wiki/log.md` — append-only operation log
- `<wiki-root>/_wiki/templates/` — frontmatter templates

Default `<wiki-root>` is `Wiki/` relative to the vault root. Override via
`obsidian_wiki_root:` in `~/.claude/CLAUDE.md` or `wiki_root:` in the vault's `CLAUDE.md` (the latter wins). The migration backlog soft cap
(default: 50 files) is configurable via `wiki_migration_cap: <n>`.

---

## Changelog

### Version 2.0.2 (2026-11-14)

No change in behaviour or invocations; the long recipes moved out of the always-loaded skill text.

- `today` and `weekly-review` share one description of how to read Plane work items through GraphQL (`skills/_shared/plane-graphql.md`); `weekly-review` no longer points into the other skill.
- The Reminders script of `today` lives in `skills/today/references/reminders.md` and loads only when `remindctl` is available.
- `today` drops the direct file-scan fallback for TaskNotes: without the script it skips TaskNotes and says so.
- `ideas` cut from 256 to 94 lines (the shell snippets for `gh`, `find` and `ls` are gone; the signals, scoring, output format and frontmatter stay).

### Version 2.0.1 (2026-11-14)

- The wiki skills call `markdown-syntax-formatter` as a skill of the `education` plugin (it was an agent, which `education` 5.0.0 removes).

### Version 2.0.0 (2026-11-14)

**Breaking:**

- Removed the skills `project-pulse` (a `gh` query the model answers directly) and `wiki-think` (a conversation mode without tooling). `wiki-query` stays.
- `wiki-maintain` is now a thin wrapper over `wiki-lint` (flags, report file, exit code only); the duplicated check descriptions are gone.
- Fixed the invocation names in skill descriptions and recipes: skills are called `/obsidian:today`, `/obsidian:wiki-ingest` and so on, not `/today` or `/wiki:ingest` (the natural-language triggers are unchanged). Scheduled jobs must use the plugin form, for example `claude -p "/obsidian:wiki-maintain --auto-fix --quiet"`.
- One rule for the wiki root: `wiki_root` in the vault's `CLAUDE.md`, else `obsidian_wiki_root` in `~/.claude/CLAUDE.md`, else `Wiki`.
- `tasknotes` skill text cut from 169 to 40 lines (same commands).

### Version 1.6.0 (2026-11-14)

- `today` and `weekly-review` no longer default to a specific Plane workspace or URL. `plane_workspace` has no default and the Plane step is skipped when it is unset; `plane_url` is optional and without it identifiers are shown without a link. Example identifiers are `PROJ-123`. **Migration:** set `plane_workspace` (and `plane_url`) in `~/.claude/CLAUDE.md` or the environment if you use Plane

### Version 1.5.1 (2026-11-11)

- `today`: reads every Plane page per project until `hasNextPage` is `false` (safety cap 20 pages) instead of stopping after 5; handles the compact table result format and retries on HTTP 429

### Version 1.5.0 (2026-11-08)

- `today`: Plane replaces Linear as ticket source. Queries all projects through the MCP GraphQL tool (the self-hosted edition has no PQL and no workspace-wide list) and filters client-side; deep links point to the configured `plane_url`
- `today`: Apple Reminders as new source via `remindctl` (overdue ≤ 7 days and due today scored; older ones are only counted); new config keys `plane_workspace`, `plane_url`, `reminders_lists`
- `weekly-review`: Plane replaces Linear for weekly progress

### Version 1.4.0 (2026-06-22)

- Added shared validation module (`skills/_shared/scripts/validate.py` + `validation-rules.md`) providing a deterministic, reusable frontmatter and link-integrity checker
- Added write-time validation gate to `wiki-ingest` and `wiki-migrate-file`: malformed pages are blocked with a clear error before any vault write occurs
- Added contradiction detect-and-confirm workflow to `wiki-ingest`: conflicting claims are surfaced for user review before the ingested page is committed
- Added `wiki-think` skill: deep structured reasoning against the knowledge base in challenge / connect / socratic mode; optional `type: thinking` page output
- Added `wiki-maintain` skill: non-interactive lint + deterministic auto-fix pass with a written report, designed for unattended cron/launchd scheduling; recipes provided in `skills/wiki-maintain/references/cron-recipes.md`
- Refactored `wiki-lint` to delegate all deterministic checks to the shared validation module (behavior unchanged; prose fallback retained for environments without PyYAML)
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

- **[Project Management](https://talent-factory.github.io/claude-plugins/plugins/project-management/)** — PRD and task planning
- **[Git Workflow](https://talent-factory.github.io/claude-plugins/plugins/git-workflow/)** — Commit and PR automation

---

## License

MIT License — see [LICENSE](https://github.com/talent-factory/claude-plugins/blob/main/LICENSE) for details.

---

**Made with care by Talent Factory GmbH**
