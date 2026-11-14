---
name: ideas
description: >
  Surfaces new product, feature, and business ideas by cross-referencing the user's
  knowledge wiki, GitHub repositories, customer or project notes, and current market
  trends. Writes a structured ideas document to the Obsidian vault. Activate when the
  user runs "/obsidian:ideas", asks "what could I build next", "give me new project ideas",
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

## Sources

Gather these in parallel; each one degrades gracefully when it is not available.

1. **Wiki:** `<wiki-root>/_wiki/index.md`, the last 80 lines of `log.md` and the most recently modified pages. Extract active domains, recurring themes, technologies being tracked. Skip if the wiki root does not exist.
2. **GitHub** (needs `GITHUB_ORG`): non-archived repositories with description and `pushedAt` (`gh repo list`), repositories without a push for 90 days (stalled), and your open issues. Extract active projects, dormant repositories with potential, gaps visible in open issues.
3. **Stakeholders:** the first 30 lines of every note in `obsidian_companies_dir`. Extract industries, recurring pain points, requests that repeat across stakeholders. Skip if the folder is not configured or missing.
4. **Personal context:** the last seven daily notes that mention ideas, opportunities or TODOs, and the notes in `obsidian_context_dir` if configured.
5. **Market:** three to five targeted `WebSearch` queries derived from the domains found in 1 to 3 (market trends, open source alternatives to stalled projects, AI automation in the stakeholders' industries, new uses of the tech stack).

## Synthesis

| Signal | Source |
|---|---|
| Deep expertise | Wiki topics with many entries |
| Stalled potential | GitHub repositories dormant for more than 90 days |
| Stakeholder demand | Recurring themes in stakeholder notes |
| Market pull | Web search trends |
| Low-hanging fruit | Open issues not yet started |

**An idea emerges when at least two signals align.** Typical signals and how to read them: [references/idea-signals.md](references/idea-signals.md).

Score each idea. **Effort** (MVP): S = days with the existing stack, M = weeks (new module or integration), L = months (new product). **Value:** High = clear demand that fits stakeholders or portfolio, Medium = speculative but sound, Low = interesting, weak pull.

## Output

Write `<ideas-dir>/YYYY-MM-DD-ideas.md` (`obsidian_ideas_dir`, default `Ideas`; create the folder) with this frontmatter, since the note is a raw source for the wiki:

```yaml
---
kind: source
type: idea-session
title: "Ideas — YYYY-MM-DD"
domain: [main domains covered]
status: raw
tags: [ideas, opportunity-mining]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

Body, in this order:

1. **Context snapshot:** active domains, strongest wiki clusters, active projects, stakeholder industries, and how many pages, repositories, stakeholders and searches were used.
2. **⚡ Quick wins** (effort S): per idea a title, effort and value, source of the signal, two or three sentences on what and why, and one concrete next step of 30 minutes or less.
3. **🚀 Strategic initiatives** (effort M or L): same fields.
4. **🔭 Market observations:** trend plus one or two sentences on its relevance. No action needed.
5. **🗂️ Raw signals:** unprocessed hints for later.

## Terminal summary

```
✓ Ideas → Ideas/2026-05-08-ideas.md
📊 Sources: 47 wiki pages · 12 GitHub repos · 5 stakeholders · 4 web searches
⚡ 3 quick wins · 🚀 4 strategic initiatives · 🔭 5 market observations
Top idea: [Title] — [one-line description]
```
