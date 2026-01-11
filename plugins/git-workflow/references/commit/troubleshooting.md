# Troubleshooting: Commit-Probleme

## Build-Fehler

### Java Build schlägt fehl

**Problem**: Maven/Gradle Build-Fehler

**Diagnose**:

```bash
mvn clean compile          # Maven
./gradlew clean build      # Gradle
```

**Häufige Ursachen**:

1. **Kompilierfehler im Code**
   - Syntax-Fehler
   - Fehlende Imports
   - Type Mismatches

   **Lösung**: Fehler aus Compiler-Output beheben

2. **Fehlende Dependencies**

   ```bash
   mvn dependency:resolve    # Maven
   ./gradlew dependencies    # Gradle
   ```

3. **Veraltete Build-Artefakte**

   ```bash
   mvn clean                 # Maven
   ./gradlew clean          # Gradle
   ```

### Python Build-Fehler

**Problem**: Linting oder Test-Fehler

**Diagnose**:

```bash
ruff check .              # Linting
pytest -v                # Tests mit Details
```

**Häufige Ursachen**:

1. **Ruff/Flake8 Violations**

   ```bash
   ruff check --fix .     # Auto-Fix
   black .               # Formatierung
   ```

2. **Import-Fehler**

   ```bash
   pip install -e .      # Editable Install
   pip install -r requirements.txt
   ```

3. **Test-Abhängigkeiten fehlen**

   ```bash
   pip install -e ".[test]"
   ```

### React/Node Build-Fehler

**Problem**: TypeScript oder ESLint-Fehler

**Diagnose**:

```bash
npm run lint             # ESLint
tsc --noEmit            # TypeScript Check
npm run build           # Full Build
```

**Häufige Ursachen**:

1. **ESLint-Fehler**

   ```bash
   npm run lint -- --fix  # Auto-Fix
   ```

2. **TypeScript-Fehler**
   - Fehlende Type-Definitionen
   - Type Mismatches

   **Lösung**:

   ```bash
   npm install --save-dev @types/[package]
   ```

3. **Node Modules veraltet**

   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

## Test-Fehler

### Tests schlagen fehl

**Problem**: Unit Tests oder Integration Tests fehlgeschlagen

**Optionen**:

1. **Tests überspringen** (nur für Debugging):

   ```bash
   /commit --skip-tests
   ```

2. **Einzelne Tests debuggen**:

   ```bash
   # Java
   mvn test -Dtest=ClassName#methodName

   # Python
   pytest tests/test_file.py::test_function -v

   # JavaScript
   npm test -- --testNamePattern="test name"
   ```

3. **Test-Output analysieren**:
   - Stack Traces
   - Assertion-Fehler
   - Setup/Teardown-Probleme

### Flaky Tests

**Problem**: Tests schlagen manchmal fehl

**Diagnose**:

```bash
# Mehrfach ausführen
for i in {1..10}; do npm test; done
```

**Häufige Ursachen**:

- Race Conditions
- Nicht isolierte Tests
- Externe Abhängigkeiten (Zeit, Netzwerk)
- Shared State zwischen Tests

**Lösungen**:

- Mocking verwenden
- Test-Isolation sicherstellen
- Deterministische Seeds für Zufallswerte

## Linting-Probleme

### Automatische Fixes funktionieren nicht

**Problem**: Linter meldet Fehler, die nicht auto-fixbar sind

**Strategien**:

1. **Schrittweise fixen**:

   ```bash
   # Python
   black .              # Formatierung zuerst
   isort .             # Dann Imports
   ruff check --fix .  # Dann Linting

   # JavaScript
   prettier --write .  # Formatierung zuerst
   eslint --fix .     # Dann Linting
   ```

2. **Einzelne Regeln temporär deaktivieren**:

   ```python
   # noqa: E501  (nur wenn wirklich nötig)
   ```

   ```javascript
   // eslint-disable-next-line rule-name
   ```

3. **Konfiguration überprüfen**:
   - `.eslintrc`, `pyproject.toml`, etc.
   - Konflikte zwischen Tools

### Formatierung überschreibt Code

**Problem**: Auto-Formatter zerstört gewollte Formatierung

**Lösung**:

```python
# fmt: off
special_formatting = [
    1,  2,  3,
    4,  5,  6,
]
# fmt: on
```

```javascript
// prettier-ignore
const matrix = [
  1, 0, 0,
  0, 1, 0,
  0, 0, 1,
];
```

## Merge-Konflikte

### Konflikte vor Commit

**Problem**: Merge-Konflikte erkannt

**Lösung**:

1. **Aktuellen Stand committen**:

   ```bash
   git stash                    # Changes sichern
   git pull --rebase origin main # Aktualisieren
   git stash pop               # Changes zurückholen
   ```

