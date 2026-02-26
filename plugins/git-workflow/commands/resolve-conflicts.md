---
description: Analysiere und loese Merge-Konflikte intelligent mit automatischer Test-Validierung
category: develop
argument-hint: "[PR-Nr|Branch] [--target develop] [--dry-run] [--no-tests] [--strategy ours|theirs|smart]"
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Glob
  - Grep
---

# Claude Command: Merge-Konflikte loesen

Analysiere und loese Merge-Konflikte intelligent mit automatischer Ursachenanalyse, semantischer Code-Zusammenfuehrung und Test-Validierung.

**Alle Ausgaben und Commit-Nachrichten werden in Deutsch verfasst.**

## Verwendung

Standard (aktuellen Branch mit Target mergen):

```bash
/git-workflow:resolve-conflicts
```

Mit Optionen:

```bash
/git-workflow:resolve-conflicts --target develop          # Ziel-Branch (Standard: develop)
/git-workflow:resolve-conflicts --dry-run                 # Nur Analyse, keine Aenderungen
/git-workflow:resolve-conflicts --no-tests                # Tests ueberspringen
/git-workflow:resolve-conflicts --strategy smart          # Strategie: smart (Standard), ours, theirs
/git-workflow:resolve-conflicts feature/task-009          # Spezifischen Branch angeben
/git-workflow:resolve-conflicts 42                        # PR-Nummer angeben
```

## Parameter

| Parameter | Beschreibung | Standard |
|-----------|-------------|----------|
| `[Branch\|PR-Nr]` | Zu mergender Branch oder PR-Nummer | Aktueller Branch |
| `--target` | Ziel-Branch von dem gemerged wird | `develop` |
| `--dry-run` | Nur analysieren, keine Aenderungen | `false` |
| `--no-tests` | Test-Ausfuehrung ueberspringen | `false` |
| `--strategy` | Loesungsstrategie: `smart`, `ours`, `theirs` | `smart` |

## Workflow

### Schritt 1: Umgebung erkennen

- Pruefe ob wir in einem Worktree sind: `git rev-parse --show-toplevel` und `git worktree list`
- Pruefe auf uncommitted Changes: `git status --porcelain`
  - Falls vorhanden: **HALT** - Benutzer muss zuerst committen oder stashen
- Erkenne Projekttyp anhand vorhandener Dateien:
  - `pyproject.toml` / `setup.py` → Python
  - `package.json` → Frontend/Node
  - `pom.xml` / `build.gradle` → Java
- Merke erkannten Projekttyp fuer Schritte 7-8

### Schritt 2: Eingabe parsen

- **Kein Argument**: Verwende aktuellen Branch, merge vom `--target` (Standard: `develop`)
- **Branch-Name** (z.B. `feature/task-009`): Checke diesen Branch aus
- **PR-Nummer** (z.B. `42`): Ermittle Branch via `gh pr view 42 --json headRefName -q .headRefName`
- Parse alle Flags: `--target`, `--dry-run`, `--no-tests`, `--strategy`

### Schritt 3: Konflikte erkennen

```bash
# Remote aktualisieren
git fetch origin

# Merge-Base bestimmen
git merge-base HEAD origin/<target>

# Nicht-destruktiven Merge starten
git merge --no-commit --no-ff origin/<target>
```

- Falls **keine Konflikte**: Merge abbrechen (`git merge --abort`), Meldung ausgeben, fertig
- Falls **Konflikte**: Konfliktdateien sammeln via `git diff --name-only --diff-filter=U`
- Ausgabe: Tabelle mit allen Konfliktdateien und ihrer Kategorie

### Schritt 4: Konflikt-Ursachen analysieren

Fuer jede Konfliktdatei:

1. **Merge-Base analysieren**: `git diff <merge-base>..HEAD -- <datei>` (unsere Aenderungen)
2. **Target-Aenderungen**: `git diff <merge-base>..origin/<target> -- <datei>` (ihre Aenderungen)
3. **Ursache identifizieren**:
   - Gleiche Zeilen geaendert → Inhaltlicher Konflikt
   - Benachbarte Aenderungen → Kontextkonflikt
   - Strukturelle Aenderungen (Imports, Exports) → Additive Zusammenfuehrung moeglich
