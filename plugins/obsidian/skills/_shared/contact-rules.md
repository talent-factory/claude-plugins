# Contact Validation Rules

Deterministische Regeln für `30 Persons` und `35 Companies`. Referenz für den
Fallback, wenn `contacts.py` mangels PyYAML mit Exit-Code 2 abbricht.

Geschrieben wird ausschliesslich über `contacts.py --migrate --alias-map <datei>
--apply`. Frontmatter von Hand zu editieren ist nicht vorgesehen: der
chirurgische Editor ersetzt nur die berührten Schlüssel und lässt jede andere
Zeile byteidentisch, ein Neu-Rendern durch PyYAML schreibt dagegen 600 der 1260
Personenseiten um.

## Blinde Flecken

Was die Regeln nicht abdecken — bei jedem Report mitnennen, damit eine niedrige
Fundzahl nicht als geprüft missverstanden wird:

- **`frontmatter` prüft nur `30 Persons`.** Für Firmenseiten gibt es keine
  Frontmatter-Regel. `query-drift` und `orphan-company` sehen von einer
  Firmenseite nur den Query-Block bzw. die eingehenden Links.
- **Zwei Firmenseiten kommen in keiner Regel vor.** `BiCT AG` und
  `SYTRAX Intelligence AG` wurden bei der Migration abgelehnt (mehrdeutig
  abgegrenztes Frontmatter) und erzeugen in keiner Regel ein Finding — auch
  nicht in `orphan-company`. Wer sie prüfen will, muss sie von Hand ansehen.
- **`company_legacy` erzeugt kein Finding.** Siehe eigenen Abschnitt unten.

## frontmatter

- `tags` enthält `person` — minor, autofixable
- `kind` ∈ `{contact, student, alumni}` — minor, autofixable
- `company` ist eine Liste (nicht Skalar) — minor, autofixable
  (eine leere/fehlende `company` wird als `company:` (null) geschrieben, nicht
  als `company: []` — das zaehlt als leere Liste)
- Fehlendes oder defektes YAML — critical, nicht autofixable

## slug-drift

Zwei Formen, beide minor:

- **Freitext statt Wikilink** — ein `company:`-Wert ganz ohne `[[…]]`.
  Autofixable nur, wenn der Slug genau eine Firmenseite trifft.
- **Enthält einen Wikilink, ist aber keiner** — z. B.
  `"[[BEDAG Informatik AG]] (bis 2024)"`. Nie autofixable: welcher Teil die
  Firma benennt, lässt sich nicht entscheiden, und der Zusatz trägt Bedeutung,
  die das Werkzeug nicht erhalten kann. Wird gemeldet, nie umgeschrieben.

Was als Wikilink gilt, entscheidet ein einziges Prädikat (`is_wikilink`), das
Lese- und Schreibpfad teilen. Vorher fragte der Lesepfad „enthält einen
Wikilink“ und der Schreibpfad „ist ein Wikilink“ — die zweite Form oben war
dadurch für alle Regeln sauber und wurde bei der Migration nach
`company_legacy` verschoben.

## deadlinks

`company:`- oder `topics:`-Wikilink ohne Zieldatei — critical, nicht
autofixable.

## query-drift

Ein Block, der `contains(company, this.file.link)` bereits enthält, ist migriert
und erzeugt kein Finding. Sonst gilt, in dieser Reihenfolge:

- **Hartkodierter Slug** in erkannter Form — `contains(company, "x")` oder
  `company = "x"`. Minor; autofixable nur bei `dataview`, weil die Bases-Syntax
  kein geprüftes Selbstreferenz-Äquivalent hat.
- **`company` in nicht umschreibbarer Form** — minor, nicht autofixable,
  manuelle Prüfung. Hierher fallen negierte Prädikate (`!contains(...)`),
  Vergleiche (`company != "x"`), Funktionsformen wie `startsWith(company, …)`
  und die Bases-Methodensyntax `company.contains("x")`.
- **Kein `company`-Prädikat** — minor, nicht autofixable, manuelle Prüfung.
  Tag-basierte Queries.

Ein Code-Fence wird auch mit Rand erkannt (` ```base `, Tab, CRLF). Bis das
korrigiert war, machte ein einziger Fence mit Leerzeichen die *ganze* Datei
unsichtbar: 10 Firmenseiten trugen `company.contains(...)`, gesehen wurden 5,
und die 5 unsichtbaren liessen 17 Personen in leer gerenderten Tabellen
stehen, während die Regel Entwarnung gab.

Das negierte Prädikat ist der Grund für den Negative-Lookbehind im Regex: Ein
`!contains(company, "x")` auf `contains(company, this.file.link)` umzuschreiben
würde die Bedeutung der Query umkehren.

## orphan-company

Firmenseite ohne verweisende Person — minor, nicht autofixable. Erlaubt, aber
soll absichtlich sein.

## dupes

Gleiche E-Mail oder gleicher normalisierter Name auf zwei Seiten — minor, nicht
autofixable. `email:` wird flach gelesen, Liste wie Skalar: 102 der 308
Personenseiten mit E-Mail speichern sie als Liste, und eine Liste als Ganzes
zu stringifizieren machte sie mit einem Skalar unvergleichbar.

## company_legacy

Kein Finding, sondern der Arbeitsvorrat. Stand 2026-07-30: 103 Personenseiten
tragen den Schlüssel — die Zahl soll schrumpfen, prüfen statt zitieren.

Er enthält den Wert, den `company:` vor der Migration hatte, für Slugs, die
auf keine existierende Firmenseite aufgelöst werden konnten — entweder weil es
die Seite nicht gibt, oder weil die Alias-Map bewusst `target: null` sagt. Das
Werkzeug rät nicht: statt eine plausible Firma zu erfinden, hebt es den
Originalwert auf und leert `company:`.

Solange der Schlüssel gesetzt ist, fehlt die Person in der Mitarbeitertabelle
ihrer Firma. Das ist der Preis dafür, nicht zu raten, und der Grund, warum der
Vorrat sichtbar bleiben soll.

**Der Vorrat lässt sich derzeit nicht automatisch abarbeiten.** Nachgeprüft am
2026-07-30: Ist die Firmenseite angelegt und der Slug in der Alias-Map von
`null` auf den Seitennamen gesetzt, meldet ein erneuter `--migrate`-Lauf für
diese Person trotzdem `touched: []`. `migrate_person` liest nur `company:`,
und das ist leer — `company_legacy` wird von keinem Schreibpfad gelesen.

Wer den Vorrat abarbeiten will, muss den Slug zuerst wieder in `company:`
eintragen und die Migration danach laufen lassen. Das ist die eine Stelle, an
der eine Handänderung am Frontmatter unvermeidlich ist; sie betrifft genau
eine Zeile und sollte einzeln und geprüft erfolgen. Angemessener wäre, dass
`contacts.py` beim Migrieren auch `company_legacy` gegen die Alias-Map prüft
— diese Funktion gibt es noch nicht.
