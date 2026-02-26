# Commit-Workflow Integration

Der `/git-workflow:create-pr` Command integriert sich mit dem `/git-workflow:commit` Command für professionelle Commits.

## Workflow-Übersicht

```text
Aktueller Branch prüfen
        │
        ├─ Geschützt (main/master/develop)?
        │       │
        │       └─ JA → Neuer Branch MUSS erstellt werden
        │
        └─ Feature-Branch?
                │
                └─ NEIN → Verwende aktuellen Branch
                          │
Uncommitted Changes?      │
        │                 │
        ├─ JA  → Rufe /commit auf
        │           │
        │           ├─ Pre-Commit Checks
        │           ├─ Staging
        │           ├─ Commit-Nachricht
        │           └─ Commit erstellt
        │
        └─ NEIN → Verwende bestehende Commits
                      │
                      └─ Branch erstellen (falls nötig)
                         Push to remote
                         PR erstellen
```

## Branch-Status Prüfung ⚠️ WICHTIG

**ERSTER SCHRITT** vor jeder PR-Erstellung!

### Geschützte Branches erkennen

```bash
# Aktuellen Branch ermitteln
current_branch=$(git branch --show-current)

# Geschützte Branches definieren
protected_branches=("main" "master" "develop")

# Prüfen ob aktueller Branch geschützt ist
if [[ " ${protected_branches[*]} " =~ " ${current_branch} " ]]; then
  echo "⚠️ Auf geschütztem Branch: $current_branch"
  echo "➡️ Neuer Feature-Branch wird erstellt"
else
  echo "✅ Auf Feature-Branch: $current_branch"
  echo "➡️ Verwende aktuellen Branch"
fi
```

### Warum diese Prüfung?

**Geschützte Branches** (`main`, `master`, `develop`):

- ❌ Direkte Commits sind verboten
- ❌ PRs auf sich selbst sind nicht möglich
- ✅ Neuer Branch MUSS erstellt werden
- ✅ PR wird gegen geschützten Branch erstellt

**Feature-Branches** (z.B. `feature/xyz`, `bugfix/abc`):

- ✅ Bereits auf einem separaten Branch
- ✅ Kein neuer Branch nötig
- ✅ PR kann direkt erstellt werden

### Beispiel-Szenarien

**Auf `main` Branch:**

```bash
$ git branch --show-current
main

# /git-workflow:create-pr erkennt: geschützter Branch!
# → Erstellt: feature/neue-funktion-2024-12-12
# → PR: feature/neue-funktion → main
```

**Auf `feature/login` Branch:**

```bash
$ git branch --show-current
feature/login

# /git-workflow:create-pr erkennt: Feature-Branch!
# → Kein neuer Branch nötig
# → PR: feature/login → main
```

## Integration mit /commit

### Voraussetzungen

Der `/git-workflow:create-pr` Command:

- **Prüft auf uncommitted Changes**
- **Ruft `/git-workflow:commit` auf** falls nötig
- **Verwendet bestehende Commits** für PR
- **Erstellt KEINE eigenen Commits**

### Warum diese Integration?

**Konsistenz**: Ein Command für Commits = konsistente Qualität

**Keine Duplikation**: Commit-Logik nur in `/git-workflow:commit`

**Flexibilität**: Du kannst Commits manuell erstellen oder automatisch

## Workflow-Szenarien

### Szenario 1: Keine Commits vorhanden

**Situation**: Du hast Änderungen, aber noch keinen Commit

```bash
$ git status
modified: src/app.py
modified: tests/test_app.py
```

**Workflow**:

```bash
/git-workflow:create-pr
```

1. **Erkennt uncommitted Changes**
2. **Ruft `/git-workflow:commit` auf**
   - Pre-Commit-Checks
   - Staging
   - Commit-Erstellung
3. **Erstellt Branch**: `feature/neue-funktion-2024-10-30`
4. **Pushed Branch**
5. **Erstellt PR**

### Szenario 2: Commits bereits vorhanden

**Situation**: Du hast bereits Commits erstellt

```bash
$ git log --oneline -3
abc1234 (HEAD -> main) ✨ feat: Neue Funktion hinzugefügt
def5678 🧪 test: Tests für neue Funktion
ghi9012 📚 docs: Dokumentation aktualisiert
```

**Workflow**:

```bash
/git-workflow:create-pr
```

