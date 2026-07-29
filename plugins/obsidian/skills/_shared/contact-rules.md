# Contact Validation Rules

Deterministische Regeln für `30 Persons` und `35 Companies`. Referenz für den
Fallback, wenn `contacts.py` mangels PyYAML mit Exit-Code 2 abbricht.

## frontmatter

- `tags` enthält `person` — minor, autofixable
- `kind` ∈ `{contact, student, alumni}` — minor, autofixable
- `company` ist eine Liste (nicht Skalar) — minor, autofixable
- Fehlendes oder defektes YAML — critical, nicht autofixable

## slug-drift

Ein `company:`-Wert ohne `[[…]]` — minor, autofixable, sofern die Alias-Map den
Slug eindeutig auflöst.

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
  und die Bases-Methodensyntax `company.contains("x")`. Im Vault sind das
  aktuell 5 Bases-Blöcke.
- **Kein `company`-Prädikat** — minor, nicht autofixable, manuelle Prüfung.
  Tag-basierte Queries; aktuell 3 Stück.

Das negierte Prädikat ist der Grund für den Negative-Lookbehind im Regex: Ein
`!contains(company, "x")` auf `contains(company, this.file.link)` umzuschreiben
würde die Bedeutung der Query umkehren.

## orphan-company

Firmenseite ohne verweisende Person — minor, nicht autofixable. Erlaubt, aber
soll absichtlich sein.

## dupes

Gleiche E-Mail oder gleicher normalisierter Name auf zwei Seiten — minor, nicht
autofixable.
