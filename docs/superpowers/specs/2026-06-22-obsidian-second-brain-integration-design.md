# Obsidian Plugin — Second-Brain Integration (v1.4.0)

**Status:** Design approved, ready for implementation planning
**Date:** 2026-06-22
**Author:** Daniel Senften
**Source analysis:** `~/Obsidian/Private/85 Wissen/_wiki/compare/Obsidian-Second-Brain-Systeme.md`
**Reference project:** https://github.com/eugeniughelbur/obsidian-second-brain

## Summary

Extend the existing `obsidian` plugin (v1.3.1) with four capabilities adapted from the
`obsidian-second-brain` project, following an *extend, do not replace* strategy. The work
ships as a single coherent release, **obsidian v1.4.0**, comprising two new skills
(`wiki-think`, `wiki-maintain`), one shared validation module, and targeted upgrades to
three existing skills (`wiki-ingest`, `wiki-migrate-file`, `wiki-lint`).

The headline architectural decision is **maximum reuse via a shared validation module**:
`wiki-lint` already implements frontmatter, dead-link, asymmetric-reference, and
heuristic-contradiction checks. Rather than duplicating these across the new write paths,
the rules are extracted once into `_shared/` and referenced everywhere. This eliminates the
rule drift that caused the false positives fixed in v1.3.1.

## Context and Constraints

- The plugin is a **distributed marketplace plugin** — other users install it. This rules
  out anything that depends on the maintainer's private environment (a global hook firing on
  every user's writes, a self-started daemon/scheduler).
- The plugin has **no build step**; validation is structural/syntactic. Wiki skills are
  currently prose- and LLM-driven, with a few Python helper scripts (`tasks.py`,
  `update_daily_note.py`).
- All documentation must be **professional English**; remaining German text uses Swiss
  orthography (`ss` not `ß`, proper umlauts).

## Goals

1. **Write-Time-Validator** — proactive frontmatter/cross-reference validation before any
   plugin-driven wiki write.
2. **Contradiction-Reconcile** — `wiki-ingest` resolves conflicts between a new source and an
   existing page via propose-and-confirm, instead of silent append.
3. **Thinking-Tools** — a new `wiki-think` skill that argues with the user's notes.
4. **Scheduled-Maintenance** — a `wiki-maintain` skill bundling lint + auto-fix + report,
   runnable on-demand and schedulable by the user via a documented cron/launchd recipe.

## Non-Goals (YAGNI)

- Cross-CLI portability (Codex/OpenCode) — explicitly rejected in the source analysis.
- Live research integration (Perplexity/Gemini) — explicitly rejected in the source analysis.
- A global `PostToolUse` hook — intrusive for installers, hard to test.
- A real background daemon/scheduler — not portable in a distributed plugin.

## Design Decisions (resolved during brainstorming)

| Decision | Choice | Rationale |
|---|---|---|
| Validator mechanism | **In-skill validation** (pre-write gate) | No global side effects on third-party files; cleanly packageable; runs only on plugin writes. |
| Maintenance mechanism | **`wiki-maintain` skill + documented cron recipe** | Plugin stays portable; the user owns scheduling. |
| Reconcile behaviour | **Propose + confirm** (fallback: flag-only) | Protects curated knowledge from silent data loss. |
| Thinking modes | **challenge + connect + socratic**, optional wiki-page output | Covers full ideation range; output integrates into wiki linking. |
| Structuring approach | **Shared validation module** (Approach A) | No rule duplication → no drift; matches existing style; hybrid script/prose. |

## Architecture

### New artifacts

```
plugins/obsidian/skills/
├── _shared/
│   ├── validation-rules.md         # single source of truth for all checks
│   └── scripts/
│       └── validate.py             # deterministic checks (CLI, testable)
├── wiki-think/
│   ├── SKILL.md
│   └── references/
│       └── thinking-modes.md       # challenge / connect / socratic
└── wiki-maintain/
    ├── SKILL.md
    └── references/
        └── cron-recipes.md         # launchd/crontab examples
```

### Changed artifacts

- `wiki-ingest/SKILL.md` — pre-write validation gate (calls `validate.py`) + Contradiction-Reconcile (propose+confirm).
- `wiki-migrate-file/SKILL.md` — pre-write validation gate.
- `wiki-lint/SKILL.md` — refactored to cite `_shared/validation-rules.md` instead of inlining
  rules; delegates deterministic checks to `validate.py`.
