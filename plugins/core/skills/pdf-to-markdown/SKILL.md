---
name: pdf-to-markdown
description: Converts PDF files to Markdown. Use when user wants to convert a PDF document, extract PDF content, or transform PDF to Markdown format. Supports simple text extraction (fast) and complex layouts with code/tables (vision). Invoke with the PDF file path.
---

# PDF to Markdown Converter

Convert PDF documents to structured Markdown with automatic mode selection.

## Workflow

When the user requests PDF conversion:

1. **Get PDF path** - Ask for the PDF file path if not provided
2. **Determine mode** - Ask user preference or auto-select based on document type
3. **Convert** - Execute the appropriate conversion method
4. **Output** - Save Markdown file and report results

## Mode Selection

Ask the user which mode to use:

| Mode | Best For | Speed |
|------|----------|-------|
| **fast** | Simple text documents, reports | Very fast |
| **vision** | Complex layouts, code, tables, scans | Medium |

## Execution

### Fast Mode (PyMuPDF)

Run the converter script:

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/pdf-to-markdown/scripts/pdf_converter.py "<pdf_path>" --mode fast
```

The script outputs:
- `<name>.md` - Markdown file with extracted text
- `<name>_images/` - Extracted images (if any)

Report the result to the user.

### Vision Mode (Claude Code Analysis)

**Step 1:** Convert PDF to page images:

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/pdf-to-markdown/scripts/pdf_converter.py "<pdf_path>" --mode vision [--pages START-END] [--dpi 150]
```

This creates `<name>_pages/` with PNG images.

**Step 2:** Read each page image using the Read tool and analyze the content.

**Step 3:** For each page, generate Markdown following these rules:

- Preserve heading hierarchy (# ## ###)
- Format code blocks with language detection (```java, ```python, etc.)
- Convert tables to Markdown table syntax
- Describe images/diagrams as `[Image: description]`
- Merge multi-column layouts logically into single-column flow
- Apply Swiss German orthography (ß → ss)
- Ignore page numbers and headers/footers unless relevant

**Step 4:** Combine all pages into a single Markdown file:

```markdown
# Document Title

<!-- Page 1 -->

[page 1 content]

---

<!-- Page 2 -->

[page 2 content]
```

**Step 5:** Write the final Markdown file using the Write tool.

**Step 6:** Clean up temporary page images (ask user first).

## User Interaction Examples

### Example 1: Simple Document

```
User: Konvertiere /Users/me/report.pdf zu Markdown

Claude: Ich konvertiere das PDF. Welchen Modus bevorzugst du?
- **fast**: Schnelle Textextraktion (für einfache Dokumente)
- **vision**: Bildanalyse (für komplexe Layouts, Code, Tabellen)

User: fast

Claude: [Runs script, reports result]
Fertig! Erstellt:
- /Users/me/report.md
- /Users/me/report_images/ (3 Bilder)
```

### Example 2: Technical Book

```
User: Konvertiere java-buch.pdf zu Markdown, hat viel Code

Claude: Da das Dokument Code enthält, empfehle ich den Vision-Modus.
Soll ich das gesamte PDF oder nur bestimmte Seiten konvertieren?

User: Seiten 10-30

Claude: [Converts pages to images]
[Reads each page image]
[Generates structured Markdown with code blocks]
[Writes output file]

Fertig! Erstellt: java-buch.md (21 Seiten)
Soll ich die temporären Seitenbilder löschen?
```

### Example 3: Direct Invocation

```
User: /pdf-to-markdown /path/to/document.pdf

Claude: [Asks for mode preference]
[Executes conversion]
[Reports result]
```

## Prerequisites

Ensure dependencies are installed before first use:

```bash
# Fast mode
pip install PyMuPDF Pillow --break-system-packages

# Vision mode (additional)
pip install pdf2image --break-system-packages
brew install poppler  # macOS
```

## Options Reference

| Option | Description | Default |
|--------|-------------|---------|
| `--mode fast` | PyMuPDF text extraction | Default |
| `--mode vision` | Prepare images for analysis | - |
| `--pages START-END` | Process specific pages | All |
| `--dpi N` | Image resolution | 150 |
| `--no-images` | Skip image extraction (fast) | - |

## Special Features

- **LaTeX Umlaut Correction**: Fixes ¨a → ä, ¨o → ö, ¨u → ü
- **Swiss German**: Converts ß → ss automatically
- **Quote Normalization**: Fixes `` and '' → "
- **Code Detection**: Identifies programming languages in code blocks
- **Table Recognition**: Converts visual tables to Markdown syntax
