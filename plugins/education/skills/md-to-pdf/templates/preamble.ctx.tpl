% Vorspann für ConTeXt (md-to-pdf). Platzhalter {{...}} setzt scripts/md_to_pdf.py.
\setuppapersize[A4][A4]
\setuplayout[width=middle,height=middle,topspace=2.2cm,bottomspace=2.2cm,backspace={{RAND_CM}}cm,header=0.8cm,footer=0.8cm]
\definefontfamily[main][rm][{{SCHRIFT}}]
% Code (Hervorhebung und \type{}) braucht eine dichtengleiche Schrift, sonst stimmen Einrückungen nicht.
\definefontfamily[main][tt][Latin Modern Typewriter][features=none]
% Pandoc legt Codeblöcke in ein Shaded-Rahmen. Beim Seitenumbruch ragt dann die letzte Zeile in die Fusszeile.
\definetyping [highlighting] [escape=yes, before={}, after={}]
\setupbodyfont[main,{{GROESSE}}]
\setupinteraction[state=stop]
\setuppagenumbering[location={footer,right}]
\setupheader[state=start]
\setupfooter[state=start]
\setupheadertexts[{{KOPF_LINKS}}][{{KOPF_RECHTS}}]
\setupfootertexts[{{FUSS_LINKS}}][{{FUSS_RECHTS}}]
\starttext
