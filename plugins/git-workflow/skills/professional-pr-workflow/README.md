# Professional PR Workflow - Skill

Automatisiert Pull-Request-Erstellung mit Branch-Management, Code-Formatierung und GitHub CLI Integration.

## Features

- ✅ **Intelligentes Branch-Management** - Erkennt geschützte Branches (main/master/develop)
- ✅ **Integration mit professional-commit-workflow** - Keine Commit-Duplikation
- ✅ **Automatische Code-Formatierung** (Biome, Black, Prettier)
- ✅ **GitHub CLI Integration** - PR-Erstellung via `gh pr create`
- ✅ **Draft-PR Support** - WIP-PRs markieren
- ✅ **Zero Python Dependencies** - Nur stdlib

## Installation

```bash
cd ~/.dotfiles/agents/claude/skills
# Skill ist bereits vorhanden

# GitHub CLI installieren (falls nicht vorhanden)
# macOS: brew install gh
# Linux: siehe https://cli.github.com/
# Windows: siehe https://cli.github.com/

# GitHub CLI authentifizieren
gh auth login
```

## Usage

### Via Claude Code (empfohlen)

```
Erstelle einen Pull Request mit dem professional-pr-workflow Skill
```

### Via Python direkt

```bash
python scripts/main.py                # Standard-PR
python scripts/main.py --draft        # Draft-PR
python scripts/main.py --no-format    # Ohne Formatierung
python scripts/main.py --target develop  # Target Branch ändern
```

## Workflow

1. **Branch-Status prüfen**
   - Geschützter Branch? → Neuer Feature-Branch erstellen
   - Feature-Branch? → Aktuellen Branch verwenden

2. **Commits validieren**
   - Keine Commits? → User muss commit-workflow ausführen
   - Commits vorhanden? → Weiter zu Schritt 3

3. **Code formatieren** (optional)
   - JavaScript: Biome
   - Python: Black, isort
   - Markdown: markdownlint

4. **PR erstellen**
   - Push Branch zu Remote
   - `gh pr create` ausführen
   - PR-URL zurückgeben

## Supported Formatters

- **JavaScript/TypeScript**: Biome (bevorzugt), Prettier, ESLint
- **Python**: Black, isort, Ruff
- **Java**: Google Java Format (via Maven/Gradle)
- **Markdown**: markdownlint, mdformat

## Configuration

Siehe `config/pr_config.json` für Anpassungen:
- Protected branches
- Default target branch
- Formatter preferences
- PR template options

## Documentation

- **[code-formatting.md](docs/code-formatting.md)**: Formatter-Details
- **[commit-workflow.md](docs/commit-workflow.md)**: Integration mit Commit-Skill
- **[pr-template.md](docs/pr-template.md)**: PR-Best-Practices
- **[troubleshooting.md](docs/troubleshooting.md)**: Fehlerbehebung

## Version

**Version**: 1.0.0
**Date**: 2024-12-21
**Refactored from**: `/create-pr` Command
