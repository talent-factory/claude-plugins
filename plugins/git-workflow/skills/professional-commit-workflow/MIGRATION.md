# Migration Guide: `/commit` Command → `professional-commit-workflow` Skill

Dieses Dokument beschreibt die Migration vom alten `/commit` Slash-Command zum neuen `professional-commit-workflow` Skill.

## Warum migrieren?

### Probleme mit dem alten Command-Ansatz

**Performance:**
- ❌ ~1.370 Zeilen Dokumentation bei jedem Aufruf geladen
- ❌ Hoher Token-Verbrauch durch Progressive Disclosure
- ❌ Langsame Verarbeitung bei komplexen Workflows

**Wartung:**
- ❌ Command-Dateien in jedem Projekt dupliziert
- ❌ Schwierige Updates (jedes Projekt einzeln)
- ❌ Version-Drift zwischen Projekten

**Distribution:**
- ❌ Nicht als standalone Package distributable
- ❌ Wiederverwendung erfordert manuelle Kopie

### Vorteile des Skill-Ansatzes

**Performance:**
- ✅ Code statt Prompts → schnellere Ausführung
- ✅ Modulare Validatoren → nur relevante Checks laden
- ✅ Reduzierter Token-Verbrauch (~70% weniger)

**Wartung:**
- ✅ Zentrale Installation → ein Update für alle Projekte
- ✅ Versioniert und getestet
- ✅ Keine Duplikation

**Distribution:**
- ✅ Als ZIP distributable
- ✅ Wiederverwendbar über Projekte hinweg
- ✅ Installation via Git oder Package

## Migrations-Schritte

### Schritt 1: Skill installieren

```bash
# In dotfiles-Repository
cd ~/.dotfiles/agents/claude/skills

# Falls nicht vorhanden, erstellen
mkdir -p ~/.dotfiles/agents/claude/skills

# Skill-Verzeichnis ist bereits vorhanden (erstellt durch dieses Refactoring)
ls -la professional-commit-workflow/
```

### Schritt 2: Dependencies installieren (optional)

```bash
cd ~/.dotfiles/agents/claude/skills/professional-commit-workflow
pip install -r requirements.txt --break-system-packages
```

**Hinweis**: Requirements sind optional. Das Skill funktioniert mit Python Standard Library.

### Schritt 3: Scripts testen

```bash
# In einem Test-Projekt
cd /path/to/test-project

# Project Detection testen
python3 ~/.dotfiles/agents/claude/skills/professional-commit-workflow/scripts/project_detector.py

# Commit Message Generator testen
python3 ~/.dotfiles/agents/claude/skills/professional-commit-workflow/scripts/commit_message.py --generate
```

### Schritt 4: Alten Command deaktivieren (optional)

**Option A: Command umbenennen (für Legacy-Support)**

```bash
cd ~/.dotfiles/agents/_shared/commands
mv commit.md commit-legacy.md
```

**Option B: Command löschen**

```bash
cd ~/.dotfiles/agents/_shared/commands
rm commit.md

# Referenzen bleiben erhalten für Dokumentation
# agents/_shared/references/commit/ bleibt
```

**Option C: Command behalten**

Beide können koexistieren:
- `/commit` für einfache Workflows (Prompt-basiert)
- Skill für komplexe Workflows (Performance-optimiert)

### Schritt 5: Claude Code neu starten

Claude erkennt das neue Skill automatisch nach Neustart.

### Schritt 6: Skill verwenden

In Claude Code:

```
Erstelle einen professionellen Commit mit dem professional-commit-workflow Skill
```

oder

```
Nutze das professional-commit-workflow Skill um Änderungen zu committen
```

## Feature-Vergleich

| Feature | `/commit` Command | Skill |
|---------|------------------|-------|
| **Projekterkennung** | ✅ Via Prompts | ✅ Python Script (schneller) |
| **Pre-Commit-Checks** | ✅ Bash-basiert | ✅ Python-Module (strukturiert) |
| **Commit-Messages** | ✅ Prompt-generiert | ✅ Script-generiert |
| **Emoji Conventional** | ✅ | ✅ |
| **Java-Support** | ✅ | ✅ (optimiert) |
| **Python-Support** | ✅ | ✅ (optimiert) |
| **React-Support** | ✅ | ✅ (optimiert) |
| **Docs-Support** | ✅ | ✅ (optimiert) |
| **Performance** | ❌ Langsam (Prompts) | ✅ Schnell (Code) |
| **Token-Verbrauch** | ❌ Hoch (~1.4k Zeilen) | ✅ Niedrig (~300 Zeilen) |
| **Distribution** | ❌ Nicht standalone | ✅ ZIP/Git distributable |
| **Wiederverwendbar** | ❌ Pro Projekt | ✅ Global |
| **Updates** | ❌ Manuell pro Projekt | ✅ Zentral |
| **Konfigurierbar** | ⚠️ Prompt-Änderungen | ✅ JSON-Config |
| **Erweiterbar** | ⚠️ Prompts bearbeiten | ✅ Python-Module |

## Workflow-Unterschiede

### Alter Command-Workflow