4. **PR/Commit-Quelle identifizieren**: `git log --oneline <merge-base>..origin/<target> -- <datei>`

**Ausgabe**:

```
Datei                          | Ursache              | Quelle           | Risiko
-------------------------------|----------------------|------------------|--------
src/api/auth/__init__.py       | Import-Erweiterung   | task-006 + 007   | Niedrig
src/api/routes/v1/__init__.py  | Route-Registrierung  | task-006 + 007   | Niedrig
alembic/versions/...           | Revision-Chain       | task-003         | Mittel
src/services/email.py          | Logik-Aenderung      | task-007         | Hoch
```

**Bei `--dry-run`**: Nach diesem Schritt `git merge --abort` ausfuehren und Bericht anzeigen. FERTIG.

### Schritt 5: Konflikte loesen

Konflikte werden in folgender Reihenfolge geloest (einfach → komplex):

#### 5a: Lock-Files (`uv.lock`, `bun.lockb`, `package-lock.json`)

```bash
git checkout --theirs <lock-file>
```

Anschliessend Lock-File regenerieren:
- Python: `uv lock`
- Frontend: `bun install` oder `npm install`

Falls Regenerierung fehlschlaegt: **HALT** und Benutzer informieren.

#### 5b: Konfigurationsdateien (`pyproject.toml`, `package.json`, `tsconfig.json`)

- **Union bilden**: Beide Seiten der Dependency-Listen zusammenfuehren
- Duplikate entfernen, hoehere Version bevorzugen
- Datei lesen, Conflict-Marker verstehen, zusammengefuehrte Version schreiben

#### 5c: Quellcode-Dateien

Je nach `--strategy`:

- **`smart`** (Standard): Semantische Analyse
  - **Import-Bloecke**: Beide Import-Listen zusammenfuehren, sortieren
  - **Additive Aenderungen** (z.B. neue Funktionen, neue Routes): Beide Seiten behalten
  - **Gleiche Stelle geaendert**: Kontext analysieren, unsere Logik priorisieren, Target-Aenderungen integrieren
  - **Strukturelle Konflikte**: Architektur verstehen, korrekt zusammenfuehren
- **`ours`**: Bei Konflikten unsere Version behalten (`git checkout --ours <datei>`)
- **`theirs`**: Bei Konflikten deren Version behalten (`git checkout --theirs <datei>`)

#### 5d: Spezialfall Alembic-Migrationen

- `down_revision`-Chain linearisieren
- Pruefen ob mehrere Heads entstehen: `alembic heads`
- Falls Multiple Heads: Merge-Migration erstellen

#### 5e: Spezialfall Architektonische Konflikte

Wenn eine Datei **grundlegend umstrukturiert** wurde (z.B. Klasse aufgeteilt, API geaendert):
- **HALT**: Benutzer fragen wie die Zusammenfuehrung aussehen soll
- Optionen praesentieren mit Code-Auszuegen beider Seiten
- Erst nach Benutzer-Entscheidung fortfahren

#### 5f: Test-Dateien

- Beide Test-Suites zusammenfuehren
- Test-Importe und Fixtures aus beiden Seiten behalten
- Doppelte Test-Funktionen erkennen und Benutzer fragen

### Schritt 6: Syntaktische Validierung

Nach der Aufloesung jeder Datei:

```bash
# Keine Conflict-Marker uebrig?
grep -rn "<<<<<<< \|======= \|>>>>>>> " <datei>

# Python-Syntax gueltig?
python -c "import ast; ast.parse(open('<datei>').read())"

# TypeScript/JavaScript-Syntax gueltig?
# (nur pruefen wenn tsc/node verfuegbar)
```

Falls Conflict-Marker gefunden: Datei erneut analysieren und loesen.
Falls Syntax ungueltig: Fehler anzeigen und Datei erneut bearbeiten.

### Schritt 7: Tests ausfuehren (wenn nicht `--no-tests`)

Basierend auf erkanntem Projekttyp:

