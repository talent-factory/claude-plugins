---
description: Erstelle professionelle Git-Commits mit automatischen Checks für Java, Python und React Projekte
category: develop
allowed-tools:
  - Bash
  - Read
  - Glob
---

# Claude Command: Commit

Erstelle professionelle Git-Commits mit automatischen Qualitätschecks und konventionellen Commit-Nachrichten.

**Alle Commits und Nachrichten werden in Deutsch verfasst.**

## Verwendung

Standard-Commit:

```bash
/commit
```

Mit Optionen:

```bash
/commit --no-verify     # Überspringt Pre-Commit-Checks
/commit --force-push    # Führt force push aus (Vorsicht!)
/commit --skip-tests    # Überspringt Testausführung
/commit --with-skills   # Erstelle einen Commit mit professional-commit-workflow
```

## Workflow

### Bei `--with-skills` Option

Wenn `--with-skills` verwendet wird, wird der **professional-commit-workflow Skill** aktiviert und der restliche Command-Workflow wird ignoriert:

1. **Skill-Ausführung**: Nutze den professional-commit-workflow Skill
   - Location: `../skills/professional-commit-workflow/`
   - Performance: ~70% schneller als der Command
   - Features: Automatische Projekterkennung, Pre-Commit-Validierung, Emoji Conventional Commits

2. **Skill-Details**: Siehe [professional-commit-workflow README](../skills/professional-commit-workflow/README.md)

### Standard Workflow (ohne `--with-skills`)

1. **Pre-Commit-Checks** (optional mit `--no-verify` überspringen)
   - Automatische Projekterkennung (Java, Python, React, Docs)
   - Relevante Checks ausführen (Build, Tests, Linting)
   - Details siehe: [pre-commit-checks.md](../references/commit/pre-commit-checks.md)

2. **Staging-Analyse**
   - Prüfe gestakte Dateien mit `git status`
   - Füge automatisch Änderungen hinzu falls nötig
   - Zeige Übersicht der zu committenden Dateien

3. **Diff-Analyse**
   - Analysiere `git diff` für Änderungsumfang
   - Erkenne mehrere logische Änderungen
   - Schlage Commit-Aufteilung vor bei Bedarf

4. **Commit-Nachricht**
   - Verwende Emoji Conventional Commit Format
   - Automatische Typerkennung basierend auf Änderungen
   - Deutsche, imperative Beschreibung
   - Referenz: [commit-types.md](../references/commit/commit-types.md)

5. **Commit erstellen**
   - Erstelle Commit mit aussagekräftiger Nachricht
   - **WICHTIG:** KEINE "Co-Authored-By" oder "Generated with Claude Code" Zusätze hinzufügen
   - Optional: Push zum Remote-Repository anbieten

## Commit-Typen (Auswahl)

- ✨ `feat`: Neue Funktionalität
- 🐛 `fix`: Fehlerbehebung
- 📚 `docs`: Dokumentationsänderungen
- 💎 `style`: Code-Formatierung
- ♻️ `refactor`: Code-Umstrukturierung
- ⚡ `perf`: Performance-Verbesserungen
- 🧪 `test`: Tests hinzufügen/korrigieren
- 🔧 `chore`: Build, Tools, Konfiguration

**Vollständige Liste**: [commit-types.md](../references/commit/commit-types.md)

## Unterstützte Projekttypen

- **Java**: Maven, Gradle, Spring Boot
- **Python**: Ruff, Black, pytest, mypy
- **React/Node.js**: ESLint, Prettier, TypeScript, Jest/Vitest
- **Dokumentation**: LaTeX, Markdown, AsciiDoc

**Details zu Checks**: [pre-commit-checks.md](../references/commit/pre-commit-checks.md)

## Professional Commit Workflow Skill

Die `--with-skills` Option nutzt den **professional-commit-workflow Skill** für verbesserte Performance und Wiederverwendbarkeit.

### Vorteile vs. Standard Command

| Feature | Standard Command | Skill (`--with-skills`) |
|---------|------------------|------------------------|
| Performance | Langsam | ✅ ~70% schneller |
| Token-Verbrauch | ~1.4k Zeilen | ✅ ~300 Zeilen |
| Wiederverwendbarkeit | Pro Projekt | ✅ Global installiert |
| Konfigurierbarkeit | Prompts | ✅ JSON-Config |
| Erweiterbarkeit | Begrenzt | ✅ Python-Module |

### Skill Verwendung

```bash
# Direkte Skill-Ausführung (Alternative)
cd ../skills/professional-commit-workflow
python scripts/main.py

# Oder via Command mit --with-skills
/commit --with-skills
```

**Skill-Dokumentation**: [professional-commit-workflow/README.md](../skills/professional-commit-workflow/README.md)

## Commit-Nachricht Format

**WICHTIG:** Commit-Nachrichten dürfen KEINE der folgenden Zusätze enthalten:

- ❌ `🤖 Generated with [Claude Code](https://claude.com/claude-code)`
- ❌ `Co-Authored-By: Claude <noreply@anthropic.com>`
- ❌ Ähnliche automatische Signaturen

Die Commit-Nachricht soll nur den eigentlichen Commit-Inhalt beschreiben.

## Weitere Informationen

- **Best Practices**: [best-practices.md](../references/commit/best-practices.md)
- **Troubleshooting**: [troubleshooting.md](../references/commit/troubleshooting.md)
