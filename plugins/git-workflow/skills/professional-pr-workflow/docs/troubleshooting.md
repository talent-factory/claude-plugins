# Troubleshooting: PR-Erstellung

## Branch-Probleme

### Branch existiert bereits

**Problem**: Branch-Name kollidiert mit bestehendem Branch

**Symptom**:

```bash
fatal: A branch named 'feature/neue-funktion' already exists.
```

**Diagnose**:

```bash
git branch -a                    # Alle Branches anzeigen
git branch -r | grep feature     # Remote Feature-Branches
```

**Lösungen**:

1. **Automatisches Suffix** (Command macht das automatisch):

   ```
   feature/neue-funktion    → feature/neue-funktion-v2
   ```

2. **Bestehenden Branch verwenden**:

   ```bash
   git checkout feature/neue-funktion
   /create-pr
   ```

3. **Alten Branch löschen** (Vorsicht!):

   ```bash
   git branch -D feature/alte-funktion
   git push origin --delete feature/alte-funktion
   ```

### Branch kann nicht erstellt werden

**Problem**: Uncommitted Changes blockieren Branch-Wechsel

**Symptom**:

```bash
error: Your local changes would be overwritten by checkout
```

**Lösungen**:

1. **Changes committen**:

   ```bash
   /commit
   /create-pr
   ```

2. **Changes stashen**:

   ```bash
   git stash
   /create-pr
   git stash pop
   ```

### Falscher Base-Branch

**Problem**: Branch wurde von falschem Branch abgezweigt

**Symptom**: PR enthält ungewollte Commits

**Diagnose**:

```bash
git log --oneline --graph
```

**Lösung**: Branch rebasen

```bash
git rebase --onto main old-base feature-branch
```

## Formatierungs-Probleme

### Formatierung schlägt fehl

**Problem**: Code-Formatter findet Fehler

**Symptom**:

```bash
Error: Biome formatting failed
Error: Black formatting failed
```

**Diagnose**:

```bash
# JavaScript
npx biome check .

# Python
black --check .

# Java
mvn fmt:check
```

**Lösungen**:

1. **Fehler beheben**:

   ```bash
   # Auto-Fix
   npx biome format --write .
   black .
   mvn fmt:format
   ```

2. **Formatierung überspringen**:

   ```bash
   /create-pr --no-format
   ```

3. **Spezifische Dateien exkludieren**:

   ```toml
   # pyproject.toml
   [tool.black]
   extend-exclude = '''
   /(
     problematic_dir
   )/
   '''
   ```

### Formatierung zu langsam

**Problem**: Formatierung dauert sehr lange

**Diagnose**:

```bash
time black .
time npx biome format .
```

**Lösungen**:

1. **Nur geänderte Dateien**:

   ```bash
   black $(git diff --name-only --diff-filter=ACM "*.py")
   ```

2. **Parallel-Verarbeitung**:

   ```bash
   black --fast .
   ```

3. **Formatierung überspringen**:

   ```bash
   /create-pr --no-format
   ```

### Formatierungs-Konflikte

**Problem**: Verschiedene Formatter widersprechen sich

**Symptom**: File wird mehrfach unterschiedlich formatiert

**Lösung**: Tool-Priorität festlegen

```ini
# .editorconfig
root = true

[*.py]
indent_style = space
indent_size = 4
max_line_length = 88

[*.js]
indent_style = space
indent_size = 2
```

## GitHub CLI (gh) Probleme

### GitHub CLI nicht konfiguriert

**Problem**: `gh` Befehle funktionieren nicht

**Symptom**:

```bash
gh: command not found
# Oder
error: gh: To get started with GitHub CLI, please run: gh auth login
```

**Lösung**:

```bash
# Installation (macOS)
brew install gh

# Installation (Linux)
sudo apt install gh

# Authentifizierung
gh auth login
```

**Setup überprüfen**:

```bash
gh auth status
gh repo view
```

### Keine Berechtigung für Repository

**Problem**: Fehlende Push-Berechtigung

**Symptom**:

```bash
remote: Permission to user/repo.git denied
```

**Diagnose**:

