# Professional Commit Workflow - Skill

Automatisiert den kompletten Git-Commit-Workflow mit professionellen Qualitätschecks und konventionellen Commit-Nachrichten für Java, Python, React und Dokumentations-Projekte.

## Features

- ✅ **Automatische Projekterkennung** - Erkennt Java, Python, React, Dokumentation
- ✅ **Pre-Commit-Validierung** - Build, Tests, Linting, Type-Checking
- ✅ **Emoji Conventional Commits** - ✨ feat, 🐛 fix, 📚 docs, etc.
- ✅ **Intelligente Staging-Analyse** - Automatisches Add bei Bedarf
- ✅ **Atomare Commit-Empfehlungen** - Erkennt multiple logische Änderungen
- ✅ **Performance-optimiert** - Modulare Validator-Architektur
- ✅ **Wiederverwendbar** - Funktioniert in jedem Projekt
- ✅ **Zero Dependencies** - Nutzt nur Python Standard Library

## Installation

### 1. Skill installieren

```bash
# In Claude Code dotfiles
cd ~/.dotfiles/agents/claude/skills
git clone <dieses-repo> professional-commit-workflow

# Oder: ZIP-Download und entpacken
unzip professional-commit-workflow.zip -d ~/.dotfiles/agents/claude/skills/
```

### 2. Python-Abhängigkeiten (optional)

```bash
cd professional-commit-workflow
pip install -r requirements.txt --break-system-packages
```

**Hinweis**: Das Skill funktioniert ohne zusätzliche Python-Pakete. `requirements.txt` enthält nur optionale Tools für erweiterte Validierung.

### 3. Skill-Scripts ausführbar machen

```bash
chmod +x scripts/*.py
```

### 4. In Claude Code verwenden

Das Skill wird automatisch von Claude erkannt und kann wie folgt verwendet werden:

```
Erstelle einen professionellen Commit für die aktuellen Änderungen
```

oder

```
Führe Pre-Commit-Checks aus und erstelle einen Commit mit Emoji Conventional Commit-Format
```

## Verwendung

### Standard-Workflow

```bash
# Via Python direkt
python scripts/main.py

# Via Claude Code (empfohlen)
# Claude: "Erstelle einen Commit mit dem professional-commit-workflow Skill"
```

### Mit Optionen

```bash
# Checks überspringen
python scripts/main.py --no-verify

# Nur Tests überspringen
python scripts/main.py --skip-tests

# Nur Validierung, kein Commit
python scripts/main.py --validate-only

# Mit Force-Push (Vorsicht!)
python scripts/main.py --force-push
```

### Workflow-Schritte

1. **Projekt-Detection**: Automatisch Java/Python/React/Docs erkennen
2. **Git-Status**: Staging-Status analysieren, Auto-Add anbieten
3. **Pre-Commit-Validierung**: Projektspezifische Checks
   - Java: Maven/Gradle Build, Tests, Checkstyle, SpotBugs
   - Python: Ruff, Black, isort, mypy, pytest
   - React: ESLint, Prettier, TypeScript, Jest/Vitest, Build
   - Docs: LaTeX compile, markdownlint, AsciiDoc
4. **Diff-Analyse**: Mehrere Änderungen? → Atomare Commits empfehlen
5. **Commit-Message**: Emoji Conventional Commit generieren
6. **Commit erstellen**: Git commit ausführen
7. **Push anbieten**: Optional zu Remote pushen

## Projektspezifische Validierung

### Java-Projekte

**Erkannt durch**: `pom.xml`, `build.gradle`, `build.gradle.kts`

**Checks**:
- ✅ Maven/Gradle Compile
- ✅ Unit Tests
- ✅ Checkstyle (falls konfiguriert)
- ✅ SpotBugs (falls konfiguriert)

**Beispiel**:
```bash
# Maven
mvn compile
mvn test
mvn checkstyle:check

# Gradle
./gradlew build
./gradlew test
```

### Python-Projekte

**Erkannt durch**: `pyproject.toml`, `requirements.txt`, `setup.py`

**Checks**:
- ✅ Ruff Linting
- ✅ Black Formatting
- ✅ isort Import Sorting
- ✅ mypy Type Checking (falls konfiguriert)
- ✅ pytest Tests