1. **Erkennt bestehende Commits**
2. **Überspringt Commit-Erstellung**
3. **Erstellt Branch**: `feature/neue-funktion-2024-10-30`
4. **Pushed Branch mit allen Commits**
5. **Erstellt PR** basierend auf Commit-Historie

### Szenario 3: Gemischte Situation

**Situation**: Commits vorhanden + neue Änderungen

```bash
$ git log --oneline -1
abc1234 (HEAD -> main) ✨ feat: Neue Funktion hinzugefügt

$ git status
modified: src/app.py  # Weitere Änderungen
```

**Workflow**:

```bash
/git-workflow:create-pr
```

1. **Erkennt uncommitted Changes**
2. **Ruft `/git-workflow:commit` auf** für neue Änderungen
3. **Erstellt Branch** mit allen Commits
4. **Pushed und erstellt PR**

## Commit-Aufteilung

Der `/git-workflow:commit` Command kann Änderungen automatisch in logische Commits aufteilen.

### Automatische Erkennung

**Beispiel**: Mehrere unabhängige Änderungen

```bash
$ git status
modified: src/auth/login.py       # Auth-Feature
modified: src/dashboard/ui.py     # UI-Update
modified: tests/test_auth.py      # Auth-Tests
modified: tests/test_dashboard.py # UI-Tests
modified: README.md               # Docs
```

**Workflow**:

```bash
/git-workflow:commit
```

Kann in separate Commits aufteilen:

```text
✨ feat: Login-Funktionalität verbessert
├─ src/auth/login.py
└─ tests/test_auth.py

💎 style: Dashboard UI aktualisiert
├─ src/dashboard/ui.py
└─ tests/test_dashboard.py

📚 docs: README mit neuen Features aktualisiert
└─ README.md
```

### Warum Commit-Aufteilung?

**Vorteile**:

- **Atomare Commits**: Jeder Commit ist unabhängig
- **Besseres Review**: Reviewer sehen klare Struktur
- **Einfaches Debugging**: git bisect funktioniert besser
- **Cherry-Picking**: Einzelne Features können isoliert werden

### Single-Commit Option

**Wenn du alles in einem Commit möchtest**:

```bash
/git-workflow:create-pr --single-commit
```

## Branch-Erstellung

### Automatische Branch-Namen

**Format**: `<type>/<description>-<date>`

**Beispiele**:

```text
feature/user-authentication-2024-10-30
bugfix/memory-leak-fix-2024-10-30
refactor/api-restructure-2024-10-30
```

### Branch-Naming basierend auf Commits

Der Branch-Name wird aus den Commit-Nachrichten abgeleitet:

**Commits**:

```text
✨ feat: Benutzer-Dashboard hinzugefügt
🧪 test: Dashboard Tests implementiert
```

**Branch**: `feature/benutzer-dashboard-2024-10-30`

### Kollisionen vermeiden

**Problem**: Branch existiert bereits

**Lösung**: Automatisches Suffix

```text
feature/neue-funktion-2024-10-30
feature/neue-funktion-2024-10-30-v2
feature/neue-funktion-2024-10-30-v3
```

## Push-Strategie

### First-Time Push

**Erster Push eines neuen Branches**:

```bash
git push -u origin feature/neue-funktion
```

**Das `-u` Flag**:

- Setzt upstream Branch
- Erlaubt einfaches `git push` später
- Tracked Remote Branch

### Commit-Historie präsentieren

**Alle Commits werden gepushed**:

```bash
git log --oneline origin/main..HEAD
```

### Force Push vermeiden

**Prinzip**: Niemals `--force` ohne Notwendigkeit

**Ausnahme**: Nur bei expliziter Anfrage

```bash
/git-workflow:create-pr --force-push  # ⚠️ Vorsicht!
```

## PR-Erstellung basierend auf Commits

### Commit-Analyse

Der Command analysiert alle Commits:

```bash
git log --oneline origin/main..HEAD
```

### PR-Titel Generierung

**Single Commit**: Commit-Nachricht als Titel

```text
✨ feat: Benutzer-Dashboard hinzugefügt
```

→ PR-Titel: **"Benutzer-Dashboard hinzugefügt"**

**Multiple Commits**: Zusammenfassung erstellen

```text
✨ feat: Login-System implementiert
🧪 test: Login-Tests hinzugefügt
📚 docs: Login-Dokumentation erstellt
```