- Vault templates: new `type: thinking` for `wiki-think` output.
- `README.md`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`,
  `docs/plugins/index.md`, `CHANGELOG.md` — version maintenance.

### Component responsibilities

| Component | Single responsibility | Dependencies |
|---|---|---|
| `validate.py` | Deterministic structural/link checks; returns JSON findings | stdlib + PyYAML |
| `validation-rules.md` | Defines *all* rules (deterministic + semantic) as a reference | — |
| `wiki-ingest` (changed) | Source → wiki, now with validation gate + reconcile | `_shared` |
| `wiki-migrate-file` (changed) | Legacy file → wiki schema, with validation gate | `_shared` |
| `wiki-lint` (changed) | Read-only health report over the whole wiki | `_shared` |
| `wiki-maintain` (new) | Non-interactive lint + auto-fix + report for cron | `_shared`, `wiki-lint` logic |
| `wiki-think` (new) | Argues with notes (3 modes), optional wiki page | reads `_wiki/`, optional `_shared` for output validation |

## Component Contracts

### `validate.py`

- **Invocation:** `validate.py <file-or-dir> [--rules <csv>] [--format json]`
- **Scope:** only inspects files under `_wiki/` and `_raw/`; ignores everything else.
- **Output:** JSON array of findings: `[{file, severity, rule, message, autofixable}]`
  where `severity ∈ {critical, minor}`.
- **Rules implemented (deterministic subset):** frontmatter completeness, `kind`/`type`
  consistency (incl. new `type: thinking`), dead wikilinks (resolving against `_wiki/`,
  `_raw/`, and media files, with the v1.3.1 normalisation rules — alias stripping,
  code-span skipping, log/report exemptions), asymmetric `related:` fields.
- **Dependencies:** Python stdlib + PyYAML only.

### `validation-rules.md`

The authoritative description of every check (deterministic and semantic). `validate.py`
implements the deterministic subset; the LLM-driven skills implement the semantic subset
(stale claims, contradiction detection, hub gaps, source gaps) by reading this file.

## Data Flow

### 1. Write-Time-Validator (in-skill gate)

```
wiki-ingest / wiki-migrate builds page content
        ↓
validate.py <file.md> --rules frontmatter,kindtype,deadlinks,asymmetric  → JSON
        ↓
   findings? ── no ──► write
        │ yes
        ▼
   critical (missing required fields, wrong kind/type) ► auto-correct where trivial,
   otherwise show user + confirm  ► then write
   minor ► report only, do not block
```

Pre-write, `validate.py` inspects only the touched file(s) for speed. `critical` findings
block the write until fixed or confirmed; `minor` findings are reported.

### 2. Contradiction-Reconcile (wiki-ingest, step 4)

```
target page exists + new source contradicts an existing claim?
        ↓
skill contrasts:   OLD: "<claim>" (sources: …)
                   NEW: "<claim>" (source: <new source>)
        ↓
skill proposes a resolved wording (+ supersede/timeline note if relevant)
        ↓
   user confirms ─► revise page, log: "reconcile | old→new"
   user rejects  ─► set contradiction callout only (fallback = flag-only)
```

Detection is an LLM judgement performed when updating an existing page (not a script). This
replaces the prior edge-case rule of merely flagging the conflict in the lint report. No
silent overwrite ever occurs.

### 3. wiki-maintain (Scheduled-Maintenance)

```
/wiki:maintain [--auto-fix] [--quiet]
        ↓
validate.py over the whole _wiki/ + _raw/   → all deterministic findings
        ↓
LLM checks (stale claims, contradictions, hub gaps)  ← from validation-rules.md
        ↓
--auto-fix: apply trivial fixes (asymmetric related, missing created/domain)
        ↓
write report: _wiki/maintain-report-YYYY-MM-DD.md  + log entry
        ↓
--quiet (for cron): exit code + one stdout line, no interactive prompts
```

Difference from `wiki-lint`: lint is read-only and interactive; maintain is
**non-interactive + auto-fix**, built for the cron run. `cron-recipes.md` provides a launchd
`.plist` and a crontab example (weekly) invoking
`claude -p "/wiki:maintain --auto-fix --quiet"`. Destructive reconciles never run in
`--quiet` mode — they require confirmation and therefore only happen interactively.

### 4. wiki-think (Thinking-Tools)

```
/wiki:think <topic|page> [--mode challenge|connect|socratic] [--save]
        ↓
