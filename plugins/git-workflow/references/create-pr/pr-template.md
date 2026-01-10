# Pull Request Template und Best Practices

## Standard PR-Template

### Grundstruktur

```markdown
## Beschreibung

[Kurze Zusammenfassung der Änderungen in 2-3 Sätzen]

## Änderungen

- Hauptänderung 1
- Hauptänderung 2
- Hauptänderung 3

## Test-Plan

- [ ] Manuelle Tests durchgeführt
- [ ] Unit Tests laufen durch
- [ ] Integration Tests erfolgreich
- [ ] E2E Tests durchgeführt (falls relevant)

## Breaking Changes

[Falls vorhanden, Breaking Changes auflisten]
[Oder: "Keine"]

## Zusätzliche Informationen

[Screenshots, Links, weitere Kontext-Informationen]
```

## Beschreibungs-Abschnitt

### Was gehört in die Beschreibung?

**Gute Beschreibung**:

- **Was**: Welche Änderungen wurden gemacht?
- **Warum**: Warum waren diese Änderungen nötig?
- **Wie**: Wie wurde das Problem gelöst?

**Beispiel**:

```markdown
## Beschreibung

Diese PR implementiert Rate Limiting für alle API-Endpoints, um DoS-Angriffe
zu verhindern. Der Token-Bucket-Algorithmus limitiert Requests auf 100 pro
Minute pro User. Bei Überschreitung wird HTTP 429 zurückgegeben.
```

### Kontext bieten

**Hilfreich für Reviewer**:

- Ticket/Issue-Links
- Design-Dokumente
- Vorherige PRs
- Diskussionen

**Beispiel**:

```markdown
## Kontext

Diese Änderung adressiert #123 und implementiert das Design aus
docs/rate-limiting-spec.md. Siehe auch #456 für verwandte Diskussion.
```

## Änderungs-Liste

### Strukturierte Übersicht

**Nach Kategorien gruppieren**:

```markdown
## Änderungen

### Backend

- ✨ Rate Limiting Middleware implementiert
- ♻️ API-Error-Handling verbessert
- 🧪 Integration Tests für Rate Limiting

### Frontend

- 💎 Error-Anzeige für 429 Responses
- 📚 Benutzer-Dokumentation aktualisiert

### Infrastructure

- 🔧 Redis für Rate-Limit-Speicherung konfiguriert
```

### Quantifizierung

**Messbare Änderungen erwähnen**:

```markdown
## Änderungen

- ✨ 3 neue API-Endpoints hinzugefügt
- 🧪 Test-Coverage von 75% auf 92% erhöht
- ⚡ API-Response-Zeit um 40% verbessert
- 🐛 5 kritische Bugs behoben
```

## Test-Plan

### Umfassende Test-Checkliste

```markdown
## Test-Plan

### Unit Tests

- [x] Alle bestehenden Tests laufen durch
- [x] 15 neue Tests für Rate Limiting hinzugefügt
- [x] Test-Coverage > 90%

### Integration Tests

- [x] Rate Limiting bei normalem Traffic
- [x] 429 Response bei Limit-Überschreitung
- [x] Redis-Failover-Szenario getestet

### Manuelle Tests

- [x] API-Calls mit verschiedenen Users
- [x] Grenzwert-Tests (99, 100, 101 Requests)
- [x] Performance unter Last

### E2E Tests

- [x] Frontend zeigt 429-Error korrekt an
- [x] Retry-Logic funktioniert
- [x] User wird über Limit informiert

### Performance Tests

- [x] Load-Test mit 1000 concurrent Users
- [x] Latenz < 10ms für Rate-Limit-Check
- [x] Redis-Memory-Usage akzeptabel
```

### Test-Ergebnisse

**Konkrete Zahlen hinzufügen**:

```markdown
## Test-Ergebnisse

- ✅ 127/127 Unit Tests passed
- ✅ 45/45 Integration Tests passed
- ✅ Load Test: 10,000 req/s ohne Fehler
- ✅ Memory: 150MB Redis (acceptable)
```

