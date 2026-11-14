#!/usr/bin/env python3
"""Erzeugt aus Markdown ein PDF oder eine ConTeXt-Quelle (.tex) mit frei konfigurierbarer Kopf-/Fusszeile.

Engines:
  context   pandoc (-s) -> ConTeXt. Eigener Vorspann folgt nach dem pandoc-Vorspann und überschreibt Layout,
            Schrift und Kopf-/Fusszeile. Pfeile, Mathe-Relationen und Hoch-/Tiefstellung (CTX_UNICODE)
            werden als ConTeXt-Befehle gesetzt. Andere fehlende Zeichen werden gemeldet.
  xelatex   pandoc -> XeLaTeX (PDF). Zeichen aus --fallback-chars über eine Systemschrift.

Konfiguration: Datei md-to-pdf.toml, wird vom Quellordner aufwärts gesucht. CLI-Optionen überschreiben sie.
Profil thesis: Layout für Abschlussarbeiten (Titelseite, Verzeichnisse, römische und arabische
Seitenzahlen). Die Angaben zur Titelseite stehen im Abschnitt [thesis] der md-to-pdf.toml.
Mermaid-Blöcke (```mermaid) werden mit mermaid-cli als PNG gerendert. Die Quelldatei bleibt unverändert.

Beispiel:

    python3 md_to_pdf.py QUELLE.md ZIEL.pdf --header-left "DuA_P · Block 05 · Aufgabenblatt" \\
        --header-right "Binäre Suchbäume"
"""

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
TEMPLATES = HERE / "templates"
CONFIG_NAME = "md-to-pdf.toml"
DEFAULTS = {
    "engine": "context",
    "format": "pdf",
    "profile": "",
    "header_left": "",
    "header_right": "",
    "footer_left": "",
    "footer_right": "",
    "font": "Charter",
    "font_size": "11pt",
    "margin": "2.0",
    "fallback_chars": "",
    "mermaid": True,
    "mermaid_width": "55%",
}
# Standardwerte je Profil; Konfigurationsdatei und CLI überschreiben sie.
PROFILE_DEFAULTS = {
    "thesis": {"font": "TeX Gyre Heros"},  # Helvetica-Nachbau aus TeX Live
}
THESIS_FELDER = {"title", "subtitle", "document_type", "institution", "program", "author", "supervisor_role", "supervisor",
                 "submitted_to", "residence", "date", "dedication", "logo", "title_image"}
THESIS_PFLICHT = ("title", "author", "supervisor", "submitted_to", "residence")
THESIS_ZEILEN = {"supervisor", "submitted_to", "dedication"}  # Text oder Liste von Zeilen
# Abschnitte der ersten Ebene ohne Kapitelnummer. Vor dem Hauptteil stehen sie im Vorspann, Literatur und
# Selbstständigkeitserklärung nach dem Hauptteil.
UNNUMMERIERT = ("Zusammenfassung", "Abstract", "Abkürzungen", "Abkürzungsverzeichnis", "Literatur",
                "Selbstständigkeitserklärung")
MONATE = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober",
          "November", "Dezember"]
LATEX_SPECIAL = {"_": r"\_", "&": r"\&", "%": r"\%", "#": r"\#", "$": r"\$"}
MISSING_TEX_RE = re.compile(r"Missing character: There is no (\S) \(U\+")
MISSING_CTX_RE = re.compile(r"char (\S) \(U\+[0-9A-F]+\) in font .*: missing")
SECTION_RE = re.compile(r"\\(start|stop)sectionlevel(\[[^\]]*\])?")
TITEL_RE = re.compile(r"title=\{([^}]*)\}")
KOPF_RE = re.compile(r"^#[ \t]+(.+?)[ \t]*$")
FENCE = "`" * 3  # Codeblock-Zaun für rohes ConTeXt in Markdown
MERMAID_RE = re.compile(r"^```mermaid[ \t]*\n(.*?)^```[ \t]*$", re.S | re.M)

