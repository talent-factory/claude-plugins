"""Tests für md_to_pdf.py, Profil ffhs-thesis.

Ausführung: python3 -m unittest discover -s scripts -p 'test_*.py'
Der End-to-End-Test läuft nur, wenn pandoc und context installiert sind.
"""

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import md_to_pdf as m  # noqa: E402

SCRIPT = Path(__file__).resolve().parent / "md_to_pdf.py"


def these_cfg(**felder):
    basis = {"titel": "T", "autor": "A", "referent": ["R"], "eingereicht_bei": ["E"], "wohnort": "W"}
    basis.update(felder)
    return {"these": basis, "groesse": "11pt"}


class ThesisMarkdownTest(unittest.TestCase):
    def positionen(self, md):
        zeilen = m.thesis_markdown(md).split("\n")
        return {
            "verz": zeilen.index("\\ffhsVerzeichnisse") if "\\ffhsVerzeichnisse" in zeilen else None,
            "start": zeilen.index("\\startThesis") if "\\startThesis" in zeilen else None,
            "zeilen": zeilen,
        }

    def test_abkuerzungen_nach_hauptteil_bleibt_ohne_einfluss(self):
        p = self.positionen("# Zusammenfassung\n\nZ\n\n# Einleitung\n\nE\n\n# Abkürzungen\n\nA\n")
        einleitung = p["zeilen"].index("# Einleitung")
        self.assertIsNotNone(p["verz"])
        self.assertLess(p["verz"], einleitung, "Verzeichnisse dürfen nicht im Hauptteil stehen")

    def test_verzeichnis_vor_abkuerzungen_im_vorspann(self):
        p = self.positionen("# Zusammenfassung\n\nZ\n\n# Abstract\n\nA\n\n# Abkürzungen\n\nX\n\n# Einleitung\n\nE\n")
        self.assertLess(p["verz"], p["zeilen"].index("# Abkürzungen"))
        self.assertGreater(p["verz"], p["zeilen"].index("# Abstract"))

    def test_verzeichnis_ohne_abkuerzungen_vor_erstem_vorspann(self):
        p = self.positionen("# Zusammenfassung\n\nZ\n\n# Einleitung\n\nE\n")
        self.assertLess(p["verz"], p["zeilen"].index("# Zusammenfassung"))

    def test_startthesis_vor_hauptteil(self):
        p = self.positionen("# Zusammenfassung\n\nZ\n\n# Einleitung\n\nE\n")
        self.assertLess(p["start"], p["zeilen"].index("# Einleitung"))

    def test_ueberschrift_im_codeblock_ist_kein_kapitel(self):
        md = "# Zusammenfassung\n\n```\n# Kommentar\n```\n\n# Einleitung\n\nE\n"
        p = self.positionen(md)
        self.assertLess(p["start"], p["zeilen"].index("# Einleitung"))
        self.assertEqual(p["zeilen"].count("\\startThesis"), 1)

    def test_ohne_hauptteil_unveraendert(self):
        md = "# Zusammenfassung\n\nZ\n"
        self.assertEqual(m.thesis_markdown(md), md)


class ThesisBodyTest(unittest.TestCase):
    PANDOC = (
        "\\startsectionlevel[title={Zusammenfassung},reference={z}]\nZ\n\\stopsectionlevel\n"
        "\\startsectionlevel[title={Einleitung},reference={e}]\nE\n"
        "\\startsectionlevel[title={Problem},reference={p}]\nP\n\\stopsectionlevel\n"
        "\\stopsectionlevel\n"
        "\\startsectionlevel[title={Literatur},reference={l}]\nL\n\\stopsectionlevel\n"
    )

    def test_vorspann_wird_unstrukturiert(self):
        out = m.thesis_body(self.PANDOC)
        self.assertIn("\\ffhsVorspann{Zusammenfassung}", out)
        self.assertNotIn("\\startsectionlevel[title={Zusammenfassung}", out)

    def test_nachspann_bleibt_unnummerierter_abschnitt(self):
        out = m.thesis_body(self.PANDOC)
        self.assertIn("\\startsectionlevel[title={Literatur},reference={l},number=no]", out)

    def test_hauptteil_bleibt_nummeriert_und_klammern_ausgeglichen(self):
        out = m.thesis_body(self.PANDOC)
        self.assertIn("\\startsectionlevel[title={Einleitung},reference={e}]", out)
        self.assertEqual(out.count("\\startsectionlevel"), out.count("\\stopsectionlevel"))


