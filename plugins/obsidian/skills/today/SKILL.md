---
name: today
description: >
  Produces a prioritised daily briefing by aggregating tasks from Obsidian TaskNotes,
  Apple Reminders, Google Calendar, Gmail, Plane, and GitHub, then writes the result to
  today's daily note in the Obsidian vault. Activate when the user runs "/obsidian:today", asks
  "what's on my plate today", "give me my daily briefing", "what do I need to do today",
  or "morning briefing". Works from any directory without requiring Obsidian to be running.
---

# Today Briefing

Collect all relevant tasks and events for today from all configured sources, rank them
by urgency, and write a structured briefing to today's Obsidian daily note.

## Configuration

Read the following keys from `~/.claude/CLAUDE.md` at skill start. Environment
variables listed under each key take precedence over the CLAUDE.md value.

| CLAUDE.md key | Env var | Default | Description |
|---|---|---|---|
| `obsidian_vault` | `OBSIDIAN_VAULT` | auto-detect via `.obsidian` | Absolute path to vault root |
| `obsidian_daily_dir` | `OBSIDIAN_DAILY_DIR` | `Daily` | Daily notes folder (relative to vault) |
| `obsidian_template_daily` | `OBSIDIAN_TEMPLATE_DAILY` | `<vault>/Templates/Daily Note.md` | Daily note template |
| `user_email` | `USER_EMAIL` | `git config user.email` | Your email address (used to detect unanswered Gmail threads) |
| `plane_workspace` | `PLANE_WORKSPACE` | — | Plane workspace slug (first path segment of the Plane URL); the Plane step is skipped if not set |
| `plane_url` | `PLANE_URL` | — | Base URL of the Plane instance (used for deep links); without it, identifiers are shown without a link |
| `reminders_lists` | `REMINDERS_LISTS` | all lists | Comma-separated Apple Reminders lists to include |

**Vault auto-detection** (applied when `obsidian_vault` is not set):
```bash
find "$HOME" -maxdepth 5 -name ".obsidian" -type d 2>/dev/null | head -1 | xargs dirname
```
Halt with a clear error message if the vault cannot be resolved.

**Script locations** (resolved at runtime via the plugin root):
```bash
# Note update script
SCRIPT="${CLAUDE_PLUGIN_ROOT}/skills/today/scripts/update_daily_note.py"

# TaskNotes script (same plugin)
TASKNOTES="${CLAUDE_PLUGIN_ROOT}/skills/tasknotes/scripts/tasks.py"
# Fallback: plugin cache
[ -f "$TASKNOTES" ] || TASKNOTES=$(find ~/.claude/plugins/cache/talent-factory/obsidian \
  -name "tasks.py" -path "*/tasknotes/scripts/*" 2>/dev/null | sort -V | tail -1)
```
If `TASKNOTES` remains empty, skip Step 1.

## Execution Steps

Resolve configuration, then run steps 1–6 in parallel. Compose and write the
briefing afterwards. Every source degrades gracefully: if one is unavailable,
skip it and continue with the rest.

### Step 1 — TaskNotes

```bash
uv run "$TASKNOTES" list --scan \
  | python3 -c "
import json, sys
from datetime import date
today = date.today().isoformat()
data = json.load(sys.stdin)
# tasks.py prints {"success", "count", "tasks": [...]}; tolerate a bare list too
tasks = data['tasks'] if isinstance(data, dict) else data
out = []
for t in tasks:
    if t.get('status') == 'done':
        continue
    due   = (t.get('due') or '')[:10]
    sched = (t.get('scheduled') or '')[:10]
    status = t.get('status', '')
    if due == today or sched == today:
        t['_bucket'] = 'today'
    elif due and due < today:
        t['_bucket'] = 'overdue'
    elif status == 'in-progress':
        t['_bucket'] = 'in-progress'
    else:
        continue
    out.append(t)
print(json.dumps(out, indent=2))
"
```

If the script is unavailable (no `uv`, plugin not found), skip TaskNotes and say so in the terminal summary.

Relevant fields per task: filename (= title), `priority`, `due`, `scheduled`,
`status`, `projects`, `_bucket`.

### Step 2 — Google Calendar