# Unicode-Zeichen, die Charter nicht hat, auf ConTeXt-Befehle abgebildet (Math-Schrift liefert sie).
CTX_UNICODE = {
    "→": r"\mathematics{\rightarrow}", "←": r"\mathematics{\leftarrow}",
    "↔": r"\mathematics{\leftrightarrow}", "⇒": r"\mathematics{\Rightarrow}",
    "⇐": r"\mathematics{\Leftarrow}", "≤": r"\mathematics{\leq}",
    "≥": r"\mathematics{\geq}", "≠": r"\mathematics{\neq}", "×": r"\mathematics{\times}",
    **{c: rf"\low{{{i}}}" for i, c in enumerate("₀₁₂₃₄₅₆₇₈₉")},
    "²": r"\high{2}", "³": r"\high{3}",
}
# Code bleibt unverändert: Codeblöcke (Tabelle, siehe codeblock_tabelle), Inline-Code (\type{...}).
CTX_VERBATIM_RE = re.compile(r"\\startframedtable.*?\\stopframedtable|\\type\{[^{}]*\}", re.S)
CODEBLOCK_RE = re.compile(r"\\starthighlighting\n(.*?)\n\\stophighlighting", re.S)
EINZUG_RE = re.compile(r"\s*\\NormalTok\{((?:\s*\{ \})+)")
FENCE_RE = re.compile(r"^(\s*)(`{3,})\s*(.*?)\s*$")
TABELLEN_TITEL_RE = re.compile(r"^:\s+(?:Table:\s+)?(\S.*?)\s*$")


def latex_escape(text):
    return "".join(LATEX_SPECIAL.get(ch, ch) for ch in text)


def ctx_escape(text):
    return re.sub(r"([\\{}%#&$^~_])", r"\\\1", text)


def ctx_unicode(text):
    """Ersetzt Zeichen ausserhalb von Code durch ConTeXt-Befehle."""
    def convert(chunk):
        for ch, repl in CTX_UNICODE.items():
            chunk = chunk.replace(ch, repl)
        return chunk
    parts, pos = [], 0
    for m in CTX_VERBATIM_RE.finditer(text):
        parts.append(convert(text[pos:m.start()]))
        parts.append(m.group(0))
        pos = m.end()
    parts.append(convert(text[pos:]))
    return "".join(parts)


def codeblock_tabelle(body):
    """Ersetzt pandocs \\starthighlighting durch eine Framed-Tabelle mit grauem Hintergrund.

    Typing mit Hintergrund bricht nicht über Seiten um, \\startshaded und \\startframed auch nicht.
    Eine Framed-Tabelle schon: jede Quellzeile wird eine Zeile. pandoc markiert Zeilen als /BTEX…/ETEX,
    das entfernt. Führende Leerzeichen bleiben als \\hskip erhalten.
    """
    def zeile(text):
        text = text.replace("/BTEX", "").replace("/ETEX", "")
        einzug = len(text) - len(text.lstrip(" "))
        # pandoc setzt Leerzeichen am Zeilenanfang als { } je zwei Zeichen in den ersten \NormalTok-Block
        m = EINZUG_RE.match(text)
        if m:
            einzug += 2 * m.group(1).count("{ }")
            text = text[:m.start()] + "\\NormalTok{" + text[m.end():]
        rest = text.lstrip(" ")
        vorn = f"\\hskip{einzug * 0.5:g}em" if einzug else ""
        return f"\\startframedrow\\startframedcell{vorn}{rest}\\stopframedcell\\stopframedrow"

    def ersetze(m):
        zeilen = [zeile(z) for z in m.group(1).split("\n")]
        return "\\startframedtable\n" + "\n".join(zeilen) + "\n\\stopframedtable\n\\blank[2*big]"

    return CODEBLOCK_RE.sub(ersetze, body)


