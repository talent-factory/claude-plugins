# Loesungsstrategien fuer Merge-Konflikte

## Strategie-Uebersicht

Der `/git-workflow:resolve-conflicts` Command unterstuetzt drei Strategien:

| Strategie | Beschreibung | Anwendungsfall |
|-----------|-------------|----------------|
| `smart` | Semantische Analyse und intelligente Zusammenfuehrung | Standard, beste Ergebnisse |
| `ours` | Bei Konflikten unsere Version behalten | Feature-Branch hat Vorrang |
| `theirs` | Bei Konflikten deren Version behalten | Target-Branch hat Vorrang |

## Smart-Strategie: Entscheidungsbaum

Die Smart-Strategie analysiert jeden Konflikt individuell und waehlt die beste Aufloesung. Der Entscheidungsbaum hat 5 Stufen:

### Stufe 1: Generierte Dateien

**Erkennung**: Lock-Files, Build-Artefakte, generierte Typen

```
uv.lock, bun.lockb, package-lock.json, yarn.lock
*.generated.ts, *.generated.py
```

**Strategie**: `checkout --theirs` + Regenerierung

**Begruendung**: Generierte Dateien werden aus Quelldateien abgeleitet. Nach der Aufloesung aller Quellkonflikte werden sie neu generiert, wodurch beide Seiten korrekt abgebildet werden.

### Stufe 2: Additive Aenderungen

**Erkennung**: Beide Seiten fuegen neue Elemente hinzu, ohne bestehende zu aendern

Typische Faelle:
- **Import-Bloecke**: Neue Imports auf beiden Seiten
- **Route-Registrierungen**: Neue API-Endpunkte
- **Konfigurationslisten**: Neue Dependencies, neue Plugins
- **Export-Listen**: Neue Module exportiert

**Strategie**: Union (beide Seiten zusammenfuehren)

```python
# Konflikt in __init__.py
<<<<<<< HEAD
from .auth import router as auth_router
from .email import router as email_router
=======
from .auth import router as auth_router
from .campaigns import router as campaign_router
>>>>>>> origin/develop

# Aufloesung: Union
from .auth import router as auth_router
from .campaigns import router as campaign_router
from .email import router as email_router
```

**Sortierung**: Imports und Listen alphabetisch sortieren fuer Konsistenz.

### Stufe 3: Gleiche Stelle geaendert

**Erkennung**: Beide Seiten aendern denselben Code-Block

**Strategie**: Kontextanalyse

1. **Funktionssignatur geaendert**: Beide Signaturen vergleichen, kompatible Version waehlen
2. **Funktionskoerper geaendert**: Logik beider Seiten verstehen, zusammenfuehren wenn moeglich
3. **Konfligierende Logik**: Unsere Version priorisieren (`ours`), da der Feature-Branch die aktive Arbeit darstellt

```python
# Konflikt: Beide aendern dieselbe Funktion
<<<<<<< HEAD
def send_email(to: str, subject: str, template: str) -> SendResult:
    """Mit Template-Support."""
    rendered = render_template(template)
    return provider.send(to, subject, rendered)
=======
def send_email(to: str, subject: str, body: str, priority: int = 0) -> SendResult:
    """Mit Priority-Support."""
    return provider.send(to, subject, body, priority=priority)
>>>>>>> origin/develop

# Aufloesung: Features zusammenfuehren
def send_email(
    to: str,
    subject: str,
    template: str,
    priority: int = 0,
) -> SendResult:
    """Mit Template- und Priority-Support."""
    rendered = render_template(template)
    return provider.send(to, subject, rendered, priority=priority)
```

### Stufe 4: Strukturelle Aenderungen

**Erkennung**: Eine Seite hat die Dateistruktur geaendert (Klasse aufgeteilt, Modul umbenannt, API refactored)

**Strategie**: Manuelle Intervention empfohlen

- Beide Versionen dem Benutzer zeigen
- Erklaeren welche strukturellen Aenderungen vorgenommen wurden
- Optionen praesentieren:
  1. Unsere Struktur behalten, deren Funktionalitaet integrieren
  2. Deren Struktur uebernehmen, unsere Funktionalitaet integrieren
  3. Benutzer entscheidet manuell

### Stufe 5: Architektonische Konflikte

**Erkennung**: Grundlegende Designentscheidungen divergieren

Beispiele:
- Synchroner vs. asynchroner Code
- Unterschiedliche Datenmodelle
- Verschiedene Dependency-Injection-Patterns

**Strategie**: **HALT** - Immer den Benutzer fragen

Diese Konflikte koennen nicht automatisch geloest werden, da sie architektonische Entscheidungen erfordern.

## Dateityp-spezifische Strategien

### Python-Dateien (`.py`)

