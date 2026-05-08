---
name: today
description: >
  Produces a prioritised daily briefing by aggregating tasks from Obsidian TaskNotes,
  Google Calendar, Gmail, Linear, and GitHub, then writes the result to today's daily
  note in the Obsidian vault. Activate when the user runs "/today", asks "what's on
  my plate today", "give me my daily briefing", "what do I need to do today", or
  "morning briefing". Works from any directory without requiring Obsidian to be running.
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
If `TASKNOTES` remains empty, fall back to the direct file scan in Step 1b.

## Execution Steps

Resolve configuration, then run steps 1–5 in parallel. Compose and write the
briefing afterwards.

### Step 1 — TaskNotes

**1a — via script (preferred):**

```bash
uv run "$TASKNOTES" list --scan \
  | python3 -c "
import json, sys
from datetime import date
today = date.today().isoformat()
tasks = json.load(sys.stdin)
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

**1b — direct file scan (fallback when script is unavailable):**

```bash
grep -rl 'tags:.*task\|tag: task' "$VAULT" --include="*.md" -l \
  | xargs python3 -c "
import sys, re
from datetime import date
from pathlib import Path
today = date.today().isoformat()
for path in sys.argv[1:]:
    text = Path(path).read_text()
    fm = re.search(r'^---\n(.*?)\n---', text, re.DOTALL)
    if not fm: continue
    block = fm.group(1)
    def val(k): m = re.search(rf'^{k}:\s*(.+)', block, re.M); return m.group(1).strip() if m else ''
    status = val('status')
    if status == 'done': continue
    due = val('due')[:10]; sched = val('scheduled')[:10]
    if due == today or sched == today:    bucket = 'today'
    elif due and due < today:             bucket = 'overdue'
    elif status == 'in-progress':         bucket = 'in-progress'
    else: continue
    print(bucket, Path(path).stem, 'due='+due, 'sched='+sched, 'prio='+val('priority'))
"
```

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

### Step 4 — Linear

```
Tool: mcp__plugin_linear_linear__list_issues
(filter: assigned to me, state not completed/cancelled)
```

Sort by priority: urgent → high → normal → low. Flag any issue with
`dueDate ≤ today`.

### Step 5 — GitHub

```bash
gh pr list --author @me --state open \
  --json number,title,headRepository,updatedAt,reviewDecision 2>/dev/null

gh pr list --review-requested @me --state open \
  --json number,title,headRepository,updatedAt 2>/dev/null

gh issue list --assignee @me --state open \
  --json number,title,repository,labels,updatedAt 2>/dev/null
```

Skip silently if `gh` is unavailable or unauthenticated.

## Priority Scoring

Assign each item a score and sort descending. Top 10 items → **Priorities**
list; remainder → source sections.

| Score | Condition |
|---|---|
| 100 | Linear: Urgent |
| 85 | TaskNote: overdue > 2 days, priority urgent/high |
| 70 | Linear: High + due today |
| 65 | TaskNote: overdue, any priority |
| 55 | Linear: High |
| 50 | TaskNote: due today, priority urgent/high |
| 45 | GitHub PR: CHANGES_REQUESTED |
| 35 | Gmail: unread > 24 h, actionable |
| 30 | TaskNote: due today, priority normal |
| 25 | GitHub PR: open, no review yet |
| 20 | Linear: Normal |
| 15 | TaskNote: scheduled today |
| 10 | GitHub issue assigned |
| 5  | Linear: Low |

Priority emoji by score: 🔴 ≥ 65 · 🟠 35–64 · 🟡 15–34 · ⚪ < 15

## Briefing Format

Always include deep links so every item is directly clickable:

- **Linear**: `[ID](url)` — `url` field from the API response
- **Gmail**: `[Mail](https://mail.google.com/mail/u/0/#inbox/<thread_id>)` — `id` field
- **TaskNotes**: `[[Filename without .md]]` — Obsidian internal link, clickable in vault
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
1. 🔴 [Linear] **[ABC-17 Title](https://linear.app/...)** — URGENT
2. 🟠 [Task] **[[TaskNote Filename]]** — 3 days overdue
3. 🟡 [GitHub] **[PR #N Title](github-url)** (repo) — awaiting review
...

#### Emails
- **Sender**: [Subject](https://mail.google.com/mail/u/0/#inbox/thread-id) (age)
*(omit section if empty)*

#### GitHub
- [PR #N **Title**](github-url) (repo) — status
*(omit section if empty)*
```

Source labels: `[Task]` `[Linear]` `[GitHub]` `[Mail]`

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
📧 2 emails  ·  GitHub: 1 PR, 2 issues
```

## Additional Resources

- **`references/priority-guide.md`** — Extended priority rules, edge cases, and tuning guidance
- **`scripts/update_daily_note.py`** — Note create/update script (configurable via CLI flags)
