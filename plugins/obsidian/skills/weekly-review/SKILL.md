---
name: weekly-review
description: >
  Collects completed tasks, GitHub activity, calendar meetings, wiki learnings, and
  Linear progress for the past week, then writes a structured retrospective to the
  Obsidian vault. Activate when the user runs "/weekly-review", asks "what did I
  accomplish this week", "weekly retrospective", "summarise my week", or "prepare
  weekly review". Works from any directory.
---

# Weekly Review

Collect everything that happened in the past week and write a structured retrospective
to the vault. Combines reflection on what was accomplished with intentional focus-setting
for the week ahead.

## Configuration

Read the following keys from `~/.claude/CLAUDE.md` at skill start. Environment
variables listed under each key take precedence over the CLAUDE.md value.

| CLAUDE.md key | Env var | Default | Description |
|---|---|---|---|
| `obsidian_vault` | `OBSIDIAN_VAULT` | auto-detect via `.obsidian` | Absolute path to vault root |
| `obsidian_daily_dir` | `OBSIDIAN_DAILY_DIR` | `Daily` | Daily notes folder (relative to vault) — output is written here |
| `obsidian_template_weekly` | `OBSIDIAN_TEMPLATE_WEEKLY` | `<vault>/Templates/Weekly Review.md` | Weekly review template |
| `obsidian_wiki_root` | — | `Wiki` | Wiki root folder (relative to vault) — used to read the log |
| `github_org` | `GITHUB_ORG` | — | GitHub organisation; GitHub step is skipped if not set |

**Vault auto-detection** (applied when `obsidian_vault` is not set):
```bash
find "$HOME" -maxdepth 5 -name ".obsidian" -type d 2>/dev/null | head -1 | xargs dirname
```
Halt with a clear error message if the vault cannot be resolved.

**TaskNotes script location:**
```bash
TASKNOTES="${CLAUDE_PLUGIN_ROOT}/skills/tasknotes/scripts/tasks.py"
[ -f "$TASKNOTES" ] || TASKNOTES=$(find ~/.claude/plugins/cache/talent-factory/obsidian \
  -name "tasks.py" -path "*/tasknotes/scripts/*" 2>/dev/null | sort -V | tail -1)
```

## Week Range Calculation

```bash
TODAY=$(date +%Y-%m-%d)
DOW=$(date +%u)          # 1=Mon … 7=Sun

WEEK_START=$(date -v-$((DOW-1))d +%Y-%m-%d 2>/dev/null || \
             date -d "$((DOW-1)) days ago" +%Y-%m-%d)

WEEK_END=$(date -v+$((7-DOW))d +%Y-%m-%d 2>/dev/null || \
           date -d "$((7-DOW)) days from now" +%Y-%m-%d)

WEEK_NUM=$(date +%V)
YEAR=$(date +%Y)
OUTPUT_FILE="${YEAR}-W${WEEK_NUM}-weekly-review.md"
```

If the skill is invoked on a Monday before 10:00, use the *previous* week instead.

## Execution Steps

Run steps 1–5 in parallel.

### Step 1 — TaskNotes: Completed and open this week

```bash
uv run "$TASKNOTES" list --scan 2>/dev/null \
  | python3 -c "
import json, sys
from datetime import date, timedelta

data = json.load(sys.stdin)
tasks = data.get('tasks', data) if isinstance(data, dict) else data

today = date.today()
dow = today.weekday()
week_start = (today - timedelta(days=dow)).isoformat()
week_end   = (today + timedelta(days=6-dow)).isoformat()

done, open_late, open_this_week = [], [], []
for t in tasks:
    status    = t.get('status', '')
    due       = (t.get('due') or '')[:10]
    sched     = (t.get('scheduled') or '')[:10]
    completed = (t.get('completedDate') or '')[:10]
    title     = t.get('title', t.get('id','?').split('/')[-1].replace('.md',''))
    prio      = t.get('priority', 'normal')
    item      = {'title': title, 'priority': prio, 'due': due, 'completed': completed}

    if status == 'done' and completed >= week_start:
        done.append(item)
    elif status != 'done':
        if due and due < week_start:
            open_late.append(item)
        elif due and week_start <= due <= week_end:
            open_this_week.append(item)

print('DONE:', json.dumps(done))
print('LATE:', json.dumps(open_late))
print('THIS_WEEK:', json.dumps(open_this_week))
"
```

### Step 2 — GitHub: What was shipped?

Skip this step if `GITHUB_ORG` is not configured.