2. **Konflikte auflösen**:

   ```bash
   git status                   # Konflikt-Dateien sehen
   # Dateien manuell bearbeiten
   git add <resolved-files>
   git rebase --continue       # Oder git merge --continue
   ```

3. **Merge-Tool verwenden**:

   ```bash
   git mergetool
   ```

### Pre-Commit Hook blockiert

**Problem**: Pre-Commit Hook verhindert Commit

**Diagnose**:

```bash
git commit -v              # Verbose Output
```

**Optionen**:

1. **Hook-Fehler beheben** (empfohlen)
2. **Hook temporär überspringen**:

   ```bash
   git commit --no-verify
   # Oder
   /commit --no-verify
   ```

**Warnung**: `--no-verify` nur verwenden, wenn du weißt was du tust!

## Staging-Probleme

### Falsche Dateien staged

**Problem**: Ungewollte Dateien in Staging Area

**Lösung**:

```bash
git reset HEAD <file>          # Einzelne Datei unstagen
git reset HEAD                # Alles unstagen
```

### Dateien ignoriert werden

**Problem**: `.gitignore` blockiert gewollte Dateien

**Diagnose**:

```bash
git check-ignore -v <file>    # Welche Regel blockiert?
```

**Lösung**:

```bash
git add -f <file>             # Force add
# Oder .gitignore anpassen
```

### Zu viele untracked Files

**Problem**: Hunderte von Dateien, schwer zu überblicken

**Lösung**:

```bash
# Nur relevante Dateien adden
git add src/                  # Nur src Verzeichnis
git add *.py                 # Nur Python-Dateien
git add -p                   # Interactive staging
```

## Performance-Probleme

### Commit dauert sehr lange

**Problem**: Pre-Commit-Checks sind langsam

**Ursachen**:

1. **Zu viele Tests**
   - Option: `--skip-tests`
   - Oder: Nur relevante Tests

2. **Große Datei-Anzahl**
   - Linter scannen zu viele Dateien

   **Lösung**: Nur staged Files checken

   ```bash
   # Python
   ruff check $(git diff --staged --name-only | grep .py$)

   # JavaScript
   eslint $(git diff --staged --name-only | grep .js$)
   ```

3. **Dependency-Checks**
   - Langsame Netzwerk-Operationen

### Repository zu groß

**Problem**: Große Binärdateien in History

**Diagnose**:

```bash
git count-objects -vH
```

**Lösung**: Git LFS für große Dateien

```bash
git lfs install
git lfs track "*.pdf"
git lfs track "*.zip"
```

## Commit-Message-Probleme

### Editor öffnet nicht

**Problem**: Git öffnet falschen Editor

**Lösung**:

```bash
# Systemweit
export EDITOR=vim
export VISUAL=vim

# Git-spezifisch
git config --global core.editor "code --wait"  # VS Code
git config --global core.editor "nano"        # Nano
git config --global core.editor "vim"         # Vim
```

### Commit-Message-Validierung schlägt fehl

**Problem**: commitlint oder ähnliche Tools blockieren

**Diagnose**: Validierungsregeln überprüfen

**Lösung**: Format anpassen oder Rules ändern

```bash
# .commitlintrc.json
{
  "extends": ["@commitlint/config-conventional"],
  "rules": {
    "subject-max-length": [2, "always", 100]
  }
}
```

## Authentifizierung-Probleme

### Push nach Commit schlägt fehl

**Problem**: Authentication failed

**Lösungen**:

1. **SSH-Key verwenden**:

   ```bash
   ssh-add ~/.ssh/id_rsa
   ssh -T git@github.com      # Test Connection
   ```

2. **Token-Authentication**:

   ```bash
   git config credential.helper store
   # Beim nächsten Push Token eingeben
   ```

3. **SSH statt HTTPS**:

   ```bash
   git remote set-url origin git@github.com:user/repo.git
   ```

## Spezial-Fälle

### Commit rückgängig machen

**Nach Commit, vor Push**:

```bash
git reset HEAD~1              # Soft reset (behält Changes)
git reset --hard HEAD~1       # Hard reset (löscht Changes)
```

**Nach Push**:

```bash
git revert HEAD               # Erstellt neuen Revert-Commit
```

### Commit-Message ändern

**Letzter Commit**:

```bash
git commit --amend
```

**Älterer Commit**:

```bash
git rebase -i HEAD~5
# Markiere Commit mit 'reword'
```

### Mehrere Commits zusammenfassen

```bash
git rebase -i HEAD~5
# Markiere Commits mit 'squash'
```

## Hilfe holen

Wenn nichts funktioniert:

```bash
git status                    # Aktueller Zustand
git log --oneline -10        # Letzte Commits
git reflog                   # Alle Operationen
```

**Logs analysieren**:

- Build-Logs
- Test-Output
- Linter-Reports
- Git-Output
