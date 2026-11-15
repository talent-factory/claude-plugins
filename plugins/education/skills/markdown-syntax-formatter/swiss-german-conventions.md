# Swiss German Orthography Conventions

Swiss High German (Schweizer Hochdeutsch) conventions for German-language Markdown.

## Rules

- **No Eszett.** Replace every `ß` with `ss`: muß → muss, groß → gross, Straße → Strasse, heißt → heisst, übermäßig → übermässig.
- **Real umlauts, no digraphs.** `ä ö ü Ä Ö Ü`, never `ae oe ue Ae Oe Ue`. A digraph is converted only when it stands for a single umlaut vowel: "ue" in "abenteuerlich" or "Steuerung" belongs to two morphemes and stays.

## Where it applies

Apply to headings, body text, list items, table cells, blockquotes, image alt text, link text and Markdown comments.

Leave unchanged: code blocks (fenced and indented), inline code, URLs and file paths, technical identifiers (variables, classes, endpoints), proper nouns and brand names, and external quotations (add a note if the source uses Eszett).

## Recognising German text

German function words (der, die, das, und, ist, mit, von, für), umlauts or Eszett, and the file path or metadata. If it is unclear, ask which language the document or section is in.
