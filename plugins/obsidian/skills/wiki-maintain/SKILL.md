---
name: wiki-maintain
description: Runs non-interactive maintenance on an Obsidian-based LLM knowledge wiki — deterministic validation, semantic health checks, trivial auto-fixes, and a written report. Built to be scheduled (cron/launchd). Triggers when the user runs /wiki:maintain, asks to "run wiki maintenance", or "auto-fix the wiki".
---

# wiki-maintain

## When to invoke

The user runs `/wiki:maintain [--auto-fix] [--quiet]`, asks to run wiki
maintenance, or schedules it (see `references/cron-recipes.md`). Unlike
`wiki-lint` (read-only, interactive), this skill applies trivial fixes and is
safe to run unattended.

## Configuration

Same vault layout as `wiki-ingest`/`wiki-lint`. Rules live in
`${CLAUDE_PLUGIN_ROOT}/skills/_shared/validation-rules.md`.

## Flags

- `--auto-fix` — apply trivial, reversible fixes (asymmetric back-references,
  missing `created` from git, missing `domain` from the vault). Default off.
- `--quiet` — non-interactive: no prompts, one stdout line, machine-readable exit
  code. Required for cron. Implies that destructive operations are skipped.

## Workflow

1. **Deterministic pass.** Run the shared validator over the whole wiki:

    ```bash
    python3 "${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/validate.py" \
      --vault-root "<wiki-root>" --rules frontmatter,kindtype,deadlinks,asymmetric
    ```

    On validator exit code 2 (PyYAML missing), fall back to the deterministic
    rules in the shared reference and continue.

2. **Semantic pass.** Apply semantic rules 5–8 from the shared reference (stale
   claims, contradiction detection, hub gaps, source gaps — `type: thinking`
   exempt from source gaps).

3. **Auto-fix (only with `--auto-fix`).** Apply trivial fixes for findings whose
   `autofixable` is true. In interactive mode, show a diff per fix and confirm; in
   `--quiet` mode, apply auto-fixable findings directly and record them. Never
   perform destructive contradiction reconciles in `--quiet` mode — those require
   confirmation and only happen interactively in `wiki-ingest`.

4. **Write the report** to `<wiki-root>/_wiki/maintain-report-YYYY-MM-DD.md` with
   frontmatter `kind: wiki, type: note`, summarizing files checked, findings by
   severity, and fixes applied.

5. **Append a log entry** to `<wiki-root>/_wiki/log.md`:

    ```text
    ## [YYYY-MM-DD HH:MM] maintain | <report-name>
    - findings: M (X critical, Y minor)
    - auto-fixes applied: K
    ```

6. **Output.**
   - Interactive: the report path, finding counts, and fixes applied.
   - `--quiet`: a single stdout line `maintain: M findings (X critical), K fixes`
     and a non-zero process exit when unresolved critical findings remain.

## Edge Cases

- **Runs alongside manual editing:** only writes its own report plus auto-fixable
  changes with a git-inspectable diff. No interactive reconciles in `--quiet` mode.
- **No vault configured:** abort early with a clear message.
