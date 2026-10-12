% Vorspann für ConTeXt, Profil ffhs-thesis (md-to-pdf). Orientiert sich an ffhsthesis.cls:
% A4, 11 pt, serifenlose Schrift, 1.5-facher Zeilenabstand, Seitenränder 3 cm links und rechts,
% Seitenzahl unten zentriert, römisch im Vorspann, arabisch ab dem Hauptteil.
% Platzhalter {{...}} setzt scripts/md_to_pdf.py.
\setuppapersize[A4][A4]
\setuplayout[width=15cm,backspace=3cm,topspace=2.5cm,bottomspace=2.5cm,header=1cm,footer=1cm]
\definefontfamily[main][rm][{{SCHRIFT}}]
\setupbodyfont[main,{{GROESSE}}]
% 1,5-facher Zeilenabstand (Vorlage: onehalfspacing), aus der Schriftgrösse berechnet. Relative Angaben wirken in ConTeXt nicht zuverlässig.
\setupinterlinespace[line={{ZEILENABSTAND}}]
\setupwhitespace[medium]
\setuphead[section,subsection][number=yes]
\setuphead[section][page=yes]
\setupinteraction[state=stop]
\setupheader[state=stop]
\setupfooter[state=start]
\setuppagenumbering[location={footer,middle}]
\setupuserpagenumber[numberconversion=romannumerals]
\mainlanguage[de]

% Unnummerierte Überschrift des Vorspanns. Bewusst ohne Gliederungseintrag, siehe thesis_body in md_to_pdf.py.
\unexpanded\def\ffhsVorspann#1{%
  \page
  {\switchtobodyfont[17.3pt]\bf #1\par}
  \blank[big]
}

% Verzeichnisse (vor dem Hauptteil platziert) und Beginn des Hauptteils mit arabischer Seitenzahl.
% criterium=all: ohne diese Option fehlen im Inhaltsverzeichnis Einträge, die vor der Position stehen.
\unexpanded\def\ffhsVerzeichnisse{%
  \page
  {\switchtobodyfont[17.3pt]\bf Inhaltsverzeichnis\par}
  \blank[big]
  \placecontent[criterium=all]
{{ABBILDUNGEN}}{{TABELLEN}}}
\unexpanded\def\startThesis{%
  \page
  \setupuserpagenumber[numberconversion=numbers]
  \setcounter[userpage][1]
}

\starttext

% Titelseite
\setupfooter[state=stop]
\starttabulate[|p(5cm)|p(10cm)|]
\NC {{LOGO}} \NC \startalignment[flushright]\switchtobodyfont[small]Fernfachhochschule Schweiz\crlf Studiengang {{STUDIENGANG}}\stopalignment \NR
\stoptabulate
\vfill
\startalignment[center]
{\switchtobodyfont[24pt]\bf {{TITEL}}\par}
{{UNTERTITEL}}
\blank[2*big]
{{TITELBILD}}
\blank[2*big]
{{DOKUMENTTYP}} im Studiengang {{STUDIENGANG}}
\blank[big]
von
\blank[small]
{\bf {{AUTOR}}}
\stopalignment
\vfill
\starttabulate[|p(7.5cm)|p(7.5cm)|]
\NC \startalignment[flushleft]Eingereicht bei:\crlf\blank[small]{{EINGEREICHT_BEI}}\stopalignment
\NC \startalignment[flushleft]{{REFERENT_ROLLE}}:\crlf\blank[small]{{REFERENT}}\stopalignment \NR
\stoptabulate
\blank[2*big]
\startalignment[center]{{WOHNORT}}, {{DATUM}}\stopalignment

{{WIDMUNG}}

\setupfooter[state=start]
\page