```
User: /commit
↓
Claude lädt commit.md (96 Zeilen)
↓
Claude lädt Progressive Disclosure Dateien:
  - pre-commit-checks.md (150 Zeilen)
  - commit-types.md (205 Zeilen)
  - best-practices.md (333 Zeilen)
  - troubleshooting.md (486 Zeilen)
↓
Claude interpretiert Prompts und führt Bash aus
↓
~5-10 Sekunden Verarbeitung
↓
Commit erstellt
```

**Token-Verbrauch**: ~1.400 Zeilen Prompts

### Neuer Skill-Workflow

```
User: "Erstelle Commit mit professional-commit-workflow"
↓
Claude lädt SKILL.md (~200 Zeilen)
↓
Claude führt Python-Script aus:
  python scripts/main.py
↓
Script führt Validierung, Analyse, Commit durch
↓
~2-3 Sekunden Verarbeitung
↓
Commit erstellt
```

**Token-Verbrauch**: ~200 Zeilen Prompt + Script-Output

## Breaking Changes

### Keine Breaking Changes für Nutzer

Die Migration ist **nicht-invasiv**:

1. ✅ Alter Command kann parallel laufen
2. ✅ Keine Änderungen an bestehenden Projekten nötig
3. ✅ Skill funktioniert sofort nach Installation

### API-Unterschiede (für Entwickler)

**Command-Optionen:**

```bash
# Alt
/commit --no-verify
/commit --force-push
/commit --skip-tests
```

**Skill-Optionen:**

```bash
# Neu (via Python)
python scripts/main.py --no-verify
python scripts/main.py --force-push
python scripts/main.py --skip-tests

# Via Claude (automatisch)
Claude: "Erstelle Commit ohne Checks" → --no-verify
Claude: "Commite und überschreibe Remote" → --force-push
```

## Rollback

Falls Probleme auftreten, Rollback in 2 Schritten:

### 1. Skill deaktivieren

```bash
cd ~/.dotfiles/agents/claude/skills
mv professional-commit-workflow professional-commit-workflow.disabled
```

### 2. Alten Command wiederherstellen

```bash
cd ~/.dotfiles/agents/_shared/commands
# Falls umbenannt:
mv commit-legacy.md commit.md

# Falls gelöscht:
git checkout agents/_shared/commands/commit.md
```

### 3. Claude neu starten

## Troubleshooting

### Skill wird nicht erkannt

**Problem**: Claude findet Skill nicht

**Lösung**:

```bash
# Prüfe Skill-Verzeichnis
ls -la ~/.dotfiles/agents/claude/skills/professional-commit-workflow/

# Prüfe SKILL.md
cat ~/.dotfiles/agents/claude/skills/professional-commit-workflow/SKILL.md | head -10

# Claude Code neu starten
```

### Python-Fehler

**Problem**: "ModuleNotFoundError" oder ähnlich

**Lösung**:

```bash
# Prüfe Python-Version
python3 --version  # Mindestens 3.8

# Prüfe Script-Pfade
cd ~/.dotfiles/agents/claude/skills/professional-commit-workflow
python3 -c "import sys; sys.path.insert(0, 'scripts'); from project_detector import ProjectDetector; print('OK')"
```

### Scripts nicht ausführbar

**Problem**: "Permission denied"

**Lösung**:

```bash
cd ~/.dotfiles/agents/claude/skills/professional-commit-workflow
chmod +x scripts/*.py
```

## Best Practices

### Graduelle Migration

**Phase 1**: Skill installieren, parallel zu Command
- ✅ Beide Ansätze testen
- ✅ Feature-Parität verifizieren
- ✅ Performance vergleichen

**Phase 2**: Skill als Default
- ✅ Hauptsächlich Skill verwenden
- ✅ Command als Fallback behalten

**Phase 3**: Command deaktivieren
- ✅ Command umbenennen oder löschen
- ✅ Nur noch Skill verwenden

### Anpassungen

**Config anpassen**:

```bash
# Commit-Typen erweitern
vim config/commit_types.json

# Validierungs-Regeln anpassen
vim config/validation_rules.json
```

**Eigene Validatoren hinzufügen**:

```python
# scripts/validators/my_validator.py
from base_validator import BaseValidator

class MyValidator(BaseValidator):
    def detect(self):
        return self.file_exists('my_config.yml')

    def validate(self):
        # Custom checks
        pass
```

## Support

Bei Fragen oder Problemen:

1. **Dokumentation**: [README.md](README.md)
2. **Troubleshooting**: [docs/troubleshooting.md](docs/troubleshooting.md)
3. **Issues**: GitHub Issues erstellen

## Zusammenfassung

**Empfehlung**: Migration durchführen für:

- ✅ **Performance-kritische Workflows**
- ✅ **Mehrere Projekte** mit gleichen Anforderungen
- ✅ **Distribution** an andere Nutzer
- ✅ **Erweiterbarkeit** (eigene Validatoren)

**Command behalten** für:

- ✅ **Einfache Workflows** ohne komplexe Validierung
- ✅ **Legacy-Projekte** ohne Änderungsbedarf
- ✅ **Prompt-basierte Anpassungen** bevorzugt

**Hybrid-Ansatz**: Beide parallel nutzen je nach Use Case.

---

**Version**: 1.0.0
**Migration durchgeführt**: 2024-12-21
**Autor**: talent-factory
