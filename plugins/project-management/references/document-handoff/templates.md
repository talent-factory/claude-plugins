# Handoff Templates

## Vollständiges Template

```markdown
# Handoff: [Aufgaben-Titel]

**Datum**: [YYYY-MM-DD HH:MM]
**Branch**: [branch-name]
**Linear Issue**: [TF-XXX] - [Issue-Titel] (falls vorhanden)

## Original-Aufgabe

[Beschreibung der ursprünglichen Anforderung]

**Warum wichtig**: [Business Value / Kontext]

## Bereits erledigt

### Änderungen

| Datei | Änderung | Status |
|-------|----------|--------|
| `path/to/file1.py` | [Beschreibung] | Committed / Uncommitted |
| `path/to/file2.tsx` | [Beschreibung] | Committed / Uncommitted |

### Erfolgreiche Ansätze

1. **[Ansatz 1]**
   - Was: [Beschreibung]
   - Warum erfolgreich: [Begründung]
   - Relevante Dateien: `path/to/file.py:123`

2. **[Ansatz 2]**
   - Was: [Beschreibung]
   - Warum erfolgreich: [Begründung]

## Gescheiterte Versuche

### Versuch 1: [Kurze Beschreibung]

**Was versucht**: [Detaillierte Beschreibung]

**Fehlermeldung**:
```
[Relevante Fehlermeldung oder Log-Output]
```

**Warum gescheitert**: [Analyse der Ursache]

**Lessons Learned**: [Was daraus gelernt wurde]

### Versuch 2: [Kurze Beschreibung]

[Gleiche Struktur wie oben]

## Aktueller Zustand

### Git Status

```bash
[Output von git status]
```

### Uncommitted Changes

```bash
[Output von git diff --stat]
```

### Modified Files

| Datei | Beschreibung der Änderungen |
|-------|----------------------------|
| `path/to/file1.py` | [Kurze Beschreibung] |
| `path/to/file2.tsx` | [Kurze Beschreibung] |

### Environment

- **Services**: [Welche laufen / nicht laufen]
- **Database**: [Status, relevante Daten]
- **Dependencies**: [Relevante Pakete, Versionen]
- **Config**: [Wichtige Konfigurationen]

## Nächste Schritte

### Priorität 1: [Titel]

**Was**: [Detaillierte Beschreibung der Aufgabe]

**Wo**: `path/to/file.py:123-145`

**Wie**:
1. [Schritt 1]
2. [Schritt 2]
3. [Schritt 3]

**Akzeptanzkriterien**:
- [ ] [Kriterium 1]
- [ ] [Kriterium 2]

### Priorität 2: [Titel]

[Gleiche Struktur wie oben]

### Priorität 3: [Titel]

[Gleiche Struktur wie oben]

## Wichtige Referenzen

### Relevante Dateien

| Datei | Zeilen | Warum relevant |
|-------|--------|----------------|
| `path/to/main.py` | 712-750 | [Beschreibung] |
| `path/to/config.ts` | 45-60 | [Beschreibung] |
| `.env.example` | - | [Was beachten] |

### Dokumentation

- [Link zu relevanter Doku]
- [Link zu ähnlichem gelöstem Problem]
- [Link zu API-Dokumentation]

### Code-Patterns

```python
# Beispiel eines wichtigen Patterns im Projekt
def example_pattern():
    # So wird X im Projekt üblicherweise gemacht
    pass
```

## Wichtige Hinweise

- [Warnung 1: z.B. "Nicht X machen, weil Y"]
- [Warnung 2: z.B. "Environment Variable Z muss gesetzt sein"]
- [Besonderheit: z.B. "Tests müssen mit --flag ausgeführt werden"]

## Für den nächsten Agent

[Zusammenfassung in 2-3 Sätzen: Was muss der nächste Agent wissen, um sofort loszulegen? Wichtigste Erkenntnis und nächster konkreter Schritt.]
```

## Minimales Template

Für schnelle Übergaben bei weniger komplexen Aufgaben:

```markdown
# Handoff: [Aufgaben-Titel]

**Datum**: [YYYY-MM-DD HH:MM]
**Branch**: [branch-name]

## Original-Aufgabe

[1-2 Sätze zur Aufgabe]

## Bereits erledigt

- [Änderung 1]
- [Änderung 2]

## Aktueller Zustand

**Modified Files**: [Liste oder "git status" Output]

## Nächste Schritte

1. **[Schritt 1]**: `path/to/file.py:123`
2. **[Schritt 2]**: `path/to/file.tsx:45`

## Für den nächsten Agent

[1-2 Sätze Zusammenfassung]
```

## Template-Auswahl

| Situation | Template | Begründung |
|-----------|----------|------------|
| Komplexe Feature-Entwicklung | Vollständig | Viele Dateien, Dependencies, gescheiterte Versuche |
| Bug-Fix mit Recherche | Vollständig | Gescheiterte Versuche dokumentieren wichtig |
| Einfache Änderung | Minimal | Wenig Kontext nötig |
| Ende des Arbeitstages | Minimal | Nur Status festhalten |
| Team-Übergabe | Vollständig | Maximale Klarheit für andere Person |

## Platzhalter-Erklärung

| Platzhalter | Beschreibung |
|-------------|--------------|
| `[YYYY-MM-DD HH:MM]` | Datum und Uhrzeit der Handoff-Erstellung |
| `[branch-name]` | Aktueller Git-Branch |
| `[TF-XXX]` | Linear Issue ID (falls vorhanden) |
| `path/to/file.py:123` | Dateipfad mit Zeilennummer |
| `path/to/file.py:123-145` | Dateipfad mit Zeilenbereich |
