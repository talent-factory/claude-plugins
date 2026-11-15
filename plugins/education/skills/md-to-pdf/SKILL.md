---
name: md-to-pdf
description: >-
  Converts Markdown into a PDF or a ConTeXt source (.tex) with a freely configurable header and footer. Engine ConTeXt (default) or XeLaTeX. Renders Mermaid diagrams automatically. Module-independent: header, footer and font come from the CLI or from an md-to-pdf.toml in the repository. Triggers: "als PDF", "PDF erstellen", "ConTeXt", "md to pdf", "/education:md-to-pdf".
---

# md-to-pdf

Markdown-to-PDF conversion for any course or module repository. Header, footer, font, page margins and Mermaid behaviour are parameters; nothing is hard-wired to a specific module.

## Requirements

Invocation within the plugin: `${CLAUDE_PLUGIN_ROOT}` points to `plugins/education`. Outside the plugin (directly in the repository), use the path `plugins/education/skills/md-to-pdf/scripts/md_to_pdf.py`.

- `pandoc` (tested with 3.1.8), Python 3.11+ (because of `tomllib`)
- Engine `context`: ConTeXt (`context` on the `PATH`, e.g. MacTeX or TeX Live with ConTeXt)
- Engine `xelatex`: XeLaTeX and the font given by `--font`
- Mermaid: `npx` (Node.js); the package `@mermaid-js/mermaid-cli` is fetched on demand

## Usage

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/md-to-pdf/scripts/md_to_pdf.py SOURCE.md TARGET.pdf \
  --header-left "Module · Block 05 · Worksheet" \
  --header-right "Binary search trees" \
  --footer-left "Hochschule · Modul Datenstrukturen"
```

## Configuration file `md-to-pdf.toml`

The script searches for the file from the source folder upwards. CLI options override it. Use `--config PATH` or `--no-config` to control this. Unknown keys abort the run.

```toml
engine = "context"          # context | xelatex
format = "pdf"              # pdf | tex | both (tex/both only with context)
footer_left = "Hochschule · Modul Datenstrukturen"
footer_right = ""            # empty = page number
font = "Charter"
font_size = "11pt"            # context only
margin = "2.0"                # cm
fallback_chars = ""       # xelatex only, e.g. "→₂"
mermaid = true
mermaid_width = "55%"
```

The header (`header_left`, `header_right`) usually belongs to the document and is passed on the CLI.

### Options

| Option | Purpose |
|---|---|
| `--engine` | `context` or `xelatex` |
| `--format` | `pdf`, `tex` (ConTeXt source only) or `both` |
| `--header-left`, `--header-right` | Header |
| `--footer-left`, `--footer-right` | Footer |
| `--font`, `--font-size`, `--margin` | Typography |
| `--fallback-chars` | Characters for the XeLaTeX fallback |
| `--mermaid on\|off`, `--mermaid-width` | Mermaid processing |
| `--profile` | Preset profile, currently `thesis` |
| `--config`, `--no-config` | Choose or disable the configuration file |

## Profile `thesis`

For theses and similar long documents. The layout: A4, 11 pt, a Helvetica clone (`TeX Gyre Heros`, available with TeX Live), 1.5 line spacing, side margins of 3 cm, page number centred at the bottom. Only for `engine = "context"`.

Select it via the CLI (`--profile thesis`) or in `md-to-pdf.toml` (`profile = "thesis"`). The title page data lives in the `[thesis]` section:

```toml
profile = "thesis"

