# Markdown Linter Exceptions

Respect these exceptions according to the document's context instead of applying lint rules blindly. A project's own markdownlint configuration (`.markdownlint.*`, `.markdownlintrc`, `.markdownlint-cli2.*`) always comes first: read it, and do not "fix" what it allows.

## MD024: duplicate headings

Legitimate in:

- **Training materials:** "Exercise", "Solution" or "Summary" repeated in every chapter
- **API documentation:** the same method or parameter sections for every endpoint
- **Templates** with recurring sections
- **Multi-part tutorials:** "Setup", "Testing", "Cleanup" in each part
- **Changelogs:** "Added", "Fixed", "Changed" per version

Decision: identify the document type from context, path or content. For these types accept duplicates and do not suggest renaming. For regular documentation or articles suggest more specific headings ("Setup, part 1"). If the type is unclear, ask.

A project may switch the rule off (`"MD024": false`) or allow duplicates between siblings only (`"MD024": {"siblings_only": true}`); follow it.

## Other rules

- **MD013 line length:** do not break table rows, URLs, code blocks or headings.
- **MD033 inline HTML:** `<details>`, `<summary>`, `<br>`, `<sub>`, `<sup>`, `<kbd>` and `<img>` with size attributes are fine.
- **MD041 first line heading:** frontmatter, badges, a license notice or generated metadata may come first.

If a warning falls under an exception, leave the content as it is and say why; if it points to a real problem, fix it; if unsure, ask.
