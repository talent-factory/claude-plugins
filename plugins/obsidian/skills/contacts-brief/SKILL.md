---
name: contacts-brief
description: Assembles a briefing dossier about a contact from an Obsidian vault — person page, company page, topic edges, and every daily-note mention. Read-only. Triggers when the user runs /contacts:brief, asks "what do I know about <person>", or asks for a briefing before a meeting.
---

# contacts-brief

## When to invoke

The user runs `/contacts:brief <Name>` or asks what they know about a person.

## Gather

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/contacts.py" \
  --vault-root "<vault-root>" --dossier "<Name>"
```

Exit code 2 with an `error` key means the person was not found. Offer the three
closest matching filenames from `30 Persons` rather than guessing.

## Synthesise

Write the briefing directly to the chat. Never write a file — this skill is
read-only.

Structure:

1. **Wer** — Rolle, Firma, Kontaktdaten aus dem Frontmatter.
2. **Firma** — was auf der Firmenseite steht, verdichtet auf zwei bis drei Sätze.
3. **Verlauf** — die Daily-Erwähnungen chronologisch, jeweils eine Zeile mit
   Datum und Kern.
4. **Themen** — die `topics:`-Kanten, jeweils mit einem Satz, warum sie dranhängen.
5. **Was fehlt** — leere Felder, die vor einem Gespräch stören würden (keine
   E-Mail, keine Erwähnung seit über einem Jahr, kein Thema verknüpft).

Abschnitt 5 ist der Punkt der Übung. Ein Dossier, das nur wiedergibt, was
dasteht, hilft nicht — es soll zeigen, was du nicht weisst.