def run(cmd, cwd=None):
    return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)


def find_config(start):
    """Sucht md-to-pdf.toml vom Startordner aufwärts."""
    for folder in [start, *start.parents]:
        candidate = folder / CONFIG_NAME
        if candidate.is_file():
            return candidate
    return None


def load_config(path):
    if path is None:
        return {}
    with path.open("rb") as f:
        data = tomllib.load(f)
    these = data.pop("thesis", None)
    unknown = set(data) - set(DEFAULTS)
    if unknown:
        sys.exit(f"Fehler: unbekannte Optionen in {path}: {', '.join(sorted(unknown))}")
    if these is not None:
        unknown = set(these) - THESIS_FELDER
        if unknown:
            sys.exit(f"Fehler: unbekannte Optionen in [thesis] in {path}: {', '.join(sorted(unknown))}")
        for feld, wert in these.items():
            if feld in THESIS_ZEILEN:
                gueltig = isinstance(wert, str) or (isinstance(wert, list) and all(isinstance(z, str) for z in wert))
                erwartet = "Text oder eine Liste von Zeilen"
            else:
                gueltig, erwartet = isinstance(wert, str), "Text"
            if not gueltig:
                sys.exit(f"Fehler: [thesis].{feld} in {path} muss {erwartet} sein")
        data["thesis"] = these
    return data


def ctx_zeilen(werte):
    """Eine oder mehrere Zeilen mit ConTeXt-Zeilenumbruch."""
    if isinstance(werte, str):
        werte = [werte]
    return "\\crlf\n".join(ctx_escape(z) for z in werte)


def deutsches_datum(tag):
    return f"{tag.day}. {MONATE[tag.month - 1]} {tag.year}"


def zeilenabstand(groesse):
    """1,5-facher Zeilenabstand (onehalfspacing) als Näherung: 1,5 × 1,2 × Schriftgrösse."""
    m = re.fullmatch(r"(\d+(?:\.\d+)?)pt", groesse)
    if not m:
        sys.exit(f"Fehler: groesse '{groesse}' muss in pt angegeben sein, z. B. 11pt")
    return f"{float(m.group(1)) * 1.8:.1f}pt"


def thesis_werte(cfg, resource_dir, tmp, abbildungen, tabellen):
    """Platzhalter der Titelseite aus dem Abschnitt [thesis]. Bilder werden in den Arbeitsordner kopiert."""
    these = cfg["thesis"]

    def bild(name, optionen):
        # Eckige Klammern würden das ConTeXt-Argument von \externalfigure abschneiden
        if re.search(r"[\[\],{}]", name):
            sys.exit(f"Fehler: Bildname in [thesis] darf keine der Zeichen [ ] , {{ }} enthalten: {name}")
        quelle = resource_dir / name
        if not quelle.is_file():
            sys.exit(f"Fehler: Bild aus [thesis] fehlt: {quelle}")
        shutil.copy(quelle, tmp / quelle.name)
        return f"\\externalfigure[{quelle.name}][{optionen}]"

    return {
        "LINE_SPACING": zeilenabstand(cfg["font_size"]),
        "LOGO": bild(these["logo"], "height=2cm") if "logo" in these else "",
        "TITLE_IMAGE": f"\\blank[big]\n{bild(these['title_image'], 'width=10cm')}" if "title_image" in these else "",
        "TITLE": ctx_escape(these["title"]),
        "SUBTITLE": (f"\\blank[small]\n{{\\switchtobodyfont[14pt]{ctx_escape(these['subtitle'])}\\par}}"
                       if "subtitle" in these else ""),
        "DOCUMENT_TYPE": ctx_escape(these.get("document_type", "Thesis")),
        "INSTITUTION": ctx_escape(these["institution"]) + "\\crlf " if these.get("institution") else "",
        "PROGRAM": ctx_escape(these.get("program", "")),
        "AUTHOR": ctx_escape(these["author"]),
        "SUPERVISOR_ROLE": ctx_escape(these.get("supervisor_role", "Referent(in)")),
        "SUPERVISOR": ctx_zeilen(these["supervisor"]),
        "SUBMITTED_TO": ctx_zeilen(these["submitted_to"]),
        "RESIDENCE": ctx_escape(these["residence"]),
        "DATE": ctx_escape(these.get("date") or deutsches_datum(date.today())),
        "FIGURES": ("\\blank[2*big]\n{\\switchtobodyfont[17.3pt]\\bf Abbildungsverzeichnis\\par}\n"
                        "\\blank[big]\n\\placelistoffigures\n" if abbildungen else ""),
        "TABLES": ("\\blank[2*big]\n{\\switchtobodyfont[17.3pt]\\bf Tabellenverzeichnis\\par}\n"
                     "\\blank[big]\n\\placelistoftables\n" if tabellen else ""),
        "DEDICATION": (f"\\page\n\\vfill\n\\startalignment[center]{ctx_zeilen(these['dedication'])}"
                    "\\stopalignment\n\\vfill" if "dedication" in these else ""),
    }