class ConfigValidationTest(unittest.TestCase):
    def lade(self, inhalt):
        with tempfile.TemporaryDirectory() as t:
            pfad = Path(t) / "md-to-pdf.toml"
            pfad.write_text(inhalt, encoding="utf-8")
            return m.load_config(pfad)

    def test_text_statt_liste_ist_erlaubt_fuer_referent(self):
        cfg = self.lade('[these]\ntitel = "T"\nreferent = "Name"\n')
        self.assertEqual(cfg["these"]["referent"], "Name")

    def test_liste_fuer_titel_wird_abgelehnt(self):
        with self.assertRaises(SystemExit):
            self.lade('[these]\ntitel = ["T"]\n')

    def test_unbekannter_schluessel_wird_abgelehnt(self):
        with self.assertRaises(SystemExit):
            self.lade('[these]\nfoo = "x"\n')

    def test_zeilenabstand_folgt_der_schriftgroesse(self):
        self.assertEqual(m.zeilenabstand("11pt"), "19.8pt")
        self.assertEqual(m.zeilenabstand("12pt"), "21.6pt")

    def test_zeilenabstand_ohne_pt_wird_abgelehnt(self):
        with self.assertRaises(SystemExit):
            m.zeilenabstand("11")


class ThesisValuesTest(unittest.TestCase):
    def test_bildname_mit_klammer_wird_abgelehnt(self):
        cfg = these_cfg(logo="a]b.pdf")
        with tempfile.TemporaryDirectory() as t:
            with self.assertRaises(SystemExit):
                m.thesis_werte(cfg, Path(t), Path(t), False, False)

    def test_zeilen_werden_mit_crlf_verbunden(self):
        self.assertEqual(m.ctx_zeilen(["a", "b"]), "a\\crlf\nb")
        self.assertEqual(m.ctx_zeilen("a"), "a")

    def test_zeilenabstand_im_werte_dict(self):
        with tempfile.TemporaryDirectory() as t:
            werte = m.thesis_werte(these_cfg(), Path(t), Path(t), False, False)
        self.assertEqual(werte["ZEILENABSTAND"], "19.8pt")


@unittest.skipUnless(shutil.which("pandoc") and shutil.which("context"), "pandoc und context nötig")
class EndToEndTest(unittest.TestCase):
    def test_thesis_baut_pdf(self):
        md = "# Zusammenfassung\n\nZ\n\n# Einleitung\n\nE\n\n## Unter\n\nU\n\n# Literatur\n\nL\n"
        toml = '[these]\ntitel = "T"\nautor = "A"\nreferent = ["R"]\neingereicht_bei = ["E"]\nwohnort = "W"\n'
        with tempfile.TemporaryDirectory() as t:
            quelle = Path(t) / "these.md"
            quelle.write_text(md, encoding="utf-8")
            (Path(t) / "md-to-pdf.toml").write_text('profil = "ffhs-thesis"\n' + toml, encoding="utf-8")
            ziel = Path(t) / "out" / "these.pdf"
            res = subprocess.run([sys.executable, str(SCRIPT), str(quelle), str(ziel)], capture_output=True, text=True)
            self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
            self.assertTrue(ziel.exists())


