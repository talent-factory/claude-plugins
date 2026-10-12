#!/usr/bin/env python3
"""Erzeugt aus Markdown ein PDF oder eine ConTeXt-Quelle (.tex) mit frei konfigurierbarer Kopf-/Fusszeile.

Engines:
  context   pandoc (-s) -> ConTeXt. Eigener Vorspann folgt nach dem pandoc-Vorspann und überschreibt Layout,
            Schrift und Kopf-/Fusszeile. Pfeile, Mathe-Relationen und Hoch-/Tiefstellung (CTX_UNICODE)
            werden als ConTeXt-Befehle gesetzt. Andere fehlende Zeichen werden gemeldet.
  xelatex   pandoc -> XeLaTeX (PDF). Zeichen aus --fallback-zeichen über eine Systemschrift.

Konfiguration: Datei md-to-pdf.toml, wird vom Quellordner aufwärts gesucht. CLI-Optionen überschreiben sie.
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
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
TEMPLATES = HERE / "templates"
CONFIG_NAME = "md-to-pdf.toml"
DEFAULTS = {
    "engine": "context",
    "format": "pdf",
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
LATEX_SPECIAL = {"_": r"\_", "&": r"\&", "%": r"\%", "#": r"\#", "$": r"\$"}
MISSING_TEX_RE = re.compile(r"Missing character: There is no (\S) \(U\+")
MISSING_CTX_RE = re.compile(r"char (\S) \(U\+[0-9A-F]+\) in font .*: missing")
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
    unknown = set(data) - set(DEFAULTS)
    if unknown:
        sys.exit(f"Fehler: unbekannte Optionen in {path}: {', '.join(sorted(unknown))}")
    return data


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
    values = {
        "KOPF_LINKS": ctx_escape(cfg["kopf_links"]),
        "KOPF_RECHTS": ctx_escape(cfg["kopf_rechts"]),
        "FUSS_LINKS": ctx_escape(cfg["fuss_links"]),
        "FUSS_RECHTS": cfg["fuss_rechts"] or "\\pagenumber",
        "SCHRIFT": cfg["schrift"],
        "GROESSE": cfg["groesse"],
        "RAND_CM": cfg["rand"],
    }
    own = (TEMPLATES / "preamble.ctx.tpl").read_text(encoding="utf-8")
    for k, v in values.items():
        own = own.replace("{{" + k + "}}", ctx_unicode(str(v)))
    out_tex.write_text(pandoc_pre + own + ctx_unicode(body) + "\\stoptext\n", encoding="utf-8")
    return out_tex


def compile_context(tex, out_pdf):
    if not shutil.which("context"):
        sys.exit("Fehler: 'context' nicht gefunden (ConTeXt installieren, z. B. MacTeX/texlive mit context).")
    res = run(["context", "--result=" + out_pdf.stem, tex.name], cwd=tex.parent)
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
    cfg = dict(DEFAULTS)
    cfg.update(load_config(config_path))
    if config_path:
        print(f"Konfiguration: {config_path}")
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

    out = args.output.resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    missing = []

    with tempfile.TemporaryDirectory(prefix="md-to-pdf-") as t:
        tmp = Path(t)
        md = source.read_text(encoding="utf-8")
        if cfg["mermaid"]:
            md = render_mermaid(md, tmp, cfg["mermaid_breite"])
        prepared = tmp / "quelle.md"
        prepared.write_text(md, encoding="utf-8")
        resource_dir = source.parent

        if cfg["engine"] == "context":
            tex = build_context(cfg, prepared, resource_dir, tmp, tmp / "dokument.tex")
            if cfg["format"] in ("tex", "both"):
                tex_out = out.with_suffix(".tex")
                # Diagramme liegen sonst im temporären Ordner, der nach dem Lauf verschwindet.
                text = tex.read_text(encoding="utf-8")
                for png in sorted(tmp.glob("mermaid*.png")):
                    bilder = out.parent / f"{out.stem}_bilder"
                    bilder.mkdir(exist_ok=True)
                    shutil.copy(png, bilder / png.name)
                    text = text.replace(str(png), f"{bilder.name}/{png.name}")
                tex_out.write_text(text, encoding="utf-8")
                print(f"ConTeXt-Quelle: {tex_out}")
            if cfg["format"] in ("pdf", "both"):
                pdf_out = out.with_suffix(".pdf")
                missing = compile_context(tex, pdf_out)
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
