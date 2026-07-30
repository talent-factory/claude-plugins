---
name: contacts-lint
description: Runs a structural health check on the contact and company graph of an Obsidian vault. Detects frontmatter issues, plain-text company slugs, dead company and topic wikilinks, hardcoded Dataview slugs, orphan company pages, and duplicate persons. Produces a structured report. Triggers when the user runs /contacts:lint, asks for a "contacts health check", or asks to lint contacts and companies.
---

# contacts-lint

## When to invoke

The user runs `/contacts:lint` or asks for a health check of contacts and
companies.

## Configuration

Vault root defaults to the current working directory. Folders are fixed:
`30 Persons`, `35 Companies`, `85 Wissen/_wiki`.

## Run deterministic checks

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/contacts.py" \
  --vault-root "<vault-root>" \
  --rules frontmatter,slug-drift,deadlinks,query-drift,orphan-company,dupes
```

Exit code 1 means at least one `critical` finding. Exit code 2 means the run
never happened — read the `error` field to tell the cases apart:

| `error` contains       | Meaning                                                                                                                 |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `PyYAML not installed` | Fall back to the prose rules in `${CLAUDE_PLUGIN_ROOT}/skills/_shared/contact-rules.md`.                                  |
| `vault-root fehlt`     | The path is not a vault. Ask the user for the right one; do not report a clean result.                                    |
| `unbekannte Regel(n)`  | A rule name is misspelled. The valid names come back in `gueltige_regeln`.                                                |

An exit code 2 is never a clean bill of health. Report it as a failed run.

## Semantic checks

Beyond the deterministic findings, read the prose of company pages and check:

- A person named in the NOTIZEN text of a company page that is not linked from
  any person's `company:` field.
- A person's `role:` contradicting what the company page states about them.

Report these under **Semantic Findings**; never auto-fix them.

## Fixing findings

**`contacts.py` is the only thing that writes to `30 Persons` and
`35 Companies`. Never hand-edit frontmatter yourself — not one key, not one
line, not even a value you are certain about.** The script edits surgically:
it replaces only the touched keys in the original text and leaves every other
line byte-identical. An assistant rewriting YAML instead re-renders it, and
that measurably destroys data in this vault — list indentation changes, `"5.7"`
becomes a float, `off` becomes `False`, wikilinks lose their quotes, long
values reflow at column 80, and block scalars collapse. Measured across the
1260 real person pages, a parse-and-redump rewrites 600 files it was never
asked to touch.

There is no `--fix` flag, and `autofixable: true` does not mean the script
will act on the finding. It is a triage signal for the human: *this finding
has exactly one unambiguous resolution*, as opposed to one that needs a
decision. Treat it as "safe to decide", not "already decided".

The single write path is the reviewed alias map:

```bash
# 1. Propose. Writes nothing; prints YAML to stdout.
python3 "${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/contacts.py" \
  --vault-root "<vault-root>" --propose-aliases > alias-map.yaml

# 2. The user reviews every entry. `target:` names a company page;
#    `target: null` means "deliberately unresolved" and preserves the old
#    value in the person's `company_legacy`. A `CHOOSE:` marker left
#    unresolved is rejected rather than guessed at.

# 3. Dry run. Prints the full manifest of what would change.
python3 "${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/contacts.py" \
  --vault-root "<vault-root>" --migrate --alias-map alias-map.yaml

# 4. Apply, only after the user confirms the dry-run manifest.
python3 "${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/contacts.py" \
  --vault-root "<vault-root>" --migrate --alias-map alias-map.yaml --apply
```

The reviewed map for this vault lives at `docs/contacts/alias-map.yaml`. Reuse
it rather than regenerating decisions the user has already made.

Findings the migration cannot resolve — `deadlinks`, `orphan-company`,
`dupes`, the Bases-syntax half of `query-drift`, and any `slug-drift` value
that carries a wikilink without being one — are reported for the user to act
on. Present them; do not act on them. Never guess a company for an ambiguous slug —
report it instead.

## Blind spots to state in the report

Three things lint cannot see. Say so, rather than letting a low finding count
imply they were checked:

- **`frontmatter` covers `30 Persons` only.** No rule validates a company
  page's frontmatter.
- **Two company pages are invisible to every rule.** `BiCT AG` and
  `SYTRAX Intelligence AG` were refused during migration for ambiguous
  frontmatter delimiters, and they appear in no finding of any rule — not
  even `orphan-company`.
- **`company_legacy` is a backlog, not a finding.** No rule reports it (103
  person pages carried it on 2026-07-30 — count it, do not quote that
  number). It holds the pre-migration `company:` value for a slug that
  resolved to no company page, and it is the work to do when those pages get
  created. See the `company_legacy` section of
  `${CLAUDE_PLUGIN_ROOT}/skills/_shared/contact-rules.md`.

## Report

Present the findings in the conversation first. **Write a report file only
after the user confirms they want one on disk** — a file in `docs/contacts/`
is a change to the user's vault like any other. Create the directory if it
does not exist; it is not part of a stock vault.

On confirmation, write `docs/contacts/contacts-lint-YYYY-MM-DD.md`:

```markdown
# Contacts Lint Report YYYY-MM-DD

Persons checked: N | Companies checked: M
Issues: X (Y critical, Z minor)

## Critical Issues

## Minor Issues

## Semantic Findings

## Blind Spots

## Open Decisions
```

`Open Decisions` lists findings that need the user to choose (an unresolved
slug, a duplicate to merge). It does not list changes the assistant may make
on its own — there are none.

Run the `markdown-syntax-formatter` agent on the report. Skip if the education
plugin is not installed.
