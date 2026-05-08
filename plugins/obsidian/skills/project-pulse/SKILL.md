---
name: project-pulse
description: >
  Provides a quick status snapshot of all GitHub repositories in a configured
  organisation — active, dormant, stalled — plus open pull requests and issues.
  Terminal output only, optimised for speed. Activate when the user runs
  "/project-pulse", asks "what is the status of my GitHub projects", "show me
  my repos", "which projects are active", "project overview", "GitHub pulse", or
  "what is happening in [org]". Works from any directory.
---

# Project Pulse

Quick status snapshot of all GitHub repositories in the configured organisation.
Optimised for speed — terminal output only, no vault writes.

## Configuration

Read the following key from `~/.claude/CLAUDE.md` at skill start.

| CLAUDE.md key | Env var | Required | Description |
|---|---|---|---|
| `github_org` | `GITHUB_ORG` | Yes | GitHub organisation name |

If `github_org` is not set and cannot be inferred from the current git remote,
halt with:
> "Error: GitHub organisation not configured. Add `github_org: <your-org>` to ~/.claude/CLAUDE.md or export GITHUB_ORG=<your-org>"

**Auto-detect from git remote** (fallback when key is not set):
```bash
git remote get-url origin 2>/dev/null | sed -E 's|.*[:/]([^/]+)/[^/]+\.git.*|\1|'
```

## Execution

Run all queries in parallel:

```bash
# 1. All non-archived repos sorted by last push
gh repo list "$GITHUB_ORG" --limit 50 \
  --json name,description,pushedAt,isArchived,isPrivate \
  --jq 'sort_by(.pushedAt) | reverse | .[] | select(.isArchived == false)' \
  2>/dev/null

# 2. Open PRs authored by me
gh pr list --author @me --state open \
  --json number,title,headRepository,updatedAt,reviewDecision \
  2>/dev/null

# 3. Open issues assigned to me
gh issue list --assignee @me --state open \
  --json number,title,repository,labels,createdAt \
  2>/dev/null

# 4. Repos with activity in the past 7 days
WEEK_AGO=$(date -v-7d +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || \
           date -d "7 days ago" +%Y-%m-%dT%H:%M:%SZ)
gh repo list "$GITHUB_ORG" --limit 50 \
  --json name,pushedAt \
  --jq --arg w "$WEEK_AGO" '[.[] | select(.pushedAt >= $w) | .name]' \
  2>/dev/null
```

## Categorisation

Group repositories into three buckets based on `pushedAt`:

| Category | Criterion | Icon |
|---|---|---|
| **Active** | pushed within the last 14 days | 🟢 |
| **Dormant** | 15–90 days since last push | 🟡 |
| **Stalled** | > 90 days since last push | 🔴 |

## Output Format

Terminal-only. Compact and scannable:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PROJECT PULSE — <github_org>  (YYYY-MM-DD)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🟢 ACTIVE (last 14 days)
  repo-name-a    today       Description of repo A
  repo-name-b    yesterday   Description of repo B

🟡 DORMANT (15–90 days)
  repo-name-c    35 days ago   Description of repo C

🔴 STALLED (> 90 days)
  repo-name-d    95 days ago   Description of repo D

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 OPEN PRs (authored or review-requested)
  #42 repo-name-a  "Feature: title"    (2 days old)

🐛 OPEN ISSUES (assigned to me)
  #123  repo-name-b  "Issue title"        HIGH

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5 active · 4 dormant · 6 stalled · 1 PR · 2 issues
```

## Relative Time Helper

Use the following Python helper to format dates in the output:

```python
from datetime import datetime, timezone

def rel(iso: str) -> str:
    d = datetime.fromisoformat(iso.replace('Z', '+00:00'))
    days = (datetime.now(timezone.utc) - d).days
    if days == 0:  return "today"
    if days == 1:  return "yesterday"
    if days < 14:  return f"{days} days ago"
    if days < 30:  return f"{days // 7} weeks ago"
    return f"{days // 30} months ago"
```

## Optional Flag: `--stalled-only`

If the user writes `/project-pulse --stalled-only`, show only the 🔴 stalled
repositories with a one-line prompt:

> "These repositories have been inactive for > 90 days. Archive, reactivate, or dismiss?"
