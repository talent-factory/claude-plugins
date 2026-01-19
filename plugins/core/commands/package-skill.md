---
description: Validiere und paketiere einen Claude Code Skill als verteilbare ZIP-Datei
allowed-tools:
  - Bash
  - Read
---

# Skill für Distribution paketieren

Validiere und paketiere einen Claude Code Skill als verteilbare ZIP-Datei

## Anweisungen

Dieser Command validiert und paketiert einen bestehenden Skill für die Distribution. Folge diesen Schritten:

### Phase 1: Skill-Auswahl

1. **Zu paketierenden Skill identifizieren**
   - Skill-Speicherort ermitteln (persönlich oder Projekt)
   - Verifizieren, dass Skill existiert und SKILL.md hat
   - Aktuellen Zustand des Skills prüfen

2. **Vorab-Prüfungen**
   - Sicherstellen, dass alle TODOs abgeschlossen sind
   - Verifizieren, dass Dokumentation finalisiert ist
   - Prüfen, dass Beispiele getestet sind

### Phase 2: Validierung

1. **Schnellvalidierung ausführen**
   - Das quick_validate.py-Script verwenden
   - YAML-Frontmatter-Gültigkeit prüfen
   - Erforderliche Felder verifizieren (name, description)
   - Auf verbotene Zeichen prüfen
   - Verzeichnisstruktur validieren

2. **Umfassende Validierung ausführen** (falls Schnellvalidierung bestanden)
   - validate-skill.sh für detaillierte Prüfungen verwenden
   - Alle 10 Validierungsphasen verifizieren
   - Wortanzahl für Progressive Disclosure prüfen
   - Dateireferenzen validieren
   - Script-Syntax testen

3. **Validierungsergebnisse überprüfen**
   - Kritische Fehler beheben
   - Warnungen bei Bedarf adressieren
   - Nach Korrekturen erneut validieren

### Phase 3: Paketierung

1. **Paketierungs-Script ausführen**

   ```bash
   python .claude/commands/skills/references/scripts/package_skill.py <skill-pfad> [ausgabe-verzeichnis]
   ```

2. **Paketerstellungsprozess**
   - Script validiert erneut vor Paketierung
   - Erstellt ZIP-Datei mit Skill-Namen
   - Enthält alle Dateien unter Beibehaltung der Struktur
   - Schliesst versteckte Dateien und `__pycache__` aus

3. **Paket verifizieren**
   - Prüfen, dass ZIP-Datei erfolgreich erstellt wurde
   - Dateianzahl und Grösse notieren
   - Bereitschaft zur Distribution bestätigen

### Phase 4: Distributionsoptionen

1. **Persönliche Distribution**
   - ZIP-Datei direkt teilen
   - Auf Datei-Sharing-Dienst hochladen
   - Installationsanweisungen beifügen

2. **Team-Distribution**
   - Zum gemeinsamen Repository hinzufügen
   - In Team-Speicher hochladen
   - Im Team-Wiki dokumentieren

3. **Öffentliche Distribution**
   - Zum Skill-Marketplace hochladen (falls verfügbar)
   - Auf GitHub teilen
   - Zu Community-Repositories hinzufügen

## Befehlsausführungsablauf

### Schritt 1: Skill lokalisieren

```bash
# Persönliche Skills
ls ~/.claude/skills/

# Projekt-Skills
ls .claude/skills/
```

### Schritt 2: Schnellvalidierung

```bash
python .claude/commands/skills/references/scripts/quick_validate.py <skill-pfad>
```

Erwartete Ausgabe:

- Skill-Validierung bestanden!
- Oder spezifische Fehlermeldungen zum Beheben

### Schritt 3: Umfassende Validierung (Optional)

```bash
.claude/commands/skills/references/scripts/validate-skill.sh <skill-pfad>
```

Erwartete Ausgabe:

- Detaillierter 10-Phasen-Validierungsbericht
- Bewertung und Empfehlungen

### Schritt 4: Paketerstellung

```bash
# Ins aktuelle Verzeichnis paketieren
python .claude/commands/skills/references/scripts/package_skill.py ~/.claude/skills/mein-skill

# In spezifisches Verzeichnis paketieren
python .claude/commands/skills/references/scripts/package_skill.py ~/.claude/skills/mein-skill ./dist
```

Erwartete Ausgabe:

```text
Validiere Skill...
Skill-Validierung bestanden!

Erstelle Paket...
  Hinzugefügt: mein-skill/SKILL.md
  Hinzugefügt: mein-skill/scripts/helper.py
  Hinzugefügt: mein-skill/references/api-docs.md
  ...

Skill erfolgreich paketiert!
   Paket: ./mein-skill.zip
   Dateien: 8
   Grösse: 0.15 MB

Bereit zur Distribution!
```

## Validierungskriterien

Das Paketierungs-Script prüft:

### Erforderliche Elemente

- SKILL.md existiert
- Gültiges YAML-Frontmatter
- Name- und Description-Felder vorhanden
- Keine TODO-Marker in der Beschreibung

### Qualitätsprüfungen

- Beschreibung in dritter Person
- Beschreibung erwähnt, wann Skill zu verwenden ist
- Keine spitzen Klammern in der Beschreibung
- Wortanzahl innerhalb der Grenzen (<5.000 für SKILL.md)

