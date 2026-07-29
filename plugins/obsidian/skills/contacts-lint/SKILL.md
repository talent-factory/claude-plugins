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

Exit code 2 means PyYAML is missing; fall back to the prose rules in
`${CLAUDE_PLUGIN_ROOT}/skills/_shared/contact-rules.md`.

## Semantic checks

Beyond the deterministic findings, read the prose of company pages and check:

- A person named in the NOTIZEN text of a company page that is not linked from
  any person's `company:` field.
- A person's `role:` contradicting what the company page states about them.

Report these under **Semantic Findings**; never auto-fix them.

## Auto-fix

Only with explicit user confirmation, and only for findings marked
`autofixable`. Show a diff first. Never guess a company for an ambiguous slug —
report it instead.

## Report

Write to `docs/contacts/contacts-lint-YYYY-MM-DD.md` in the vault:

```markdown
# Contacts Lint Report YYYY-MM-DD

Persons checked: N | Companies checked: M
Issues: X (Y critical, Z minor)

## Critical Issues

## Minor Issues

## Semantic Findings

## Auto-Fix Suggestions
```

Run the `markdown-syntax-formatter` agent on the report. Skip if the education
plugin is not installed.
