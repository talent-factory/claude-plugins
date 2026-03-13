# Code Formatting Before PR

Automatic code formatting based on project type (optionally skip with `--no-format`).

## JavaScript/TypeScript - Biome

**Biome** is a fast linter and formatter for JavaScript/TypeScript.

### Installation Check

```bash
npx biome --version
```

### Formatting

```bash
npx biome format --write .
npx biome check --apply .
```

### Configuration

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

### Black Formatting

**Standard formatter for Python**

```bash
black .
black --check .              # Check only
black --diff .              # Show changes
```

**Configuration** (`pyproject.toml`):

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

### isort - Import Sorting

```bash
isort .
isort --check-only .
isort --diff .
```

**Configuration** (`pyproject.toml`):

```toml
[tool.isort]
profile = "black"
line_length = 88
multi_line_output = 3
include_trailing_comma = true
```

### Ruff - Fast Linting

```bash
ruff check .
ruff check --fix .
```

**Configuration** (`pyproject.toml`):

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

### Formatting

```bash
# Maven
mvn fmt:format

# Gradle
./gradlew googleJavaFormat

# CLI Tool
java -jar google-java-format.jar --replace $(find . -name "*.java")
```

### Configuration

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

**Configuration** (`.markdownlint.json`):

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

**Configuration** (`pyproject.toml`):

```toml
[tool.mdformat]
wrap = 80
number = false
```

## Formatting in the Workflow

### Automatic Workflow

1. **Detect project type**
   - package.json → JavaScript/TypeScript
   - pyproject.toml → Python
   - pom.xml/build.gradle → Java
   - *.md files → Markdown

2. **Execute formatter**
   - With appropriate options
   - Error handling

3. **Stage changes**
   - Only formatted files
   - Automatic add

4. **Create commit**
   - Via `/git-workflow:commit` command
   - With formatting note

### Manual Execution

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

## Avoiding Format Conflicts

### Using EditorConfig

**File** (`.editorconfig`):

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

### Tool Priority

When conflicts arise between tools:

1. **Prettier/Biome** over ESLint (JavaScript)
2. **Black** over Ruff/Flake8 (Python)
3. **google-java-format** over Checkstyle (Java)

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

### Formatting Overwrites Intended Changes

**Solution**: Define formatter exceptions

```python
# fmt: off
special_code = [...]
# fmt: on
```

```javascript
// prettier-ignore
const matrix = [...];
```

### Tool Not Found

**Diagnosis**:

```bash
which black
which biome
which markdownlint
```

**Solution**: Install the tool

```bash
# Python
pip install black isort ruff

# JavaScript
npm install -g @biomejs/biome

# Markdown
npm install -g markdownlint-cli
```

### Formatting Fails

**Option**: Skip formatting

```bash
/git-workflow:create-pr --no-format
```

### Excessive Execution Time

**Problem**: Formatters scan too many files

**Solution**: Format only changed files

```bash
# Git-based
black $(git diff --name-only --diff-filter=ACM "*.py")
prettier --write $(git diff --name-only --diff-filter=ACM "*.{js,ts,jsx,tsx}")
```

## Best Practices

### Formatting in CI/CD

**GitHub Actions example**:

```yaml
- name: Check formatting
  run: |
    black --check .
    isort --check-only .
```

### Team Standards

- **Commit formatter configuration** to the repository
- **EditorConfig** for editor integration
- **Pre-commit hooks** for automatic checks
- **CI/CD integration** for PR validation

### Gradual Adoption

When a project is not yet formatted:

```bash
# Only new/changed files
black $(git diff --name-only main...)
```

Or: Separate formatting commit

```text
💎 style: Apply project-wide code formatting with Black

All Python files formatted with Black 23.9.1.
No functional changes.
```
