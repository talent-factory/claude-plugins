#!/usr/bin/env python3
"""Erzeugt aus Markdown ein PDF oder eine ConTeXt-Quelle (.tex) mit frei konfigurierbarer Kopf-/Fusszeile.

Engines:
  context   pandoc (-s) -> ConTeXt. Eigener Vorspann folgt nach dem pandoc-Vorspann und überschreibt Layout,
            Schrift und Kopf-/Fusszeile. Pfeile, Mathe-Relationen und Hoch-/Tiefstellung (CTX_UNICODE)
            werden als ConTeXt-Befehle gesetzt. Andere fehlende Zeichen werden gemeldet.
  xelatex   pandoc -> XeLaTeX (PDF). Zeichen aus --fallback-zeichen über eine Systemschrift.

Konfiguration: Datei md-to-pdf.toml, wird vom Quellordner aufwärts gesucht. CLI-Optionen überschreiben sie.
Profil ffhs-thesis: Layout nach der FFHS-Thesis-Vorlage (Titelseite, Verzeichnisse, römische und arabische
Seitenzahlen). Die Angaben zur Titelseite stehen im Abschnitt [these] der md-to-pdf.toml.
Mermaid-Blöcke (```mermaid) werden mit mermaid-cli als PNG gerendert. Die Quelldatei bleibt unverändert.

Beispiel:

    python3 md_to_pdf.py QUELLE.md ZIEL.pdf --kopf-links "DuA_P · Block 05 · Aufgabenblatt" \\
        --kopf-rechts "Binäre Suchbäume"
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
    "profil": "",
    "kopf_links": "",
    "kopf_rechts": "",
    "fuss_links": "",
    "fuss_rechts": "",
    "schrift": "Charter",
    "groesse": "11pt",
    "rand": "2.0",
    "fallback_zeichen": "",
    "mermaid": True,
    "mermaid_breite": "55%",
}
# Standardwerte je Profil; Konfigurationsdatei und CLI überschreiben sie.
PROFILE_DEFAULTS = {
    "ffhs-thesis": {"schrift": "TeX Gyre Heros"},  # Helvetica-Nachbau aus TeX Live, wie helvet in der Vorlage
}
THESIS_FELDER = {"titel", "untertitel", "dokumenttyp", "studiengang", "autor", "referent_rolle", "referent",
                 "eingereicht_bei", "wohnort", "datum", "widmung", "logo", "titelbild"}
THESIS_PFLICHT = ("titel", "autor", "referent", "eingereicht_bei", "wohnort")
# Abschnitte der ersten Ebene ohne Kapitelnummer. Vor dem ersten anderen Kapitel stehen sie im Vorspann.
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
# Code bleibt unverändert: Hervorhebungsblöcke und Inline-Code (\type{...}).
CTX_VERBATIM_RE = re.compile(r"\\starthighlighting.*?\\stophighlighting|\\type\{[^{}]*\}", re.S)


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
    these = data.pop("these", None)
    unknown = set(data) - set(DEFAULTS)
    if unknown:
        sys.exit(f"Fehler: unbekannte Optionen in {path}: {', '.join(sorted(unknown))}")
    if these is not None:
        unknown = set(these) - THESIS_FELDER
        if unknown:
            sys.exit(f"Fehler: unbekannte Optionen in [these] in {path}: {', '.join(sorted(unknown))}")
        data["these"] = these
    return data


def ctx_zeilen(werte):
    """Eine oder mehrere Zeilen mit ConTeXt-Zeilenumbruch."""
    if isinstance(werte, str):
        werte = [werte]
    return "\\crlf\n".join(ctx_escape(z) for z in werte)


def deutsches_datum(tag):
    return f"{tag.day}. {MONATE[tag.month - 1]} {tag.year}"


def thesis_werte(cfg, resource_dir, tmp, abbildungen, tabellen):
    """Platzhalter der Titelseite aus dem Abschnitt [these]. Bilder werden in den Arbeitsordner kopiert."""
    these = cfg["these"]

    def bild(name, optionen):
        quelle = resource_dir / name
        if not quelle.is_file():
            sys.exit(f"Fehler: Bild aus [these] fehlt: {quelle}")
        shutil.copy(quelle, tmp / quelle.name)
        return f"\\externalfigure[{quelle.name}][{optionen}]"

    return {
        "LOGO": bild(these["logo"], "height=2cm") if "logo" in these else "",
        "TITELBILD": f"\\blank[big]\n{bild(these['titelbild'], 'width=10cm')}" if "titelbild" in these else "",
        "TITEL": ctx_escape(these["titel"]),
        "UNTERTITEL": (f"\\blank[small]\n{{\\switchtobodyfont[14pt]{ctx_escape(these['untertitel'])}\\par}}"
                       if "untertitel" in these else ""),
        "DOKUMENTTYP": ctx_escape(these.get("dokumenttyp", "Thesis")),
        "STUDIENGANG": ctx_escape(these.get("studiengang", "")),
        "AUTOR": ctx_escape(these["autor"]),
        "REFERENT_ROLLE": ctx_escape(these.get("referent_rolle", "Referent(in)")),
        "REFERENT": ctx_zeilen(these["referent"]),
        "EINGEREICHT_BEI": ctx_zeilen(these["eingereicht_bei"]),
        "WOHNORT": ctx_escape(these["wohnort"]),
        "DATUM": ctx_escape(these.get("datum") or deutsches_datum(date.today())),
        "ABBILDUNGEN": ("\\blank[2*big]\n{\\switchtobodyfont[17.3pt]\\bf Abbildungsverzeichnis\\par}\n"
                        "\\blank[big]\n\\placelistoffigures\n" if abbildungen else ""),
        "TABELLEN": ("\\blank[2*big]\n{\\switchtobodyfont[17.3pt]\\bf Tabellenverzeichnis\\par}\n"
                     "\\blank[big]\n\\placelistoftables\n" if tabellen else ""),
        "WIDMUNG": (f"\\page\n\\vfill\n\\startalignment[center]{ctx_zeilen(these['widmung'])}"
                    "\\stopalignment\n\\vfill" if "widmung" in these else ""),
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
    verzeichnis = next((i for i, t in kopfzeilen if t in ("Abkürzungen", "Abkürzungsverzeichnis")), None)
    if verzeichnis is None:
        verzeichnis = next((i for i, t in kopfzeilen if t in UNNUMMERIERT), koerper)
    einfuegen = {}
    einfuegen.setdefault(verzeichnis, []).extend([FENCE + "{=context}", "\\ffhsVerzeichnisse", FENCE, ""])
    einfuegen.setdefault(koerper, []).extend([FENCE + "{=context}", "\\startThesis", FENCE, ""])
    neu = []
    for i, zeile in enumerate(zeilen):
        neu.extend(einfuegen.get(i, []))
        neu.append(zeile)
    return "\n".join(neu)


def thesis_body(body):
    """Vorspann-Abschnitte vor dem Hauptteil als unstrukturierte Überschriften setzen (\\ffhsVorspann).

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
            ausgabe.append("\\ffhsVorspann{" + name + "}")
            continue
        if oberste and name not in UNNUMMERIERT:
            im_hauptteil = True
        if oberste and name in UNNUMMERIERT:
            ausgabe.append("\\startsectionlevel" + args[:-1] + ",number=no]")
        else:
            ausgabe.append(m.group(0))
        stapel.append("section")
    ausgabe.append(body[pos:])
    return "".join(ausgabe)


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
    body = rest.rsplit("\\stoptext", 1)[0]
    thesis = cfg["profil"] == "ffhs-thesis"
    if thesis:
        body = thesis_body(body)
    values = {
        "KOPF_LINKS": ctx_escape(cfg["kopf_links"]),
        "KOPF_RECHTS": ctx_escape(cfg["kopf_rechts"]),
        "FUSS_LINKS": ctx_escape(cfg["fuss_links"]),
        "FUSS_RECHTS": cfg["fuss_rechts"] or "\\pagenumber",
        "SCHRIFT": cfg["schrift"],
        "GROESSE": cfg["groesse"],
        "RAND_CM": cfg["rand"],
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
        "KOPF_LINKS": latex_escape(cfg["kopf_links"]),
        "KOPF_RECHTS": latex_escape(cfg["kopf_rechts"]),
        "FUSS_LINKS": latex_escape(cfg["fuss_links"]),
        "SCHRIFT": cfg["schrift"],
        "FALLBACK_DEF": fallback_definition(cfg["fallback_zeichen"]),
    }
    for k, v in values.items():
        text = text.replace("{{" + k + "}}", v)
    hdr.write_text(text, encoding="utf-8")
    cmd = pandoc_base(source, resource_dir) + [
        "--to", "pdf", "--pdf-engine=xelatex", "-H", str(hdr),
        "-V", "documentclass=article", "-V", "fontsize=11pt", "-V", "geometry:a4paper",
        "-V", f"geometry:margin={cfg['rand']}cm", "-V", "lang=de-CH", "-V", "colorlinks=true",
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
    p.add_argument("--profil", choices=sorted(PROFILE_DEFAULTS),
                   help="Vorgabe-Profil, z. B. ffhs-thesis (Layout und Titelseite der FFHS-Thesis)")
    p.add_argument("--format", choices=["pdf", "tex", "both"],
                   help="pdf: PDF; tex: nur ConTeXt-Quelle; both: beides")
    p.add_argument("--kopf-links")
    p.add_argument("--kopf-rechts")
    p.add_argument("--fuss-links")
    p.add_argument("--fuss-rechts", help="Standard: Seitenzahl")
    p.add_argument("--schrift")
    p.add_argument("--groesse", help="Schriftgrösse (nur ConTeXt)")
    p.add_argument("--rand", help="Seitenrand in cm")
    p.add_argument("--fallback-zeichen", help="Zeichen für den XeLaTeX-Fallback, z. B. '→₂'")
    p.add_argument("--mermaid", choices=["on", "off"], help="Mermaid-Blöcke rendern")
    p.add_argument("--mermaid-breite", help="Breite der Diagramme, z. B. 55%%")
    args = p.parse_args()

    if not args.source.is_file():
        sys.exit(f"Fehler: Quelldatei fehlt: {args.source}")
    source = args.source.resolve()

    config_path = None if args.no_config else (args.config or find_config(source.parent))
    config = load_config(config_path)
    if config_path:
        print(f"Konfiguration: {config_path}")
    profil = args.profil or config.get("profil", "")
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
    if args.mermaid_breite is not None:
        cfg["mermaid_breite"] = args.mermaid_breite

    if not shutil.which("pandoc"):
        sys.exit("Fehler: 'pandoc' nicht gefunden.")
    if cfg["format"] in ("tex", "both") and cfg["engine"] != "context":
        sys.exit("Fehler: format tex/both braucht engine context.")
    if cfg["profil"] == "ffhs-thesis":
        if cfg["engine"] != "context":
            sys.exit("Fehler: Profil ffhs-thesis braucht engine context.")
        these = cfg.get("these")
        if these is None:
            sys.exit(f"Fehler: Profil ffhs-thesis braucht einen Abschnitt [these] in {CONFIG_NAME}.")
        fehlend = [k for k in THESIS_PFLICHT if k not in these]
        if fehlend:
            sys.exit(f"Fehler: Pflichtangaben in [these] fehlen: {', '.join(fehlend)}")
        ignoriert = [k for k in ("kopf_links", "kopf_rechts", "fuss_links", "fuss_rechts") if cfg[k]]
        if ignoriert:
            print("Hinweis: Profil ffhs-thesis setzt keine Kopf- und Fusszeile, ignoriert: " + ", ".join(ignoriert))

    out = args.output.resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    missing = []

    with tempfile.TemporaryDirectory(prefix="md-to-pdf-") as t:
        tmp = Path(t)
        md = source.read_text(encoding="utf-8")
        if cfg["mermaid"]:
            md = render_mermaid(md, tmp, cfg["mermaid_breite"])
        if cfg["profil"] == "ffhs-thesis":
            md = thesis_markdown(md)
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
                missing = compile_context(tex, pdf_out, laeufe=3 if cfg["profil"] == "ffhs-thesis" else 1)
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
