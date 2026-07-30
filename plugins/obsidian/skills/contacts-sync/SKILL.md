---
name: contacts-sync
description: Derives contact graph edges from an Obsidian vault's daily notes. Converts plain-text person mentions into wikilinks, proposes topic edges into the wiki, and proposes missing company edges. All changes are presented as a confirmable diff. Triggers when the user runs /contacts:sync or asks to sync contacts from daily notes.
---

# contacts-sync

## When to invoke

The user runs `/contacts:sync` or asks to derive contact edges from the dailies.

## Determine the window

Read the last `contacts-sync` entry from `docs/contacts/log.md` in the vault and
use its date as `--since`. If the log has no entry, ask the user for a start
date rather than scanning all 886 dailies at once.

## Gather mentions

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/contacts.py" \
  --vault-root "<vault-root>" --mentions --since YYYY-MM-DD
```

## Derive edges

The link graph cannot supply topic edges: of 284 wiki pages only 11 are ever
linked from a daily, and the co-occurrence of `[[Person]]` and `[[Wiki-Page]]`
in the same daily is zero. Derive them semantically instead.

For each mention, read its `context` and propose:

1. **Linkify** — `linked: false` means the name appears as plain text. Propose
   replacing it with `[[Name]]`.
2. **Topic edge** — match the context against the titles, tags and aliases of
   pages under `85 Wissen/_wiki`. Propose adding the page to the person's
   `topics:`. Only propose a match you can justify from the context; a vague
   thematic association is not enough.
3. **Company edge** — if the context names a company that has a page in
   `35 Companies` and the person has no `company:` entry, propose it.

## Confirm before writing

Present every proposal as a diff grouped by person. Write nothing without
explicit confirmation. A rejected proposal is not re-proposed in the same run.

## Log

Append to `docs/contacts/log.md`:

```text
## [YYYY-MM-DD HH:MM] contacts-sync | since YYYY-MM-DD
- mentions scanned: N
- linkified: A | topic edges: B | company edges: C
- rejected: D
```