→ PR-Titel: **"Login-System mit Tests und Dokumentation"**

### PR-Beschreibung Generierung

**Basierend auf Commits**:

```markdown
## Beschreibung

Diese PR implementiert ein neues Login-System mit OAuth2-Support.

## Änderungen

- ✨ Login-System implementiert
- 🧪 Login-Tests hinzugefügt
- 📚 Login-Dokumentation erstellt

## Test-Plan

- [ ] Manuelle Tests durchgeführt
- [ ] Unit Tests laufen durch (18 neue Tests)
- [ ] Integration Tests erfolgreich

## Breaking Changes

Keine
```

## Best Practices

### Commit-Hygiene vor PR

**Checkliste**:

- [ ] Alle Commits haben aussagekräftige Nachrichten
- [ ] Commits sind logisch aufgeteilt
- [ ] Keine "WIP" oder "fix" Commits
- [ ] Commit-Historie ist sauber

**Falls nötig**: Commits aufräumen vor `/git-workflow:create-pr`

```bash
git rebase -i HEAD~5
# Commits squashen, reword, etc.
```

### Commit-Nachrichten als Dokumentation

**Commits dokumentieren das "Warum"**:

```text
✨ feat: Rate Limiting für API-Endpoints

Implementiert Token-Bucket-Algorithmus für API-Rate-Limiting.
Limit: 100 Requests pro Minute pro User.

Grund: Schutz vor API-Missbrauch und DoS-Angriffen.
```

### Atomare Feature-Branches

**Ein Branch = Ein Feature**

```text
✅ feature/user-authentication
✅ bugfix/login-memory-leak
❌ feature/multiple-unrelated-things
```

## Troubleshooting

### /commit wird nicht aufgerufen

**Problem**: Änderungen werden erkannt, aber `/git-workflow:commit` nicht aufgerufen

**Diagnose**:

```bash
git status
git diff
```

**Mögliche Ursachen**:

- Alle Änderungen bereits committed
- Working Directory ist clean
- Nur untracked Files

### Commits sind in falscher Reihenfolge

**Problem**: Commit-Historie ist durcheinander

**Lösung**: Rebase vor PR

```bash
git rebase -i origin/main
# Commits neu anordnen
```

### Branch-Name passt nicht

**Problem**: Automatischer Branch-Name ist unpassend

**Lösung**: Branch manuell erstellen

```bash
git checkout -b feature/besserer-name
/git-workflow:create-pr
# Verwendet bestehenden Branch-Namen
```

### Zu viele Commits

**Problem**: PR hat 20+ Commits, schwer zu reviewen

**Lösung**: Commits squashen

```bash
git rebase -i origin/main
# Markiere Commits als 'squash'
```

Oder verwenden:

```bash
/git-workflow:create-pr --single-commit
```

## Integration mit Git Hooks

### Pre-Push Hook

**Automatische Validierung vor Push**:

```bash
#!/bin/bash
# .git/hooks/pre-push

# Alle Commits prüfen
for commit in $(git rev-list origin/main..HEAD); do
  msg=$(git log -1 --format=%s $commit)
  if ! echo "$msg" | grep -E "^(feat|fix|docs|style|refactor|test|chore):"; then
    echo "❌ Commit $commit hat keine Convention-Nachricht"
    exit 1
  fi
done
```

### Commit-Message Hook

**Validierung beim Committen**:

```bash
#!/bin/bash
# .git/hooks/commit-msg

msg=$(cat "$1")
if ! echo "$msg" | grep -E "^(✨|🐛|📚|💎|♻️|⚡|🧪|🔧)"; then
  echo "❌ Commit-Nachricht benötigt Emoji"
  exit 1
fi
```

## Workflow-Beispiele

### Einfacher Feature-Workflow

```bash
# 1. Änderungen machen
vim src/feature.py

# 2. PR erstellen (inkl. Commit)
/git-workflow:create-pr

# Fertig! Branch, Commits, und PR erstellt
```

### Komplexer Multi-Commit-Workflow

```bash
# 1. Feature implementieren
vim src/auth.py
/git-workflow:commit

# 2. Tests hinzufügen
vim tests/test_auth.py
/git-workflow:commit

# 3. Docs aktualisieren
vim README.md
/git-workflow:commit

# 4. PR erstellen
/git-workflow:create-pr

# Branch mit 3 sauberen Commits + PR
```