```bash
gh auth status
git remote -v
```

**Lösungen**:

1. **Token-Berechtigungen prüfen**:

   ```bash
   gh auth refresh -s repo
   ```

2. **SSH statt HTTPS**:

   ```bash
   git remote set-url origin git@github.com:user/repo.git
   ```

3. **Repository-Zugriff prüfen**:
   - Fork erstellen wenn nötig
   - Team-Mitgliedschaft überprüfen

### PR kann nicht erstellt werden

**Problem**: `gh pr create` schlägt fehl

**Symptom**:

```bash
error: could not create pull request
```

**Häufige Ursachen**:

1. **Branch nicht gepusht**:

   ```bash
   git push -u origin branch-name
   gh pr create
   ```

2. **Keine Änderungen**:

   ```bash
   git diff origin/main...HEAD
   # Falls leer: Keine Änderungen vorhanden
   ```

3. **PR existiert bereits**:

   ```bash
   gh pr list
   gh pr view <number>
   ```

## Commit-Integration-Probleme

### /commit wird nicht aufgerufen

**Problem**: Uncommitted Changes, aber kein Commit erstellt

**Diagnose**:

```bash
git status
git diff --stat
```

**Mögliche Ursachen**:

1. **Nur untracked Files**:

   ```bash
   git add .
   /create-pr
   ```

2. **Alle Changes bereits staged**:

   ```bash
   git reset HEAD
   /create-pr  # Jetzt wird /commit aufgerufen
   ```

### Commits in falscher Reihenfolge

**Problem**: Commit-Historie ist unlogisch

**Lösung**: Interactive Rebase

```bash
git rebase -i HEAD~5
# Commits neu anordnen
```

**Oder**: Commits squashen

```bash
git rebase -i HEAD~3
# Markiere mit 'squash'
```

### Zu viele Commits

**Problem**: PR hat 30+ Commits, schwer zu reviewen

**Lösungen**:

1. **Commits squashen**:

   ```bash
   git rebase -i origin/main
   # Markiere Commits als 'squash'
   ```

2. **Single-Commit Option**:

   ```bash
   /create-pr --single-commit
   ```

## Push-Probleme

### Push rejected

**Problem**: Remote hat neuere Commits

**Symptom**:

```bash
! [rejected] feature-branch -> feature-branch (non-fast-forward)
```

**Lösung**:

```bash
git pull --rebase origin feature-branch
git push
```

### Push zu groß

**Problem**: Push-Limit überschritten

**Symptom**:

```bash
remote: error: GH001: Large files detected
```

**Lösung**: Git LFS verwenden

```bash
git lfs install
git lfs track "*.psd" "*.zip"
git add .gitattributes
git commit -m "Add Git LFS"
```

### Protected Branch

**Problem**: Kann nicht direkt nach main/master pushen

**Symptom**:

```bash
remote: error: GH006: Protected branch update failed
```

**Lösung**: Das ist gewollt! Immer über Feature-Branches:

```bash
git checkout -b feature/new-feature
/create-pr
```

## PR-Beschreibung-Probleme

### PR-Beschreibung ist leer

**Problem**: Keine aussagekräftige Beschreibung generiert

**Ursache**: Keine sinnvollen Commit-Nachrichten

**Lösung**: Commit-Messages verbessern

```bash
# Commits reword
git rebase -i HEAD~3
# Markiere mit 'reword'
```

### Breaking Changes nicht erkannt

**Problem**: Breaking Changes nicht in PR dokumentiert

**Lösung**: Manuell ergänzen

```bash
gh pr edit <number> --body "$(cat <<EOF
## Breaking Changes

- API v1 deprecated
- Database Schema Changed

$(gh pr view <number> --json body -q .body)
EOF
)"
```

## Test-Probleme

### Tests schlagen in CI fehl

**Problem**: Tests lokal OK, in CI fehlgeschlagen

**Diagnose**:

```bash
gh pr checks <number>
gh run view <run-id>
```

**Häufige Ursachen**:

1. **Umgebungs-Unterschiede**:
   - Verschiedene Node/Python-Versionen
   - Fehlende Dependencies
   - Umgebungsvariablen

