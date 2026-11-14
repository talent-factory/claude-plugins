---
name: markdown-syntax-formatter
description: >
  Fixes and normalises Markdown: heading hierarchy, list and code block syntax, emphasis, and Swiss
  German orthography (no ß, proper umlauts) in German text. Respects the project's markdownlint
  configuration. Use when formatting or reviewing Markdown files, fixing heading levels, converting
  text with visual cues (ALL CAPS headings, bullet characters) into Markdown, or applying Swiss
  German orthography to a document.
allowed-tools:
  - Read
  - Edit
  - Write
  - Grep
  - Glob
---

# Markdown Syntax Formatter

Make a Markdown document correct and consistent without changing what it says.

## Rules

- **Headings:** ATX style (`#`), one top-level heading, no skipped levels, a blank line before and after. Visual cues (ALL CAPS lines, underlined titles) become headings of the right level.
- **Lists:** `-` for bullets, `1.` for ordered lists, nested lists indented consistently (2 or 4 spaces), blank lines around list blocks.
- **Code:** fenced blocks with a language identifier, matching fences, inline code for short references. Indented code blocks become fenced blocks.
- **Emphasis:** `**bold**` and `*italic*`; no underscores in file names or mixed contexts.
- **German text:** Swiss orthography: `ss` instead of `ß`, real umlauts instead of `ae`/`oe`/`ue`. Not in code blocks, URLs or quotations. Details and examples: [swiss-german-conventions.md](swiss-german-conventions.md). In mixed-language documents change only the German parts; if the language of a section is unclear, ask.
- **Linting:** read the project's `.markdownlint.json` or `.markdownlint-cli2.*` first. What the project allows is not "fixed". Legitimate exceptions, for example MD024 (duplicate headings) in training material and templates: [linter-exceptions.md](linter-exceptions.md).

## Steps

1. Read the file and the lint configuration.
2. Apply the rules; leave wording, links and front matter alone.
3. Report what changed in a few lines. For a large document with many issues, fix structure first (headings, code blocks), then lists and emphasis, and say so.