### Strukturvalidierung

- Korrekte Verzeichnisorganisation
- Scripts sind ausführbar
- Dateireferenzen sind gültig
- Kein doppelter Inhalt zwischen SKILL.md und references/

## Distributionsrichtlinien

### Installationsanweisungen-Vorlage

Mit deinem paketierten Skill beifügen:

```markdown
# Installation von {{SKILL_NAME}}

## Persönliche Installation
1. {{skill-name}}.zip herunterladen
2. Nach ~/.claude/skills/ extrahieren
3. Claude Code neu starten

## Projekt-Installation
1. Nach .claude/skills/ im Projekt extrahieren
2. In Versionskontrolle committen
3. Teammitglieder erhalten Skill beim Pull

## Verifizierung
Nach Installation testen mit:
"Verwende den {{SKILL_NAME}} Skill für {{Beispielaufgabe}}"
```

### Versionsverwaltung

Für Skill-Updates:

1. Skill-Dateien aktualisieren
2. Änderungen in SKILL.md dokumentieren
3. Version erhöhen, falls Versionierung verwendet wird
4. Mit gleichem Prozess neu paketieren
5. Neues Paket verteilen

## Fehlerbehebung

### Validierung schlägt fehl

**Problem**: Paketierungs-Script meldet Validierungsfehler

**Lösung**:

1. quick_validate.py ausführen, um spezifische Fehler zu sehen
2. Gemeldete Probleme beheben
3. Validierung erneut ausführen
4. Paketierung erneut versuchen

### Paket nicht erstellt

**Problem**: ZIP-Datei nicht generiert

**Mögliche Ursachen**:

- Validierung fehlgeschlagen (zuerst Fehler beheben)
- Keine Schreibrechte (Verzeichnis prüfen)
- Speicherplatzprobleme (verfügbaren Platz prüfen)

### Scripts nicht ausführbar

**Problem**: Warnung über nicht ausführbare Scripts

**Lösung**:

```bash
chmod +x <skill-pfad>/scripts/*.py
chmod +x <skill-pfad>/scripts/*.sh
```

### Grosse Paketgrösse

**Problem**: Paket ist sehr gross

**Lösungen**:

- Grosse Dokumentationen ins references/-Verzeichnis verschieben
- Unnötige Dateien entfernen
- Bilder komprimieren, falls enthalten
- .gitignore-Muster verwenden

## Best Practices

1. **Alle TODOs abschliessen** vor der Paketierung
2. **Skill gründlich testen** vor der Distribution
3. **Abhängigkeiten klar dokumentieren**
4. **Funktionierende Beispiele beifügen**
5. **Skills versionieren** für Updates
6. **Installation testen** auf sauberem System
7. **Deinstallationsanweisungen beifügen** falls komplex

## Beispiele

### Beispiel 1: Einfachen Skill paketieren

```bash
# Zuerst validieren
python .claude/commands/skills/references/scripts/quick_validate.py ~/.claude/skills/commit-helper

# Falls gültig, paketieren
python .claude/commands/skills/references/scripts/package_skill.py ~/.claude/skills/commit-helper

# Ergebnis: commit-helper.zip erstellt
```

### Beispiel 2: In Distributionsverzeichnis paketieren

```bash
# Dist-Verzeichnis erstellen
mkdir -p ~/skill-packages

# An spezifischen Ort paketieren
python .claude/commands/skills/references/scripts/package_skill.py \
  ~/.claude/skills/pdf-processor \
  ~/skill-packages

# Ergebnis: ~/skill-packages/pdf-processor.zip
```

### Beispiel 3: Korrigieren und neu paketieren

```bash
# Initiale Validierung schlägt fehl
python .claude/commands/skills/references/scripts/quick_validate.py ~/.claude/skills/mein-skill
# Beschreibung enthält TODO-Marker

# Problem beheben
# SKILL.md bearbeiten, um TODOs abzuschliessen

# Erneut validieren
python .claude/commands/skills/references/scripts/quick_validate.py ~/.claude/skills/mein-skill
# Skill-Validierung bestanden!

# Paketieren
python .claude/commands/skills/references/scripts/package_skill.py ~/.claude/skills/mein-skill
# Erfolgreich paketiert!
```

## Ausgabeformat

Der Command liefert klares Feedback:

```text
Paketiere Skill: {{skill-name}}

Validiere Skill...
[Validierungsergebnisse]

Erstelle Paket...
[Dateiliste]

Skill erfolgreich paketiert!
   Paket: {{pfad/zum/paket.zip}}
   Dateien: {{anzahl}}
   Grösse: {{grösse}} MB

Bereit zur Distribution!
```

## Nächste Schritte

Nach der Paketierung:

1. **Installation testen** auf anderem System
2. **Mit Team teilen** oder Community
3. **Im Skill-Katalog dokumentieren**
4. **Feedback sammeln** für Verbesserungen
5. **Updates planen** basierend auf Nutzung

## Verwandte Commands

- `/build-skill` - Neue Skills erstellen
- `/package-skill` - Skill für Distribution paketieren

## Verwendete Scripts

- `package_skill.py` - Haupt-Paketierungs-Script
- `quick_validate.py` - Schnelle Validierung
- `validate-skill.sh` - Umfassende Validierung

Dein Skill ist jetzt bereit zur Distribution!
