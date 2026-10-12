% Vorspann für ConTeXt (md-to-pdf). Platzhalter {{...}} setzt scripts/md_to_pdf.py.
\setuppapersize[A4][A4]
\setuplayout[width=middle,height=middle,topspace=2.2cm,bottomspace=2.2cm,backspace={{RAND_CM}}cm,header=0.8cm,footer=0.8cm]
\definefontfamily[main][rm][{{SCHRIFT}}]
% Code (Hervorhebung und \type{}) braucht eine dichtengleiche Schrift, sonst stimmen Einrückungen nicht.
\definefontfamily[main][tt][Latin Modern Typewriter][features=none]
\setupbodyfont[main,{{GROESSE}}]
% Codeblöcke als umbrechbare Tabelle mit grauem Hintergrund (md_to_pdf.py, codeblock_tabelle).
\definecolor[codegrau][s=0.93]
\setupframedtable[frame=off]
\setupframedtablerow[frame=off]
\setupframedtablecolumn[1][width=\hsize,frame=off,background=color,backgroundcolor=codegrau,align=normal,strut=no]
% Listing-Nummer und Titel vor jedem Codeblock (md_to_pdf.py, codeblock_beschriftung), Abstände vor und nach dem Block.
\newcount\mdCodeNr
\def\mdListing#1{\blank[big]\advance\mdCodeNr by 1\par\noindent{\bf Listing \the\mdCodeNr\ifx\relax#1\relax\else: #1\fi}\par\blank[big]}
\setupinteraction[state=stop]
\setuppagenumbering[location={footer,right}]
\setupheader[state=start]
\setupfooter[state=start]
\setupheadertexts[{{KOPF_LINKS}}][{{KOPF_RECHTS}}]
\setupfootertexts[{{FUSS_LINKS}}][{{FUSS_RECHTS}}]
\starttext
