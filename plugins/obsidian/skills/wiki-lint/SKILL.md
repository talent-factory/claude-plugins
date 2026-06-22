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

### Deterministic Checks (shared validator)

Run the shared validator over the whole wiki and parse its JSON findings:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/validate.py" \
  --vault-root "<wiki-root>" --rules frontmatter,kindtype,deadlinks,asymmetric
```

If the validator exits with code 2 (PyYAML missing), fall back to applying the
deterministic rules manually from `${CLAUDE_PLUGIN_ROOT}/skills/_shared/validation-rules.md`.

Map findings into the report: `critical` findings go under **Critical Issues**
(Structural for `frontmatter`/`kindtype`, Linking for `deadlinks`/`asymmetric`);
`minor` findings go under **Minor Issues**. All rule definitions live in
`_shared/validation-rules.md` — do not restate them here.

(Note: if `${CLAUDE_PLUGIN_ROOT}` is unavailable in the runtime, resolve the path relative to this skill: `../_shared/scripts/validate.py`.)

### Semantic Checks (LLM judgement)

Apply semantic rules 5–8 and template-compliance from
`${CLAUDE_PLUGIN_ROOT}/skills/_shared/validation-rules.md` (stale claims,
contradiction detection, hub gaps, source gaps — `type: thinking` exempt from
source gaps). Keep the Tag Discipline checks (singleton tags, status-as-tag) and
the Migration Backlog soft-cap check as they are today.

### Tag Discipline

9. **Singleton tags:** tags that occur in only one file (aggregated across all frontmatter).
10. **Status-as-tag:** tags such as `#draft`, `#tbd`, `#wip` (these belong in the `status:` field).

### Migration Backlog

11. **Soft cap check:** count `.md` files in `<wiki-root>/` that live outside `_raw/` and `_wiki/` (templates are inside `_wiki/templates/` and therefore already excluded). If the count exceeds the soft cap (default 50): emit a WARNING.

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

Run the `markdown-syntax-formatter` agent (from the education plugin) on the report. If the education plugin is not installed, skip this step.
