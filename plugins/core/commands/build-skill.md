---
description: Erstelle umfassende Claude Code Skills durch Elicitation-getriebene Entwicklung
allowed-tools:
  - Task
  - Read
  - Write
---

# Claude Code Skill erstellen

Erstelle umfassende Claude Code Skills durch Elicitation-getriebene Entwicklung

## Anweisungen

Dieser Command orchestriert vier spezialisierte Agenten, um produktionsreife Claude Code Skills aus Benutzeranforderungen zu erstellen. Folge diesem strukturierten Workflow:

### Phase 1: Anforderungserhebung

**Agent**: `skill-elicitation-agent`

1. **Elicitation-Agent aktivieren**
   - Starte den skill-elicitation-agent mit dem Task-Tool
   - Gib Kontext: "Der Benutzer möchte einen neuen Claude Code Skill erstellen"
   - Füge alle initialen Anforderungen oder Ideen hinzu, die der Benutzer geteilt hat

2. **Elicitation-Fragen**
   - Der Agent stellt 3-5 gezielte Fragen, um zu verstehen:
     - Zweck und Umfang des Skills
     - Komplexitäts- und Strukturanforderungen
     - Benötigte Tool-Berechtigungen
     - Kontext und Referenzen
     - Erfolgskriterien

3. **Spezifikationserstellung**
   - Agent erstellt ein umfassendes Skill-Spezifikationsdokument
   - Enthält: Metadaten, Struktur, Anweisungsübersicht, Code-Anforderungen, Beispiele, Abhängigkeiten
   - Verwendet Progressive-Disclosure-Strategie
   - Validiert Vollständigkeit vor dem Fortfahren

4. **Benutzerfreigabe**
   - Präsentiere die Spezifikation dem Benutzer
   - Bestätige Verständnis und Zustimmung
   - Nimm Anpassungen vor, falls nötig
   - Hole explizite Freigabe zum Fortfahren mit der Generierung

### Phase 2: Skill-Generierung

**Agent**: `skill-generator-agent`

1. **Generator-Agent aktivieren**
   - Starte den skill-generator-agent mit dem Task-Tool
   - Übergib das freigegebene Spezifikationsdokument
   - Spezifiziere Zielort (persönlicher, Projekt- oder Plugin-Skill)

2. **Verzeichnisstruktur erstellen**
   - Agent erstellt die entsprechende Verzeichnisstruktur:

     ```text
     skill-name/
     ├── SKILL.md (erforderlich)
     ├── reference.md (falls benötigt)
     ├── examples.md (falls benötigt)
     ├── scripts/ (falls benötigt)
     └── templates/ (falls benötigt)
     ```

3. **SKILL.md-Generierung**
   - Erstellt Haupt-Skill-Datei mit korrektem Frontmatter
   - Enthält klare Anweisungen und Beispiele
   - Folgt Progressive-Disclosure-Prinzipien
   - Verlinkt zu unterstützenden Dateien

4. **Unterstützende Dateien generieren**
   - Erstellt Referenzdokumentation
   - Generiert Beispieldateien
   - Schreibt Scripts mit korrekter Fehlerbehandlung
   - Erstellt wiederverwendbare Templates

5. **Abhängigkeitsdokumentation**
   - Dokumentiert alle erforderlichen Pakete
   - Stellt Installationsanweisungen bereit
   - Notiert Versionsanforderungen

6. **Qualitätsprüfungen**
   - Validiert YAML-Frontmatter
   - Prüft Dateistruktur
   - Verifiziert Code-Syntax
   - Testet Progressive Disclosure

### Phase 3: Validierung und Tests

**Agent**: `skill-validator-agent`

1. **Validator-Agent aktivieren**
   - Starte den skill-validator-agent mit dem Task-Tool
   - Gib Pfad zum generierten Skill an
   - Fordere umfassende Validierung an

2. **YAML-Validierung**
   - Prüfe Frontmatter-Syntax
   - Verifiziere erforderliche Felder
   - Validiere optionale Felder
   - Teste YAML-Parsing

3. **Beschreibungsanalyse**
   - Bewerte Auffindbarkeit
   - Prüfe Trigger-Schlüsselwörter
   - Verifiziere Klarheit und Vollständigkeit
   - Vergleiche mit Best Practices

4. **Strukturvalidierung**
   - Verifiziere Dateiorganisation
   - Prüfe alle Referenzen
   - Teste Script-Ausführung
   - Validiere Berechtigungen

5. **Code-Tests**
   - Syntax-Validierung
   - Sicherheitsprüfungen
   - Abhängigkeitsverifizierung
   - Fehlerbehandlungstests