## Breaking Changes

### Klare Kommunikation

**Falls Breaking Changes vorhanden**:

```markdown
## Breaking Changes

### API Endpoint Änderungen

❌ **Entfernt**: `GET /api/v1/users/list`

✅ **Neu**: `GET /api/v2/users` (mit Pagination)

### Migration

Für Migration von v1 zu v2:

1. Update API-Base-URL zu `/api/v2`
2. Implementiere Pagination-Handling
3. Siehe Migration Guide: docs/migration-v1-v2.md

### Deprecation Timeline

- **2024-11-01**: v1 als deprecated markiert
- **2024-12-01**: v1 wird entfernt
```

### Keine Breaking Changes

**Explizit kommunizieren**:

```markdown
## Breaking Changes

Keine. Diese PR ist vollständig abwärtskompatibel.
```

## Zusätzliche Informationen

### Screenshots

**UI-Änderungen visualisieren**:

```markdown
## Screenshots

### Vorher

![Before](https://example.com/before.png)

### Nachher

![After](https://example.com/after.png)

### Mobile View

![Mobile](https://example.com/mobile.png)
```

### Performance-Metriken

```markdown
## Performance-Vergleich

| Metrik | Vorher | Nachher | Verbesserung |
|--------|--------|---------|--------------|
| API Latenz | 150ms | 90ms | 40% |
| DB Queries | 15 | 3 | 80% |
| Memory | 500MB | 350MB | 30% |
```

### Code-Beispiele

```markdown
## Verwendung

```python
# Vorher
user = User.query.get(id)

