# Markdown Linter Exceptions

This reference documents legitimate exceptions to Markdown linting rules. When formatting
documents, respect these exceptions based on document context rather than applying rules
blindly.

## MD024 -- Duplicate Headings

Duplicate headings are flagged by most Markdown linters but are legitimate in specific
document types.

### Allowed Use Cases

- **Training materials:** Repeating sections such as "Exercise", "Solution", or "Summary"
  in each chapter
- **API documentation:** Repeating method names or parameter sections across endpoints
- **Templates:** Structured templates with recurring section headings
- **Multi-part tutorials:** Identical headings across different parts (e.g., "Setup",
  "Testing", "Cleanup")
- **Changelogs:** Repeating section headers per version entry (e.g., "Added", "Fixed",
  "Changed")

### Decision Logic

1. **Identify document type** from context, file path, or content patterns
2. **If training material, API docs, template, or tutorial:** Accept duplicate headings
   without modification. Do not suggest renaming.
3. **If regular documentation or article:** Suggest more specific headings or add
   numbering (e.g., "Setup -- Part 1", "Setup -- Part 2")
4. **If uncertain:** Ask the user about the document type before suggesting changes

### Project Configuration

When a `.markdownlint.json`, `.markdownlintrc`, or `.markdownlint.yaml` file exists in
the project, respect its configuration:

**Rule disabled entirely:**

```json
{
  "MD024": false
}
```

**Siblings only (allow duplicates in different sections):**

```json
{
  "MD024": {
    "siblings_only": true
  }
}
```

When project configuration exists, follow it. When it does not exist, apply the decision
logic above.

## MD013 -- Line Length

Long lines are common in Markdown documents with complex content.

### Allowed Exceptions

- **Tables:** Table rows often exceed line length limits. Do not break table rows.
- **URLs:** Long URLs should not be broken. Use reference-style links if readability
  suffers.
- **Code blocks:** Do not wrap lines inside fenced code blocks.
- **Headings:** Do not break headings across lines.

## MD033 -- Inline HTML

Some HTML elements are acceptable in Markdown depending on the rendering context.

### Allowed Exceptions

- **`<details>` and `<summary>`:** Collapsible sections (GitHub Flavored Markdown)
- **`<br>`:** Explicit line breaks where Markdown trailing spaces are fragile
- **`<sub>` and `<sup>`:** Subscript and superscript text
- **`<kbd>`:** Keyboard key representations
- **`<img>` with attributes:** When width/height control is needed

## MD041 -- First Line Heading

Some documents legitimately start with content other than a heading.

### Allowed Exceptions

- **YAML frontmatter:** Documents with frontmatter before the first heading
- **Badges and shields:** README files starting with status badges
- **License files:** Starting with copyright notice
- **Generated content:** Auto-generated files with metadata headers

## General Approach

When encountering linter warnings during formatting:

1. Check whether the warning falls under a documented exception
2. Check for project-level linter configuration
3. If the exception is legitimate, leave the content as-is and document the rationale
4. If the warning indicates a genuine issue, fix it
5. When uncertain, ask the user for their preference