load relevant _wiki/ pages (index-first, like wiki-query)
        ↓
mode logic from thinking-modes.md:
   challenge → assumptions / counter-examples / blind spots
   connect   → non-obvious cross-refs + hub suggestions
   socratic  → probing questions instead of answers
        ↓
terminal output  ── --save ──►  _wiki/thinking/<slug>.md  (kind: wiki, type: thinking)
                                 → validated via validate.py (reuses gate #1)
```

Default mode (no `--mode`): `challenge`. Modes are combinable (`--mode challenge,connect`).
`--save` pages set `sources:` to the referenced pages so they integrate into wiki linking.

## Error Handling and Degradation

- **`validate.py` not executable / PyYAML missing:** skills fall back to the prose check in
  `validation-rules.md`, with a warning in the output. No hard fail — the plugin remains
  usable without Python.
- **`validate.py` reports errors in content to be written:** the write does **not** proceed
  until critical findings are fixed or confirmed. Under `--quiet` (maintain/cron),
  non-autofixable critical findings produce a non-zero exit code plus the report; no
  half-finished corrections are written.
- **No configured vault / missing `wiki-root`:** all skills abort early with a clear message
  (existing pattern).
- **`markdown-syntax-formatter` agent (education) not installed:** skip (existing pattern,
  retained).

## Edge Cases

- **Contradiction, user unsure:** a third option beside confirm/reject — "flag only"
  (contradiction callout) — so nothing is lost.
- **`type: thinking` vs. lint:** `validate.py` and `validation-rules.md` must add `thinking`
  to the allowed `kind: wiki` type list, otherwise lint flags every saved think page.
  (Cross-cutting change, explicitly planned.)
- **`wiki-think --save` without real sources:** `sources:` may be empty for `type: thinking`
  (it is derived reasoning, not a factual assertion); `validate.py` exempts `thinking` from
  the "empty sources + factual claim" rule.
- **maintain runs alongside manual editing:** maintain writes only its own report plus
  trivial fixes with a git-inspectable diff; no destructive reconciles in `--quiet` mode.
- **`validate.py` on a non-wiki file:** only files under `_wiki/`/`_raw/` are checked; all
  else is ignored (no global side effect).

## Testing Strategy

The repository has no build step; validation is structural.

- **`validate.py`:** a standalone `pytest` suite with a fixture vault (valid + intentionally
  broken `.md` files), covering every rule with a positive and a negative case. Runs locally;
  optionally a CI job.
- **Skill structure:** `/core:check-commands` + `/core:check-agents` must pass (mandatory
  before PR per CLAUDE.md).
- **Manual smoke tests:** `claude --plugin-dir ./plugins/obsidian`, then one run per new
  skill against a test vault; validator gate against an intentionally broken page.
- **Regression:** compare `wiki-lint` output against a known vault before/after the refactor
  — identical findings (now deterministically consistent).

## Versioning and Documentation (v1.4.0)

Per the CLAUDE.md "Update Plugin Version" checklist:

- `plugins/obsidian/.claude-plugin/plugin.json` → `1.4.0`
- `.claude-plugin/marketplace.json` → obsidian entry to `1.4.0`
- `plugins/obsidian/README.md` → header, skill list (now 11 skills), changelog section, new
  trigger phrases, note on `_shared/validate.py` + PyYAML dependency, cron-setup reference
- `docs/plugins/index.md` → version line
- `CHANGELOG.md` → v1.4.0 entry
- `cron-recipes.md` → launchd `.plist` + crontab example for weekly
  `/wiki:maintain --auto-fix --quiet`

## Implementation Phases (dependency-ordered)

1. **Foundation:** `_shared/validation-rules.md` + `validate.py` + pytest suite (includes the
   `type: thinking` rules; basis for everything).
2. **Refactor:** move `wiki-lint` onto `_shared`; regression against a known vault.
3. **Write gate:** wire pre-write validation into `wiki-ingest` + `wiki-migrate-file`.
4. **Reconcile:** add contradiction propose+confirm to `wiki-ingest`.
5. **New skills:** `wiki-maintain` (+ cron-recipes), then `wiki-think` (+ thinking-modes).
6. **Release:** version/doc maintenance, `/core:check-*`, smoke tests, branch
   `feature/obsidian-second-brain-integration`.
