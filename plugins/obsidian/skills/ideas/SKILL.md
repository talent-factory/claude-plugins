---
name: ideas
description: >
  Surfaces new product, feature, and business ideas by cross-referencing the user's
  knowledge wiki, GitHub repositories, customer or project notes, and current market
  trends. Writes a structured ideas document to the Obsidian vault. Activate when the
  user runs "/ideas", asks "what could I build next", "give me new project ideas",
  "what opportunities am I missing", "brainstorm project ideas", or "what should I
  work on strategically".
---

# Ideas — Opportunity Mining

Surface new product, feature, and business ideas by cross-referencing what you know,
what you have built, who your stakeholders are, and what the market is doing right now.

## Configuration

Read the following keys from `~/.claude/CLAUDE.md` at skill start. Environment
variables listed under each key take precedence over the CLAUDE.md value.

| CLAUDE.md key | Env var | Default | Description |
|---|---|---|---|
| `obsidian_vault` | `OBSIDIAN_VAULT` | auto-detect via `.obsidian` | Absolute path to vault root |
| `obsidian_wiki_root` | — | `Wiki` | Wiki root folder (relative to vault) |
| `obsidian_companies_dir` | — | `Companies` | Folder containing customer/stakeholder notes (relative to vault) |
| `obsidian_ideas_dir` | — | `Ideas` | Output folder for ideas documents (relative to vault) |
| `obsidian_daily_dir` | — | `Daily` | Daily notes folder (relative to vault) |
| `obsidian_context_dir` | — | — | Optional: folder with strategic or organisational context notes |
| `github_org` | `GITHUB_ORG` | — | GitHub organisation; GitHub step is skipped if not set |

**Vault auto-detection** (applied when `obsidian_vault` is not set):
```bash
find "$HOME" -maxdepth 5 -name ".obsidian" -type d 2>/dev/null | head -1 | xargs dirname
```
Halt with a clear error message if the vault cannot be resolved.

## Execution Steps

Run steps 1–5 in parallel, then synthesise.

### Step 1 — Wiki: What am I deep in?

Read the wiki index and recent log entries to understand current knowledge focus:

```bash
# Recent wiki activity (last 80 lines of log)
tail -80 "$VAULT/$WIKI_ROOT/_wiki/log.md" 2>/dev/null

# Recently modified wiki pages
find "$VAULT/$WIKI_ROOT/_wiki" -name "*.md" \
  -not -name "index.md" -not -name "log.md" \
  | xargs ls -t 2>/dev/null | head -20

# Wiki index
cat "$VAULT/$WIKI_ROOT/_wiki/index.md" 2>/dev/null
```

Extract: active domains, recurring themes, technologies being tracked, sources
recently ingested.

Skip gracefully if the wiki root does not exist.

### Step 2 — GitHub: What has been built and what is stalled?

Skip this step if `GITHUB_ORG` is not configured.

```bash
# All non-archived repos sorted by last push
gh repo list "$GITHUB_ORG" --limit 50 \
  --json name,description,updatedAt,isArchived,pushedAt \
  --jq '.[] | select(.isArchived == false) | {name, description, pushedAt}' \
  2>/dev/null | sort

# Open issues assigned to me
gh issue list --assignee @me --state open \
  --json number,title,repository,labels,createdAt \
  2>/dev/null

# Repos with no push in > 90 days (stalled)
gh repo list "$GITHUB_ORG" --limit 50 \
  --json name,pushedAt \
  --jq '.[] | select(.isArchived == false) |
    select((.pushedAt | fromdateiso8601) < (now - 7776000)) |
    .name + " (stalled)"' \
  2>/dev/null
```

Extract: active projects, dormant repositories with potential, feature gaps
visible in open issues, cross-portfolio patterns.

### Step 3 — Stakeholders: What do they need?

```bash
# All notes in companies or stakeholders folder
ls "$VAULT/$COMPANIES_DIR/" 2>/dev/null

# Brief summary of each note (first 30 lines)
for f in "$VAULT/$COMPANIES_DIR/"*.md; do
  echo "=== $(basename $f) ==="
  head -30 "$f"
done
```

Extract: industries served, recurring pain points, requests that recur across
multiple stakeholders, under-served needs.

