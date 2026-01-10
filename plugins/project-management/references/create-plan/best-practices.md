# Best Practices für Projektplanung

Umfassender Guide für professionelle Projektplanung mit PRD-basiertem Task-Management in Linear.

## Grundprinzipien

### 1. PRD-zentrierte Planung

**Immer vom PRD ausgehen**:
- ✅ PRD als Single Source of Truth
- ✅ Alle Tasks aus PRD ableitbar
- ✅ Vollständige PRD-Analyse vor Task-Erstellung
- ✅ PRD-Link in EPIC-Description

**DON'T**:
- ❌ Tasks ohne PRD-Referenz
- ❌ Ad-hoc Tasks ohne Kontext
- ❌ Feature-Creep ignorieren

### 2. Konsistenz über alles

**Konsistenz-Checks vor Speichern**:
- [ ] Keine Duplikate
- [ ] Keine Redundanzen
- [ ] Kein widersprüchliches Gesamtbild
- [ ] Logische Priorisierung
- [ ] Korrekte Dependencies

**DON'T**:
- ❌ Linear ohne Duplikat-Check befüllen
- ❌ Inkonsistente Prioritäten
- ❌ Widersprüchliche Anforderungen

### 3. Actionable über alles

**Jeder Task muss umsetzbar sein**:
- ✅ Klare Beschreibung
- ✅ Eindeutige Akzeptanzkriterien
- ✅ Keine offenen Fragen
- ✅ Alle Informationen vorhanden

**DON'T**:
- ❌ Vage Tasks ("Performance verbessern")
- ❌ Tasks mit Interpretation-Bedarf
- ❌ Fehlende Akzeptanzkriterien

## Workflow Best Practices

### PRD-Analyse

**1. Vollständig lesen**:
```markdown
- [ ] Executive Summary verstanden
- [ ] Problemstellung klar
- [ ] Ziele & Metriken definiert
- [ ] User Stories gelesen
- [ ] Funktionale Anforderungen (Must/Should/Could)
- [ ] Nicht-funktionale Anforderungen
- [ ] Out of Scope verstanden
- [ ] Risiken identifiziert
- [ ] Timeline realistisch
```

**2. Anforderungen gruppieren**:
```typescript
const requirements = {
  mustHave: extractRequirements(prd, "must"),
  shouldHave: extractRequirements(prd, "should"),
  couldHave: extractRequirements(prd, "could"),
  wontHave: extractRequirements(prd, "won't")
}
```

**3. NFRs extrahieren**:
```typescript
const nfrs = {
  performance: extractNFRs(prd, "performance"),
  security: extractNFRs(prd, "security"),
  scalability: extractNFRs(prd, "scalability"),
  usability: extractNFRs(prd, "usability"),
  accessibility: extractNFRs(prd, "accessibility")
}
```

### EPIC-Erstellung

**Best Practices**:

**✅ DO**:
```yaml
EPIC:
  Title: "[Feature-Name]" (< 50 chars, beschreibend)
  Description: |
    ## Executive Summary
    [3-5 Sätze aus PRD]

    ## Business Value
    - Warum wird das gebaut?
    - Welchen Impact hat es?
    - Für wen ist es wichtig?

    ## Success Metrics
    - Metrik 1: [Baseline → Target]
    - Metrik 2: [Baseline → Target]

    ## Timeline
    - Phase 1: [Meilenstein]
    - Phase 2: [Meilenstein]

    ## Full PRD
    Link: [PRD-Pfad oder URL]

  Status: planned
  Priority: high (basierend auf Must-Have %)
  Labels: [epic, feature, tech-stack]
```

**❌ DON'T**:
```yaml
EPIC:
  Title: "Feature" # Zu vage
  Description: "Build feature X" # Zu kurz
  Status: in_progress # Noch nicht gestartet!
  Priority: urgent # Alles ist urgent → nichts ist urgent
```

### Task-Erstellung

**Best Practices**:

**✅ DO**:
```markdown
Task: "[Prägnanter Titel]" (< 60 chars)

## Description
[Vollständige Beschreibung: Was, Warum, Wie]

## Acceptance Criteria
- [ ] Kriterium 1 (testbar, messbar)
- [ ] Kriterium 2 (testbar, messbar)
- [ ] Kriterium 3 (testbar, messbar)

## Technical Notes
- Implementation-Details
- API-Endpoints
- Database-Schema
- Third-Party-Dependencies

## Edge Cases
- Edge Case 1: [Wie behandeln?]
- Edge Case 2: [Wie behandeln?]

## Testing Requirements
- **Unit Tests**: [Was testen?]
- **Integration Tests**: [Was testen?]
- **E2E Tests**: [Welche Flows?]

## Dependencies
- **Depends on**: LIN-123, LIN-124
- **Blocks**: LIN-125

## Agent Recommendation
- **Agent**: `java-developer`
- **Rationale**: Spring Boot expertise erforderlich

## Definition of Done
- [ ] Code implementiert
- [ ] Tests geschrieben (Coverage > 80%)
- [ ] Code-Review durchgeführt
- [ ] Dokumentiert
- [ ] In Staging deployed
```