```
Tool: mcp__claude_ai_Google_Calendar__list_events
Parameters:
  timeMin: <today>T00:00:00
  timeMax: <today>T23:59:59
  maxResults: 20
```

Extract: `summary`, `start.dateTime`, `end.dateTime`, `location`. Compute
**free time blocks** ≥ 30 min within 08:00–18:00 and suggest them as focus
windows in the briefing.

### Step 3 — Gmail

```
Tool: mcp__claude_ai_Gmail__search_threads
Parameters:
  query: "is:unread newer_than:7d -from:noreply -from:no-reply -category:promotions -category:updates"
  maxResults: 15
```

Flag a thread as "needs reply" if the last message in the thread is not from
`$USER_EMAIL`. Extract: sender, subject, age.

### Step 4 — Plane

Plane is the ticket system. The MCP server `plane` serves all workspaces; pass the workspace on every call as `workspace: $PLANE_WORKSPACE`. If `PLANE_WORKSPACE` is not set, skip this step and note "Plane not configured".

Fetch the work items as described in [_shared/plane-graphql.md](../_shared/plane-graphql.md) (self-hosted limits, one GraphQL query for all projects, paging until `hasNextPage` is `false`, REST fallback). Then filter:

4. Keep an item only if all of these hold:
   - `me.id` is in `assignees[].id`
   - `state.group` is `unstarted` or `started`, or it is `backlog` and
     `targetDate` ≤ today
   - `completedAt` is empty

   Never keep `completed` or `cancelled` items.
5. Per item use: `identifier` (e.g. `PROJ-123`), `name`, `priority` (`urgent`,
   `high`, `medium`, `low`, `none`), `targetDate`, `state.name`.

Deep link: `<PLANE_URL>/<workspace>/browse/<identifier>/` (plain identifier if `PLANE_URL` is not set)

If Plane is not connected at all, skip it silently and note "Plane unavailable"
in the terminal summary.

### Step 5 — Apple Reminders

Uses the `remindctl` CLI (`brew install steipete/tap/remindctl`). Skip this step
silently if `command -v remindctl` is empty. If macOS has not granted access
(`remindctl status` does not report authorized), skip and print the hint
`run: remindctl authorize` in the terminal summary.

The script reads the list filter only from the environment. Resolve
`reminders_lists` (env var `REMINDERS_LISTS` first, then the CLAUDE.md value) and
export it in the same shell command, e.g. `REMINDERS_LISTS="Inbox,Work" python3 - <<'PY'`.
Leave it unset to include all lists.

Run the script in [references/reminders.md](references/reminders.md). It reads the list filter only from the environment.

Buckets:

- `today` — due today. A due time of exactly 00:00 means an all-day reminder
  (Apple stores date-only reminders at local midnight); omit the time then.
- `overdue` — overdue by 1–7 days. Treated like an overdue TaskNote.
- `stale` — overdue by more than 7 days. These are usually read-later links
  and forgotten items. Do **not** list them one by one; report only the count
  ("N stale reminders") so they do not bury real work.

Relevant fields per reminder: `title`, `listName`, `priority`
(`none`/`low`/`medium`/`high`), `notes`, `_due_local`, `_age_days`, `_bucket`.

Reminders have no stable deep link, so show the title as plain text with the
list name in parentheses.

If a reminder's title contains a Plane identifier (e.g. `PROJ-123`), merge it
with the matching Plane item (see `references/priority-guide.md`).

### Step 6 — GitHub

```bash
gh pr list --author @me --state open \
  --json number,title,headRepository,updatedAt,reviewDecision 2>/dev/null

# `gh pr list` has no --review-requested flag; use `gh search prs`
gh search prs --review-requested @me --state open \
  --json number,title,repository,url,updatedAt 2>/dev/null

# `gh issue list` has no `repository` field; search across repos instead
gh search issues --assignee @me --state open \
  --json number,title,repository,labels,url,updatedAt 2>/dev/null
```

Skip silently if `gh` is unavailable or unauthenticated.

## Priority Scoring

Assign each item a score and sort descending. Top 10 items → **Priorities**
list; remainder → source sections.