Skip gracefully if `obsidian_companies_dir` is not configured or the folder
does not exist.

### Step 4 — Personal context: What is top of mind?

```bash
# Recent daily notes (last 7 days)
ls -t "$VAULT/$DAILY_DIR/"*.md 2>/dev/null | head -7 \
  | xargs grep -l -E "(idea|opportunity|could|potential|TODO)" 2>/dev/null \
  | xargs head -50 2>/dev/null

# Strategic context folder (if configured)
if [ -n "$CONTEXT_DIR" ] && [ -d "$VAULT/$CONTEXT_DIR" ]; then
  find "$VAULT/$CONTEXT_DIR" -name "*.md" | xargs head -20 2>/dev/null
fi
```

### Step 5 — Market: What is happening right now?

Based on the domains found in steps 1–3, run 3–5 targeted web searches. Adapt
queries to the actual findings — examples:

- `"[dominant domain] market trends [current year]"`
- `"[stalled project topic] open source alternatives [current year]"`
- `"[stakeholder industry] AI automation opportunities"`
- `"[tech stack] new use cases [current year]"`
- `"solo developer SaaS opportunities [domain]"`

Use the `WebSearch` tool for each query. Extract: market gaps, emerging demand,
competitor moves, adjacent opportunities.

## Synthesis

After collecting all data, apply the following framework to generate ideas.

### Cross-reference matrix

| Signal | Source |
|---|---|
| Deep expertise | Wiki topics with many entries |
| Stalled potential | GitHub repos dormant > 90 days |
| Stakeholder demand | Recurring themes in company/stakeholder notes |
| Market pull | Web search trends |
| Low-hanging fruit | Open issues not yet started |

**An idea emerges when ≥ 2 signals align.**

### Idea scoring

Rate each idea on two axes:

**Effort** (to build an MVP):
- S = days (solo developer, existing stack)
- M = weeks (new module or integration)
- L = months (new product)

**Value** (expected return — revenue, learning, or strategic position):
- High = clear demand, fits existing stakeholders or portfolio
- Medium = speculative but directionally sound
- Low = interesting but weak pull

## Output Format

```markdown
# Ideas — YYYY-MM-DD
_Generated from: wiki ([N] pages), GitHub ([N] repos), [N] stakeholders, [N] web searches_

## Context Snapshot
**Active domains:** [list]
**Strongest wiki clusters:** [list]
**Active projects:** [list]
**Stakeholder industries:** [list]

---

## ⚡ Quick Wins
_Effort S · immediately actionable with the existing stack_

### 💡 [Idea Title]
**Effort:** S · **Value:** High
**Source:** [Wiki insight / GitHub gap / Stakeholder feedback / Market trend]
**Description:** 2–3 sentences on what and why.
**Next step:** One concrete first action (30 minutes or less).

[repeat for each quick win]

---

## 🚀 Strategic Initiatives
_Effort M/L · larger opportunities worth planning_

### 💡 [Idea Title]
**Effort:** M · **Value:** High
**Source:** [...]
**Description:** ...
**Next step:** ...

[repeat]

---

## 🔭 Market Observations
_What the market is doing — no immediate action required, but worth noting_

- **[Trend]**: [1–2 sentences on the observation and its relevance]

---

## 🗂️ Raw Signals
_Unprocessed hints from the sources — for later consideration_
- [signal]
```

## Save to Vault

```bash
OUTPUT_DIR="$VAULT/$IDEAS_DIR"
mkdir -p "$OUTPUT_DIR"
OUTPUT_FILE="$OUTPUT_DIR/$(date +%Y-%m-%d)-ideas.md"
```

Use the following frontmatter (this is a raw source file):
```yaml
---
kind: source
type: idea-session
title: "Ideas — YYYY-MM-DD"
domain: [list main domains covered]
status: raw
tags: [ideas, opportunity-mining]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

## Terminal Summary

```
✓ Ideas → Ideas/2026-05-08-ideas.md

📊 Sources: 47 wiki pages · 12 GitHub repos · 5 stakeholders · 4 web searches
⚡ 3 quick wins · 🚀 4 strategic initiatives · 🔭 5 market observations

Top idea: [Title] — [one-line description]
```

## Additional Resources

- **`references/idea-signals.md`** — Checklist of typical signals and how to interpret them