**❌ DON'T**:
```markdown
Task: "Do stuff" # Zu vage

## Description
Build feature X # Keine Details

# Keine Acceptance Criteria ❌
# Keine Dependencies ❌
# Keine Agent-Empfehlung ❌
```

### Duplikat-Vermeidung

**Strategie**:

**1. Vor EPIC-Erstellung**:
```typescript
// Suche nach ähnlichen EPICs
const existingEPICs = await linear.listProjects({
  teamId: TEAM_ID,
  status: "planned,in_progress"
})

const similarEPICs = existingEPICs.filter(epic => {
  return similarity(epic.name, newEPICName) > 0.7
})

if (similarEPICs.length > 0) {
  // Interaktive Bestätigung
  console.log("⚠️  Ähnliche EPICs gefunden:")
  similarEPICs.forEach(epic => {
    console.log(`  - ${epic.identifier}: ${epic.name}`)
  })

  const userChoice = await askUser(
    "Möchten Sie trotzdem fortfahren?",
    ["Ja", "Nein, abbrechen", "Existierendes EPIC erweitern"]
  )
}
```

**2. Vor Issue-Erstellung**:
```typescript
// Suche nach ähnlichen Issues im EPIC
const existingIssues = await linear.listIssues({
  projectId: EPIC_ID
})

const duplicates = existingIssues.filter(issue => {
  // Exakte Titel-Übereinstimmung
  if (issue.title === newIssueTitle) return true

  // Hohe Ähnlichkeit
  if (similarity(issue.title, newIssueTitle) > 0.85) return true

  return false
})

if (duplicates.length > 0) {
  console.log(`⚠️  Duplikat gefunden: ${duplicates[0].identifier}`)
  console.log("→ Überspringe Issue-Erstellung")
}
```

**3. Similarity-Check**:
```typescript
function similarity(str1: string, str2: string): number {
  // Levenshtein Distance oder andere Similarity-Metric
  const distance = levenshtein(str1.toLowerCase(), str2.toLowerCase())
  const maxLength = Math.max(str1.length, str2.length)
  return 1 - (distance / maxLength)
}
```

### Priorisierung

**MoSCoW-Mapping zu Linear-Priorities**:

| MoSCoW | Linear Priority | Rationale |
|--------|----------------|-----------|
| **Must-Have** | `urgent` oder `high` | Kritisch für MVP |
| **Should-Have** | `medium` | Wichtig, nicht kritisch |
| **Could-Have** | `low` | Nice-to-Have |
| **Won't-Have** | ❌ Keine Issues | Out of Scope |

**Priorisierungs-Algorithmus**:
```typescript
function mapPriority(moscowPriority: string, businessValue: number): string {
  if (moscowPriority === "must") {
    return businessValue > 8 ? "urgent" : "high"
  }

  if (moscowPriority === "should") {
    return businessValue > 6 ? "high" : "medium"
  }

  if (moscowPriority === "could") {
    return "low"
  }

  // won't-have: Keine Issue erstellen
  return null
}
```

**DON'T**:
- ❌ Alles als "urgent" markieren
- ❌ Prioritäten ignorieren
- ❌ Won't-Have als Issues erstellen

### Estimation Best Practices

**T-Shirt Sizing → Story Points**:

| T-Shirt | Story Points | Dauer | Beispiel |
|---------|--------------|-------|----------|
| **XS** | 1 | < 2h | Config-Änderung |
| **S** | 2 | 2-4h | Einfaches CRUD |
| **M** | 3-5 | 4-8h | Standard Feature |
| **L** | 8 | 1-2 Tage | Komplexes Feature |
| **XL** | 13+ | 2+ Tage | **ZU GROSS!** |

**Estimation-Faktoren**:
```typescript
function estimateTask(task: Task): number {
  let estimate = 2 // Baseline

  // Komplexität
  if (task.hasMultipleEdgeCases) estimate += 1
  if (task.isNewTechnology) estimate += 2
  if (task.hasComplexAlgorithm) estimate += 2

  // Unsicherheit
  if (task.requirementsUnclear) estimate += 1
  if (task.isUnknownCodebase) estimate += 1

  // Dependencies
  if (task.dependencies.length > 2) estimate += 1

  // Testing
  if (task.requiresE2ETests) estimate += 1

  // Cap at 8 (anything > 8 should be split)
  return Math.min(estimate, 8)
}
```

**DON'T**:
- ❌ Zu optimistische Schätzungen
- ❌ Testing-Aufwand vergessen
- ❌ Tasks > 8 SP nicht aufteilen

