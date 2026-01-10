# Task Breakdown Strategien

Umfassender Guide zur Aufteilung von PRD-Anforderungen in atomare, umsetzbare Tasks.

## Grundprinzipien

### Was ist ein "guter" Task?

Ein guter Task erfüllt die **ATOMIC**-Kriterien:

- **A**ctionable: Sofort umsetzbar ohne weitere Klärung
- **T**estable: Klare Akzeptanzkriterien
- **O**wnable: Einer Person/einem Agenten zuweisbar
- **M**easurable: Fortschritt messbar (Story Points)
- **I**ndependent: Minimal abhängig von anderen Tasks
- **C**omplete: In sich abgeschlossen

### Task-Größe

**Ideale Größe**: 2-5 Story Points (1-2 Tage Arbeit)

| Story Points | Beschreibung | Beispiel |
|--------------|--------------|----------|
| **1** | Trivial, < 2h | Config-Änderung, Typo-Fix |
| **2** | Einfach, 2-4h | Einfaches CRUD, CSS-Anpassung |
| **3** | Standard, 4-8h | Feature mit wenigen Edge Cases |
| **5** | Komplex, 1-2 Tage | Feature mit mehreren Edge Cases |
| **8** | Sehr komplex, 2-3 Tage | Große Feature, viele Dependencies |
| **13+** | **ZU GROSS!** | In kleinere Tasks aufteilen |

**Faustregel**: Tasks > 8 SP → Aufteilen!

## Breakdown-Strategien

### 1. Aus funktionalen Anforderungen

**PRD-Abschnitt**: Funktionale Anforderungen (MoSCoW-priorisiert)

#### Strategie

Jede Anforderung wird in **1-N Tasks** zerlegt:

**Beispiel-Anforderung**:
> **Must-Have**: User kann Dark Mode in Settings togglen

**Breakdown**:

1. **UI Toggle Component** (3 SP)
   - Toggle-Switch in Settings-Page
   - Visual Feedback beim Toggle
   - Accessibility (ARIA-Labels)

2. **Theme State Management** (5 SP)
   - Zustand speichern (Context/Redux)
   - Theme-Provider implementieren
   - Theme-Wechsel propagieren

3. **CSS Variables Setup** (2 SP)
   - CSS-Variablen für Light/Dark definieren
   - Alle Komponenten auf Variables umstellen
   - Theme-spezifische Styles

4. **Local Storage Persistence** (2 SP)
   - Theme-Präferenz speichern
   - Beim Load wiederherstellen
   - Fallback auf System-Theme

#### Mapping zu Tasks

```typescript
function breakdownFunctionalRequirement(requirement) {
  const tasks = []

  // Pattern 1: UI-Component Task
  if (requirement.hasUI) {
    tasks.push({
      title: `Implement ${requirement.name} UI Component`,
      type: "frontend",
      estimate: estimateUIComplexity(requirement),
      labels: ["feature", "ui"],
      agent: "react-developer"
    })
  }

  // Pattern 2: Backend Logic Task
  if (requirement.hasBackendLogic) {
    tasks.push({
      title: `Implement ${requirement.name} Backend Logic`,
      type: "backend",
      estimate: estimateBackendComplexity(requirement),
      labels: ["feature", "backend"],
      agent: "java-developer" || "python-expert"
    })
  }

  // Pattern 3: State Management Task
  if (requirement.hasStateManagement) {
    tasks.push({
      title: `Implement ${requirement.name} State Management`,
      type: "state",
      estimate: 3,
      labels: ["feature", "state-management"],
      agent: "react-developer"
    })
  }

  // Pattern 4: Persistence Task
  if (requirement.hasPersistence) {
    tasks.push({
      title: `Implement ${requirement.name} Persistence`,
      type: "persistence",
      estimate: 2,
      labels: ["feature", "database"],
      agent: "java-developer"
    })
  }

  return tasks
}
```

### 2. Aus nicht-funktionalen Anforderungen

**PRD-Abschnitt**: Nicht-funktionale Anforderungen (NFRs)

#### Performance-Tasks

**Beispiel-NFR**:
> **Performance**: Seite muss in < 2s laden

**Breakdown**:

1. **Performance Baseline** (2 SP)
   - Aktuelle Ladezeit messen
   - Bottlenecks identifizieren
   - Lighthouse-Report generieren

2. **Code Splitting** (5 SP)
   - Lazy Loading implementieren
   - Route-based Code Splitting
   - Bundle-Größe optimieren

3. **Image Optimization** (3 SP)
   - Responsive Images
   - WebP-Format
   - Lazy Loading

4. **Caching Strategy** (5 SP)
   - Service Worker
   - HTTP-Caching
   - LocalStorage/IndexedDB

#### Security-Tasks

**Beispiel-NFR**:
> **Security**: OWASP Top 10 Compliance

**Breakdown**:

1. **Security Audit** (3 SP)
   - OWASP Top 10 Check
   - Dependency Audit
   - Security-Scan (SAST)

2. **Input Validation** (5 SP)
   - XSS-Prevention
   - SQL-Injection Prevention
   - CSRF-Protection

3. **Authentication Hardening** (8 SP)
   - Password Policy
   - MFA Implementation
   - Session Management

4. **Security Testing** (5 SP)
   - Penetration Testing
   - Security Unit Tests
   - Vulnerability Scanning

#### Accessibility-Tasks

**Beispiel-NFR**:
> **Accessibility**: WCAG 2.1 Level AA

**Breakdown**:

1. **Accessibility Audit** (2 SP)
   - Axe/Lighthouse Scan
   - Keyboard Navigation Test
   - Screen Reader Test

2. **Semantic HTML** (3 SP)
   - ARIA-Labels
   - Heading Hierarchy
   - Landmark Regions

3. **Keyboard Navigation** (3 SP)
   - Tab-Order optimieren
   - Focus States
   - Skip Links

4. **Accessibility Testing** (3 SP)
   - Automated Tests (axe-core)
   - Manual Testing
   - Screen Reader Testing

### 3. Cross-Cutting Concerns

Tasks, die über mehrere Features hinweg relevant sind:

#### Testing

**Breakdown**:

1. **Unit Tests** (3 SP pro Feature)
   - Component Tests
   - Function Tests
   - Edge Cases

2. **Integration Tests** (5 SP pro Feature)
   - API Integration
   - Component Integration
   - E2E Happy Path

3. **E2E Tests** (5 SP)
   - User Flows
   - Critical Paths
   - Cross-Browser

#### Documentation

**Breakdown**:

1. **Code Documentation** (2 SP)
   - JSDoc/JavaDoc
   - README Updates
   - Architecture Docs

2. **User Documentation** (3 SP)
   - User Guide
   - Tutorials
   - FAQ

3. **API Documentation** (3 SP)
   - OpenAPI/Swagger
   - Endpoint Descriptions
   - Example Requests

#### DevOps/Infrastructure

**Breakdown**:

1. **CI/CD Pipeline** (5 SP)
   - Build Pipeline
   - Test Integration
   - Deployment Automation

2. **Monitoring & Observability** (5 SP)
   - Logging Setup
   - Metrics Collection
   - Alerting

3. **Infrastructure as Code** (8 SP)
   - Terraform/CloudFormation
   - Environment Setup
   - Configuration Management

## Dependency-Management

### Dependency-Typen

**Blocking**: Task A muss vor Task B fertig sein
**Related**: Tasks teilen Code/Kontext
**Sequential**: Logische Reihenfolge

### Dependency-Mapping

```typescript
// Beispiel: Dark Mode Feature
const tasks = [
  {
    id: "T1",
    title: "CSS Variables Setup",
    dependencies: [] // Keine Dependencies
  },
  {
    id: "T2",
    title: "Theme State Management",
    dependencies: ["T1"] // Blocked by T1
  },
  {
    id: "T3",
    title: "UI Toggle Component",
    dependencies: ["T2"] // Blocked by T2
  },
  {
    id: "T4",
    title: "Local Storage Persistence",
    dependencies: ["T2"] // Blocked by T2
  },
  {
    id: "T5",
    title: "Unit Tests",
    dependencies: ["T3", "T4"] // Blocked by T3 and T4
  }
]

// Visualisierung:
//     T1
//     ↓
//     T2
//    ↙ ↘
//  T3   T4
//    ↘ ↙
//     T5
```