**Beispiel**:
```bash
ruff check .
black --check .
isort --check-only .
mypy .
pytest
```

### React/Node.js-Projekte

**Erkannt durch**: `package.json` mit react/next/vue/svelte

**Checks**:
- ✅ ESLint
- ✅ Prettier Formatting
- ✅ TypeScript Compiler (falls tsconfig.json)
- ✅ Tests (Jest/Vitest)
- ✅ Production Build

**Beispiel**:
```bash
npm run lint
npx prettier --check .
tsc --noEmit
npm test
npm run build
```

### Dokumentations-Projekte

**Erkannt durch**: `*.tex`, `*.md` (>2 Dateien), `*.adoc`

**Checks**:
- ✅ LaTeX Compilation (pdflatex/xelatex)
- ✅ Markdown Linting (markdownlint)
- ✅ AsciiDoc Rendering (asciidoctor)

**Beispiel**:
```bash
pdflatex main.tex
markdownlint **/*.md
asciidoctor *.adoc
```

## Konfiguration

### commit_types.json

Definiert Emoji-Mappings für Conventional Commits:

```json
{
  "feat": {
    "emoji": "✨",
    "description": "Neue Funktionalität"
  },
  "fix": {
    "emoji": "🐛",
    "description": "Fehlerbehebung"
  }
}
```

**Vollständige Liste**: Siehe [config/commit_types.json](config/commit_types.json)

### validation_rules.json

Projektspezifische Validierungsregeln:

```json
{
  "python": {
    "checks": {
      "ruff": {"enabled": true, "timeout": 60},
      "pytest": {"enabled": true, "skippable": true}
    }
  }
}
```

**Vollständige Konfiguration**: Siehe [config/validation_rules.json](config/validation_rules.json)

## Architektur

```text
professional-commit-workflow/
├── SKILL.md                      # Skill-Definition für Claude Code
├── README.md                     # Diese Datei
├── requirements.txt              # Python-Dependencies (optional)
│
├── scripts/                      # Executable Scripts
│   ├── main.py                   # Haupt-Orchestrator
│   ├── commit_message.py         # Commit-Message-Generator
│   ├── project_detector.py       # Projekt-Typ-Erkennung
│   ├── git_analyzer.py           # Git-Status-Analyse
│   ├── utils.py                  # Hilfsfunktionen
│   └── validators/               # Projekt-Validatoren
│       ├── base_validator.py     # Base-Klasse
│       ├── java_validator.py     # Java (Maven, Gradle)
│       ├── python_validator.py   # Python (Ruff, Black, pytest)
│       ├── react_validator.py    # React/Node.js (ESLint, TS)
│       └── docs_validator.py     # Dokumentation (LaTeX, MD)
│
├── config/                       # Konfigurationsdateien
│   ├── commit_types.json         # Emoji Conventional Commits
│   └── validation_rules.json     # Validierungs-Regeln
│
└── docs/                         # Migrated Documentation
    ├── best-practices.md         # Git Commit Best Practices
    ├── commit-types.md           # Alle Commit-Typen
    ├── pre-commit-checks.md      # Check-Beschreibungen
    └── troubleshooting.md        # Fehlerbehebung
```

## Beispiele

### Erfolgreicher Python-Commit

```text
$ python scripts/main.py

============================================================
  Professional Commit Workflow
============================================================

✓ Projekt-Typen erkannt: python
✓ 3 Dateien bereit zum Commit
  - src/api/routes.py
  - tests/test_routes.py
  - README.md

============================================================
  Pre-Commit-Validierung
============================================================

✓ Ruff Linting: Keine Linting-Fehler
✓ Black Formatting: Code korrekt formatiert
✓ pytest: Alle Tests bestanden

Validierungs-Ergebnis: 3/3 Checks bestanden

============================================================
  Diff-Analyse
============================================================

ℹ️  Dateien geändert: 3
ℹ️  Einfügungen: +47
ℹ️  Löschungen: -12

============================================================
  Commit-Nachricht
============================================================

ℹ️  Generiert: ✨ feat: API Routes für User-Verwaltung hinzufügen
Commit-Nachricht verwenden? [Y/n] y

============================================================
  Commit erstellen
============================================================

✓ Commit erstellt: ✨ feat: API Routes für User-Verwaltung hinzufügen

============================================================
  Push zum Remote
============================================================

Push zu 'main'? [Y/n] y
✓ Push zu 'main' erfolgreich

✅ Commit-Workflow erfolgreich abgeschlossen
```

