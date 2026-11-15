# md-to-pdf implementation notes

For changes to `scripts/md_to_pdf.py`; not needed to use the skill.

## Unicode in ConTeXt

The text font Charter has no arrows and no superscript or subscript glyphs. The script replaces them with ConTeXt commands from the `CTX_UNICODE` table (e.g. `→` becomes `\mathematics{\rightarrow}`, `₂` becomes `\low{2}`). Code (`\type{}`, highlighted blocks) is left unchanged. A fallback font via `\definefontfallback` is not loaded in ConTeXt (tested).

## Code blocks

In the ConTeXt output, code blocks are set as a framed table with a grey background. `codeblock_tabelle()` in `scripts/md_to_pdf.py` converts pandoc's `\starthighlighting`, one table row per source line. The table breaks across pages, and header and footer are preserved. The typing options `background`/`frame` are not rendered in this ConTeXt version, and `\startshaded` and `\startframed` do not break across pages (tested). Pandoc encodes leading spaces as `{ }` groups (one group per two spaces); the conversion restores the indentation with `\hskip`. Line numbers are not configured. The setting only takes effect with `engine = "context"`; the test `CodeblockFrameTest` checks the conversion in the generated `.tex`.

## Listings

Every code block receives a numbered listing: `Listing 1: Titel`. The title is taken from the info string, i.e. ```` ```python Titel ````. Without a title, only `Listing 2` appears. Mermaid blocks get no listing. The caption requires `engine = "context"`; `codeblock_beschriftung()` in `scripts/md_to_pdf.py` emits it as the raw block `\mdListing{...}`.

## Table captions

The caption of a pipe table is a separate line directly below it, preceded by a blank line: `: Titel` or `: Table: Titel`. Both spellings are equivalent; `tabellen_beschriftung()` normalises them to `: Titel`. On GitHub and in Obsidian the line renders as plain text and the table is unchanged. In the PDF, the caption is left-aligned at the text margin as `Tabelle N: Titel` (numbering via `\setupfloat[table]` in the templates).