### Minimierung von Dependencies

**DO ✅**:
- Tasks so unabhängig wie möglich gestalten
- Interfaces/Contracts früh definieren
- Parallele Arbeit ermöglichen

**DON'T ❌**:
- Lange Dependency-Ketten (> 3 Ebenen)
- Zirkuläre Dependencies
- Unnötige Dependencies

## Story Point Estimation

### Estimation-Faktoren

**Komplexität**:
- Anzahl Edge Cases
- Algorithmus-Komplexität
- Neue vs. bekannte Technologie

**Unsicherheit**:
- Klare Anforderungen?
- Bekannte Codebase?
- Bekannte Tools/Frameworks?

**Aufwand**:
- Coding-Aufwand
- Testing-Aufwand
- Review-Aufwand
- Documentation-Aufwand

### Planning Poker

Team-basierte Estimation:

1. **Task vorstellen**: PO erklärt Task
2. **Fragen klären**: Team fragt nach
3. **Privat schätzen**: Jeder wählt Story Points
4. **Gleichzeitig aufdecken**: Alle zeigen Schätzung
5. **Diskutieren**: Bei großen Unterschieden
6. **Konsens finden**: Team einigt sich

### Estimation-Beispiele

#### Beispiel 1: Einfaches CRUD

**Task**: "User kann Profil bearbeiten"

**Analyse**:
- ✅ Bekanntes Pattern (CRUD)
- ✅ Klare Anforderungen
- ✅ Wenige Edge Cases

**Estimation**: **3 SP**

#### Beispiel 2: Komplexe Authentifizierung

**Task**: "MFA mit TOTP implementieren"

**Analyse**:
- ⚠️ Neue Technologie (TOTP)
- ⚠️ Security-kritisch
- ⚠️ Viele Edge Cases (Device Lost, Backup Codes)

**Estimation**: **8 SP**

#### Beispiel 3: Performance-Optimierung

**Task**: "Seite Load-Zeit um 50% reduzieren"

**Analyse**:
- ❌ Unklare Anforderungen (Wo optimieren?)
- ❌ Hohe Unsicherheit
- ❌ Viele potenzielle Bottlenecks

**Estimation**: **13 SP** → **ZU GROSS, AUFTEILEN!**

**Besserer Breakdown**:
1. Performance Baseline (2 SP)
2. Bottleneck-Analyse (3 SP)
3. Spezifische Optimierungen (je 3-5 SP)

## Task-Templates

### Feature-Task Template

```markdown
## Task: [Feature-Name]

### Description
[Kurze Beschreibung der Funktionalität]

### Acceptance Criteria
- [ ] Kriterium 1 (testbar, messbar)
- [ ] Kriterium 2
- [ ] Kriterium 3

### Technical Notes
- Implementation Details
- API Endpoints
- Database Schema

### Edge Cases
- Edge Case 1
- Edge Case 2

### Testing Requirements
- Unit Tests: [Was testen?]
- Integration Tests: [Was testen?]
- E2E Tests: [Welche Flows?]

### Dependencies
- Depends on: [Task-IDs]
- Blocks: [Task-IDs]

### Agent Recommendation
- **Agent**: [agent-name]
- **Rationale**: [Warum dieser Agent?]

### Estimate
**Story Points**: [1, 2, 3, 5, 8]
```

### Bug-Task Template

```markdown
## Task: Fix [Bug-Name]

### Description
[Was ist kaputt?]

### Steps to Reproduce
1. Step 1
2. Step 2
3. Observe error

### Expected Behavior
[Was sollte passieren?]

### Actual Behavior
[Was passiert tatsächlich?]

### Root Cause
[Ursache des Bugs]

### Fix Description
[Wie wird es gefixt?]

### Testing Requirements
- Unit Tests: [Neue Tests?]
- Regression Tests: [Welche Flows erneut testen?]

### Estimate
**Story Points**: [1, 2, 3]
```

### Documentation-Task Template

