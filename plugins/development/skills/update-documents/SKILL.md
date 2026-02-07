---
name: update-documents
description: Synchronisiert Dokumentation zwischen CLAUDE.md, README.md und docs/. Verwende diesen Skill um Dokumentations-Inkonsistenzen zu beheben.
---

# Update Documentation

Synchronisiere die Projekt-Dokumentation automatisch zwischen den verschiedenen Dokumentationsdateien.

## Sync-Regeln

| Source | Abschnitt | Targets |
|--------|-----------|---------|
| CLAUDE.md | Tech Stack | README.md, docs/index.md |
| CLAUDE.md | Development Commands | README.md, docs/development/local-setup.md |
| CLAUDE.md | Project Structure | README.md |
| README.md | Quick Start | docs/getting-started/quickstart.md |

**Prinzip:** CLAUDE.md ist die technische Source of Truth, README.md das User-facing Einstiegsdokument.

## Workflow

### 1. Analyse ausführen

Prüfe zuerst den aktuellen Sync-Status:

```bash
cd ${PROJECT_ROOT} && python ${SKILL_DIR}/scripts/main.py --analyze
```

### 2. Output interpretieren

Das Script zeigt:

- ✓ Synchron: Abschnitte sind identisch
- ⚠ Veraltet: Target weicht von Source ab
- ✗ Fehlend: Section existiert nicht

### 3. Bei Unterschieden synchronisieren

Wenn Unterschiede gefunden wurden:

```bash
cd ${PROJECT_ROOT} && python ${SKILL_DIR}/scripts/main.py --sync
```

### 4. Ergebnis prüfen

Nach dem Sync:

- Prüfe die aktualisierten Dateien auf korrekte Formatierung
- Stelle sicher, dass keine kontextspezifischen Anpassungen verloren gingen
- Bei Bedarf: Manuelle Nachbearbeitung für Target-spezifische Formulierungen

### 5. Zusammenfassung ausgeben

Gib dem User eine kurze Zusammenfassung:

```
✓ Dokumentation synchronisiert

Aktualisiert:
  - README.md: Tech Stack, Development
  - docs/index.md: Tech Stack

Unverändert:
  - docs/getting-started/quickstart.md
```

## Konfiguration anpassen

Die Sync-Regeln sind in `${SKILL_DIR}/config/sync_rules.json` definiert.

Neue Regel hinzufügen:

```json
{
  "id": "neue-regel",
  "source": {"file": "SOURCE.md", "section": "Section Name"},
  "targets": [
    {"file": "TARGET.md", "section": "Target Section"}
  ]
}
```

## Hinweise

- **Keine automatischen Commits**: Der Skill ändert nur Dateien, committed nicht
- **Whitespace-tolerant**: Kleine Formatierungsunterschiede werden ignoriert
- **Section-Matching**: Case-insensitive Heading-Suche
- **Backup**: Bei Bedarf manuell erstellen vor dem Sync
