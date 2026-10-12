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
| `--profil` | Vorgabe-Profil, derzeit `ffhs-thesis` |
| `--config`, `--no-config` | Choose or disable the configuration file |

## Profil `ffhs-thesis`

Für Thesen an der FFHS. Das Layout folgt der Vorlage `ffhsthesis.cls`: A4, 11 pt, Helvetica-Nachbau (`TeX Gyre Heros`, mit TeX Live verfügbar), 1.5-facher Zeilenabstand, Seitenränder 3 cm links und rechts, Seitenzahl unten zentriert. Nur für `engine = "context"`.

Aufruf per CLI (`--profil ffhs-thesis`) oder in `md-to-pdf.toml` (`profil = "ffhs-thesis"`). Die Angaben zur Titelseite stehen im Abschnitt `[these]`:

```toml
profil = "ffhs-thesis"

[these]
titel = "Titel der Thesis"                 # Pflicht
untertitel = "Optionaler Untertitel"
dokumenttyp = "Bachelor-Thesis"            # Standard: Thesis
studiengang = "INF/WI"
autor = "Max Muster"                       # Pflicht
referent_rolle = "Referentin"              # Standard: Referent(in)
referent = ["Name", "Titel", "Fach"]       # Pflicht, eine Zeile je Eintrag
eingereicht_bei = ["Prof. Dr. X", "Departement Informatik"]   # Pflicht
wohnort = "Zürich"                         # Pflicht
datum = "1. Dezember 2026"                 # Standard: heutiges Datum
widmung = ["Diese Thesis widme ich", "meiner Familie."]       # optional, eigene Seite
logo = "ffhslogo.pdf"                      # Logo oben links, relativ zum Quellordner
titelbild = "bild.png"                     # optional, mittig auf der Titelseite
```

Fehlende Pflichtangaben und unbekannte Schlüssel in `[these]` brechen den Lauf ab. Die Schrift lässt sich mit `schrift` überschreiben.

**Aufbau der Markdown-Quelle:**

- `# Zusammenfassung`, `# Abstract` und `# Abkürzungen` sind unnummerierte Vorspannabschnitte. Sie stehen in dieser Reihenfolge vor dem Hauptteil.
- Das Inhaltsverzeichnis, das Abbildungs- und das Tabellenverzeichnis folgen dem Abstract. Das Abbildungsverzeichnis erscheint nur bei Bildern, das Tabellenverzeichnis nur bei Tabellen mit Beschriftung (`: Titel` unter der Tabelle).
- Der Hauptteil beginnt mit der ersten `#`-Überschrift, die keiner dieser Vorspann-Überschriften entspricht. Davor stehen römische Seitenzahlen, danach arabische ab 1.
- `# Literatur` und `# Selbstständigkeitserklärung` nach dem Hauptteil sind unnummerierte Abschnitte mit Inhaltsverzeichnis-Eintrag.
- Es gibt keine Kopf- und Fusszeile. Entsprechende Optionen werden mit einem Hinweis ignoriert.

**Bekannte Abweichungen von der Vorlage:**

- Zusammenfassung, Abstract und Abkürzungen stehen nicht im Inhaltsverzeichnis. Die Vorlage nimmt Abkürzungen auf. Ein Eintrag wäre nur über einen nummerierten Vorspann-Abschnitt möglich, und der verschiebt die Nummerierung des Hauptteils (siehe Pitfalls).
- Die Selbstständigkeitserklärung ist nur eine Überschrift mit dem Text aus der Quelle. Der Wortlaut der Vorlage muss im Markdown stehen.
- Der Zitierstil ist nicht vorgegeben. Literatur ist eine normale Überschrift mit Text.

## Mermaid