```markdown
## Task: Document [Feature-Name]

### Description
[Was soll dokumentiert werden?]

### Documentation Scope
- [ ] User Guide
- [ ] API Documentation
- [ ] Architecture Docs
- [ ] Code Comments

### Target Audience
[Entwickler, User, Admin, etc.]

### Deliverables
- File 1: [Path]
- File 2: [Path]

### Estimate
**Story Points**: [2, 3]
```

## Häufige Fehler

### ❌ Zu große Tasks

**Problem**: Tasks > 8 SP

**Beispiel**:
> "User Authentication System implementieren" (21 SP)

**Lösung**: Aufteilen in:
1. User Registration (5 SP)
2. Login/Logout (3 SP)
3. Password Reset (3 SP)
4. Session Management (5 SP)
5. MFA (8 SP)

### ❌ Vage Beschreibungen

**Problem**: Unklare Anforderungen

**Schlecht**:
> "Performance verbessern"

**Gut**:
> "Seite Load-Zeit von 5s auf < 2s reduzieren durch Code Splitting und Image Optimization"

### ❌ Fehlende Akzeptanzkriterien

**Problem**: Nicht testbar

**Schlecht**:
> "Dark Mode implementieren"

**Gut**:
> "Dark Mode implementieren"
> - [ ] Toggle in Settings vorhanden
> - [ ] Theme wechselt bei Toggle
> - [ ] Präferenz wird in LocalStorage gespeichert
> - [ ] Theme wird beim Load wiederhergestellt

### ❌ Ignorieren von Dependencies

**Problem**: Tasks in falscher Reihenfolge

**Beispiel**:
- Task 1: "E2E Tests implementieren"
- Task 2: "Feature implementieren"

**Problem**: E2E Tests können nicht vor Feature implementiert werden!

**Lösung**: Dependencies explizit machen:
- Task 1: "Feature implementieren"
- Task 2: "E2E Tests implementieren" (depends on Task 1)

## Best Practices

### DO ✅

**Atomare Tasks**:
- Eine logische Einheit pro Task
- 2-5 SP ideal
- In sich abgeschlossen

**Klare Beschreibungen**:
- Was soll gebaut werden?
- Warum wird es gebaut?
- Wie wird Erfolg gemessen?

**Testbare Akzeptanzkriterien**:
- Messbar und verifizierbar
- Checkbox-Format
- Keine Interpretation nötig

**Realistische Schätzungen**:
- Planning Poker verwenden
- Historical Data berücksichtigen
- Bei Unsicherheit: Höher schätzen

**Dependencies dokumentieren**:
- Blocking Tasks identifizieren
- Parallele Arbeit ermöglichen
- Visuell darstellen (Graph)

### DON'T ❌

**Zu große Tasks**:
- > 8 SP → Aufteilen
- Mehrere logische Einheiten → Aufteilen

**Vage Anforderungen**:
- Keine klaren Akzeptanzkriterien
- Interpretation nötig
- Scope-Creep möglich

**Ignorieren von Constraints**:
- NFRs vergessen
- Cross-Cutting Concerns auslassen
- Testing als Afterthought

**Unrealistische Schätzungen**:
- Zu optimistisch
- Dependencies ignorieren
- Testing-Aufwand unterschätzen

## Checkliste: Ist mein Task gut?

Vor dem Erstellen eines Tasks in Linear:

- [ ] **Atomic**: Eine logische Einheit?
- [ ] **Actionable**: Sofort umsetzbar?
- [ ] **Testable**: Akzeptanzkriterien definiert?
- [ ] **Ownable**: Einer Person zuweisbar?
- [ ] **Measurable**: Estimate vorhanden (2-8 SP)?
- [ ] **Independent**: Minimal abhängig?
- [ ] **Complete**: In sich abgeschlossen?
- [ ] **Described**: Vollständige Beschreibung?
- [ ] **Agent-Mapped**: Empfohlener Agent angegeben?
- [ ] **Labeled**: Labels für Kategorisierung?

Wenn **alle Punkte** ✅: Task ist bereit!

---

**Siehe auch**:
- [linear-integration.md](linear-integration.md) - Linear-API Details
- [agent-mapping.md](agent-mapping.md) - Agent-Empfehlungen
- [best-practices.md](best-practices.md) - Allgemeine Best Practices