6. **Integrationstests**
   - Teste Skill-Laden
   - Verifiziere Triggering
   - Prüfe Ausführungsablauf
   - Validiere Ausgaben

7. **Validierungsbericht**
   - Generiere umfassenden Bericht
   - Bewerte jede Kategorie
   - Liste Probleme nach Schweregrad
   - Stelle umsetzbare Korrekturen bereit

8. **Problemlösung**
   - Falls Probleme gefunden, arbeite mit Generator-Agent zur Behebung
   - Re-validiere nach Korrekturen
   - Iteriere bis Validierung bestanden

### Phase 4: Dokumentationsverbesserung

**Agent**: `skill-documenter-agent`

1. **Documenter-Agent aktivieren**
   - Starte den skill-documenter-agent mit dem Task-Tool
   - Gib Skill-Pfad und Spezifikation an
   - Fordere umfassende Dokumentation an

2. **SKILL.md-Verbesserung**
   - Verfeinere Anweisungen für Klarheit
   - Füge umfassende Beispiele hinzu
   - Integriere Best Practices
   - Erstelle Troubleshooting-Abschnitt

3. **Referenzdokumentation**
   - Erstelle detaillierte technische Referenz (falls benötigt)
   - Dokumentiere API und Konfiguration
   - Stelle fortgeschrittene Muster bereit
   - Integriere Performance-Tuning-Tipps

4. **Beispielsammlung**
   - Generiere Beispiele von Anfänger bis Fortgeschritten
   - Füge Troubleshooting-Beispiele hinzu
   - Zeige Integrationsmuster
   - Stelle Fallstudien bereit

5. **README-Erstellung**
   - Erstelle Skill-Verzeichnis-README (falls zur Verteilung)
   - Dokumentiere Installation
   - Stelle Schnellstart bereit
   - Verlinke zur vollständigen Dokumentation

6. **Dokumentationsqualitätsprüfung**
   - Verifiziere Klarheit und Vollständigkeit
   - Teste alle Code-Beispiele
   - Prüfe Organisation
   - Validiere Genauigkeit

### Phase 5: Finale Lieferung

1. **Zusammenfassung generieren**
   - Liste alle erstellten Dateien
   - Dokumentiere Speicherort (persönlich/Projekt/Plugin)
   - Stelle Nutzungsanweisungen bereit
   - Füge Testszenarien hinzu

2. **Installationsverifizierung**
   - Bestätige, dass Skill am korrekten Ort ist
   - Verifiziere Dateiberechtigungen
   - Prüfe, dass Abhängigkeiten dokumentiert sind
   - Teste Skill-Laden

3. **Nutzungsanleitung**
   - Erkläre, wie der Skill ausgelöst wird
   - Stelle Beispiel-Prompts bereit
   - Zeige erwartetes Verhalten
   - Verlinke zur Dokumentation

4. **Nächste Schritte**
   - Schlage Testansatz vor
   - Empfehle Verbesserungen
   - Erkläre Wartung
   - Notiere zukünftige Erweiterungen

## Agentenkoordination

### Sequenzieller Ablauf

```text
Benutzeranfrage
    ↓
skill-elicitation-agent (Anforderungen)
    ↓
Benutzerfreigabe
    ↓
skill-generator-agent (Erstellung)
    ↓
skill-validator-agent (Tests)
    ↓
Korrekturen falls nötig (zurück zum Generator)
    ↓
skill-documenter-agent (Verbesserung)
    ↓
Finale Lieferung
```

### Agentenkommunikation

**Zwischen Agenten**:

- Elicitation → Generator: Übergabe des Spezifikationsdokuments
- Generator → Validator: Übergabe von Skill-Ort und Dateien
- Validator → Generator: Übergabe von Validierungsproblemen (falls vorhanden)
- Generator → Documenter: Übergabe des Skills zur Verbesserung
- Documenter → Benutzer: Finale Dokumentation

**Mit Benutzer**:

- Freigabe nach Elicitation einholen
- Standortpräferenz bestätigen (persönlich/Projekt)
- Validierungsergebnisse überprüfen
- Finales Ergebnis freigeben

## Best Practices

1. **Immer mit Elicitation beginnen**
   - Die Fragephase nicht überspringen
   - Tiefgreifend verstehen vor dem Bauen
   - Benutzerfreigabe zur Spezifikation einholen

2. **Alle vier Agenten verwenden**
   - Jeder hat spezialisierte Expertise
   - Vollständiger Ablauf sichert Qualität
   - Den Prozess nicht abkürzen

3. **Basierend auf Validierung iterieren**
   - Probleme sofort beheben
   - Nach Änderungen re-validieren
   - Nicht mit Fehlern fortfahren

