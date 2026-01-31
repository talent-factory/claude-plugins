---
name: professional-init-project
description: Initialisiert Open-Source-Projekte mit GitHub Best Practices und Git-Branching-Strategie
version: 1.0.0
---

# Professional Init-Project Workflow

## Overview

Automatisiert die Projekt-Initialisierung mit:
- **Git-Branching**: develop → main Strategie (Standard)
- **Community Standards**: LICENSE, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY
- **GitHub Templates**: Issue-Templates, PR-Template
- **Projekttyp-spezifisch**: Java/Gradle, Python/uv, Node.js, Go, Rust

## Prerequisites

- Git 2.0+
- Python 3.8+ (für Scripts)
- Optional: gh CLI (für GitHub-Repository-Erstellung)
- Optional: Gradle 8.x (für Java, wird via Wrapper bereitgestellt)

## Usage Workflow

1. **Projekttyp erkennen** aus Argumenten:
   - `--git`: Standard Git-Projekt
   - `--java`: Java mit Gradle Kotlin DSL
   - `--uv`: Python mit uv
   - `--node`: Node.js/TypeScript
   - `--go`: Go-Projekt
   - `--rust`: Rust-Projekt

2. **Projekt-Detection ausführen**:
   ```bash
   python scripts/main.py --type <type> --name <name>
   ```

3. **Git-Repository initialisieren**:
   ```bash
   python scripts/git_initializer.py
   ```
   - Erstellt Repository
   - Wechselt zu `develop` Branch
   - Erstellt `main` nach initialem Commit

4. **Projektstruktur generieren**:
   - Community Standards (LICENSE, etc.)
   - GitHub Templates (.github/)
   - Projekttyp-spezifische Dateien

5. **Initialen Commit erstellen**:
   ```bash
   git add .
   git commit -m "feat: Initial open source setup"
   ```

6. **Branches synchronisieren**:
   ```bash
   git branch main  # main von develop erstellen
   ```

## Configuration

### project_types.json

```json
{
  "java": {
    "build_tool": "gradle-kotlin",
    "java_version": 21,
    "test_framework": "junit5"
  },
  "python": {
    "package_manager": "uv",
    "python_version": "3.12"
  }
}
```

## Output

```text
✓ Git-Repository initialisiert
✓ Branch 'develop' erstellt (aktiv)
✓ Projektstruktur generiert (Java/Gradle)
✓ Community Standards erstellt
✓ GitHub Templates erstellt
✓ Initialer Commit erstellt
✓ Branch 'main' erstellt (synchron mit develop)

📁 Projekt bereit: my-project/
   Branch: develop (aktiv)
   Nächster Schritt: Entwicklung starten
```

## Error Handling

**Git nicht installiert:**
- Zeige Fehlermeldung mit Installationsanleitung
- Beende mit Exit-Code 1

**Verzeichnis existiert bereits:**
- Frage ob überschreiben oder abbrechen
- Bei --force: Überschreiben ohne Nachfrage

**Gradle nicht gefunden (bei --java):**
- Erstelle Wrapper manuell aus Templates
- Warnung anzeigen, dass Gradle für Build benötigt wird

## Best Practices

**Atomare Initialisierung:**
- Alle Dateien werden vor dem ersten Commit erstellt
- Kein inkonsistenter Zustand möglich

**Flexible Konfiguration:**
- project_types.json für Anpassungen
- Templates können überschrieben werden

**Erweiterbarkeit:**
- Neue Projekttypen einfach hinzufügbar
- Generator-Module sind unabhängig

## References

- **[docs/branching-strategy.md](docs/branching-strategy.md)**: Git-Branching Details
- **[docs/templates.md](docs/templates.md)**: Template-Anpassung
- **[docs/troubleshooting.md](docs/troubleshooting.md)**: Fehlerbehebung
