# Swiss German Orthography Conventions

This reference defines the Swiss High German (Schweizer Hochdeutsch) writing conventions
applied when formatting German-language Markdown documents.

## Core Rule: Replace ß with ss

Swiss German orthography does not use the Eszett character (ß). All instances of ß in
German text are replaced with "ss".

### Examples

| Incorrect (Eszett)  | Correct (Swiss) |
|---------------------|-----------------|
| muß                 | muss            |
| groß                | gross           |
| Straße              | Strasse         |
| heißt               | heisst          |
| außerdem            | ausserdem       |
| Fußnote             | Fussnote        |
| schließen           | schliessen      |
| übermäßig           | übermässig      |

## Umlaut Rule: Use Proper Umlaut Characters

Always use actual umlaut characters. Never substitute with digraphs (ae, oe, ue).

### Examples

| Incorrect (Digraph)  | Correct (Umlaut)  |
|----------------------|-------------------|
| ae                   | ä                 |
| oe                   | ö                 |
| ue                   | ü                 |
| Ae                   | Ä                 |
| Oe                   | Ö                 |
| Ue                   | Ü                 |

**Note:** The digraph "ue" can appear legitimately in compound words where "u" and "e"
belong to different morphemes (e.g., "abenteuerlich"). Apply umlaut conversion only when
the digraph represents a single umlaut vowel.

## Scope of Application

### Apply Conventions To

- Headings and subheadings
- Body text and paragraphs
- List items
- Table cell content
- Blockquote text
- Image alt text and link text
- Markdown comments

### Do Not Apply To

- **Code blocks** (fenced and indented) -- leave unchanged
- **Inline code** -- leave unchanged
- **URLs and file paths** -- leave unchanged
- **Technical identifiers** (variable names, class names, API endpoints) -- leave unchanged
- **External quotations** -- leave unchanged, but add a note if the source uses Eszett
- **Proper nouns and brand names** -- preserve original spelling

## Automatic Conversion Behavior

When creating or editing German-language Markdown files:

1. Scan all non-code text for Eszett characters (ß)
2. Replace each ß with "ss"
3. Scan for umlaut digraphs in non-code text
4. Replace digraphs with proper umlaut characters where appropriate
5. Preserve all code blocks, inline code, URLs, and technical identifiers unchanged

## Detection Heuristics

To determine whether a document is German-language:

- Check for German-specific words (der, die, das, und, ist, mit, von, für, etc.)
- Check for umlaut characters or Eszett
- Check file path or metadata for language indicators
- When uncertain, ask the user about the document language