# Nachher
user = UserService.get_by_id(id)  # Mit Caching
```

## PR-Titel Best Practices

### Klare, prägnante Titel

✅ **Gut**:

```text
✨ feat: Rate Limiting für API-Endpoints implementiert
🐛 fix: Memory Leak in WebSocket-Connections behoben
♻️ refactor: User Service in Microservices aufgeteilt
```

❌ **Schlecht**:

```text
updates
fix stuff
changes
PR for feature
```

### Titel-Format

**Format**: `<emoji> <type>: <description>`

- **Länge**: 50-70 Zeichen
- **Sprache**: Konsistent (Deutsch oder Englisch)
- **Imperativ**: "Implementiert" nicht "Implementieren"

## Labels und Tags

### Automatische Labels

**Basierend auf Commit-Typen**:

- `feat` → `enhancement`, `feature`
- `fix` → `bug`, `bugfix`
- `docs` → `documentation`
- `refactor` → `refactoring`
- `perf` → `performance`
- `test` → `testing`

### Zusätzliche Labels

**Manuell hinzufügen**:

- `needs-review` - Wartet auf Review
- `work-in-progress` - Noch nicht fertig
- `breaking-change` - Breaking Changes
- `high-priority` - Dringend
- `dependencies` - Dependency-Updates

## Reviewer-Zuweisung

### Wen zuweisen?

**Code-Ownership**:

- Experten für betroffene Module
- Team-Mitglieder mit Kontext
- Mindestens 1-2 Reviewer

**CODEOWNERS** (`.github/CODEOWNERS`):

```text
# Backend
/src/api/**        @backend-team @senior-dev

# Frontend
/src/components/** @frontend-team

# Docs
/docs/**          @tech-writers
```

## Review-Prozess

### Als PR-Ersteller

**Checkliste vor Review-Anfrage**:

- [ ] Self-Review durchgeführt
- [ ] Alle Checks (CI/CD) sind grün
- [ ] Tests laufen durch
- [ ] Dokumentation aktualisiert
- [ ] Screenshots hinzugefügt (bei UI-Änderungen)
- [ ] Breaking Changes dokumentiert

### Review-Kommentare adressieren

**Workflow**:

1. **Kommentare lesen** und verstehen
2. **Fragen klären** wenn unklar
3. **Änderungen umsetzen**
4. **Commit und Push**
5. **Kommentare als "Resolved" markieren**
6. **Reviewer re-reviewen lassen**

## Draft vs. Ready PRs

### Draft PR

**Wann verwenden**:

```bash
/create-pr --draft
```

**Für**:

- Work in Progress
- Feedback zu Ansatz einholen
- CI/CD testen
- Frühes Review

**Label**: Automatisch als "Draft" markiert

### Ready PR

**Wann verwenden**:

- Code ist fertig
- Tests laufen durch
- Bereit für Review und Merge

**Conversion**:

```bash
gh pr ready <pr-number>
```

## PR-Größe

### Ideale Größe

**Empfehlung**:

- **150-400 Zeilen**: Ideal für Review
- **400-800 Zeilen**: Noch akzeptabel
- **800+**: Zu groß, sollte aufgeteilt werden

### Zu große PRs aufteilen

**Strategien**:

1. **Nach Features**: Jedes Feature eigene PR
2. **Nach Schichten**: Backend, Frontend, Tests
3. **Nach Refactoring**: Refactoring → Feature
4. **Stacked PRs**: PR1 → PR2 → PR3

**Beispiel für Stacked PRs**:

```text
PR #1: ♻️ refactor: User Service Refactoring
PR #2: ✨ feat: Rate Limiting (base on #1)
PR #3: 🧪 test: Integration Tests (base on #2)
```

## Merge-Strategien

### Squash and Merge

**Wann**: Feature-Branches mit vielen kleinen Commits

**Resultat**: Ein sauberer Commit in main

```
Squash and Merge: ✨ feat: Rate Limiting implementiert
```

### Rebase and Merge

**Wann**: Branches mit sauberer Commit-Historie

**Resultat**: Alle Commits werden in main übernommen

```text
✨ feat: Rate Limiting Middleware
🧪 test: Rate Limiting Tests
📚 docs: Rate Limiting Dokumentation
```

### Merge Commit

**Wann**: Feature-Branches die als Einheit erhalten bleiben sollen

**Resultat**: Merge-Commit mit kompletter Historie

```
Merge pull request #123 from feature/rate-limiting
```

## PR-Beschreibung Templates

### Projektspezifische Templates

**GitHub Template** (`.github/pull_request_template.md`):

```markdown
## Beschreibung

<!-- Kurze Zusammenfassung -->

## Typ der Änderung

- [ ] 🐛 Bug Fix
- [ ] ✨ Neues Feature
- [ ] ♻️ Refactoring
- [ ] 📚 Dokumentation
- [ ] 🧪 Tests

## Test-Plan

<!-- Beschreibe wie du getestet hast -->

## Checkliste

- [ ] Code folgt Projekt-Style-Guide
- [ ] Self-Review durchgeführt
- [ ] Tests hinzugefügt/aktualisiert
- [ ] Dokumentation aktualisiert
- [ ] Keine Merge-Konflikte

## Screenshots

<!-- Falls UI-Änderungen -->

## Verwandte Issues

Fixes #
Relates to #
```

## Best Practices Zusammenfassung

### DO ✅

- Aussagekräftige Titel und Beschreibungen
- Umfassender Test-Plan
- Screenshots bei UI-Änderungen
- Breaking Changes klar dokumentieren
- Self-Review vor Submission
- Kleine, fokussierte PRs
- Links zu Issues/Tickets

### DON'T ❌

- Vage Titel wie "Updates" oder "Fixes"
- PRs ohne Beschreibung
- Riesige PRs (1000+ Zeilen)
- Ungetesteter Code
- "WIP" ohne Draft-Status
- Fehlende Dokumentation
- Merge-Konflikte ignorieren

## Automatisierung

### GitHub Actions

**Automatische Labels**:

```yaml
name: PR Labeler
on: [pull_request]
jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/labeler@v4
```

### PR-Checks

**Pflicht-Checks vor Merge**:

- ✅ CI/CD Pipeline erfolgreich
- ✅ Code-Coverage > 80%
- ✅ Keine Linting-Fehler
- ✅ Mindestens 1 Approval
- ✅ Keine offenen Kommentare
