---
name: contacts-sync
description: Derives contact graph edges from an Obsidian vault's daily notes. Converts plain-text person mentions into wikilinks, proposes topic edges into the wiki, and proposes missing company edges. All changes are presented as a confirmable diff. Triggers when the user runs /contacts:sync or asks to sync contacts from daily notes.
---

# contacts-sync

## When to invoke

The user runs `/contacts:sync` or asks to derive contact edges from the dailies.

## Determine the window

Read the last `contacts-sync` entry from `docs/contacts/log.md` in the vault and
use its date as `--since`. If the log is missing or has no entry, ask the user
for a start date rather than scanning every daily note in the vault at once.

`--since` must be a `YYYY-MM-DD` date. Anything else exits 2 — it used to sort
above every daily's filename and silently skip all of them.

## Gather mentions

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/contacts.py" \
  --vault-root "<vault-root>" --mentions --since YYYY-MM-DD
```

## Derive edges

The link graph cannot supply topic edges: only a small fraction of the wiki
pages is ever linked from a daily, and the co-occurrence of `[[Person]]` and
`[[Wiki-Page]]` in the same daily note is essentially nil. Derive them
semantically instead.

For each mention, read its `context` and propose:

1. **Linkify** — `linked: false` means the name appears as plain text that is
   not already inside a link. Propose replacing it with `[[Name]]`.

   `linked: true` covers a `[[Wikilink]]`, an alias link `[[Page|Name]]`, and
   a markdown link `[Name](url)`; frontmatter is not scanned at all. Never
   propose a linkify for those — wrapping a name that is already inside a link
   produces `[[[Name]](url)` or a broken target, and rewriting a frontmatter
   value treats a machine-read field as prose.
2. **Topic edge** — match the context against the titles, tags and aliases of
   pages under `85 Wissen/_wiki`. Propose adding the page to the person's
   `topics:`. Only propose a match you can justify from the context; a vague
   thematic association is not enough.
3. **Company edge** — if the context names a company that has a page in
   `35 Companies` and the person has no `company:` entry, propose it.

## Confirm before writing

Present every proposal as a diff grouped by person. Write nothing without
explicit confirmation. A rejected proposal is not re-proposed in the same run.

Frontmatter changes (`topics:`, `company:`) go through
`contacts.py --migrate --alias-map <file> --apply`, never through a hand-edit
of the YAML. See the "Fixing findings" section of the `contacts-lint` skill.

## Log

Append to `docs/contacts/log.md` — but only after the user has confirmed the
run, and only recording what was actually written. Create `docs/contacts/`
first if it does not exist; it is not part of a stock vault. If the user
rejected everything, there is nothing to log.

```text
## [YYYY-MM-DD HH:MM] contacts-sync | since YYYY-MM-DD
- mentions scanned: N
- linkified: A | topic edges: B | company edges: C
- rejected: D
```