[thesis]
title = "Titel der Thesis"                 # required
subtitle = "Optionaler Untertitel"
document_type = "Bachelor-Thesis"            # default: Thesis
institution = "Name der Hochschule"        # optional, top right of the title page
program = "INF/WI"
author = "Max Muster"                       # required
supervisor_role = "Referentin"              # default: Referent(in)
supervisor = ["Name", "Titel", "Fach"]       # required, one line per entry
submitted_to = ["Prof. Dr. X", "Departement Informatik"]   # required
residence = "Zürich"                         # required
date = "1. Dezember 2026"                 # default: today's date
dedication = ["Diese Thesis widme ich", "meiner Familie."]       # optional, own page
logo = "logo.pdf"                           # logo top left, relative to the source folder
title_image = "bild.png"                     # optional, centred on the title page
```

Missing required fields and unknown keys in `[thesis]` abort the run. The font can be overridden with `font`.

**Structure of the Markdown source:**

- `# Zusammenfassung`, `# Abstract` and `# Abkürzungen` are unnumbered front matter sections. They appear in this order before the main part.
- The table of contents and the lists of figures and tables follow the abstract. The list of figures only appears if there are images; the list of tables only if there are tables with a caption (`: Titel` below the table).
- The main part starts with the first `#` heading that matches none of these front matter headings. Roman page numbers precede it; arabic numbers start at 1 afterwards.
- `# Literatur` and `# Selbstständigkeitserklärung` after the main part are unnumbered sections with a table of contents entry.
- There is no header or footer. Corresponding options are ignored with a notice.

**Known limitations:**

- Zusammenfassung, Abstract and Abkürzungen do not appear in the table of contents. An entry would only be possible via a numbered front matter section, which shifts the numbering of the main part (see Known pitfalls).
- The Selbstständigkeitserklärung is only a heading with the text from the source. The wording must be provided in the Markdown.
- The citation style is not prescribed. Literatur is a regular heading with text.

## Mermaid

Mermaid blocks (```` ```mermaid ````) are rendered to PNG with mermaid-cli before typesetting and embedded in a working copy in a temporary folder. The source stays unchanged. Diagrams appear without a caption, with their width set by `mermaid_width`.

Note for `flowchart` trees: children appear in the order of the edges in the source, and a single child is placed directly below its parent. The workaround is an invisible placeholder node on the opposite side.

## Verification after every build

1. Read the output. `Keine fehlenden Zeichen gemeldet.` (no missing characters reported) is the goal. `Nicht gedruckte Zeichen` (characters not printed) means the font lacks these characters; add an entry to `CTX_UNICODE` (ConTeXt) or `--fallback-chars` (XeLaTeX).
2. Render one page (`pdftoppm -r 60 -png -f 1 -l 1 FILE.pdf /path/page`) and check header, footer, tables and diagrams.
3. Check the page count.

## Code blocks, listings, captions

In the ConTeXt output, code blocks are a breakable framed table with a grey background, each with a numbered caption `Listing N: Title` (the title is the info string: ```` ```python Title ````). A pipe table takes its caption from the line below it, `: Title` or `: Table: Title`, and prints as `Tabelle N: Title`. This needs `engine = "context"`. How these are built, and the Unicode table for characters the font lacks: [references/implementation-notes.md](references/implementation-notes.md).

## Known pitfalls

- **Table of contents empty or numbering shifted:** Do not place unnumbered sections with `\startsectionlevel` before the main part. ConTeXt counts them and the counter cannot be reset. The `thesis` profile handles this via `\thesisVorspann`. The table of contents needs `criterium=all`, and the profile runs ConTeXt three times.

- **Header disappears:** The pandoc preamble (`-s`) contains `\setupbackend[export=yes]`, which removes header and footer in ConTeXt. The script removes exactly this line. If the pandoc preamble changes, check this spot.
- **Fonts** are macOS-specific (Charter, Arial Unicode).

## Rules

- The output PDF is written to the given target. Do not place files in the module folder that the user did not order.
- Do not commit. The user decides on commits.
- Rebuild after every source change.

## Structure

- `scripts/md_to_pdf.py`: main script
- `scripts/test_md_to_pdf.py`: tests for the engine (thesis profile, code blocks, listings, captions). Run with `python3 -m unittest discover -s scripts -p 'test_*.py'` (from the skill folder). The end-to-end test needs pandoc and context.
- `templates/preamble.ctx.tpl`: ConTeXt preamble with placeholders (layout, font, header and footer)
- `templates/header.tex.tpl`: XeLaTeX header and footer with placeholders
- `templates/thesis.ctx.tpl`: ConTeXt preamble and title page for profile `thesis`
