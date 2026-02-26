# Troubleshooting: Merge-Konflikte

## Merge bereits aktiv

### Problem

```
error: Merging is not possible because you have unmerged files.
fatal: Exiting because of an unresolved conflict.
```

Ein vorheriger Merge wurde nicht abgeschlossen oder abgebrochen.

### Diagnose

```bash
git status
# Zeigt: "You have unmerged paths."
```

### Loesung

**Option 1: Vorherigen Merge abbrechen** (empfohlen wenn unklar)

```bash
git merge --abort
```

Danach `/git-workflow:resolve-conflicts` erneut ausfuehren.

**Option 2: Vorherigen Merge fortsetzen** (wenn Konflikte bereits geloest)

```bash
git add .
git merge --continue
```

## Lock-File-Regenerierung fehlgeschlagen

### Problem

Nach `checkout --theirs` des Lock-Files schlaegt die Regenerierung fehl:

```
error: Failed to build 'package-name'
```

### Diagnose

```bash
# Python
uv lock --verbose

# Frontend
bun install --verbose
```

### Loesungen

**Python (`uv.lock`)**:

1. Pruefen ob `pyproject.toml` korrekt aufgeloest wurde (keine Conflict-Marker)
2. Virtual Environment neu erstellen:

```bash
rm -rf .venv
uv venv
uv sync --all-extras
```

3. Falls spezifisches Package fehlschlaegt: Version-Constraint in `pyproject.toml` pruefen

**Frontend (`bun.lockb` / `package-lock.json`)**:

1. Pruefen ob `package.json` korrekt aufgeloest wurde
2. Cache loeschen und neu installieren:

```bash
# Bun
rm -rf node_modules bun.lockb
bun install

# npm
rm -rf node_modules package-lock.json
npm install
```

3. Falls Versionskonflikt: `package.json` Dependencies pruefen

## Alembic Multiple Heads

### Problem

```
FAILED: Multiple head revisions are present for given argument 'head'
```

Mehrere Alembic-Migrationen haben dieselbe `down_revision`, wodurch die Migrations-Kette verzweigt.

### Diagnose

```bash
# Heads anzeigen
uv run alembic heads

# Vollstaendige History
uv run alembic history --verbose
```

### Loesung

**Option 1: Merge-Migration erstellen** (empfohlen)

```bash
uv run alembic merge heads -m "merge_task_006_and_007_migrations"
```

Dies erstellt eine neue Migration die beide Heads zusammenfuehrt.

**Option 2: down_revision manuell anpassen**

Falls eine Migration logisch nach der anderen kommt:

```python
# In der spaeteren Migration
down_revision = "<revision-id-der-frueheren-migration>"
```

**Validierung**:

```bash
uv run alembic heads       # Sollte nur 1 Head zeigen
uv run alembic upgrade head # Sollte ohne Fehler durchlaufen
```

## TypeScript-Fehler nach Merge

### Problem

```
error TS2305: Module '"./types"' has no exported member 'NewType'.
```

TypeScript-Typen oder Interfaces wurden nicht korrekt zusammengefuehrt.

### Diagnose

```bash
cd apps/web
npx tsc --noEmit 2>&1 | head -50
```

### Haeufige Ursachen und Loesungen

**1. Fehlende Type-Exports**

```typescript
// types/index.ts - Export fehlt
export type { ExistingType } from './existing';
// ❌ Fehlt: export type { NewType } from './new';
```

Loesung: Fehlende Exports hinzufuegen.

**2. Interface-Konflikt**

```typescript
// ❌ Beide Seiten haben Interface erweitert, aber nicht zusammengefuehrt
interface Config {
  featureA: boolean; // Von Branch A
  // featureB fehlt, war in Branch B
}
```

Loesung: Properties aus beiden Seiten zusammenfuehren.

**3. Import-Pfade geaendert**

Falls eine Seite Dateien umstrukturiert hat, muessen Import-Pfade in allen abhaengigen Dateien angepasst werden.

## Verbleibende Conflict-Marker

### Problem

Nach `/git-workflow:resolve-conflicts` sind noch Conflict-Marker in Dateien:

```
<<<<<<< HEAD
...
=======
...
>>>>>>> origin/develop
```

### Diagnose

```bash
grep -rn "<<<<<<< \|======= \|>>>>>>> " src/ apps/ tests/
```

### Loesung

1. Dateien identifizieren die noch Marker enthalten
2. Konflikte manuell analysieren und loesen
3. Marker vollstaendig entfernen
4. Syntax validieren:

```bash
# Python
python -c "import ast; ast.parse(open('datei.py').read())"

# TypeScript
npx tsc --noEmit
```

5. Tests erneut ausfuehren

## Push rejected

### Problem

```
! [rejected]        feature/task-009 -> feature/task-009 (non-fast-forward)
error: failed to push some refs
```

### Ursache

Jemand anderes hat auf denselben Branch gepusht, oder der Branch wurde rebasesd.

### Loesung

**Option 1: Pull und erneut mergen**

```bash
git pull origin feature/task-009
# Falls neue Konflikte: /git-workflow:resolve-conflicts erneut
```

**Option 2: Force-Push** (nur auf eigenen Feature-Branches!)

```bash
# ⚠️ Nur wenn du sicher bist, dass niemand anderes auf diesem Branch arbeitet
git push --force-with-lease origin feature/task-009
```

`--force-with-lease` ist sicherer als `--force`, da es prueft ob der Remote-Branch sich seit dem letzten Fetch geaendert hat.

## Merge-Commit versehentlich erstellt

### Problem

Ein Merge-Commit wurde erstellt, aber die Aufloesung war fehlerhaft.

### Loesung

**Vor dem Push**:

```bash
# Merge-Commit rueckgaengig machen (behaelt Dateien)
git reset --soft HEAD~1

# Oder komplett zuruecksetzen
git reset --hard HEAD~1
```

**Nach dem Push**:

```bash
# Revert erstellt einen neuen Commit der den Merge rueckgaengig macht
git revert -m 1 HEAD
git push
```

## Worktree-Probleme

### Worktree zeigt falschen Branch

```bash
# Worktree-Status pruefen
git worktree list

# Falls falscher Branch: Worktree entfernen und neu erstellen
git worktree remove .worktrees/task-XXX
git worktree add -b feature/task-XXX .worktrees/task-XXX origin/develop
```

### Worktree hat abweichende Git-Config

```bash
# Worktree teilt .git/config mit dem Haupt-Repository
# Aber lokale Aenderungen (z.B. in .env) sind isoliert
```

### Aenderungen zwischen Worktrees uebertragen

Falls ein Worktree Fixes enthaelt die ein anderer braucht:

```bash
# Aus anderem Worktree cherry-picken
cd .worktrees/task-012
git cherry-pick <commit-hash-aus-task-009>
```

## Wiederherstellung

### Zustand vor dem Merge wiederherstellen

```bash
# Wenn Merge noch nicht committed
git merge --abort

# Wenn Merge committed aber nicht gepusht
git reset --hard HEAD~1

# Wenn Merge committed und gepusht
git revert -m 1 <merge-commit-hash>
```

### Reflog als Rettungsanker

Git merkt sich alle Operationen. Falls etwas schiefgeht:

```bash
# Alle Operationen anzeigen
git reflog

# Zu einem bestimmten Zustand zurueckkehren
git reset --hard HEAD@{5}
```

**Wichtig**: Reflog-Eintraege verfallen nach 90 Tagen (Standard).

### Stash als Backup vor Merge

**Empfehlung**: Vor jedem Merge-Versuch einen Stash erstellen:

```bash
# Sicherheitskopie
git stash push -m "Backup vor Merge mit develop"

# Falls Merge schiefgeht
git merge --abort
git stash pop
```

## Hilfe holen

Wenn nichts funktioniert, diese Informationen sammeln:

```bash
# Aktueller Zustand
git status
git log --oneline -10
git diff --stat

# Branch-Information
git branch -vv
git worktree list

# Merge-Status
git merge --no-commit --no-ff origin/develop 2>&1
```

Mit diesen Informationen kann das Problem besser diagnostiziert werden.
