# PDF to Markdown Conversion

Convert PDF documents to structured Markdown using natural language with the `pdf-to-markdown` skill from the **Core** plugin.

## Quick Start

Simply tell Claude Code what you want:

```
Konvertiere /path/to/document.pdf zu Markdown
```

Claude Code will:

1. Ask which mode you prefer (fast or vision)
2. Execute the conversion
3. Save the Markdown file
4. Report the results

## Invocation Examples

=== "Natural Language"

    ```
    Konvertiere report.pdf zu Markdown
    ```

=== "With Context"

    ```
    Konvertiere java-buch.pdf zu Markdown, enthält viel Code
    ```
    Claude Code will recommend vision mode automatically.

=== "Specific Pages"

    ```
    Konvertiere textbook.pdf Seiten 10-30 zu Markdown
    ```

## Overview

The skill offers two conversion modes optimized for different document types:

| Mode | Method | Speed | Best For |
|------|--------|-------|----------|
| `fast` | PyMuPDF text extraction | Very fast | Simple text documents |
| `vision` | Claude Code image analysis | Medium | Complex layouts, code, tables |

!!! tip "No Manual Steps Required"
    Unlike direct script usage, invoking the skill handles the entire workflow automatically — including image analysis in vision mode.

## Prerequisites

=== "Fast Mode"

    ```bash
    pip install PyMuPDF Pillow --break-system-packages
    ```

=== "Vision Mode"

    ```bash
    pip install pdf2image Pillow --break-system-packages

    # Install poppler
    brew install poppler        # macOS
    sudo apt install poppler-utils  # Ubuntu
    ```

=== "Vision + Direct API"

    ```bash
    pip install pdf2image Pillow anthropic tqdm --break-system-packages
    export ANTHROPIC_API_KEY="sk-ant-..."
    ```

## Use Cases

### Simple Text Document

Convert a report or whitepaper without complex formatting.

```
User: Konvertiere quarterly-report.pdf zu Markdown

Claude: Welchen Modus bevorzugst du?
- fast: Schnelle Textextraktion
- vision: Bildanalyse für komplexe Layouts

User: fast

Claude: ✅ Fertig! Erstellt:
- quarterly-report.md
- quarterly-report_images/ (3 Bilder)
```

---

### Technical Book with Code

Convert a programming textbook with code examples, tables, and multi-column layout.

```
User: Konvertiere java-textbook.pdf zu Markdown, enthält viel Java-Code

Claude: Da das Dokument Code enthält, empfehle ich den Vision-Modus.
Soll ich das gesamte PDF oder nur bestimmte Seiten konvertieren?

User: Seiten 1-50

Claude: [Konvertiert Seiten zu Bildern]
[Analysiert jede Seite]
[Erkennt Java-Code und formatiert als ```java Blöcke]
[Erstellt Markdown-Tabellen]

✅ Fertig! Erstellt: java-textbook.md (50 Seiten)
Soll ich die temporären Seitenbilder löschen?
```

!!! tip "No Extra API Costs"
    Vision mode runs on your existing Claude Code session — no separate API key required.

---

### Scientific Paper

Convert a two-column academic paper with formulas and references.

```
User: Konvertiere research-paper.pdf zu Markdown, ist ein wissenschaftliches Paper

Claude: Ich verwende den Vision-Modus für das zweispaltige Layout.
[Konvertiert und analysiert]
[Formatiert Formeln als LaTeX]
[Markiert Referenzen als Fussnoten]

✅ Fertig! Erstellt: research-paper.md
```

---

### Scanned Document (OCR)

Convert a scanned historical document or handwritten notes.

```
User: Konvertiere scanned-letter.pdf, ist ein eingescanntes Dokument

Claude: Für Scans verwende ich höhere Auflösung (300 DPI).
[Konvertiert mit OCR-Qualität]
[Analysiert Handschrift wenn vorhanden]