Mermaid blocks (```` ```mermaid ````) are rendered to PNG with mermaid-cli before typesetting and embedded in a working copy in a temporary folder. The source stays unchanged. Diagrams appear without a caption, with their width set by `mermaid_breite`.

Note for `flowchart` trees: children appear in the order of the edges in the source, and a single child is placed directly below its parent. The workaround is an invisible placeholder node on the opposite side.

## Verification after every build

1. Read the output. `Keine fehlenden Zeichen gemeldet.` (no missing characters reported) is the goal. `Nicht gedruckte Zeichen` (characters not printed) means the font lacks these characters; add an entry to `CTX_UNICODE` (ConTeXt) or `--fallback-zeichen` (XeLaTeX).
2. Render one page (`pdftoppm -r 60 -png -f 1 -l 1 DATEI.pdf /pfad/seite`) and check header, footer, tables and diagrams.
3. Check the page count.

## Unicode in ConTeXt

The text font Charter has no arrows and no superscript or subscript glyphs. The script replaces them with ConTeXt commands from the `CTX_UNICODE` table (e.g. `→` becomes `\mathematics{\rightarrow}`, `₂` becomes `\low{2}`). Code (`\type{}`, highlighted blocks) is left unchanged. A fallback font via `\definefontfallback` is not loaded in ConTeXt (tested).

## Codeblöcke

Codeblöcke werden in der ConTeXt-Ausgabe als Framed-Tabelle mit grauem Hintergrund gesetzt. `codeblock_tabelle()` in `scripts/md_to_pdf.py` wandelt pandocs `\starthighlighting` um, eine Zeile je Quellzeile. Die Tabelle bricht über Seitenwechsel um, Kopf- und Fusszeile bleiben erhalten. Die Typing-Optionen `background`/`frame` werden in dieser ConTeXt-Version nicht gerendert, `\startshaded` und `\startframed` brechen nicht um (getestet). Führende Leerzeichen kodiert pandoc als `{ }`-Gruppen (je zwei Leerzeichen eine Gruppe); die Umwandlung stellt den Einzug mit `\hskip` wieder her. Zeilennummern sind nicht eingerichtet. Die Einstellung wirkt nur mit `engine = "context"`; der Test `CodeblockFrameTest` prüft die Umwandlung im erzeugten `.tex`.

### Listings

Jeder Codeblock bekommt ein Listing mit Nummer: `Listing 1: Titel`. Der Titel steht im Info-String, also ```` ```python Titel ````. Ohne Titel erscheint nur `Listing 2`. Mermaid-Blöcke bleiben ohne Listing. Die Beschriftung braucht `engine = "context"`; `codeblock_beschriftung()` in `scripts/md_to_pdf.py` setzt sie als Rohblock `\mdListing{...}`.

### Tabellen-Captions

Die Caption einer Pipe-Tabelle steht als eigene Zeile direkt darunter, mit Leerzeile davor: `: Titel` oder `: Table: Titel`. Beide Schreibweisen sind gleichwertig; `tabellen_beschriftung()` normalisiert sie auf `: Titel`. In GitHub und Obsidian erscheint die Zeile als Text, die Tabelle bleibt unverändert.

## Known pitfalls

- **Inhaltsverzeichnis leer oder Nummerierung verschoben:** Nicht unnummerierte Abschnitte mit `\startsectionlevel` vor den Hauptteil setzen. ConTeXt zählt sie mit und lässt sich nicht zurücksetzen. Das Profil `ffhs-thesis` macht das über `\ffhsVorspann`. Das Inhaltsverzeichnis braucht `criterium=all`, und ConTeXt läuft im Profil dreimal.

- **Header disappears:** The pandoc preamble (`-s`) contains `\setupbackend[export=yes]`, which removes header and footer in ConTeXt. The script removes exactly this line. If the pandoc preamble changes, check this spot.
- **Fonts** are macOS-specific (Charter, Arial Unicode).

## Rules

- The output PDF is written to the given target. Do not place files in the module folder that the user did not order.
- Do not commit. The user decides on commits.
- Rebuild after every source change.

## Structure

- `scripts/md_to_pdf.py`: main script
- `scripts/test_md_to_pdf.py`: Tests für das Profil ffhs-thesis. Ausführung: `python3 -m unittest discover -s scripts -p 'test_*.py'` (im Skill-Ordner). Der End-to-End-Test braucht pandoc und context.
- `templates/preamble.ctx.tpl`: ConTeXt preamble with placeholders (layout, font, header and footer)
- `templates/header.tex.tpl`: XeLaTeX header and footer with placeholders
- `templates/thesis.ctx.tpl`: ConTeXt preamble and title page for profile `ffhs-thesis`