| Konflikttyp | Strategie | Details |
|-------------|-----------|---------|
| Import-Block | Union + isort | Alphabetisch, gruppiert nach stdlib/third-party/local |
| `__init__.py` Exports | Union | Alle Exports behalten |
| `__all__` Liste | Union + sortieren | Eintraege zusammenfuehren |
| Funktionssignaturen | Smart-Merge | Parameter aus beiden Seiten |
| Type Hints | Neuere/vollstaendigere behalten | Union-Types wenn noetig |
| Dekoratoren | Beide behalten | Reihenfolge pruefen |

### TypeScript/JavaScript-Dateien (`.ts`, `.tsx`, `.js`, `.jsx`)

| Konflikttyp | Strategie | Details |
|-------------|-----------|---------|
| Import-Block | Union + sortieren | Named Imports zusammenfuehren |
| Interface-Erweiterung | Union | Properties aus beiden Seiten |
| Type-Definitionen | Union-Type | `TypeA \| TypeB` wenn noetig |
| JSX-Komponenten | Kontextanalyse | Props und Children mergen |
| Barrel-Exports (`index.ts`) | Union | Alle Re-Exports behalten |

### JSON/YAML-Dateien

| Konflikttyp | Strategie | Details |
|-------------|-----------|---------|
| `dependencies` | Union, hoehere Version | Beide Dependencies behalten |
| `devDependencies` | Union, hoehere Version | Beide DevDeps behalten |
| `scripts` | Union | Beide Scripts behalten |
| Konfigurationswerte | Target-Version | Konfiguration des Ziel-Branches |
| Array-Werte | Union + deduplizieren | Einzigartige Werte behalten |

### Alembic-Migrationen

| Konflikttyp | Strategie | Details |
|-------------|-----------|---------|
| `down_revision` | Chain linearisieren | Revisionen korrekt verketten |
| Multiple Heads | Merge-Migration | `alembic merge heads` |
| Gleiche Tabelle geaendert | Reihenfolge pruefen | Abhaengigkeiten beachten |

**Alembic-Spezialbehandlung**:

```bash
# Multiple Heads erkennen
alembic heads

# Falls multiple Heads: Merge-Migration erstellen
alembic merge heads -m "merge_migrations"

# Chain validieren
alembic history --verbose
```

### Lock-Files

| Datei | Strategie | Regenerierung |
|-------|-----------|---------------|
| `uv.lock` | `--theirs` + regenerieren | `uv lock` |
| `bun.lockb` | `--theirs` + regenerieren | `bun install` |
| `package-lock.json` | `--theirs` + regenerieren | `npm install` |
| `yarn.lock` | `--theirs` + regenerieren | `yarn install` |
| `Gemfile.lock` | `--theirs` + regenerieren | `bundle install` |

## Ours-Strategie

**Verwendung**: `--strategy ours`

Bei jedem Konflikt wird unsere Version (HEAD) behalten:

```bash
git checkout --ours <datei>
git add <datei>
```

**Anwendungsfaelle**:
- Feature-Branch hat Vorrang und Target-Aenderungen sind irrelevant
- Bewusste Entscheidung, Target-Aenderungen zu ignorieren
- Schnelle Aufloesung wenn Konflikte nur kosmetisch sind

**Risiken**:
- Target-Aenderungen gehen verloren
- Neue Features/Fixes aus dem Target werden nicht integriert
- Kann zu Regressionen fuehren

## Theirs-Strategie

**Verwendung**: `--strategy theirs`

Bei jedem Konflikt wird die Target-Version behalten:

```bash
git checkout --theirs <datei>
git add <datei>
```

**Anwendungsfaelle**:
- Target-Branch (z.B. develop) hat Vorrang
- Eigene Aenderungen sollen ueberschrieben werden
- Rebase-aehnliches Verhalten gewuenscht

**Risiken**:
- Eigene Aenderungen gehen verloren
- Feature-Arbeit muss moeglicherweise wiederholt werden

## Strategie-Auswahl: Empfehlung

```
Merge-Konflikt erkannt
    │
    ├── Lock-File?
    │   └── JA → theirs + regenerieren
    │
    ├── Generierte Datei?
    │   └── JA → theirs + regenerieren
    │
    ├── Nur additive Aenderungen?
    │   └── JA → Union (beide behalten)
    │
    ├── Gleiche Stelle geaendert?
    │   ├── Kompatible Aenderungen? → Smart-Merge
    │   └── Inkompatibel? → Ours (Feature priorisieren)
    │
    ├── Strukturelle Aenderung?
    │   └── JA → Benutzer fragen
    │
    └── Architektonischer Konflikt?
        └── JA → HALT, Benutzer entscheidet
```

**Faustregel**: Im Zweifel `smart` verwenden. Nur `ours`/`theirs` waehlen wenn klar ist, dass eine Seite komplett Vorrang hat.