### Dependency-Management

**Dependency-Typen**:

**Blocking**:
```yaml
Task A: "Implement Backend API"
Task B: "Implement Frontend UI"

Relation:
  Task B depends on Task A (blocked_by)
  Task A blocks Task B (blocks)
```

**Related**:
```yaml
Task A: "Implement User Login"
Task B: "Implement User Registration"

Relation:
  Task A related to Task B (related_to)
```

**Best Practices**:

**✅ DO**:
- Dependencies explizit dokumentieren
- Visualisieren (Graph)
- Parallele Arbeit ermöglichen
- Kritischen Pfad identifizieren

**❌ DON'T**:
- Lange Dependency-Ketten (> 3 Ebenen)
- Zirkuläre Dependencies
- Dependencies nach Task-Erstellung hinzufügen

### Agent-Empfehlungen

**Immer angeben**:
```markdown
## Agent Recommendation

**Recommended Agent**: `java-developer`

**Rationale**:
Spring Boot REST Controller mit Service-Layer-Logic.
Enterprise Java Patterns erforderlich.

**Alternative Agents**:
- `python-expert` (falls Python-Rewrite gewünscht)

**Multi-Agent Workflow** (falls komplex):
1. `java-developer` - Implementation (5 SP)
2. `code-reviewer` - Quality Review (2 SP)
3. `test-automator` - E2E Tests (3 SP)
```

**DON'T**:
- ❌ Agent-Empfehlung auslassen
- ❌ Falschen Agent zuweisen
- ❌ Keine Rationale

## Qualitätskriterien

### EPIC-Qualität

**Checkliste**:
- [ ] **Titel**: Klar und prägnant (< 50 chars)
- [ ] **Executive Summary**: 3-5 Sätze
- [ ] **Business Value**: Warum & Impact
- [ ] **Success Metrics**: Messbare Ziele
- [ ] **Timeline**: Grobe Meilensteine
- [ ] **PRD-Link**: Vollständiges PRD verlinkt
- [ ] **Status**: `planned` (initial)
- [ ] **Priority**: Basierend auf MoSCoW
- [ ] **Labels**: epic, feature, tech-stack

### Task-Qualität

**Checkliste**:
- [ ] **Atomic**: Eine logische Einheit
- [ ] **Actionable**: Sofort umsetzbar
- [ ] **Testable**: Akzeptanzkriterien definiert
- [ ] **Ownable**: Einer Person zuweisbar
- [ ] **Measurable**: Estimate 2-8 SP
- [ ] **Independent**: Minimal Dependencies
- [ ] **Complete**: Alle Informationen vorhanden
- [ ] **Described**: Vollständige Description
- [ ] **Agent-Mapped**: Empfohlener Agent
- [ ] **Labeled**: Technology + Type Labels
- [ ] **DoD**: Definition of Done definiert

### Plan-Qualität

**Gesamtbild prüfen**:
- [ ] **Vollständigkeit**: Alle PRD-Anforderungen abgedeckt?
- [ ] **Konsistenz**: Keine Widersprüche?
- [ ] **Realismus**: Timeline realistisch?
- [ ] **Testbarkeit**: Alle Tasks testbar?
- [ ] **Priorisierung**: MoSCoW korrekt gemappt?
- [ ] **Dependencies**: Alle identifiziert?
- [ ] **Ressourcen**: Genug Entwickler/Zeit?

## Häufige Fehler

### ❌ PRD nicht vollständig gelesen

**Problem**: Tasks fehlen oder sind inkonsistent

**Symptom**:
```yaml
PRD: "Must-Have: Dark Mode mit Accessibility-Features"

Tasks:
  - "Implement Dark Mode Toggle" ✅
  # Accessibility fehlt! ❌
```

**Lösung**: Vollständige PRD-Analyse vor Task-Breakdown

### ❌ Zu große Tasks

**Problem**: Tasks > 8 SP

**Symptom**:
```yaml
Task: "Implement complete User Authentication System" (21 SP) ❌
```

**Lösung**: Aufteilen in atomare Tasks:
```yaml
Tasks:
  - "User Registration" (5 SP) ✅
  - "Login/Logout" (3 SP) ✅
  - "Password Reset" (3 SP) ✅
  - "Session Management" (5 SP) ✅
  - "MFA" (8 SP) ✅
```

### ❌ Vage Akzeptanzkriterien

**Problem**: Nicht testbar

**Schlecht**:
```markdown
## Acceptance Criteria
- Feature works ❌
- No bugs ❌
```

**Gut**:
```markdown
## Acceptance Criteria
- [ ] User can toggle Dark Mode in Settings ✅
- [ ] Theme persists in LocalStorage ✅
- [ ] Theme applies to all components ✅
- [ ] Keyboard accessible (Tab navigation) ✅
- [ ] Screen reader announces theme change ✅
```

