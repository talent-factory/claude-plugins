% Vorspann für ConTeXt (md-to-pdf). Platzhalter {{...}} setzt scripts/md_to_pdf.py.
\setuppapersize[A4][A4]
\setuplayout[width=middle,height=middle,topspace=2.2cm,bottomspace=2.2cm,backspace={{RAND_CM}}cm,header=0.8cm,footer=0.8cm]
\definefontfamily[main][rm][{{SCHRIFT}}]
\setupbodyfont[main,{{GROESSE}}]
% Codeblöcke (pandoc: \starthighlighting) ohne Kasten: \startshaded bricht nicht über Seiten.
\setuptyping[highlighting][before={},after={}]
\setupinteraction[state=stop]
\setuppagenumbering[location={footer,right}]
\setupheader[state=start]
\setupfooter[state=start]
\setupheadertexts[{{KOPF_LINKS}}][{{KOPF_RECHTS}}]
\setupfootertexts[{{FUSS_LINKS}}][{{FUSS_RECHTS}}]
\starttext
