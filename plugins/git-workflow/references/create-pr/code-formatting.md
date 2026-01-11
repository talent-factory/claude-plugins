# Code-Formatierung vor PR

Automatische Code-Formatierung basierend auf Projekttyp (optional mit `--no-format` überspringen).

## JavaScript/TypeScript - Biome

**Biome** ist ein schneller Linter und Formatter für JavaScript/TypeScript.

### Installation Check

```bash
npx biome --version
```

### Formatierung

```bash
npx biome format --write .
npx biome check --apply .
```

### Konfiguration

```json
// biome.json
{
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentSize": 2,
    "lineWidth": 100
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true
    }
  }
}
```

## Python - Black + isort + Ruff

### Black Formatierung

**Standard-Formatter für Python**

```bash
black .
black --check .              # Nur prüfen
black --diff .              # Änderungen anzeigen
```

**Konfiguration** (`pyproject.toml`):

```toml
[tool.black]
line-length = 88
target-version = ['py39', 'py310', 'py311']
include = '\.pyi?$'
extend-exclude = '''
/(
  \.git
  | \.venv
  | build
  | dist
)/
'''
```

### isort - Import Sortierung

```bash
isort .
isort --check-only .
isort --diff .
```

**Konfiguration** (`pyproject.toml`):

```toml
[tool.isort]
profile = "black"
line_length = 88
multi_line_output = 3
include_trailing_comma = true
```

### Ruff - Schnelles Linting

```bash
ruff check .
ruff check --fix .
```

**Konfiguration** (`pyproject.toml`):

```toml
[tool.ruff]
line-length = 88
select = ["E", "F", "I", "N", "W"]
ignore = []
fix = true
```

## Java - Google Java Format

### Installation

```bash
# Maven
<plugin>
  <groupId>com.spotify.fmt</groupId>
  <artifactId>fmt-maven-plugin</artifactId>
  <version>2.21</version>
</plugin>

# Gradle
plugins {
  id 'com.github.sherter.google-java-format' version '0.9'
}
```

### Formatierung

```bash
# Maven
mvn fmt:format

# Gradle
./gradlew googleJavaFormat

# CLI Tool
java -jar google-java-format.jar --replace $(find . -name "*.java")
```

### Konfiguration

**Checkstyle** (`checkstyle.xml`):

```xml
<module name="Checker">
  <module name="TreeWalker">
    <module name="Indentation">
      <property name="basicOffset" value="2"/>
      <property name="braceAdjustment" value="0"/>
    </module>
  </module>
</module>
```

## Markdown - markdownlint + mdformat

### markdownlint

```bash
markdownlint '**/*.md' --fix
```

**Konfiguration** (`.markdownlint.json`):

```json
{
  "default": true,
  "MD013": {
    "line_length": 100,
    "code_blocks": false
  },
  "MD033": {
    "allowed_elements": ["details", "summary"]
  }
}
```

### mdformat

```bash
mdformat .
```

**Konfiguration** (`pyproject.toml`):

```toml
[tool.mdformat]
wrap = 80
number = false
```

## Formatierung im Workflow

### Automatischer Workflow

1. **Projekttyp erkennen**
   - package.json → JavaScript/TypeScript
   - pyproject.toml → Python
   - pom.xml/build.gradle → Java
   - *.md Dateien → Markdown

2. **Formatter ausführen**
   - Mit passenden Optionen
   - Error-Handling

3. **Änderungen staged**
   - Nur formatierte Dateien
   - Automatisches Add

4. **Commit erstellt**
   - Via `/commit` Command
   - Mit Formatierungs-Hinweis

### Manuelle Ausführung

```bash
# JavaScript/TypeScript
npx biome format --write .

# Python
black . && isort . && ruff check --fix .

# Java
mvn fmt:format

# Markdown
markdownlint '**/*.md' --fix
```

## Format-Konflikte vermeiden

### EditorConfig verwenden

**Datei** (`.editorconfig`):

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true

[*.{js,jsx,ts,tsx}]
indent_style = space
indent_size = 2

[*.py]
indent_style = space
indent_size = 4

[*.{yml,yaml}]
indent_style = space
indent_size = 2
```

### Tool-Priorität

Bei Konflikten zwischen Tools:

1. **Prettier/Biome** über ESLint (JavaScript)
2. **Black** über Ruff/Flake8 (Python)
3. **google-java-format** über Checkstyle (Java)

### Pre-Commit Hooks

**Python pre-commit** (`.pre-commit-config.yaml`):

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.9.1
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix]
```

## Troubleshooting

### Formatierung überschreibt gewollte Änderungen

**Lösung**: Formatter-Ausnahmen definieren

```python
# fmt: off
special_code = [...]
# fmt: on
```

```javascript
// prettier-ignore
const matrix = [...];
```

### Tool nicht gefunden

**Diagnose**:

```bash
which black
which biome
which markdownlint
```

**Lösung**: Installieren

```bash
# Python
pip install black isort ruff

# JavaScript
npm install -g @biomejs/biome

# Markdown
npm install -g markdownlint-cli
```

### Formatierung schlägt fehl

**Option**: Formatierung überspringen

```bash
/create-pr --no-format
```

### Zu lange Ausführungszeit

**Problem**: Formatter scannen zu viele Dateien

**Lösung**: Nur geänderte Dateien formatieren

```bash
# Git-basiert
black $(git diff --name-only --diff-filter=ACM "*.py")
prettier --write $(git diff --name-only --diff-filter=ACM "*.{js,ts,jsx,tsx}")
```

## Best Practices

### Formatierung in CI/CD

**GitHub Actions Beispiel**:

```yaml
- name: Check formatting
  run: |
    black --check .
    isort --check-only .
```

### Team-Standards

- **Formatter-Konfiguration** ins Repository committen
- **EditorConfig** für Editor-Integration
- **Pre-Commit Hooks** für automatische Checks
- **CI/CD Integration** für PR-Validierung

### Graduelle Einführung

Wenn Projekt noch nicht formatiert:

```bash
# Nur neue/geänderte Dateien
black $(git diff --name-only main...)
```

Oder: Separater Formatierungs-Commit

```text
💎 style: Projekt-weite Code-Formatierung mit Black

Alle Python-Dateien mit Black 23.9.1 formatiert.
Keine funktionalen Änderungen.
```
