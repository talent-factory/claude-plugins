---
name: md-to-pdf
description: Erzeugt aus Markdown ein PDF oder eine ConTeXt-Quelle (.tex) mit frei konfigurierbarer Kopf- und Fusszeile. Engine ConTeXt (Standard) oder XeLaTeX. Rendert Mermaid-Diagramme automatisch. Modulunabhängig: Kopf-/Fusszeile und Schrift kommen per CLI oder aus einer md-to-pdf.toml im Repo. Trigger: "als PDF", "PDF erstellen", "ConTeXt", "md to pdf", "/education:md-to-pdf".
---

# md-to-pdf

Globaler Skill für Markdown-zu-PDF in beliebigen Modulrepos. Kopf- und Fusszeile, Schrift, Seitenrand und Mermaid-Verhalten sind Parameter, nichts ist modulfest verdrahtet.

## Voraussetzungen

Aufruf im Plugin: `${CLAUDE_PLUGIN_ROOT}` zeigt auf `plugins/education`. Ausserhalb des Plugins (direkt im Repo) den Pfad `plugins/education/skills/md-to-pdf/scripts/md_to_pdf.py` verwenden.

- `pandoc` (getestet 3.1.8), Python 3.11+ (wegen `tomllib`)
- Engine `context`: ConTeXt (`context` im Pfad, z. B. MacTeX/TeX Live mit ConTeXt)
- Engine `xelatex`: XeLaTeX und die Schrift aus `--schrift`
- Mermaid: `npx` (Node.js), das Paket `@mermaid-js/mermaid-cli` wird bei Bedarf geladen

## Aufruf

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/md-to-pdf/scripts/md_to_pdf.py QUELLE.md ZIEL.pdf \
  --kopf-links "DuA_P · Block 05 · Aufgabenblatt" \
  --kopf-rechts "Binäre Suchbäume" \
  --fuss-links "FFHS · Modulentwicklung Datenstrukturen und Algorithmen"
```

## Konfigurationsdatei `md-to-pdf.toml`

Das Skript sucht die Datei vom Quellordner aufwärts. Die CLI-Optionen überschreiben sie. Mit `--config PFAD` oder `--no-config` lässt sich das steuern. Unbekannte Schlüssel brechen den Lauf ab.

```toml
engine = "context"          # context | xelatex
format = "pdf"              # pdf | tex | both (tex/both nur mit context)
fuss_links = "FFHS · Modulentwicklung Datenstrukturen und Algorithmen"
fuss_rechts = ""            # leer = Seitenzahl
schrift = "Charter"
groesse = "11pt"            # nur context
rand = "2.0"                # cm
fallback_zeichen = ""       # nur xelatex, z. B. "→₂"
mermaid = true
mermaid_breite = "55%"
```

Kopfzeile (`kopf_links`, `kopf_rechts`) gehört in der Regel zum Dokument und wird per CLI übergeben.

### Optionen

| Option | Zweck |
|---|---|
| `--engine` | `context` oder `xelatex` |
| `--format` | `pdf`, `tex` (nur ConTeXt-Quelle) oder `both` |
| `--kopf-links`, `--kopf-rechts` | Kopfzeile |
| `--fuss-links`, `--fuss-rechts` | Fusszeile |
| `--schrift`, `--groesse`, `--rand` | Typografie |
| `--fallback-zeichen` | Zeichen für den XeLaTeX-Fallback |
| `--mermaid on\|off`, `--mermaid-breite` | Mermaid-Verarbeitung |
| `--config`, `--no-config` | Konfigurationsdatei wählen oder abschalten |

## Mermaid

Mermaid-Blöcke (```` ```mermaid ````) werden vor dem Satz mit mermaid-cli als PNG gerendert und in einer Arbeitskopie im temporären Ordner eingebunden. Die Quelle bleibt unverändert. Diagramme erscheinen ohne Bildunterschrift, Breite über `mermaid_breite`.

Zu beachten bei `flowchart`-Bäumen: Kinder erscheinen in der Reihenfolge der Kanten im Quelltext, und ein einzelnes Kind setzt Mermaid senkrecht darunter. Abhilfe ist ein unsichtbarer Platzhalter-Knoten auf der Gegenseite.

## Prüfung nach jedem Build

1. Ausgabe lesen. `Keine fehlenden Zeichen gemeldet.` ist das Ziel. `Nicht gedruckte Zeichen` heisst: die Schrift hat diese Zeichen nicht. Dann den Eintrag in `CTX_UNICODE` (ConTeXt) bzw. `--fallback-zeichen` (XeLaTeX) ergänzen.
2. Eine Seite rendern (`pdftoppm -r 60 -png -f 1 -l 1 DATEI.pdf /pfad/seite`) und Kopf-/Fusszeile, Tabellen und Diagramme prüfen.
3. Seitenzahl kontrollieren.

## Unicode in ConTeXt

Die Textschrift Charter hat keine Pfeile und keine Hoch-/Tiefstellung. Das Skript ersetzt sie durch ConTeXt-Befehle aus der Tabelle `CTX_UNICODE` (z. B. `→` → `\mathematics{\rightarrow}`, `₂` → `\low{2}`). Code (`\type{}`, Hervorhebungsblöcke) bleibt unverändert. Ein Fallback-Font über `\definefontfallback` wird in ConTeXt nicht geladen (getestet).

## Bekannte Fallstricke

- **Kopfzeile verschwindet:** Der Vorspann von pandoc (`-s`) enthält `\setupbackend[export=yes]`. Damit fehlen Kopf- und Fusszeile in ConTeXt. Das Skript entfernt genau diese Zeile. Wird der Vorspann von pandoc angepasst, diese Stelle prüfen.
- **Schriften** sind macOS-spezifisch (Charter, Arial Unicode).

## Regeln

- Das Ausgabe-PDF liegt am angegebenen Ziel. Keine Dateien in Modulordner ablegen, die der Nutzer nicht bestellt hat.
- Nicht committen. Der Nutzer entscheidet über Commits.
- Nach jeder Quelländerung neu bauen.

## Aufbau

- `scripts/md_to_pdf.py`: Hauptskript
- `templates/preamble.ctx.tpl`: ConTeXt-Vorspann mit Platzhaltern (Layout, Schrift, Kopf-/Fusszeile)
- `templates/header.tex.tpl`: XeLaTeX-Kopf-/Fusszeile mit Platzhaltern