✅ Fertig! Erstellt: scanned-letter.md
```

---

### Chapter-by-Chapter Conversion

Extract specific chapters from a large book.

```
User: Konvertiere nur Kapitel 3 aus textbook.pdf (Seiten 45-78)

Claude: [Konvertiert nur Seiten 45-78]

✅ Fertig! Erstellt: textbook.md (34 Seiten)
```

---

### Text Only (No Images)

Extract only text content, skip embedded images.

```
User: Extrahiere nur den Text aus manual.pdf, keine Bilder

Claude: [Verwendet fast mode ohne Bildextraktion]

✅ Fertig! Erstellt: manual.md (nur Text)
```

---

### Direct Script Usage (Advanced)

For automation or batch processing, you can also use the script directly:

```bash
# Fast mode
python scripts/pdf_converter.py document.pdf

# Vision mode with direct API (requires ANTHROPIC_API_KEY)
python scripts/pdf_converter.py document.pdf --mode vision --use-api

# Batch processing
for pdf in *.pdf; do
    python scripts/pdf_converter.py "$pdf" --mode vision --use-api
done
```

!!! warning "API Costs for Direct Mode"
    Using `--use-api` incurs charges on your Anthropic account.

## Decision Guide

| Document Type | Recommended Mode | Options |
|---------------|------------------|---------|
| Plain text | `fast` | Default |
| With images | `fast` | Default |
| Code examples | `vision` | Claude Code |
| Tables | `vision` | Claude Code |
| Multi-column | `vision` | Claude Code |
| Scans / OCR | `vision` | `--dpi 300` |
| Batch / CI | `vision --use-api` | API key |

## CLI Reference

```
python scripts/pdf_converter.py <input.pdf> [output] [options]

Options:
  --mode, -m {fast,vision}  Conversion mode (default: fast)
  --no-images               Skip image extraction (fast mode only)

Vision mode:
  --use-api                 Use direct Anthropic API
  --dpi DPI                 Image quality (default: 150)
  --pages START-END         Page range (e.g., 1-10)

Direct API (--use-api):
  --model MODEL             Claude model to use
  --api-key KEY             API key (or ANTHROPIC_API_KEY env var)
```

## Troubleshooting

### Installation Issues

??? question "PyMuPDF not found"
    ```bash
    pip install PyMuPDF --break-system-packages
    ```

??? question "Poppler not installed"
    ```bash
    # macOS
    brew install poppler

    # Ubuntu/Debian
    sudo apt-get install poppler-utils
    ```

### Conversion Quality

??? question "Umlauts display incorrectly"
    The fast mode automatically fixes LaTeX-style umlauts (¨a → ä). If issues persist, use vision mode for better character recognition.

??? question "Text is scrambled or incomplete"
    This typically indicates a complex layout. Switch to vision mode:
    ```bash
    python scripts/pdf_converter.py doc.pdf --mode vision
    ```

??? question "Password-protected PDF"
    Remove password protection first:
    ```bash
    qpdf --decrypt --password=PASSWORD locked.pdf unlocked.pdf
    ```

### Performance

??? question "Memory error on large PDFs"
    Process in smaller chunks:
    ```bash
    python scripts/pdf_converter.py big-book.pdf --mode vision --pages 1-50
    python scripts/pdf_converter.py big-book.pdf --mode vision --pages 51-100
    ```

??? question "Rate limiting with Direct API"
    The script automatically waits 60 seconds on rate limit errors. For frequent limits, reduce pages per run or upgrade your API tier.

## Tips

1. **Always test with one page first**
   ```bash
   python scripts/pdf_converter.py book.pdf --mode vision --pages 1-1
   ```

2. **Choose the right DPI**
    - 150 DPI: Standard, good balance (default)
    - 200 DPI: Better quality for vision analysis
    - 300 DPI: Optimal for scanned documents

3. **Split large PDFs**
    - Process >100 pages in chunks
    - Saves memory and allows checkpointing

4. **Quality control**
    - Always spot-check the output
    - Complex layouts may need manual cleanup