def thesis_markdown(md):
    """Setzt die Verzeichnisse vor den ersten Vorspann-Abschnitt (bzw. vor Abkürzungen) und den Hauptteil-Beginn
    (arabische Seitenzahl) vor die erste Kapitelüberschrift. Beide Blöcke stehen auf Abschnittsebene, sonst
    bleibt das Inhaltsverzeichnis in ConTeXt leer."""
    zeilen = md.split("\n")
    kopfzeilen = []  # (Zeilennummer, Titel), ohne Überschriften in Codeblöcken
    im_code = False
    for i, zeile in enumerate(zeilen):
        if zeile.startswith(("```", "~~~")):
            im_code = not im_code
            continue
        m = KOPF_RE.match(zeile)
        if not im_code and m:
            kopfzeilen.append((i, m.group(1)))
    koerper = next((i for i, t in kopfzeilen if t not in UNNUMMERIERT), None)
    if koerper is None:
        return md
    # Verzeichnisse stehen vor dem Abkürzungsverzeichnis, sofern es vor dem Hauptteil steht. Sonst vor dem ersten Vorspann-Abschnitt.
    vorspann = [i for i, _ in kopfzeilen if i < koerper]
    verzeichnis = next((i for i, t in kopfzeilen if i < koerper and t in ("Abkürzungen", "Abkürzungsverzeichnis")), None)
    if verzeichnis is None:
        verzeichnis = vorspann[0] if vorspann else koerper
    einfuegen = {}
    einfuegen.setdefault(verzeichnis, []).extend([FENCE + "{=context}", "\\thesisVerzeichnisse", FENCE, ""])
    einfuegen.setdefault(koerper, []).extend([FENCE + "{=context}", "\\startThesis", FENCE, ""])
    neu = []
    for i, zeile in enumerate(zeilen):
        neu.extend(einfuegen.get(i, []))
        neu.append(zeile)
    return "\n".join(neu)


