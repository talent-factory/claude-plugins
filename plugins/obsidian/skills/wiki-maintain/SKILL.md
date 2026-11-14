---
name: wiki-maintain
description: Runs the wiki-lint checks without prompts, applies trivial fixes and writes a report, so it can be scheduled (cron or launchd). Use when the user runs /obsidian:wiki-maintain, asks to "run wiki maintenance" or "auto-fix the wiki", or when the job is unattended.
---

# wiki-maintain

The unattended variant of `wiki-lint`. The checks, the report layout and the fix rules are those of `wiki-lint`; read that skill and run it with the differences below. Scheduling: `references/cron-recipes.md`.

## Flags

- `--auto-fix`: apply the trivial, reversible fixes of `wiki-lint` (asymmetric back-references, missing `created` from git, missing `domain`). Default off.
- `--quiet`: no prompts, one stdout line, a machine-readable exit code. Required for cron. Destructive operations are skipped.

## Differences from `wiki-lint`

1. **No confirmation.** With `--auto-fix`, auto-fixable findings are applied directly and listed in the report. Interactively (without `--quiet`) show a diff per fix and confirm.
2. **Never reconcile contradictions.** Destructive reconciles need a person and only happen interactively in `wiki-ingest`.
3. **Report file** `<wiki-root>/_wiki/maintain-report-YYYY-MM-DD.md` with frontmatter `kind: wiki, type: note`: files checked, findings by severity, fixes applied.
4. **Log entry** in `<wiki-root>/_wiki/log.md`:

   ```text
   ## [YYYY-MM-DD HH:MM] maintain | <report-name>
   - findings: M (X critical, Y minor)
   - auto-fixes applied: K
   ```

5. **Output.** Interactive: the report path, counts, fixes. `--quiet`: one line `maintain: M findings (X critical), K fixes`, and a non-zero exit code while unresolved critical findings remain.

If no vault is configured, stop with a clear message. The run may overlap with manual editing, so it only touches its own report and auto-fixable files, each change visible in `git diff`.
