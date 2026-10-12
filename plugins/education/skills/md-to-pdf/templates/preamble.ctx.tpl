% Vorspann für ConTeXt (md-to-pdf). Platzhalter {{...}} setzt scripts/md_to_pdf.py.
\setuppapersize[A4][A4]
\setuplayout[width=middle,height=middle,topspace=2.2cm,bottomspace=2.2cm,backspace={{RAND_CM}}cm,header=0.8cm,footer=0.8cm]
\definefontfamily[main][rm][{{SCHRIFT}}]
\setupbodyfont[main,{{GROESSE}}]
% Codeblöcke (pandoc: \starthighlighting) mit Rahmen und Hintergrund, analog zu minted. Muss nach pandocs \definetyping stehen.
\setuptyping[highlighting][before={\startframed[frame=on,framecolor=darkgray,rulethickness=0.5pt,offset=0.8ex,background=color,backgroundcolor=lightgray,align=normal]},after={\stopframed}]
\setupinteraction[state=stop]
\setuppagenumbering[location={footer,right}]
\setupheader[state=start]
\setupfooter[state=start]
\setupheadertexts[{{KOPF_LINKS}}][{{KOPF_RECHTS}}]
\setupfootertexts[{{FUSS_LINKS}}][{{FUSS_RECHTS}}]
\starttext