def thesis_body(body):
    """Vorspann-Abschnitte vor dem Hauptteil als unstrukturierte Überschriften setzen (\\thesisVorspann).

    pandoc setzt jede Überschrift als \\startsectionlevel. Unnummerierte Abschnitte vor dem Hauptteil würden
    dessen Nummerierung verschieben, weil ConTeXt sie dem Kapitelzähler zuordnet. Darum stehen sie ohne
    Gliederungseintrag im Vorspann. Unnummerierte Abschnitte nach dem Hauptteil (Literatur,
    Selbstständigkeitserklärung) bleiben Abschnitte mit Inhaltsverzeichnis-Eintrag.
    """
    ausgabe, stapel, pos, im_hauptteil = [], [], 0, False
    for m in SECTION_RE.finditer(body):
        ausgabe.append(body[pos:m.start()])
        pos = m.end()
        if m.group(1) == "stop":
            if stapel.pop() == "section":
                ausgabe.append("\\stopsectionlevel")
            continue
        args = m.group(2) or "[]"
        titel = TITEL_RE.search(args)
        name = titel.group(1) if titel else ""
        oberste = not stapel
        if oberste and name in UNNUMMERIERT and not im_hauptteil:
            stapel.append("vorspann")
            ausgabe.append("\\thesisVorspann{" + name + "}")
            continue
        if oberste and name not in UNNUMMERIERT:
            im_hauptteil = True
        if oberste and name in UNNUMMERIERT:
            optionen = args[1:-1]
            ausgabe.append("\\startsectionlevel[" + (optionen + "," if optionen else "") + "number=no]")
        else:
            ausgabe.append(m.group(0))
        stapel.append("section")
    ausgabe.append(body[pos:])
    return "".join(ausgabe)


def tabellen_beschriftung(md):
    """Lässt beide Caption-Schreibweisen unter einer Pipe-Tabelle zu: `: Titel` und `: Table: Titel`.

    Die Zeile wird auf `: Titel` normalisiert, pandoc setzt dann denselben Caption-Float. Eine Zeile
    `: …` ohne Tabelle direkt davor (Leerzeile erlaubt) bleibt unverändert, z. B. eine Definitionsliste.
    """
    zeilen = md.split("\n")
    for i, zeile in enumerate(zeilen):
        m = TABELLEN_TITEL_RE.match(zeile)
        if not m or i < 1:
            continue
        davor = zeilen[i - 1].strip()
        if not davor and i >= 2:
            davor = zeilen[i - 2].strip()
        if davor.startswith("|"):
            zeilen[i] = f": {m.group(1)}"
    return "\n".join(zeilen)


def codeblock_beschriftung(md):
    """Setzt vor jeden Codeblock ein Listing mit Nummer und optionalem Titel.

    Der Titel steht im Info-String: ```python Titel. Die Beschriftung ist ein ConTeXt-Rohblock
    (pandoc {=context}), der \\mdListing aufruft. Mermaid-Blöcke sind Bilder und bleiben unbeschriftet.
    """
    ausgabe, im_block = [], False
    for zeile in md.split("\n"):
        m = FENCE_RE.match(zeile)
        if m and im_block and not m.group(3):
            im_block = False
        elif m and not im_block:
            im_block = True
            einzug, zaun, info = m.groups()
            sprache, _, titel = info.partition(" ")
            if sprache != "mermaid":
                titel = ctx_escape(titel.strip())
                ausgabe += [f"{einzug}{zaun}{{=context}}", f"{einzug}\\mdListing{{{titel}}}", f"{einzug}{zaun}", ""]
                zeile = f"{einzug}{zaun}{sprache}"
        ausgabe.append(zeile)
    return "\n".join(ausgabe)


def render_mermaid(md_text, tmp, breite):
    """Ersetzt jeden Mermaid-Block durch ein gerendertes PNG (Bild ohne Bildunterschrift)."""
    blocks = MERMAID_RE.findall(md_text)
    if not blocks:
        return md_text
    if not shutil.which("npx"):
        sys.exit("Fehler: 'npx' nicht gefunden (für Mermaid nötig, Node.js installieren).")
    print(f"Mermaid: {len(blocks)} Diagramm(e) werden gerendert.")
    counter = [0]

    def replace(m):
        counter[0] += 1
        n = counter[0]
        mmd = tmp / f"mermaid{n:02d}.mmd"
        png = tmp / f"mermaid{n:02d}.png"
        mmd.write_text(m.group(1), encoding="utf-8")
        res = run(["npx", "-y", "@mermaid-js/mermaid-cli", "-i", str(mmd), "-o", str(png),
                   "-b", "white", "-s", "2"])
        if res.returncode != 0 or not png.exists():
            print(res.stdout + res.stderr)
            sys.exit(f"Fehler: Mermaid-Block {n} konnte nicht gerendert werden.")
        return f"![]({png}){{width={breite}}}"

    return MERMAID_RE.sub(replace, md_text)