```bash
# Commits across organisation repos this week
gh repo list "$GITHUB_ORG" --limit 30 --json name \
  --jq '.[].name' 2>/dev/null | head -15 | while read repo; do
    count=$(gh api "repos/$GITHUB_ORG/$repo/commits?since=${WEEK_START}T00:00:00Z&until=${WEEK_END}T23:59:59Z&per_page=10" \
      --jq 'length' 2>/dev/null || echo 0)
    if [ "$count" -gt 0 ]; then
      echo "$repo: $count commits"
      gh api "repos/$GITHUB_ORG/$repo/commits?since=${WEEK_START}T00:00:00Z&per_page=5" \
        --jq '.[].commit.message | split("\n")[0]' 2>/dev/null | head -3 | sed 's/^/  /'
    fi
  done

# Merged PRs this week
gh pr list --state merged --author @me \
  --json number,title,headRepository,mergedAt \
  --jq ".[] | select(.mergedAt >= \"${WEEK_START}\")" 2>/dev/null

# Closed issues this week
gh issue list --assignee @me --state closed \
  --json number,title,repository,closedAt \
  --jq ".[] | select(.closedAt >= \"${WEEK_START}\")" 2>/dev/null
```

### Step 3 — Google Calendar: Meetings this week

```
Tool: mcp__claude_ai_Google_Calendar__list_events
Parameters:
  startTime: <WEEK_START>T00:00:00
  endTime:   <WEEK_END>T23:59:59
  maxResults: 30
```

Extract timed events (skip all-day events). Group by day.

### Step 4 — Linear: Progress this week

```
Tool: mcp__plugin_linear_linear__list_issues
(filter: assignee = me, updatedAt within last 7 days)
```

Separate into: completed this week · still in progress · newly created.

### Step 5 — Wiki: What was learned?

```bash
WIKI_LOG="$VAULT/$WIKI_ROOT/_wiki/log.md"
WIKI_DIR="$VAULT/$WIKI_ROOT/_wiki"

# Log entries added this week
grep -E "^\-\-\- \[${YEAR}" "$WIKI_LOG" 2>/dev/null | tail -20

# Pages modified this week
find "$WIKI_DIR" -name "*.md" -newer "$WIKI_LOG" \
  -not -name "index.md" -not -name "log.md" \
  | xargs ls -t 2>/dev/null | head -10
```

Skip gracefully if the wiki root does not exist.

## Output Format

```markdown
---
tags:
  - weekly-review
week: YYYY-WNN
period: YYYY-MM-DD — YYYY-MM-DD
---

# Weekly Review — W<NN> (YYYY-MM-DD – YYYY-MM-DD)
_Generated: YYYY-MM-DD HH:MM_

## ✅ Completed

### Tasks
- **[Title]** _(priority)_

### GitHub — Shipped
- **[repo]**: [N] commits — [highlight commit message]
- PR #N **[Title]** merged

### Linear — Resolved
- [ID] **[Title]** → done

*(Omit section if empty)*

---

## 📅 Meetings & Decisions

- **Mon, DD/MM**: [Event] — [one-sentence takeaway if known]
- **Tue, DD/MM**: [Event]

*(«no events» if empty)*

---

## 📖 Learned This Week

- **[[Wiki Page]]** — [one sentence on what was new]

---

## ⚠️ Open Loops

_Tasks due this week that remain open:_

- **[Title]** — due [date], [priority]

_Linear items still in progress:_

- [ID] **[Title]** — [status]

---

## 🎯 Focus Next Week

_Top 3 from Linear + TaskNotes (by priority):_

1. [Item]
2. [Item]
3. [Item]

---

## 💭 Reflection

> **What went well?**
> [Free text — leave empty on first run; preserve on subsequent runs]

> **What would I do differently?**
>

> **What do I want to improve next week?**
>
```

## Write to Vault

```bash
NOTE_PATH="$VAULT/$DAILY_DIR/${OUTPUT_FILE}"
```

If a weekly review for this ISO week already exists, replace all sections **except**
`## 💭 Reflection` — that section is written by the user and must be preserved.
Use the same insert/replace pattern as `update_daily_note.py`.

## Terminal Summary

```
✓ Weekly Review → Daily/2026-W19-weekly-review.md

W19 (04 May – 10 May 2026)
✅ 3 tasks · 12 commits (4 repos) · 2 PRs merged · 2 Linear resolved
📅 5 meetings · 📖 4 wiki pages · ⚠️ 2 open loops
```

## Additional Resources

- **`references/weekly-cadence.md`** — Recommended cadence, reflection prompts, and pattern recognition tips
