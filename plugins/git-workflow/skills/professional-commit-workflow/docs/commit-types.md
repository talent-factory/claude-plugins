# Commit-Typen mit Emojis

Emoji Conventional Commit Format für konsistente Git-Historie.

## Standard-Typen

### ✨ feat: Neue Funktionalität

**Verwendung**: Komplett neue Features oder Funktionalität

**Beispiele**:

```text
✨ feat: Benutzer-Dashboard mit Metriken hinzugefügt
✨ feat: OAuth2 Authentifizierung implementiert
✨ feat: Dark Mode Toggle zu Einstellungen hinzugefügt
```

### 🐛 fix: Fehlerbehebung

**Verwendung**: Bug-Fixes und Korrekturen

**Beispiele**:

```text
🐛 fix: Speicherleck in Datenbank-Connection behoben
🐛 fix: Falscher Response-Code bei 404-Errors korrigiert
🐛 fix: Race Condition in async Handler gelöst
```

### 📚 docs: Dokumentation

**Verwendung**: Nur Dokumentationsänderungen

**Beispiele**:

```text
📚 docs: API-Dokumentation für v2 Endpoints aktualisiert
📚 docs: README mit Installationsanleitung ergänzt
📚 docs: JSDoc Kommentare für Core-Module hinzugefügt
```

### 💎 style: Code-Formatierung

**Verwendung**: Formatierung ohne Logikänderung (Whitespace, Einrückung)

**Beispiele**:

```text
💎 style: Prettier Formatierung auf gesamtes Projekt angewendet
💎 style: Einrückung in Config-Dateien korrigiert
💎 style: Trailing Whitespace entfernt
```

### ♻️ refactor: Code-Umstrukturierung

**Verwendung**: Code-Änderungen ohne neue Features oder Fixes

**Beispiele**:

```text
♻️ refactor: User Service in kleinere Module aufgeteilt
♻️ refactor: Dependency Injection für bessere Testbarkeit
♻️ refactor: Deprecated API durch moderne Alternative ersetzt
```

### ⚡ perf: Performance

**Verwendung**: Performance-Verbesserungen

**Beispiele**:

```text
⚡ perf: Datenbank-Queries mit Indexing optimiert
⚡ perf: Lazy Loading für große Komponenten implementiert
⚡ perf: Caching-Layer für API-Responses hinzugefügt
```

### 🧪 test: Tests

**Verwendung**: Tests hinzufügen oder korrigieren

**Beispiele**:

```text
🧪 test: Unit Tests für Authentication Service hinzugefügt
🧪 test: E2E Tests für Checkout-Flow erweitert
🧪 test: Flaky Test in CI/CD Pipeline stabilisiert
```

### 🔧 chore: Wartung

**Verwendung**: Build, Tools, Konfiguration

**Beispiele**:

```text
🔧 chore: Dependencies auf neueste Versionen aktualisiert
🔧 chore: ESLint Konfiguration verschärft
🔧 chore: Build-Script für Production optimiert
```

## Spezial-Typen

### 🚀 ci: Continuous Integration

**Verwendung**: CI/CD Pipeline-Änderungen

**Beispiele**:

```text
🚀 ci: GitHub Actions Workflow für automatisches Deployment
🚀 ci: Test-Coverage Report zu Pipeline hinzugefügt
🚀 ci: Docker Build-Stage optimiert
```

### 🔒 security: Sicherheit

**Verwendung**: Sicherheitsverbesserungen und -fixes

**Beispiele**:

```text
🔒 security: SQL Injection Schwachstelle behoben
🔒 security: CSRF-Protection für Forms implementiert
🔒 security: Abhängigkeiten mit bekannten CVEs aktualisiert
```

### 🌐 i18n: Internationalisierung

**Verwendung**: Übersetzungen und Lokalisierung

**Beispiele**:

```text
🌐 i18n: Deutsche Übersetzung für UI-Komponenten hinzugefügt
🌐 i18n: Datumsformatierung für verschiedene Locales
🌐 i18n: Sprachauswahl-Dropdown implementiert
```

### ♿ a11y: Barrierefreiheit

**Verwendung**: Accessibility-Verbesserungen

**Beispiele**:

```text
♿ a11y: ARIA-Labels für Screen Reader hinzugefügt
♿ a11y: Keyboard-Navigation für Dropdown-Menüs
♿ a11y: Farbkontraste nach WCAG 2.1 AA angepasst
```

### 📦 deps: Dependencies

**Verwendung**: Dependency-Updates (als Alternative zu chore)

**Beispiele**:

```text
📦 deps: React von 18.2 auf 18.3 aktualisiert
📦 deps: Sicherheitsupdate für lodash durchgeführt
📦 deps: Entwicklungs-Dependencies aktualisiert
```

## Best Practices

### Commit-Nachricht Format

```text
<emoji> <type>: <kurze Beschreibung>

[optionaler Body mit Details]

[optionale Footer: Breaking Changes, Issues]
```

### Imperativ-Form verwenden

✅ **Richtig**:

```text
✨ feat: Füge Benutzer-Dashboard hinzu
🐛 fix: Behebe Speicherleck in API
```

❌ **Falsch**:

```text
✨ feat: Dashboard hinzugefügt
🐛 fix: Speicherleck behoben
```

### Länge beachten

- **Subject Line**: ≤ 72 Zeichen
- **Body**: Zeilen mit max. 72 Zeichen umbrechen

### Breaking Changes kennzeichnen

```text
♻️ refactor: API v2 Endpoints eingeführt

BREAKING CHANGE: Alte v1 Endpoints sind deprecated.
Migration Guide siehe docs/migration.md
```