class CodeblockBeschriftungTest(unittest.TestCase):
    def test_titel_aus_info_string(self):
        out = m.codeblock_beschriftung("```python Musterlösung\nx = 1\n```\n")
        self.assertIn("```{=context}\n\\mdListing{Musterlösung}\n```", out)
        self.assertTrue(out.rstrip().endswith("```python\nx = 1\n```"))

    def test_ohne_titel_leerer_listing_aufruf(self):
        out = m.codeblock_beschriftung("```\nroh\n```\n")
        self.assertIn("\\mdListing{}", out)

    def test_mermaid_bleibt_unbeschriftet(self):
        md = "```mermaid\ngraph TD\n```\n"
        self.assertEqual(m.codeblock_beschriftung(md), md)

    def test_zwei_bloecke_zwei_listings(self):
        out = m.codeblock_beschriftung("```python T\n```\n```\n")
        self.assertEqual(out.count("\\mdListing"), 2)


class TabellenBeschriftungTest(unittest.TestCase):
    TABELLE = "| a | b |\n|---|---|\n| 1 | 2 |\n\n"

    def test_beide_schreibweisen_werden_gleich(self):
        self.assertIn(": Titel\n", m.tabellen_beschriftung(self.TABELLE + ": Titel\n"))
        self.assertIn(": Titel\n", m.tabellen_beschriftung(self.TABELLE + ": Table: Titel\n"))

    def test_groschreibung_und_leerzeichen(self):
        self.assertIn(": Titel\n", m.tabellen_beschriftung(self.TABELLE + ":   Table:   Titel\n"))

    def test_definitionsliste_ohne_tabelle_bleibt(self):
        md = "Definition:\n\n: Table: Titel\n"
        self.assertEqual(m.tabellen_beschriftung(md), md)

    @unittest.skipUnless(shutil.which("pandoc"), "pandoc nötig")
    def test_pandoc_erzeugt_caption_float(self):
        for schreibweise in (": Titel", ": Table: Titel"):
            with self.subTest(schreibweise=schreibweise):
                md = m.tabellen_beschriftung(self.TABELLE + schreibweise + "\n")
                res = subprocess.run(["pandoc", "--from", "markdown", "--to", "context"],
                                     input=md, capture_output=True, text=True)
                self.assertIn("\\startplacetable[title={Titel}]", res.stdout)


@unittest.skipUnless(shutil.which("pandoc"), "pandoc nötig")
class CodeblockFrameTest(unittest.TestCase):
    def test_codeblock_rahmen_nach_pandoc_definetyping(self):
        md = "# Titel\n\n```python\ndef f(x):\n    return x + 1\n```\n"
        for profil_toml in ('', 'profil = "ffhs-thesis"\n[these]\ntitel = "T"\nautor = "A"\nreferent = ["R"]\n'
                            'eingereicht_bei = ["E"]\nwohnort = "W"\n'):
            with self.subTest(profil=bool(profil_toml)), tempfile.TemporaryDirectory() as t:
                quelle = Path(t) / "q.md"
                quelle.write_text(md, encoding="utf-8")
                (Path(t) / "md-to-pdf.toml").write_text(profil_toml, encoding="utf-8")
                ziel = Path(t) / "q.tex"
                res = subprocess.run(
                    [sys.executable, str(SCRIPT), str(quelle), str(ziel), "--format", "tex"],
                    capture_output=True, text=True,
                )
                self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
                tex = ziel.read_text(encoding="utf-8")
                self.assertNotIn("\\starthighlighting", tex.split("\\starttext", 1)[1])
                self.assertLess(tex.index("\\setupframedtablecolumn"), tex.index("\\starttext"),
                                "Tabelleneinstellung muss vor dem Körper stehen")
                tabelle = tex[tex.index("\\startframedtable"):tex.index("\\stopframedtable")]
                self.assertIn("\\hskip2em", tabelle, "Einzug der Zeile mit vier Leerzeichen")
                self.assertIn("\\KeywordTok{def}", tabelle)


if __name__ == "__main__":
    unittest.main()
