---
name: markdown-syntax-formatter
description: >
  Converts text with visual formatting into proper Markdown syntax, fixes Markdown
  formatting issues, and ensures consistent document structure. Use this skill when
  formatting or reviewing Markdown files, fixing heading hierarchies, converting
  visual cues to proper syntax, applying Swiss German orthography to German-language
  documents, or checking Markdown against linting rules.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Markdown Syntax Formatter

Format and repair Markdown documents following CommonMark and GitHub Flavored Markdown
specifications. Ensure proper syntax, consistent structure, and correct rendering across
standard parsers.

## Capabilities

- Analyze document structure to identify intended hierarchy and formatting elements
- Convert visual formatting cues (ALL CAPS, bullet characters, emphasis indicators) into
  proper Markdown syntax
- Fix heading hierarchies ensuring logical progression without skipped levels
- Format lists with consistent markers and proper indentation
- Handle code blocks and inline code with appropriate language identifiers
- Apply Swiss German orthography rules to German-language content
- Respect context-specific linter exceptions (e.g., duplicate headings in training
  materials)

## Workflow

1. **Analyze** the input text to identify headings, lists, code sections, emphasis, and
   structural elements
2. **Transform** visual cues into correct Markdown syntax
3. **Ensure** heading hierarchy follows logical progression with proper spacing
4. **Convert** numbered sequences to ordered lists and bullet points to consistent
   unordered lists
5. **Apply** proper code block formatting with language identifiers where recognizable
6. **Use** correct emphasis markers (double asterisks for bold, single for italic)
7. **Apply** language-specific conventions when the document is in German (see
   [Swiss German Conventions](swiss-german-conventions.md))
8. **Verify** that all syntax renders correctly and follows Markdown best practices

## Output Standards

- Clean, well-formatted Markdown that renders correctly in standard parsers
- Proper document structure with preserved logical flow
- Consistent formatting for lists, headings, code blocks, and emphasis
- Correct spacing and line breaks following Markdown conventions
- Quality-checked output without broken formatting or parsing errors
- Context-aware formatting decisions for ambiguous cases based on common conventions

## Heading Rules

- Never skip heading levels (e.g., do not jump from `##` to `####`)
- Ensure a single `#` top-level heading per document
- Add a blank line before and after each heading
- Use ATX-style headings (`#`) consistently, not Setext-style (underlines)

## List Rules

- Use `-` for unordered lists (consistent marker)
- Use `1.` for all ordered list items (let the renderer handle numbering)
- Indent nested lists by 2 or 4 spaces consistently within a document
- Add a blank line before and after list blocks

## Code Block Rules

- Use fenced code blocks (triple backticks) with a language identifier
- Use inline code (single backticks) for short code references in prose
- Never nest code blocks
- Ensure closing fence matches opening fence

## Emphasis Rules

- Use `**bold**` for strong emphasis
- Use `*italic*` for regular emphasis
- Do not use underscores for emphasis in filenames or mixed contexts
- Avoid combining bold and italic unless semantically justified

## Language-Specific Handling

When the document contains German text, apply Swiss German orthography rules
automatically. See [Swiss German Conventions](swiss-german-conventions.md) for the
complete ruleset including:

- Replacing ß with `ss` in all German text
- Preserving proper umlauts (no digraph substitutions)
- Exceptions for code blocks, URLs, and external quotations

## Linter Exceptions

Certain Markdown linting rules have legitimate exceptions depending on document context.
See [Linter Exceptions](linter-exceptions.md) for detailed guidance on:

- MD024 (duplicate headings) in training materials, API docs, and templates
- Respecting project-level `.markdownlint.json` configuration
- When to suggest alternatives vs. when to accept exceptions

## Examples

### Fixing Heading Hierarchy

**Before:**
```markdown
# Title
### Subsection (skipped h2)
##### Detail (skipped h3, h4)
```

**After:**
```markdown
# Title

## Subsection

### Detail
```

### Converting Visual Formatting

**Before:**
```
INTRODUCTION

This is the main text. The IMPORTANT POINTS are:
* first item
* second item
  - sub item a
  - sub item b
* third item

NOTE: Pay attention to this.
```

**After:**
```markdown
## Introduction

This is the main text. The **important points** are:

- First item
- Second item
  - Sub item a
  - Sub item b
- Third item

> **Note:** Pay attention to this.
```

### Code Block Formatting

**Before:**
```
Here is some code:

    function hello() {
        console.log("hello");
    }
```

**After:**
````markdown
Here is some code:

```javascript
function hello() {
    console.log("hello");
}
```
````

## Troubleshooting

### Mixed-Language Documents

Documents containing both German and English text require careful handling:

- Apply Swiss German orthography only to German-language sections
- Leave English sections unchanged
- When language boundaries are unclear, ask the user which sections are German
- Code blocks and technical terms remain unchanged regardless of surrounding language

### Conflicting Linter Configuration

When a project's `.markdownlint.json` conflicts with this skill's formatting rules:

- Project configuration takes precedence over skill defaults
- Read the configuration file before applying formatting changes
- If a rule is disabled in project config, do not "fix" what the linter allows
- Document any deviation from standard formatting in a comment to the user

### Large Documents with Many Issues

When a document has extensive formatting problems:

- Fix structural issues first (heading hierarchy, document outline)
- Then address list formatting and consistency
- Apply code block formatting next
- Handle emphasis and inline formatting last
- Apply language conventions (Swiss German) as a final pass
- Present a summary of changes made to the user