2. **Timing-Issues**:
   - Flaky Tests
   - Race Conditions

3. **Resource-Limits**:
   - Memory-Limits
   - Timeout-Settings

**Lösungen**:

```yaml
# .github/workflows/test.yml
- name: Run Tests
  run: pytest -v --timeout=300
  timeout-minutes: 10
```

### Coverage zu niedrig

**Problem**: Code-Coverage unter Mindest-Schwelle

**Diagnose**:

```bash
pytest --cov --cov-report=term-missing
```

**Lösung**: Tests hinzufügen

```bash
# Neue Tests schreiben
vim tests/test_new_feature.py
/commit
git push
```

## Network-Probleme

### Timeout beim Push

**Problem**: Push-Operation timeout

**Lösung**:

```bash
# Timeout erhöhen
git config --global http.postBuffer 524288000

# Oder: SSH verwenden
git remote set-url origin git@github.com:user/repo.git
```

### SSL-Fehler

**Problem**: SSL-Zertifikat-Fehler

**Temporäre Lösung** (nicht empfohlen für Production):

```bash
git config --global http.sslVerify false
```

**Richtige Lösung**: CA-Zertifikate aktualisieren

```bash
# macOS
brew install ca-certificates

# Linux
sudo update-ca-certificates
```

## Draft vs. Ready

### PR als Draft erstellt, sollte Ready sein

**Problem**: PR ist noch als Draft markiert

**Lösung**:

```bash
gh pr ready <number>
```

### PR als Ready erstellt, sollte Draft sein

**Problem**: PR ist bereit, aber noch Work in Progress

**Lösung**:

```bash
gh pr ready <number> --undo
```

## Merge-Konflikte in PR

### Merge-Konflikte nach PR-Erstellung

**Problem**: Base-Branch hat sich geändert

**Diagnose**:

```bash
gh pr view <number>
# Zeigt "Merge conflicts" warning
```

**Lösung**:

```bash
git checkout feature-branch
git pull origin main --rebase
# Konflikte lösen
git add .
git rebase --continue
git push --force-with-lease
```

## Spezial-Fälle

### Monorepo mit mehreren Projekten

**Problem**: PR enthält Änderungen an mehreren Projekten

**Lösung**: PRs pro Projekt erstellen

```bash
# Backend PR
git add backend/
/commit
/create-pr

# Frontend PR
git add frontend/
/commit
/create-pr
```

### Force Push erforderlich

**Problem**: Historie wurde umgeschrieben

**Lösung** (Vorsicht!):

```bash
/create-pr --force-push
```

**Warnung**: Nur verwenden wenn:

- Du allein am Branch arbeitest
- Du weißt was du tust
- Niemals bei main/master

### PR von Fork erstellen

**Problem**: Keine Push-Berechtigung zum Original-Repo

**Workflow**:

```bash
# 1. Fork erstellen (via GitHub UI)

# 2. Fork clonen
git clone git@github.com:youruser/repo.git

# 3. Upstream hinzufügen
git remote add upstream git@github.com:original/repo.git

# 4. Branch erstellen und pushen
git checkout -b feature/new
/commit
git push origin feature/new

# 5. PR erstellen (zum upstream)
gh pr create --repo original/repo
```

## Debugging

### Verbose Output

**Mehr Details anzeigen**:

```bash
GIT_TRACE=1 git push
GH_DEBUG=1 gh pr create
```

### Logs analysieren

```bash
# Git Logs
git log --oneline --graph --all

# GitHub Actions Logs
gh run list
gh run view <run-id> --log

# PR-Status
gh pr view <number> --json statusCheckRollup
```

### Häufige Fehlerquellen

**Checkliste**:

- [ ] Git/GitHub CLI korrekt installiert und konfiguriert
- [ ] Authentifizierung funktioniert
- [ ] Repository-Berechtigungen korrekt
- [ ] Branch-Name ist einzigartig
- [ ] Working Directory ist clean
- [ ] Tests laufen lokal durch
- [ ] Keine großen Dateien (>100MB)