| Score | Condition |
|---|---|
| 100 | Plane: Urgent |
| 85 | TaskNote: overdue > 2 days, priority urgent/high |
| 70 | Plane: High + `targetDate` ≤ today |
| 65 | TaskNote: overdue, any priority |
| 65 | Plane: `targetDate` < today, any priority |
| 65 | Reminder: overdue 1–7 days, any priority |
| 55 | Plane: High |
| 50 | TaskNote: due today, priority urgent/high |
| 50 | Reminder: due today, priority high |
| 45 | GitHub PR: CHANGES_REQUESTED |
| 35 | Gmail: unread > 24 h, actionable |
| 30 | TaskNote: due today, priority normal |
| 30 | Reminder: due today, priority none/low/medium |
| 25 | GitHub PR: open, no review yet |
| 20 | Plane: Medium |
| 15 | TaskNote: scheduled today |
| 10 | GitHub issue assigned |
| 5  | Plane: Low or None |

Stale reminders (> 7 days overdue) are not scored; they appear only as a count.

Priority emoji by score: 🔴 ≥ 65 · 🟠 35–64 · 🟡 15–34 · ⚪ < 15

## Briefing Format

Always include deep links so every item is directly clickable:

- **Plane**: `[ID](url)` — built as `<PLANE_URL>/<workspace>/browse/<ID>/`
- **Gmail**: `[Mail](https://mail.google.com/mail/u/0/#inbox/<thread_id>)` — `id` field
- **TaskNotes**: `[[Filename without .md]]` — Obsidian internal link, clickable in vault
- **Reminders**: plain title, list name in parentheses (no deep link)
- **Calendar**: `[Event name](htmlLink)` — omit link for all-day/multi-day events
- **GitHub PR**: `[#N title](html_url)`

```markdown
### :LiSun: Daily Briefing — YYYY-MM-DD
_updated: HH:MM_

#### Calendar
- HH:MM [**Event**](calendar-url) (Xm) — Location
- *(no events)* if empty

**Free blocks:** HH:MM–HH:MM (Xh), HH:MM–HH:MM (Yh)

#### Priorities
1. 🔴 [Plane] **[PROJ-17 Title](https://plane.example.com/my-workspace/browse/PROJ-17/)** — URGENT
2. 🟠 [Task] **[[TaskNote Filename]]** — 3 days overdue
3. 🟠 [Reminder] **Title** (Reminders) — due today
4. 🟡 [GitHub] **[PR #N Title](github-url)** (repo) — awaiting review
...

#### Reminders
- **Title** (List) — HH:MM / all day / N days overdue
- _N stale reminders (> 7 days overdue)_
*(omit section if empty)*

#### Emails
- **Sender**: [Subject](https://mail.google.com/mail/u/0/#inbox/thread-id) (age)
*(omit section if empty)*

#### GitHub
- [PR #N **Title**](github-url) (repo) — status
*(omit section if empty)*
```

Source labels: `[Task]` `[Plane]` `[Reminder]` `[GitHub]` `[Mail]`

## Write to Daily Note

```bash
python3 "$SCRIPT" \
  "$(date +%Y-%m-%d)" \
  "<briefing markdown>" \
  --vault "$VAULT" \
  --daily-dir "$DAILY_DIR" \
  --template "$DAILY_TEMPLATE"
```

The script creates the note from template if it does not yet exist (substituting
`{{yesterday}}` / `{{tomorrow}}`), inserts the briefing after
`> ![[tasks-default.base]]` on first run, and replaces the existing
`### :LiSun: Daily Briefing` block on subsequent runs.

## Terminal Summary

After writing, output only the following (not the full briefing):

```
✓ Briefing → Daily/2026-05-08.md

📅 3 events  |  free blocks: 10:30–14:00 (3.5h)
🔴 2 urgent  🟠 4 due today  🟡 3 watch
📧 2 emails  ·  GitHub: 1 PR, 2 issues  ·  Plane: 5  ·  Reminders: 3 (+8 stale)
```

Append a short note for every skipped source, e.g. `Plane unavailable` or
`Reminders: run remindctl authorize`, `Plane: page cap (20) hit for <project>`
or `Plane: page skipped after HTTP 429`.

## Additional Resources

- **`references/priority-guide.md`** — Extended priority rules, edge cases, and tuning guidance
- **`scripts/update_daily_note.py`** — Note create/update script (configurable via CLI flags)
