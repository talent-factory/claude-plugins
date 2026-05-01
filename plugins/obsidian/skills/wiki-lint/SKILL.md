---
name: wiki-lint
description: Runs a structural and content health check on an Obsidian-based LLM knowledge wiki. Detects frontmatter issues, broken or asymmetric cross-references, contradictions, stale claims, tag discipline violations, migration backlog overflow, missing hub pages, and orphan content. Produces a structured lint report. Triggers when the user runs /wiki:lint, asks for a "wiki health check", or asks to lint the knowledge wiki.
---

# wiki-lint

## When to invoke

The user runs `/wiki:lint` (typically weekly) or asks for a wiki health check.

## Configuration

Same vault layout as `wiki-ingest`. The migration backlog soft cap (default: 50 files) is configurable via the vault's `CLAUDE.md` as `wiki_migration_cap: <n>`.

## Workflow

Read all files in `<wiki-root>/_wiki/` and `<wiki-root>/_raw/`. Run the following checks and collect issues.

### Structural Checks

1. **Frontmatter completeness:** `kind`, `type`, `title`, `domain`, `status`, `tags`, `created`, `updated` for all files. Source-specific: `source_url`, `ingested`, `distilled_into`. Wiki-specific: `sources`, `related`, `last_synthesized`.
2. **`kind`/`type` consistency:** `kind: wiki` may only have `type: concept|tool|compare|hub`. `kind: source` may only have `type: clipping|chat|note|transcript`.
3. **Template compliance:** `wiki-tool` must have a `## Setup` heading, `wiki-compare` must have an `## Options` table, `wiki-hub` must have all five sections.

### Linking Checks

4. **Orphans:** wiki pages that no other wiki page links to (and that are not present in `index.md`).
5. **Dead links:** wikilinks `[[X]]` whose target file does not exist.
6. **Asymmetric `related:` fields:** if `A.related` contains `B`, then `B.related` must contain `A`.

### Content Checks

7. **Stale claims:** wiki pages with `updated:` older than six months AND new sources added since (i.e., `sources:` count exceeds the value at `last_synthesized`).
8. **Contradiction detection (heuristic):** pages that share an entity in `related:` but make conflicting claims → flag for review.

### Tag Discipline

9. **Singleton tags:** tags that occur in only one file (aggregated across all frontmatter).
10. **Status-as-tag:** tags such as `#draft`, `#tbd`, `#wip` (these belong in the `status:` field).

### Migration Backlog

11. **Soft cap check:** count `.md` files in `<wiki-root>/` that live outside `_raw/` and `_wiki/` (templates are inside `_wiki/templates/` and therefore already excluded). If the count exceeds the soft cap (default 50): emit a WARNING.

### Hub Suggestions

12. **Hub gaps:** if 5+ pages share an overlapping tag/theme without a `kind: wiki, type: hub` page → suggest one.

### Source Gaps

13. **`sources:` backref:** wiki pages with an empty `sources:` field but content that asserts factual claims → flag.

## Auto-Fix Mode

Trivial fixes with diff preview for user confirmation:

- Derive missing `created:` from git log: `git log --diff-filter=A --follow --format=%aI -1 -- <file>`.
- Synchronize asymmetric `related:` fields bidirectionally.
- Add `domain: <vault-domain>` if the field is missing.

Everything else: report only, do not fix.

## Output

Write `<wiki-root>/_wiki/lint-report-YYYY-MM-DD.md` with frontmatter `kind: wiki, type: note` and the following structure:

```markdown
# Lint Report YYYY-MM-DD

## Summary

- Files checked: N
- Issues: M (X critical, Y minor)
- Migration Backlog: Z files (cap: 50, status: OK / OVER by N)

## Critical Issues

### Structural
- ...

### Linking
- ...

## Minor Issues

- ...

## Auto-Fix Suggestions

(diff block per suggestion; user confirms)

## Hub Suggestions

- Cluster `<theme>`: 7 pages without hub. Recommended: `_wiki/concepts/<theme>.md` as type: hub.
```

Append a log entry:

```text
## [YYYY-MM-DD HH:MM] lint | <report-name>
- issues: M (X critical, Y minor)
- migration backlog: Z files (cap: 50)
```

Run the `markdown-syntax-formatter` agent on the report.
