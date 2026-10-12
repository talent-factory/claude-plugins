---
name: md-to-pdf
description: Converts Markdown into a PDF or a ConTeXt source (.tex) with a freely configurable header and footer. Engine ConTeXt (default) or XeLaTeX. Renders Mermaid diagrams automatically. Module-independent: header, footer and font come from the CLI or from an md-to-pdf.toml in the repository. Triggers: "als PDF", "PDF erstellen", "ConTeXt", "md to pdf", "/education:md-to-pdf".
---

# md-to-pdf

Markdown-to-PDF conversion for any course or module repository. Header, footer, font, page margins and Mermaid behaviour are parameters; nothing is hard-wired to a specific module.

## Requirements

Invocation within the plugin: `${CLAUDE_PLUGIN_ROOT}` points to `plugins/education`. Outside the plugin (directly in the repository), use the path `plugins/education/skills/md-to-pdf/scripts/md_to_pdf.py`.

- `pandoc` (tested with 3.1.8), Python 3.11+ (because of `tomllib`)
- Engine `context`: ConTeXt (`context` on the `PATH`, e.g. MacTeX or TeX Live with ConTeXt)
- Engine `xelatex`: XeLaTeX and the font given by `--schrift`
- Mermaid: `npx` (Node.js); the package `@mermaid-js/mermaid-cli` is fetched on demand

## Usage

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/md-to-pdf/scripts/md_to_pdf.py QUELLE.md ZIEL.pdf \
  --kopf-links "DuA_P · Block 05 · Aufgabenblatt" \
  --kopf-rechts "Binäre Suchbäume" \
  --fuss-links "FFHS · Modulentwicklung Datenstrukturen und Algorithmen"
```

## Configuration file `md-to-pdf.toml`

The script searches for the file from the source folder upwards. CLI options override it. Use `--config PATH` or `--no-config` to control this. Unknown keys abort the run.

```toml
engine = "context"          # context | xelatex
format = "pdf"              # pdf | tex | both (tex/both only with context)
fuss_links = "FFHS · Modulentwicklung Datenstrukturen und Algorithmen"
fuss_rechts = ""            # empty = page number
schrift = "Charter"
groesse = "11pt"            # context only
rand = "2.0"                # cm
fallback_zeichen = ""       # xelatex only, e.g. "→₂"
mermaid = true
mermaid_breite = "55%"
```

The header (`kopf_links`, `kopf_rechts`) usually belongs to the document and is passed on the CLI.

### Options

| Option | Purpose |
|---|---|
| `--engine` | `context` or `xelatex` |
| `--format` | `pdf`, `tex` (ConTeXt source only) or `both` |
| `--kopf-links`, `--kopf-rechts` | Header |
| `--fuss-links`, `--fuss-rechts` | Footer |
| `--schrift`, `--groesse`, `--rand` | Typography |
| `--fallback-zeichen` | Characters for the XeLaTeX fallback |
| `--mermaid on\|off`, `--mermaid-breite` | Mermaid processing |
| `--config`, `--no-config` | Choose or disable the configuration file |

## Mermaid

Mermaid blocks (```` ```mermaid ````) are rendered to PNG with mermaid-cli before typesetting and embedded in a working copy in a temporary folder. The source stays unchanged. Diagrams appear without a caption, with their width set by `mermaid_breite`.

Note for `flowchart` trees: children appear in the order of the edges in the source, and a single child is placed directly below its parent. The workaround is an invisible placeholder node on the opposite side.

## Verification after every build

1. Read the output. `Keine fehlenden Zeichen gemeldet.` (no missing characters reported) is the goal. `Nicht gedruckte Zeichen` (characters not printed) means the font lacks these characters; add an entry to `CTX_UNICODE` (ConTeXt) or `--fallback-zeichen` (XeLaTeX).
2. Render one page (`pdftoppm -r 60 -png -f 1 -l 1 DATEI.pdf /pfad/seite`) and check header, footer, tables and diagrams.
3. Check the page count.

## Unicode in ConTeXt

The text font Charter has no arrows and no superscript or subscript glyphs. The script replaces them with ConTeXt commands from the `CTX_UNICODE` table (e.g. `→` becomes `\mathematics{\rightarrow}`, `₂` becomes `\low{2}`). Code (`\type{}`, highlighted blocks) is left unchanged. A fallback font via `\definefontfallback` is not loaded in ConTeXt (tested).

## Known pitfalls

- **Header disappears:** The pandoc preamble (`-s`) contains `\setupbackend[export=yes]`, which removes header and footer in ConTeXt. The script removes exactly this line. If the pandoc preamble changes, check this spot.
- **Fonts** are macOS-specific (Charter, Arial Unicode).

## Rules

- The output PDF is written to the given target. Do not place files in the module folder that the user did not order.
- Do not commit. The user decides on commits.
- Rebuild after every source change.

## Structure

- `scripts/md_to_pdf.py`: main script
- `templates/preamble.ctx.tpl`: ConTeXt preamble with placeholders (layout, font, header and footer)
- `templates/header.tex.tpl`: XeLaTeX header and footer with placeholders