```bash
# Python
uv run pytest

# Frontend
cd apps/web && bun run test:run

# Java
mvn test
```

- Falls **Tests bestanden**: Weiter zu Schritt 8
- Falls **Tests fehlgeschlagen**: Fehler analysieren und versuchen zu beheben
  - Maximal 2 Reparaturversuche
  - Danach: **HALT** und Benutzer informieren mit Fehlerbericht

### Schritt 8: Linting

```bash
# Python
uv run ruff check . --fix
uv run ruff format .

# Frontend
cd apps/web && bun run lint
```

Falls Linting-Fehler: Auto-Fix anwenden, bei verbleibenden Fehlern Benutzer informieren.

### Schritt 9: Bericht generieren

Zusammenfassende Tabelle ausgeben:

```
Merge-Konflikt-Bericht
======================

Target:    origin/develop → feature/task-009
Konflikte: 4 Dateien
Strategie: smart

Datei                          | Strategie    | Begruendung                     | Risiko
-------------------------------|--------------|----------------------------------|--------
uv.lock                       | regeneriert  | Lock-File neu generiert          | Kein
src/api/auth/__init__.py       | smart/union  | Imports aus beiden Tasks vereint | Niedrig
src/api/routes/v1/__init__.py  | smart/union  | Routes additiv zusammengefuehrt  | Niedrig
src/services/email.py          | smart/ours   | Unsere Logik priorisiert         | Mittel

Tests:  ✅ 47 bestanden, 0 fehlgeschlagen
Lint:   ✅ Keine Fehler
```

### Schritt 10: Commit und Push

1. **Alle aufgeloesten Dateien stagen**: `git add <dateien>`
2. **Merge abschliessen** mit aussagekraeftiger Nachricht:

```bash
git commit -m "$(cat <<'EOF'
🔀 merge: Integriere develop in feature/task-009

Konflikte in 4 Dateien aufgeloest:
- auth/__init__.py: Import-Union aus task-006 + task-007
- routes/v1/__init__.py: Route-Registrierung zusammengefuehrt
- services/email.py: Logik-Merge mit Priorisierung unserer Aenderungen
- uv.lock: Regeneriert
EOF
)"
```

3. **Push anbieten**: Benutzer fragen ob gepusht werden soll
   - Bei Bestaetigung: `git push origin <branch>`

**WICHTIG:** Commit-Nachrichten enthalten KEINE automatischen Signaturen (kein Co-Authored-By, kein Generated with Claude Code).

## Fehlerbehandlung

### Merge bereits aktiv

```
⚠️ Ein Merge ist bereits aktiv. Optionen:
1. Merge fortsetzen: git merge --continue
2. Merge abbrechen: git merge --abort
```

Benutzer fragen welche Aktion gewuenscht ist.

### Kein Remote-Branch

```
❌ Branch 'origin/<target>' nicht gefunden.
   Verfuegbare Remote-Branches: git branch -r
```

### Worktree ohne Remote-Tracking

```
⚠️ Kein Tracking-Branch gesetzt.
   Setze Tracking: git branch --set-upstream-to=origin/<branch>
```

### Lock-File-Regenerierung fehlgeschlagen

```
❌ Lock-File konnte nicht regeneriert werden.
   Bitte manuell ausfuehren: uv lock / bun install
   Dann erneut: /git-workflow:resolve-conflicts --no-tests
```

### Tests fehlgeschlagen nach Aufloesung

```
❌ Tests fehlgeschlagen nach 2 Reparaturversuchen.
   Fehlgeschlagene Tests:
   - test_email_send: AssertionError (expected 200, got 404)
   - test_auth_flow: ImportError (missing module)

   Bitte manuell pruefen und dann committen.
   Merge-Status: Alle Konflikte aufgeloest, nicht committed.
```

## Weitere Informationen

- **Loesungsstrategien**: [strategies.md](../references/resolve-conflicts/strategies.md)
- **Best Practices**: [best-practices.md](../references/resolve-conflicts/best-practices.md)
- **Troubleshooting**: [troubleshooting.md](../references/resolve-conflicts/troubleshooting.md)
