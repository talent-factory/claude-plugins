% Kopf-/Fusszeile und Typografie (md-to-pdf, Engine xelatex).
% Platzhalter {{...}} werden von scripts/md_to_pdf.py ersetzt.
\usepackage{fancyhdr}
\usepackage{lastpage}
\usepackage{xcolor}
\usepackage{array}
\usepackage{longtable}
\usepackage{booktabs}
\usepackage{etoolbox}
\usepackage{newunicodechar}
\definecolor{fhgrey}{gray}{0.4}

\newcommand{\dokKopfLinks}{\small\textcolor{fhgrey}{{{KOPF_LINKS}}}}
\newcommand{\dokKopfRechts}{\small\textcolor{fhgrey}{{{KOPF_RECHTS}}}}
\newcommand{\dokFussLinks}{\small\textcolor{fhgrey}{{{FUSS_LINKS}}}}
\newcommand{\dokFussRechts}{\small\textcolor{fhgrey}{Seite \thepage{} von \pageref{LastPage}}}

\pagestyle{fancy}
\fancyhf{}
\setlength{\headheight}{14pt}
\fancyhead[L]{\dokKopfLinks}
\fancyhead[R]{\dokKopfRechts}
\fancyfoot[L]{\dokFussLinks}
\fancyfoot[R]{\dokFussRechts}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0.4pt}
\fancypagestyle{plain}{%
  \fancyhf{}%
  \fancyhead[L]{\dokKopfLinks}%
  \fancyhead[R]{\dokKopfRechts}%
  \fancyfoot[L]{\dokFussLinks}%
  \fancyfoot[R]{\dokFussRechts}%
  \renewcommand{\headrulewidth}{0.4pt}%
  \renewcommand{\footrulewidth}{0.4pt}}

\setlength{\parskip}{0.4em}
\setlength{\parindent}{0pt}
\renewcommand{\arraystretch}{1.15}
\setlength{\LTpre}{6pt}
\setlength{\LTpost}{10pt}
\AtBeginEnvironment{longtable}{\footnotesize\setlength{\tabcolsep}{4pt}}
\AtBeginEnvironment{tabular}{\footnotesize\setlength{\tabcolsep}{4pt}}

\usepackage{fontspec}
\setmainfont{{{SCHRIFT}}}[Ligatures=TeX]
{{FALLBACK_DEF}}
