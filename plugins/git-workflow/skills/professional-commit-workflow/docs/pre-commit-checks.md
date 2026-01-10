# Pre-Commit-Checks

Automatische Qualitätschecks basierend auf erkanntem Projekttyp.

## Java-Projekte

### Maven

```bash
mvn compile          # Kompilierung
mvn test            # Unit Tests
mvn checkstyle:check # Code-Style Prüfung
```

### Gradle

```bash
./gradlew build              # Build
./gradlew test               # Tests
./gradlew checkstyleMain     # Checkstyle
```

### Spring Boot

- Automatische Erkennung von Spring Boot Projekten
- Zusätzliche Validierung von Application Properties
- Bean-Dependency Checks

## Python-Projekte

### Linting

```bash
ruff check .        # Schnelles Linting
flake8 .           # Alternative Linting
pylint .           # Umfassendes Linting
```

### Formatierung

```bash
black .            # Code-Formatierung
isort .            # Import-Sortierung
```

### Type Checking

```bash
mypy .             # Statische Type-Prüfung
```

### Tests

```bash
pytest             # Test-Ausführung
pytest --cov       # Mit Coverage
```

### Dependencies

- **Poetry**: `poetry check`
- **pip-tools**: `pip-compile --dry-run`
- **requirements.txt**: Dependency-Validierung

## React/Node.js-Projekte

### Package Manager Detection

Automatische Erkennung von: npm, pnpm, yarn, bun

### Linting

```bash
npm run lint       # ESLint
npx tslint         # TSLint (legacy)
```

### Formatierung

```bash
npx prettier --check .   # Prettier Check
```

### Type Checking

```bash
tsc --noEmit       # TypeScript Compiler
```

### Tests

```bash
npm test           # Jest/Vitest
npm run test:e2e   # Cypress/Playwright
```

### Build

```bash
npm run build      # Vite/Webpack/Next.js Build
```

## Dokumentationsprojekte

### LaTeX

```bash
pdflatex main.tex  # Kompilierung
xelatex main.tex   # Alternative Engine
```

### Markdown

```bash
markdownlint **/*.md       # Linting
markdown-link-check *.md   # Link-Validierung
```

### AsciiDoc

```bash
asciidoctor *.adoc         # Rendering
```

## Check-Ausführung

1. **Automatische Projekterkennung**: Identifiziert Projekttyp anhand von Dateien
2. **Relevante Checks**: Führt nur passende Checks aus
3. **Fehlerbehandlung**: Bei Fehlern wird Commit abgebrochen
4. **Skip-Option**: Mit `--no-verify` können Checks übersprungen werden

## Fehlerbehandlung

### Build-Fehler

- Commit wird abgebrochen
- Fehler werden vollständig angezeigt
- Hinweis auf Fehlerursache

### Test-Fehler

- Option zum Überspringen mit `--skip-tests`
- Detaillierte Test-Ausgabe
- Nur bei kritischen Fehlern abbrechen

### Linting-Probleme

- Automatische Fixes wo möglich (z.B. Black, Prettier)
- Manuelle Fixes erforderlich bei komplexen Problemen
- Warnung bei Style-Guide-Verstößen