def pandoc_base(source, resource_dir):
    return ["pandoc", str(source), "--from", "markdown", "--resource-path", str(resource_dir)]


def build_context(cfg, source, resource_dir, tmp, out_tex):
    """pandoc -s liefert Vorspann (u. a. Code-Hervorhebung) und Körper. Der eigene Vorspann folgt danach."""
    full = tmp / "pandoc.tex"
    res = run(pandoc_base(source, resource_dir) + ["--to", "context", "--standalone", "-o", str(full)])
    if res.returncode != 0:
        sys.exit("Fehler: pandoc (ConTeXt) fehlgeschlagen:\n" + res.stderr)
    pandoc_pre, _, rest = full.read_text(encoding="utf-8").partition("\\starttext")
    # pandoc setzt tagged PDF-Export (export=yes). Damit verschwinden Kopf- und Fusszeile in ConTeXt.
    pandoc_pre = pandoc_pre.replace("\\setupbackend[export=yes]\n", "")
    body = codeblock_tabelle(rest.rsplit("\\stoptext", 1)[0])
    thesis = cfg["profile"] == "thesis"
    if thesis:
        body = thesis_body(body)
    values = {
        "HEADER_LEFT": ctx_escape(cfg["header_left"]),
        "HEADER_RIGHT": ctx_escape(cfg["header_right"]),
        "FOOTER_LEFT": ctx_escape(cfg["footer_left"]),
        "FOOTER_RIGHT": cfg["footer_right"] or "\\pagenumber",
        "FONT": cfg["font"],
        "FONT_SIZE": cfg["font_size"],
        "MARGIN_CM": cfg["margin"],
    }
    if thesis:
        # Abbildungs- und Tabellenverzeichnis nur, wenn es Bilder bzw. beschriftete Tabellen gibt
        abbildungen = re.search(r"\\startplacefigure\[title=", body) is not None
        tabellen = re.search(r"\\startplacetable\[title=", body) is not None
        values.update(thesis_werte(cfg, resource_dir, tmp, abbildungen, tabellen))
    vorlage = "thesis.ctx.tpl" if thesis else "preamble.ctx.tpl"
    own = (TEMPLATES / vorlage).read_text(encoding="utf-8")
    for k, v in values.items():
        own = own.replace("{{" + k + "}}", ctx_unicode(str(v)))
    out_tex.write_text(pandoc_pre + own + ctx_unicode(body) + "\\stoptext\n", encoding="utf-8")
    return out_tex


def compile_context(tex, out_pdf, laeufe=1):
    """laeufe > 1 für Verzeichnisse: ConTeXt übernimmt Inhaltsverzeichnis und Seitenbezüge erst in späteren Läufen."""
    if not shutil.which("context"):
        sys.exit("Fehler: 'context' nicht gefunden (ConTeXt installieren, z. B. MacTeX/texlive mit context).")
    res = run(["context", f"--runs={laeufe}", "--result=" + out_pdf.stem, tex.name], cwd=tex.parent)
    log = res.stdout + res.stderr
    produced = tex.parent / (out_pdf.stem + ".pdf")
    if res.returncode != 0 or not produced.exists():
        print(log[-3000:])
        sys.exit("Fehler: ConTeXt-Lauf fehlgeschlagen (Log oben).")
    shutil.move(str(produced), str(out_pdf))
    return sorted(set(MISSING_CTX_RE.findall(log)))


def fallback_definition(chars):
    if not chars:
        return ""
    lines = ["\\newfontfamily\\dokFallback{Arial Unicode MS}"]
    lines += [f"\\newunicodechar{{{ch}}}{{{{\\dokFallback {ch}}}}}" for ch in dict.fromkeys(chars)]
    return "\n".join(lines)