### ❌ Dependencies ignoriert

**Problem**: Tasks in falscher Reihenfolge

**Beispiel**:
```yaml
Tasks:
  - "E2E Tests" (created first) ❌
  - "Feature Implementation" (created second) ❌

# E2E Tests können nicht vor Feature laufen!
```

**Lösung**:
```yaml
Tasks:
  - "Feature Implementation" (LIN-123) ✅
  - "E2E Tests" (LIN-124, depends on LIN-123) ✅
```

### ❌ Duplikate nicht geprüft

**Problem**: Redundante Issues

**Beispiel**:
```yaml
Existing:
  - LIN-123: "Implement Dark Mode"

New (Duplicate):
  - LIN-456: "Add Dark Mode Feature" ❌
```

**Lösung**: Duplikat-Check vor Erstellung

### ❌ Inkonsistente Priorisierung

**Problem**: Widersprüchliche Prioritäten

**Beispiel**:
```yaml
EPIC Priority: low
Tasks:
  - Task 1: Priority urgent ❌
  - Task 2: Priority urgent ❌

# Wenn EPIC low ist, können Tasks nicht urgent sein!
```

**Lösung**: Konsistente Prioritäten (EPIC → Tasks)

## Kommunikation & Kollaboration

### Mit Stakeholdern

**EPIC als Kommunikations-Tool**:
- Executive Summary für Management
- Success Metrics für Product Owner
- Timeline für Stakeholder
- PRD-Link für Details

**DON'T**:
- ❌ Technische Details in EPIC
- ❌ Zu viele Details (gehören in Issues)

### Mit Entwicklern

**Issues als Arbeits-Einheiten**:
- Klare Beschreibung (keine Interpretation nötig)
- Alle Informationen vorhanden
- Akzeptanzkriterien testbar
- Agent-Empfehlung hilfreich

**DON'T**:
- ❌ Vage Beschreibungen
- ❌ Fehlende Informationen
- ❌ Interpretation erforderlich

### Mit QA/Testing

**Testing-Requirements**:
- Unit Tests: Was testen?
- Integration Tests: Welche Szenarien?
- E2E Tests: Welche Flows?
- Acceptance Criteria als Test-Cases

**DON'T**:
- ❌ Testing als Afterthought
- ❌ Vage Test-Requirements
- ❌ Akzeptanzkriterien nicht testbar

## Maintenance & Updates

### Plan aktualisieren

**Während Implementation**:
- Neue Tasks hinzufügen (falls nötig)
- Estimates adjustieren (basierend auf Actual)
- Dependencies aktualisieren
- Status aktuell halten

**DON'T**:
- ❌ Plan als statisch betrachten
- ❌ Änderungen nicht dokumentieren
- ❌ Scope-Creep ignorieren

### Post-Mortem

**Nach Abschluss**:
- Actual vs. Estimated vergleichen
- Bottlenecks identifizieren
- Lessons Learned dokumentieren
- Prozess verbessern

**Template**:
```markdown
## Post-Mortem: [EPIC-Name]

### Summary
- Geschätzter Aufwand: [X SP]
- Tatsächlicher Aufwand: [Y SP]
- Delta: [Y-X SP] (±Z%)

### What went well
- [Punkt 1]
- [Punkt 2]

### What could be improved
- [Punkt 1]
- [Punkt 2]

### Lessons Learned
- [Lesson 1]
- [Lesson 2]

### Action Items
- [ ] Action 1
- [ ] Action 2
```

## Checklisten

### Vor Plan-Erstellung

- [ ] PRD vollständig gelesen
- [ ] Anforderungen verstanden
- [ ] Scope klar definiert
- [ ] Timeline realistisch
- [ ] Ressourcen verfügbar

### Während Plan-Erstellung

- [ ] EPIC erstellt mit vollständiger Description
- [ ] Duplikat-Check durchgeführt
- [ ] Alle Must-Have Tasks erstellt
- [ ] Should/Could-Have Tasks priorisiert
- [ ] Dependencies identifiziert
- [ ] Agent-Empfehlungen hinzugefügt
- [ ] Labels konsistent
- [ ] Estimates realistisch

### Nach Plan-Erstellung

- [ ] Konsistenz-Check durchgeführt
- [ ] Keine Duplikate
- [ ] Vollständigkeit geprüft
- [ ] Dependencies verknüpft
- [ ] Plan mit Team geteilt
- [ ] Fragen geklärt

---

**Siehe auch**:
- [linear-integration.md](linear-integration.md) - Linear-API Details
- [task-breakdown.md](task-breakdown.md) - Task-Breakdown Strategien
- [agent-mapping.md](agent-mapping.md) - Agent-Empfehlungen