### Bei Validierungs-Fehlern

```text
============================================================
  Pre-Commit-Validierung
============================================================

✓ Ruff Linting: Keine Linting-Fehler
✗ Black Formatting: Formatierungs-Fehler gefunden
    src/api/routes.py would be reformatted
✓ pytest: Alle Tests bestanden

Validierungs-Ergebnis: 2/3 Checks bestanden

❌ Pre-Commit-Checks fehlgeschlagen
ℹ️  Behebe die Fehler oder verwende --no-verify zum Überspringen
```

## Troubleshooting

### Tool nicht gefunden

**Problem**: "Command 'ruff' not found"

**Lösung**: Tool installieren oder Check überspringen

```bash
# Tool installieren
pip install ruff

# Oder: Check überspringen
python scripts/main.py --no-verify
```

### Tests schlagen fehl

**Problem**: Tests laufen nicht durch

**Lösungen**:

1. **Tests fixen** (empfohlen)
2. **Tests überspringen**: `--skip-tests`
3. **Alle Checks überspringen**: `--no-verify`

```bash
python scripts/main.py --skip-tests
```

### Build-Fehler

**Problem**: Maven/Gradle/npm Build schlägt fehl

**Lösung**: Siehe [docs/troubleshooting.md](docs/troubleshooting.md)

### Mehrere logische Änderungen

**Problem**: Skill warnt vor mehreren Änderungen in einem Commit

**Lösung**: Atomare Commits erstellen

```bash
# Änderungen aufteilen
git reset
git add src/feature-a/
git commit -m "✨ feat: Feature A"

git add src/feature-b/
git commit -m "✨ feat: Feature B"
```

## Best Practices

### Atomare Commits

✅ **Gut**: Ein Commit = Eine logische Änderung
```
✨ feat: User-Authentifizierung hinzufügen
🧪 test: Tests für Authentifizierung hinzufügen
📚 docs: Auth-API dokumentieren
```

❌ **Schlecht**: Alles in einem Commit
```
✨ feat: Auth, Tests, Docs, Bugfixes und Refactoring
```

### Commit-Nachrichten

✅ **Gut**: Imperativ, beschreibend, <72 Zeichen
```
✨ feat: Füge Dark Mode Toggle hinzu
🐛 fix: Behebe Speicherleck in WebSocket-Verbindungen
```

❌ **Schlecht**: Vergangenheit, vage
```
feat: Stuff hinzugefügt
fix: bug
```

### Code-Qualität

✅ **Vor jedem Commit**:
- [ ] Linting bestanden
- [ ] Tests erfolgreich
- [ ] Build erfolgreich
- [ ] Keine Debug-Ausgaben
- [ ] Keine Secrets

**Vollständige Best Practices**: [docs/best-practices.md](docs/best-practices.md)

## Documentation

- **[Pre-Commit-Checks](docs/pre-commit-checks.md)** - Detaillierte Check-Beschreibungen
- **[Commit-Types](docs/commit-types.md)** - Alle Emoji-Typen mit Beispielen
- **[Best Practices](docs/best-practices.md)** - Git-Commit-Best-Practices
- **[Troubleshooting](docs/troubleshooting.md)** - Fehlerbehebung

## Migration vom /git-workflow:commit Command

Wenn du bisher den `/git-workflow:commit` Command verwendet hast:

1. **Skill installieren** (siehe oben)
2. **Claude verwenden**: "Erstelle Commit mit professional-commit-workflow"
3. **Optional**: `/git-workflow:commit` Command deaktivieren oder für Legacy-Projekte behalten

**Vorteile**:
- ✅ Wiederverwendbar über Projekte hinweg
- ✅ Keine Duplikation von Command-Dateien
- ✅ Einfache Updates (nur Skill updaten)
- ✅ Distributable an andere Nutzer

## License

MIT License - Siehe [LICENSE](LICENSE) für Details.

## Contributing

Contributions welcome! Siehe [CONTRIBUTING.md](CONTRIBUTING.md).

## Version

**Version**: 1.0.0
**Author**: talent-factory
**Refactored from**: `/git-workflow:commit` Command
**Date**: 2024-12-21
