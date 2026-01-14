---
description: Erstelle Handoff-Dokumentation vor /compact für nahtlose Weiterarbeit
category: project
argument-hint: "[task-name] [--output <dir>] [--linear-issue TF-XXX]"
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
  - TodoWrite
  - mcp__linear__*
---

# Claude Command: Document Handoff

Erstelle eine umfassende Handoff-Dokumentation vor einem `/compact`, damit ein neuer Agent mit frischem Kontext nahtlos weiterarbeiten kann.

## Verwendung

```bash
# Standard (Task-Name aus Git Branch)
/document-handoff

# Mit explizitem Task-Namen
/document-handoff "Feature Implementation"

# Mit benutzerdefiniertem Ausgabeverzeichnis
/document-handoff "Task Name" --output docs/handoffs

# Mit Linear Issue Referenz
/document-handoff --linear-issue TF-177
```

## Wann verwenden?

**Verwenden wenn:**

- Context wird zu gross und `/compact` ist nötig
- Übergabe an anderen Developer/Agent
- Komplexe Aufgabe muss unterbrochen werden
- Viele gescheiterte Versuche dokumentiert werden müssen
- Am Ende eines Arbeitstages für morgen

**Nicht verwenden wenn:**

- Aufgabe ist in 5 Minuten fertig
- Keine relevanten Änderungen gemacht
- Nur Recherche, keine Implementierung
- Triviale Task ohne wichtigen Kontext

## Workflow

### 1. Informationen sammeln

Sammle automatisch relevante Informationen:

**Git-Status erfassen:**

- Aktueller Branch und uncommitted Changes
- Letzte 5 Commits für Kontext
- Geänderte Dateien (staged und unstaged)

**Projekt-Status:**

- Laufende Services (Docker, etc.)
- TODO/FIXME Kommentare im Code
- Relevante Environment-Variablen

**Linear Integration (optional):**

- Issue-Details abrufen falls `--linear-issue` angegeben
- Verknüpfte Issues und Kommentare

### 2. Dokumentation strukturieren

Erstelle Handoff-Dokument mit folgenden Abschnitten:

| Abschnitt | Inhalt |
|-----------|--------|
| **Original-Aufgabe** | Was soll erreicht werden? |
| **Bereits erledigt** | Änderungen, erfolgreiche Ansätze |
| **Gescheiterte Versuche** | Was nicht funktioniert hat und warum |
| **Aktueller Zustand** | Git Status, Modified Files, Environment |
| **Nächste Schritte** | Priorisierte Liste mit Dateipfaden |
| **Wichtige Referenzen** | Dateien, Dokumentation, Code-Patterns |
| **Für den nächsten Agent** | Zusammenfassung in 2-3 Sätzen |

**Template**: [templates.md](../references/document-handoff/templates.md)

### 3. Dokumentation speichern

**Ausgabe-Verzeichnis:** `.claude/handoffs/`

**Dateiname-Konvention:** `YYYY-MM-DD_[task-slug].md`

Beispiele:

- `.claude/handoffs/2026-01-14_system-prompt-extraction.md`
- `.claude/handoffs/2026-01-14_rbac-regression-fix.md`

### 4. Zusammenfassung ausgeben

Nach Erstellung:

- Pfad zur Handoff-Datei anzeigen
- Wichtigste nächsten Schritte hervorheben
- Hinweis für Weiterarbeit nach `/compact`

## Handoff-Grundprinzipien

### Selbsterklärend

Der nächste Agent braucht **keine Vorkenntnisse**:

- Vollständiger Kontext in der Dokumentation
- Keine impliziten Annahmen
- Alle relevanten Dateipfade mit Zeilennummern

### Actionable

**Konkrete Handlungsanweisungen**:

- "Zeile 123 in `file.py` ändern" statt "Code anpassen"
- Priorisierte nächste Schritte
- Klare Akzeptanzkriterien

### Vollständig

**Alles Relevante dokumentieren**:

- Erfolgreiche UND gescheiterte Versuche
- Fehlermeldungen mit Kontext
- Dependencies und externe Faktoren

## Qualitätskriterien

### Inhalt

- [ ] Original-Aufgabe klar beschrieben
- [ ] Alle Änderungen dokumentiert
- [ ] Gescheiterte Versuche mit Begründung
- [ ] Git-Status aktuell
- [ ] Nächste Schritte priorisiert
- [ ] Dateipfade mit Zeilennummern

### Format

- [ ] Konsistente Markdown-Struktur
- [ ] Code-Blöcke für Befehle und Logs
- [ ] Keine Secrets oder Credentials
- [ ] Professionelle Sprache

## Workflow mit Compact

```bash
# 1. Handoff-Dokumentation erstellen
/document-handoff "Feature Implementation"

# 2. Context komprimieren
/compact

# 3. Neue Session: Dokumentation laden
# "Lies bitte .claude/handoffs/2026-01-14_feature-implementation.md
#  und arbeite an den nächsten Schritten weiter."
```

## Wichtige Hinweise

1. **Vor Compact ausführen**: Die Dokumentation ist nutzlos nach dem Compact, wenn sie nicht erstellt wurde

2. **Keine Secrets**: Niemals API Keys, Passwörter oder Tokens in die Handoff-Dokumentation schreiben

3. **Git-Änderungen committen**: Idealerweise alle wichtigen Änderungen vor Handoff committen

4. **Aufräumen**: Alte Handoff-Dokumente regelmässig archivieren oder löschen

## Weitere Informationen

- **Templates**: [templates.md](../references/document-handoff/templates.md)
  - Vollständiges Handoff-Template
  - Minimales Template für schnelle Übergaben

- **Beispiele**: [examples.md](../references/document-handoff/examples.md)
  - Minimal-Beispiel
  - Vollständiges Beispiel

- **Best Practices**: [best-practices.md](../references/document-handoff/best-practices.md)
  - Tipps für effektive Handoffs
  - Häufige Fehler vermeiden

## Siehe auch

- **[/create-plan](./create-plan.md)** - Projektplan erstellen
- **[/implement-task](./implement-task.md)** - Task implementieren

---

**Task-Name**: $ARGUMENTS
