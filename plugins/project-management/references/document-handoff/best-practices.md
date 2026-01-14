# Handoff Best Practices

## Grundprinzipien

### 1. Selbsterklärend schreiben

Der nächste Agent hat **keinen vorherigen Kontext**. Schreibe so, dass jemand ohne Vorkenntnisse sofort verstehen kann:

**Gut:**
> Die Funktion `validateUser()` in `src/auth/validator.ts:45` wirft einen TypeError, weil `user.roles` undefined ist wenn der User über OAuth kommt. Die Rolle muss aus dem OAuth-Token extrahiert werden (siehe `src/auth/oauth.ts:123`).

**Schlecht:**
> Die Validierung funktioniert nicht bei OAuth-Usern.

### 2. Spezifisch sein

Immer konkrete Dateipfade und Zeilennummern angeben:

| Schlecht | Gut |
|----------|-----|
| "im Auth-Modul" | `src/auth/validator.ts:45-67` |
| "die Config anpassen" | `config/database.yml:12` (Wert von X auf Y ändern) |
| "Test fixen" | `tests/unit/auth.test.ts:89` (`describe` Block für OAuth) |

### 3. Gescheiterte Versuche dokumentieren

**Warum wichtig**: Verhindert, dass der nächste Agent die gleichen Fehler macht.

**Was dokumentieren**:
- Was wurde versucht?
- Welche Fehlermeldung kam?
- Warum hat es nicht funktioniert?
- Was wurde daraus gelernt?

### 4. Priorisieren

Nächste Schritte immer nach Priorität ordnen:

```markdown
### Priorität 1: [Blockierend]
### Priorität 2: [Wichtig]
### Priorität 3: [Nice-to-have]
```

## DO: Best Practices

### Vor der Handoff-Erstellung

- ✅ **Änderungen committen** (wenn möglich)
- ✅ **Git Status prüfen** und dokumentieren
- ✅ **Offene Fragen notieren**
- ✅ **Fehlermeldungen kopieren** (nicht paraphrasieren)

### In der Dokumentation

- ✅ **Kontext erklären**: Warum wurde etwas gemacht?
- ✅ **Dateipfade mit Zeilennummern**: `file.py:123` oder `file.py:123-145`
- ✅ **Code-Beispiele**: Wichtige Patterns zeigen
- ✅ **Screenshots/Logs**: Bei UI-Problemen oder komplexen Errors
- ✅ **Links**: Zu relevanter Dokumentation, Issues, PRs

### Für den nächsten Agent

- ✅ **Zusammenfassung**: 2-3 Sätze, was am wichtigsten ist
- ✅ **Erster Schritt**: Konkreter Startpunkt
- ✅ **Warnungen**: Was sollte vermieden werden?

## DON'T: Häufige Fehler

### Inhaltliche Fehler

- ❌ **Vage Beschreibungen**: "Code funktioniert nicht"
- ❌ **Fehlende Kontextinformationen**: Nur Symptome, keine Ursachen
- ❌ **Implizite Annahmen**: "Wie besprochen" (wurde nicht besprochen)
- ❌ **Unvollständige Fehlermeldungen**: Nur die letzte Zeile

### Sicherheitsfehler

- ❌ **Secrets dokumentieren**: API Keys, Passwörter, Tokens
- ❌ **Credentials in Code-Beispielen**: Auch nicht als Platzhalter
- ❌ **Private URLs**: Interne Dashboards, Admin-Panels

### Strukturelle Fehler

- ❌ **Zu lange Dokumente**: Fokus auf das Wesentliche
- ❌ **Keine Priorisierung**: Alles gleich wichtig
- ❌ **Fehlende nächste Schritte**: Nur Ist-Zustand

## Qualitätscheckliste

### Vor dem Speichern prüfen

```markdown
## Inhalt
- [ ] Original-Aufgabe klar beschrieben
- [ ] Alle relevanten Änderungen dokumentiert
- [ ] Gescheiterte Versuche mit Begründung
- [ ] Nächste Schritte priorisiert
- [ ] Dateipfade mit Zeilennummern

## Sicherheit
- [ ] Keine API Keys oder Tokens
- [ ] Keine Passwörter oder Credentials
- [ ] Keine internen URLs (ausser Linear Issues)

## Nutzbarkeit
- [ ] Selbsterklärend ohne Vorkenntnisse
- [ ] Konkrete Handlungsanweisungen
- [ ] Zusammenfassung für schnellen Einstieg
```

## Spezielle Situationen

### Bei komplexen Bugs

```markdown
## Symptom
[Was passiert?]

## Reproduktion
1. [Schritt 1]
2. [Schritt 2]
3. [Fehler tritt auf]

## Erwartetes Verhalten
[Was sollte passieren?]

## Bisherige Analyse
- Hypothese A: [Beschreibung] → [Ergebnis]
- Hypothese B: [Beschreibung] → [Ergebnis]

## Verdächtige Stellen
- `file.py:123` - [Warum verdächtig]
```

### Bei Feature-Entwicklung

```markdown
## Implementierungsstand
| Komponente | Status | Datei |
|------------|--------|-------|
| Backend API | ✅ Fertig | `api/routes.py` |
| Frontend UI | 🔄 In Arbeit | `components/Feature.tsx` |
| Tests | ❌ Fehlt | - |

## Architektur-Entscheidungen
- [Entscheidung 1]: [Begründung]
- [Entscheidung 2]: [Begründung]
```

### Bei Team-Übergaben

Zusätzliche Informationen für menschliche Entwickler:

```markdown
## Kontext für Entwickler
- **Deadline**: [Falls relevant]
- **Stakeholder**: [Wer wartet auf das Feature?]
- **Dependencies**: [Andere Teams/Services]
- **Review benötigt**: [Ja/Nein, von wem]
```

## Beispiel: Vorher/Nachher

### Vorher (Schlecht)

> Die Auth funktioniert nicht. Hab verschiedenes probiert. Muss noch gefixt werden.

### Nachher (Gut)

> **Problem**: OAuth-Login wirft TypeError bei `user.roles` (undefined).
>
> **Ursache**: OAuth-Provider liefert Rollen im `permissions` Feld, nicht `roles`.
>
> **Gescheitert**: Direktes Mapping in `oauth.ts:45` → Brach bestehende Email-Auth.
>
> **Nächster Schritt**: Adapter-Pattern in `src/auth/adapters/` implementieren, der beide Formate normalisiert. Siehe `src/auth/adapters/email.ts` als Referenz.

## Workflow-Integration

### Mit /compact

```bash
# 1. Vor Compact: Handoff erstellen
/document-handoff "Feature Name"

# 2. Compact ausführen
/compact

# 3. Nach Compact: Handoff laden
"Lies .claude/handoffs/2026-01-14_feature-name.md und arbeite weiter."
```

### Mit Linear

```bash
# Handoff mit Linear Issue verknüpfen
/document-handoff --linear-issue TF-123

# Handoff referenziert automatisch:
# - Issue-Details
# - Akzeptanzkriterien
# - Verknüpfte Issues
```

### Mit Git Workflow

```bash
# Vor Handoff: Änderungen committen
/commit "WIP: Feature in Arbeit"

# Dann Handoff erstellen
/document-handoff

# Handoff enthält automatisch:
# - Branch-Name
# - Letzte Commits
# - Uncommitted Changes
```