4. **Umfassend testen**
   - Manuelles Trigger-Testing
   - Script-Ausführungstests
   - Integrationstests
   - Tests mit realen Szenarien

5. **Gründlich dokumentieren**
   - Klare Anweisungen
   - Umfassende Beispiele
   - Troubleshooting-Anleitungen
   - Best Practices

## Speicherortoptionen

### Persönliche Skills (`~/.claude/skills/`)

Verwenden für:

- Individuelle Workflows
- Experimentelle Skills
- Persönliche Präferenzen
- Private Tools

### Projekt-Skills (`.claude/skills/`)

Verwenden für:

- Team-geteilte Workflows
- Projektspezifische Expertise
- Versionskontrollierte Skills
- Kollaborative Tools

### Plugin-Skills (Plugin-Verzeichnisstruktur)

Verwenden für:

- Verteilbare Skills
- Marketplace-Deployment
- Öffentliches Teilen
- Gebündelte Fähigkeiten

## Ausgabeformat

Stelle dem Benutzer eine umfassende Zusammenfassung bereit:

```text
Skill erfolgreich erstellt!

Skill: [Skill-Name]
Speicherort: [Pfad]
Typ: [einfach/multi-file/tool-restricted/code-execution]

Erstellte Dateien:
- SKILL.md - Haupt-Skill-Anweisungen
- reference.md - Technische Referenz (falls erstellt)
- examples.md - Umfassende Beispiele (falls erstellt)
- scripts/[name].py - Hilfsskripte (falls erstellt)
- README.md - Installationsanleitung (falls erstellt)

Validierung: BESTANDEN (Bewertung: X/10)

Abhängigkeiten:
[Liste falls vorhanden, oder "Keine"]

Nutzung:
Löse diesen Skill aus durch:
- "[Beispiel-Trigger 1]"
- "[Beispiel-Trigger 2]"

Oder explizit: "Verwende [skill-name] für [Aufgabe]"

Testen mit:
[Spezifisches Testszenario]

Dokumentation:
- Siehe SKILL.md für Anweisungen
- Siehe examples.md für umfassende Beispiele
- Siehe reference.md für technische Details

Nächste Schritte:
1. Teste den Skill mit bereitgestellten Szenarien
2. Verfeinere basierend auf Nutzung
3. Teile mit Team (falls Projekt-Skill)
4. Erwäge, weitere Beispiele hinzuzufügen
```

## Fehlerbehebung

**Agent nicht gefunden**: Stelle sicher, dass `.claude/agents/skill-builder/` mit allen Agent-Dateien existiert

**Berechtigungsfehler**: Prüfe Dateiberechtigungen mit `chmod +x scripts/*.py`

**YAML-Fehler**: Validator wird diese erfassen und melden

**Agent-Verwirrung**: Verwende explizite Agent-Namen: "Starte skill-elicitation-agent"

## Beispiele

### Beispiel 1: Einfacher Nur-Anweisungen-Skill

**Anfrage**: "Erstelle einen Skill zum Schreiben von Conventional Commit Messages"

**Ablauf**:

1. Elicitation fragt nach Commit-Stil, Projekten, Beispielen
2. Generiert einfache einzelne SKILL.md
3. Validiert Struktur und Beschreibung
4. Dokumentiert mit Beispielen und Best Practices

### Beispiel 2: Multi-File-Skill mit Scripts

**Anfrage**: "Erstelle einen Skill zum Ausfüllen von PDF-Formularen"

**Ablauf**:

1. Elicitation fragt nach PDF-Typen, Operationen, Abhängigkeiten
2. Generiert SKILL.md + scripts/fill_form.py + FORMS.md
3. Validiert Code-Ausführung und Dateistruktur
4. Dokumentiert mit umfassenden Beispielen und API-Referenz

### Beispiel 3: Tool-beschränkter Read-Only-Skill

**Anfrage**: "Erstelle einen Skill für Sicherheits-Code-Analyse"

**Ablauf**:

1. Elicitation ermittelt Read-Only-Anforderung
2. Generiert SKILL.md mit allowed-tools: Read, Grep, Glob
3. Validiert Tool-Beschränkungen
4. Dokumentiert Sicherheitsmuster und Analysetechniken

## Denke daran

- **Qualität vor Geschwindigkeit** - Nimm dir Zeit für gründliche Elicitation
- **Benutzereinbindung** - Hole Freigabe an wichtigen Stellen ein
- **Umfassende Validierung** - Teste alles
- **Exzellente Dokumentation** - Mache Skills einfach nutzbar
- **Iterative Verbesserung** - Skills können sich mit der Zeit weiterentwickeln

Dieser Command stellt sicher, dass jeder Skill produktionsreif, gut dokumentiert ist und den Claude Code Best Practices folgt!
