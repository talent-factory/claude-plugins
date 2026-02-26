# Best Practices fuer Merge-Konflikte

## Praevention

### Regelmaessig rebasen

**Prinzip**: Je haeufiger der Feature-Branch aktualisiert wird, desto kleiner sind die Konflikte.

```bash
# Taeglich oder vor jedem groesseren Commit
git fetch origin
git merge origin/develop
```

**Empfohlener Rhythmus**:
- **Kurze Tasks** (1-2 Tage): Einmal vor PR-Erstellung
- **Mittlere Tasks** (3-5 Tage): Alle 2 Tage
- **Lange Tasks** (1+ Wochen): Taeglich

### Kleine, fokussierte PRs

**Warum**: Weniger geaenderte Dateien = weniger Konfliktpotenzial

| PR-Groesse | Dateien | Konfliktrisiko |
|------------|---------|----------------|
| Klein | 1-5 | Niedrig |
| Mittel | 6-15 | Mittel |
| Gross | 16+ | Hoch |

**Regel**: Maximal eine logische Aenderung pro PR. Lieber 3 kleine PRs als 1 grosser.

### Team-Kommunikation

**Vor paralleler Arbeit an denselben Dateien**:
- Im Team absprechen wer welche Dateien aendert
- Gemeinsame Dateien (z.B. `__init__.py`, `routes.py`) als Konflikt-Hotspots identifizieren
- Abhaengigkeiten zwischen Tasks klar definieren (im STATUS.md oder Linear)

### Task-Abhaengigkeiten beachten

**Bei EPIC-Implementierung mit Worktrees**:

```
task-001 (DB Schema)
    ├── task-002 (Templates) → brancht von task-001
    ├── task-003 (Provider)  → brancht von task-001
    └── task-004 (API)       → brancht von task-001 + task-002 + task-003
                                ↑ Hohes Konfliktpotenzial!
```

**Empfehlung**: Tasks mit mehreren Abhaengigkeiten sequentiell nach deren Merge bearbeiten, nicht parallel.

## Loesungs-Reihenfolge

### Empfohlene Reihenfolge

Konflikte immer in dieser Reihenfolge loesen (einfach → komplex):

```
1. Lock-Files        → Automatisch (regenerieren)
2. Konfiguration     → Halb-automatisch (Union bilden)
3. Quellcode         → Semantische Analyse
4. Tests             → Zusammenfuehren + validieren
```

**Begruendung**:
- Lock-Files sind deterministisch regenerierbar
- Konfiguration ist meist additiv (neue Dependencies)
- Quellcode erfordert Verstaendnis der Logik
- Tests validieren die korrekte Aufloesung der vorherigen Schritte

### Innerhalb von Quellcode

```
1. __init__.py       → Meist nur Import-Unions
2. Modelle/Schemas   → Datenstrukturen zuerst
3. Services/Logik    → Abhaengig von Modellen
4. API-Routes        → Abhaengig von Services
5. Frontend-Code     → Abhaengig von API
```

## Worktree-spezifische Hinweise

### SubscribeFlow-Projekt

Das Projekt verwendet Git Worktrees fuer parallele Task-Implementierung:

```
.worktrees/
├── task-009/    # Integration Tests
├── task-012/    # Admin UI
└── task-013/    # E2E Tests
```

**Haeufige Konflikt-Hotspots in diesem Projekt**:

| Datei | Warum | Haeufigkeit |
|-------|-------|-------------|
| `src/subscribeflow/api/auth/__init__.py` | Jeder neue API-Endpoint importiert Auth | Hoch |
| `src/subscribeflow/api/routes/v1/__init__.py` | Route-Registrierung fuer neue Endpoints | Hoch |
| `pyproject.toml` | Neue Dependencies pro Task | Mittel |
| `alembic/versions/` | Neue Migrationen pro Task | Mittel |
| `apps/web/src/routes/admin/` | Neue Admin-Seiten | Mittel |

**Empfehlung**: Nach jedem Task-Merge in `develop` alle aktiven Worktrees aktualisieren:

```bash
# In jedem aktiven Worktree ausfuehren
cd .worktrees/task-XXX
git fetch origin
/git-workflow:resolve-conflicts --target develop
```

### Worktree-Erstellung nach Abhaengigkeits-Merge

Wenn ein abhaengiger Task gemerged wurde, den Worktree auf dem neuesten Stand erstellen:

```bash
# Statt von develop branchen (veraltet)
git worktree add -b feature/task-009 .worktrees/task-009 develop

# Besser: Erst develop aktualisieren
git fetch origin
git worktree add -b feature/task-009 .worktrees/task-009 origin/develop
```

## Anti-Patterns

### Blind Ours/Theirs verwenden

**Problem**: `--strategy ours` oder `--strategy theirs` ohne die Konflikte zu verstehen

```bash
# ❌ Schlecht: Blind alles ueberschreiben
/git-workflow:resolve-conflicts --strategy theirs
```

**Risiko**: Features oder Bugfixes gehen verloren

**Besser**: Zuerst analysieren, dann gezielt entscheiden

```bash
# ✅ Gut: Erst analysieren
/git-workflow:resolve-conflicts --dry-run

# Dann gezielt loesen
/git-workflow:resolve-conflicts --strategy smart
```

### Conflict-Marker manuell entfernen

**Problem**: `<<<<<<<`, `=======`, `>>>>>>>` manuell loeschen ohne den Code zu verstehen

```python
# ❌ Schlecht: Einfach alles behalten
from .auth import router as auth_router
from .email import router as email_router
from .auth import router as auth_router  # Duplikat!
from .campaigns import router as campaign_router
```

**Besser**: Semantisch verstehen was beide Seiten wollen und korrekt zusammenfuehren.

### Tests ueberspringen

**Problem**: `--no-tests` verwenden um schneller fertig zu werden

**Risiko**: Merge sieht syntaktisch korrekt aus, ist aber semantisch falsch

```bash
# ❌ Schlecht: Tests ueberspringen und sofort pushen
/git-workflow:resolve-conflicts --no-tests
git push

# ✅ Gut: Tests laufen lassen
/git-workflow:resolve-conflicts
# Tests bestanden → sicher pushen
```

**Ausnahme**: `--no-tests` ist akzeptabel wenn:
- Nur Lock-Files betroffen sind
- Die Test-Suite sehr lang laeuft und man spaeter testen will
- Man den Merge lokal testen moechte bevor man committet

### Merge-Konflikte aufschieben

**Problem**: Konflikte ignorieren und spaeter loesen

```bash
# ❌ Schlecht: Merge abbrechen und "spaeter" loesen
git merge --abort
# ... Tage vergehen, Konflikte werden groesser ...
```

**Besser**: Sofort loesen, solange der Kontext frisch ist.

### Force-Push nach Merge-Aufloesung

**Problem**: `git push --force` nach Konfliktaufloesung in einem shared Branch

**Risiko**: Anderer Teammitglieder verlieren ihre Arbeit

```bash
# ❌ Schlecht
git push --force origin develop

# ✅ Gut: Nur auf Feature-Branches force-pushen
git push --force origin feature/task-009
```

## Checkliste nach Konfliktaufloesung

- [ ] Keine Conflict-Marker (`<<<<<<<`) in Dateien
- [ ] Keine duplizierten Imports oder Funktionen
- [ ] Lock-Files regeneriert (nicht manuell bearbeitet)
- [ ] Tests bestanden
- [ ] Linting bestanden
- [ ] Commit-Nachricht beschreibt die aufgeloesten Konflikte
- [ ] Code-Logik beider Seiten korrekt integriert
- [ ] Keine versehentlich geloeschten Features