def build_xelatex(cfg, source, resource_dir, tmp, out_pdf):
    hdr = tmp / "header.tex"
    text = (TEMPLATES / "header.tex.tpl").read_text(encoding="utf-8")
    values = {
        "HEADER_LEFT": latex_escape(cfg["header_left"]),
        "HEADER_RIGHT": latex_escape(cfg["header_right"]),
        "FOOTER_LEFT": latex_escape(cfg["footer_left"]),
        "FONT": cfg["font"],
        "FALLBACK_DEF": fallback_definition(cfg["fallback_chars"]),
    }
    for k, v in values.items():
        text = text.replace("{{" + k + "}}", v)
    hdr.write_text(text, encoding="utf-8")
    cmd = pandoc_base(source, resource_dir) + [
        "--to", "pdf", "--pdf-engine=xelatex", "-H", str(hdr),
        "-V", "documentclass=article", "-V", "fontsize=11pt", "-V", "geometry:a4paper",
        "-V", f"geometry:margin={cfg['margin']}cm", "-V", "lang=de-CH", "-V", "colorlinks=true",
        "-o", str(out_pdf),
    ]
    res = run(cmd)
    if res.returncode != 0:
        print(res.stderr)
        sys.exit("Fehler: pandoc/XeLaTeX fehlgeschlagen (Log oben).")
    return sorted(set(MISSING_TEX_RE.findall(res.stdout + res.stderr)))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("source", type=Path, help="Markdown-Quelle")
    p.add_argument("output", type=Path, help="Ziel (.pdf oder .tex)")
    p.add_argument("--config", type=Path, help="Konfigurationsdatei (Standard: md-to-pdf.toml aufwärts suchen)")
    p.add_argument("--no-config", action="store_true", help="Keine Konfigurationsdatei verwenden")
    p.add_argument("--engine", choices=["context", "xelatex"])
    p.add_argument("--profile", choices=sorted(PROFILE_DEFAULTS),
                   help="Vorgabe-Profil, z. B. thesis (Layout und Titelseite einer Abschlussarbeit)")
    p.add_argument("--format", choices=["pdf", "tex", "both"],
                   help="pdf: PDF; tex: nur ConTeXt-Quelle; both: beides")
    p.add_argument("--header-left")
    p.add_argument("--header-right")
    p.add_argument("--footer-left")
    p.add_argument("--footer-right", help="Standard: Seitenzahl")
    p.add_argument("--font")
    p.add_argument("--font-size", help="Schriftgrösse (nur ConTeXt)")
    p.add_argument("--margin", help="Seitenrand in cm")
    p.add_argument("--fallback-chars", help="Zeichen für den XeLaTeX-Fallback, z. B. '→₂'")
    p.add_argument("--mermaid", choices=["on", "off"], help="Mermaid-Blöcke rendern")
    p.add_argument("--mermaid-width", help="Breite der Diagramme, z. B. 55%%")
    args = p.parse_args()

    if not args.source.is_file():
        sys.exit(f"Fehler: Quelldatei fehlt: {args.source}")
    source = args.source.resolve()

    config_path = None if args.no_config else (args.config or find_config(source.parent))
    config = load_config(config_path)
    if config_path:
        print(f"Konfiguration: {config_path}")
    profil = args.profile or config.get("profile", "")
    if profil and profil not in PROFILE_DEFAULTS:
        sys.exit(f"Fehler: unbekanntes Profil '{profil}' (erlaubt: {', '.join(sorted(PROFILE_DEFAULTS))})")
    cfg = dict(DEFAULTS)
    cfg.update(PROFILE_DEFAULTS.get(profil, {}))
    cfg.update(config)
    for key in DEFAULTS:
        if key == "mermaid":
            continue
        value = getattr(args, key, None)
        if value is not None:
            cfg[key] = value
    if args.mermaid is not None:
        cfg["mermaid"] = args.mermaid == "on"
    if args.mermaid_width is not None:
        cfg["mermaid_width"] = args.mermaid_width

    if not shutil.which("pandoc"):
        sys.exit("Fehler: 'pandoc' nicht gefunden.")
    if cfg["format"] in ("tex", "both") and cfg["engine"] != "context":
        sys.exit("Fehler: format tex/both braucht engine context.")
    if cfg["profile"] == "thesis":
        if cfg["engine"] != "context":
            sys.exit("Fehler: Profil thesis braucht engine context.")
        these = cfg.get("thesis")
        if these is None:
            sys.exit(f"Fehler: Profil thesis braucht einen Abschnitt [thesis] in {CONFIG_NAME}.")
        fehlend = [k for k in THESIS_PFLICHT if not these.get(k)]
        if fehlend:
            sys.exit(f"Fehler: Pflichtangaben in [thesis] fehlen: {', '.join(fehlend)}")
        ignoriert = [k for k in ("header_left", "header_right", "footer_left", "footer_right") if cfg[k]]
        if ignoriert:
            print("Hinweis: Profil thesis setzt keine Kopf- und Fusszeile, ignoriert: " + ", ".join(ignoriert))

    out = args.output.resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    missing = []

    with tempfile.TemporaryDirectory(prefix="md-to-pdf-") as t:
        tmp = Path(t)
        md = source.read_text(encoding="utf-8")
        if cfg["mermaid"]:
            md = render_mermaid(md, tmp, cfg["mermaid_width"])
        md = tabellen_beschriftung(md)
        if cfg["profile"] == "thesis":
            md = thesis_markdown(md)
        if cfg["engine"] == "context":
            md = codeblock_beschriftung(md)
        prepared = tmp / "quelle.md"
        prepared.write_text(md, encoding="utf-8")
        resource_dir = source.parent

        if cfg["engine"] == "context":
            tex = build_context(cfg, prepared, resource_dir, tmp, tmp / "dokument.tex")
            if cfg["format"] in ("tex", "both"):
                tex_out = out.with_suffix(".tex")
                # Diagramme und Bilder liegen sonst im temporären Ordner, der nach dem Lauf verschwindet.
                text = tex.read_text(encoding="utf-8")
                bilder = out.parent / f"{out.stem}_bilder"
                for datei in [*sorted(tmp.glob("mermaid*.png")), *sorted(tmp.glob("*.pdf"))]:
                    bilder.mkdir(exist_ok=True)
                    shutil.copy(datei, bilder / datei.name)
                    text = text.replace(str(datei), f"{bilder.name}/{datei.name}")
                    text = text.replace(f"\\externalfigure[{datei.name}]",
                                        f"\\externalfigure[{bilder.name}/{datei.name}]")
                tex_out.write_text(text, encoding="utf-8")
                print(f"ConTeXt-Quelle: {tex_out}")
            if cfg["format"] in ("pdf", "both"):
                pdf_out = out.with_suffix(".pdf")
                missing = compile_context(tex, pdf_out, laeufe=3 if cfg["profile"] == "thesis" else 1)
                print(f"PDF erstellt: {pdf_out}")
        else:
            pdf_out = out.with_suffix(".pdf")
            missing = build_xelatex(cfg, prepared, resource_dir, tmp, pdf_out)
            print(f"PDF erstellt: {pdf_out}")

    pdf_path = out.with_suffix(".pdf")
    if pdf_path.exists():
        m = re.search(r"Pages:\s+(\d+)", run(["pdfinfo", str(pdf_path)]).stdout)
        print(f"Seiten: {m.group(1) if m else 'unbekannt'}")
    if missing:
        print("Nicht gedruckte Zeichen (bitte prüfen): " + " ".join(missing))
    else:
        print("Keine fehlenden Zeichen gemeldet.")


if __name__ == "__main__":
    main()
