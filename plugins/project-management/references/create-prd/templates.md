# PRD Templates und Beispiele

Verschiedene PRD-Templates für unterschiedliche Projekttypen und Komplexitätsstufen.

## Template 1: Minimal Viable PRD (MVP)

Für kleine Features oder schnelle Iterationen.

```markdown
# PRD: [Feature Name]

**Status**: Draft | Review | Approved
**Autor**: [Name]
**Datum**: [YYYY-MM-DD]
**Version**: 1.0

## tl;dr (Executive Summary)

[2-3 Sätze: Was, Für wen, Warum, Erwarteter Impact]

## Problem

[Welches Problem lösen wir? Mit Evidenz.]

## Ziel

[1 primäres, messbares Ziel]
- **Metrik**: [Was messen wir?]
- **Target**: [Spezifischer Zielwert]
- **Timeline**: [Bis wann?]

## User Story

Als [Persona]
Möchte ich [Aktion]
Damit [Benefit]

**Akzeptanzkriterien**:
- [ ] Kriterium 1
- [ ] Kriterium 2
- [ ] Kriterium 3

## Out of Scope

- ❌ [Was nicht gebaut wird]
- ❌ [Was in späterer Version kommt]

## Success Metrics

- **Primär**: [Metrik + Target]
- **Sekundär**: [Metrik + Target]

## Risiken

- [Risiko 1 + Mitigation]
- [Risiko 2 + Mitigation]

## Timeline

- Design: [Datum]
- Development: [Datum]
- Launch: [Datum]

## Approvals

- [ ] Product Owner
- [ ] Engineering Lead
- [ ] Design Lead
```

**Wann verwenden**:

- Kleine Features (< 2 Wochen Entwicklung)
- Klarer Scope
- Wenig Abhängigkeiten
- Experimentelle Features

## Template 2: Standard Feature PRD

Für typische neue Features.

```markdown
# Product Requirements Document: [Feature Name]

---

## Dokument-Informationen

|----------------|---------------------------|
| **Status**     | Draft / Review / Approved |
| **Autor**      | [Name, Team]              |
| **Stakeholder**| [Liste]                   |
| **Erstellt**   | [Datum]                   |
| **Zuletzt aktualisiert** | [Datum]         |
| **Version**      | 1.0                     |
| **Ziel-Release** | Q[X] YYYY               |

---

## Executive Summary

[3-5 Sätze zusammenfassend:]
- Was wird gebaut?
- Für wen?
- Warum wichtig?
- Erwarteter Business-Impact?
- Timeline?

---

## Inhaltsverzeichnis

1. [Problemstellung](#problemstellung)
2. [Ziele & Erfolgsmetriken](#ziele--erfolgsmetriken)
3. [User Stories & Personas](#user-stories--personas)
4. [Funktionale Anforderungen](#funktionale-anforderungen)
5. [Nicht-funktionale Anforderungen](#nicht-funktionale-anforderungen)
6. [Abgrenzung (Out of Scope)](#abgrenzung-out-of-scope)
7. [User Experience](#user-experience)
8. [Technische Überlegungen](#technische-überlegungen)
9. [Risikobewertung](#risikobewertung)
10. [Abhängigkeiten](#abhängigkeiten)
11. [Timeline & Meilensteine](#timeline--meilensteine)
12. [Anhang](#anhang)

---

## 1. Problemstellung

### Aktueller Zustand

[Beschreibe die aktuelle Situation]

### Problembeschreibung

[Was ist das spezifische Problem? Wen betrifft es?]

### Auswirkungen

**Nutzer-Impact**:
- [Auswirkung 1 mit Daten]
- [Auswirkung 2 mit Daten]

**Business-Impact**:
- [Metrik 1: z.B. Churn-Rate]
- [Metrik 2: z.B. Support-Tickets]
- [Metrik 3: z.B. Revenue-Impact]

### Evidenz & Research

**Quantitativ**:
- Analytics: [Daten]
- Metrics: [Zahlen]

**Qualitativ**:
- User Interviews: [n=X, Key Findings]
- Support Feedback: [Patterns]
- Surveys: [n=X, Results]

**Marktanalyse**:
- Competitor Features: [Vergleich]
- Industry Trends: [Relevante Trends]

### Warum jetzt?

[Timingness, Opportunity, Strategic Importance]

---

## 2. Ziele & Erfolgsmetriken

### Produkt-Ziele

1. **[Ziel-Name]**
   - Beschreibung: [Details]
   - Rationale: [Warum wichtig?]
   - Messung: [Wie messen?]

2. **[Ziel-Name]**
   - ...

### Business-Ziele

- [Business-Ziel 1 mit Kontext]
- [Business-Ziel 2 mit Kontext]

### Erfolgsmetriken

#### Primäre Metriken (Launch + 4 Wochen)

| Metrik | Baseline | Target | Messmethode | Owner |
|--------|----------|--------|-------------|-------|
| [Metrik 1] | [Wert] | [Ziel] | [Tool/Method] | [Name] |
| [Metrik 2] | [Wert] | [Ziel] | [Tool/Method] | [Name] |

#### Sekundäre Metriken (Launch + 8 Wochen)

| Metrik | Baseline | Target | Messmethode | Owner |
|--------|----------|--------|-------------|-------|
| [Metrik 3] | [Wert] | [Ziel] | [Tool/Method] | [Name] |
| [Metrik 4] | [Wert] | [Ziel] | [Tool/Method] | [Name] |

#### Guardrail Metriken

[Metriken die nicht negativ beeinflusst werden dürfen]

---

## 3. User Stories & Personas

### Primäre Personas

#### Persona 1: [Name]

**Demographie**:
- Rolle: [z.B. Freelancer]
- Alter: [Range]
- Tech-Savviness: [Level]

**Kontext**:
- [Relevanter Background]
- [Nutzungskontext]
- [Pain Points]

**Ziele**:
- [Ziel 1]
- [Ziel 2]

**Quote**: "[Typisches Nutzer-Zitat]"

### User Stories

#### Epic 1: [Epic Name]

**US-1.1: [Story Title]** (Priority: Must-Have)

**Als** [Persona]
**Möchte ich** [Aktion/Feature]
**Damit** [Benefit/Outcome]

**Akzeptanzkriterien**:
- [ ] [Spezifisches, testbares Kriterium 1]
- [ ] [Spezifisches, testbares Kriterium 2]
- [ ] [Spezifisches, testbares Kriterium 3]

**Kontext**:
- [Zusätzliche Informationen]
- [User Research Findings]
- [Mockup Links]

**Abhängigkeiten**:
- [Technische/Feature Abhängigkeiten]

**US-1.2: [Story Title]** (Priority: Should-Have)

[...]

---

## 4. Funktionale Anforderungen

### Must-Have (MVP)

#### FR-1: [Requirement Name]

**Beschreibung**: [Detaillierte Beschreibung]

**Details**:
- [Spezifikation 1]
- [Spezifikation 2]
- [Spezifikation 3]

**User Flow**:
1. Nutzer [Aktion]
2. System [Reaktion]
3. Nutzer [Nächste Aktion]

**Akzeptanzkriterien**:
- [ ] [Kriterium 1]
- [ ] [Kriterium 2]

**Edge Cases**:
- [Edge Case 1 + Handling]
- [Edge Case 2 + Handling]

**Abhängigkeiten**:
- [API, Service, Feature]

**Mockups**: [Link]

#### FR-2: [Requirement Name]

[...]

### Should-Have (Post-MVP)

#### FR-X: [Requirement Name]

**Rationale für Should-Have**: [Warum nicht MVP?]

[...]

### Nice-to-Have (Future Consideration)

#### FR-Y: [Requirement Name]

**Rationale**: [Warum später/vielleicht?]

[...]

---

## 5. Nicht-funktionale Anforderungen

### Performance

- **NFR-1**: [Requirement mit spezifischem Target]
  - Messung: [Wie testen?]
  - Rationale: [Warum wichtig?]

### Security & Privacy

- **NFR-X**: [Security Requirement]
  - Compliance: [GDPR, HIPAA, etc.]
  - Implementation: [High-level Ansatz]

### Scalability

- **NFR-X**: [Scalability Requirement]
  - Expected Load: [Zahlen]
  - Target: [Performance bei Load]

### Usability

- **NFR-X**: [Usability Requirement]
  - Validation: [Usability Testing Plan]

### Accessibility

- **NFR-X**: WCAG 2.1 Level AA Compliance
  - Testing: [Tools & Methoden]

### Reliability

- **NFR-X**: [Uptime, Error Rate Requirements]
  - Monitoring: [Wie überwachen?]

---

## 6. Abgrenzung (Out of Scope)

### Nicht in diesem Release

| Feature | Rationale | Geplant für |
|---------|-----------|-------------|
| [Feature 1] | [Grund] | [Q/Version] |
| [Feature 2] | [Grund] | [Q/Version] |

### Explizit ausgeschlossen

- ❌ **[Feature]**: [Detaillierte Begründung]
- ❌ **[Feature]**: [Detaillierte Begründung]

---

## 7. User Experience

### User Flows

[Visuelle User Flow Diagramme oder Links]

### Wireframes/Mockups

- [Mockup 1: Screen Name] - [Link]
- [Mockup 2: Screen Name] - [Link]

### Interaction Patterns

[Beschreibung wichtiger Interaktionen]

### Mobile Considerations

[Spezifische mobile UX Anforderungen]

---

## 8. Technische Überlegungen

**Hinweis**: Fokus auf WAS, nicht WIE. Technische Entscheidungen
sind Aufgabe des Entwicklungsteams.

### Systeme betroffen

- [System 1]: [Art der Änderung]
- [System 2]: [Art der Änderung]

### APIs benötigt

- [API 1]: [Zweck]
- [API 2]: [Zweck]

### Datenmodell

[Neue Entities, wichtige Änderungen - High Level]

### Drittanbieter-Integrationen

- [Service 1]: [Zweck, Lizenz-Überlegungen]

### Performance-Überlegungen

[Kritische Performance-Aspekte]

### Sicherheits-Überlegungen

[Wichtige Security-Aspekte]

---

## 9. Risikobewertung

| ID | Risiko | Impact | Likelihood | Mitigation | Owner |
|----|--------|--------|------------|------------|-------|
| R-1 | [Risiko] | H/M/L | H/M/L | [Strategie] | [Name] |
| R-2 | [Risiko] | H/M/L | H/M/L | [Strategie] | [Name] |

### Details zu High-Priority Risiken

#### R-1: [Risiko-Name]

**Beschreibung**: [Detaillierte Beschreibung]

**Impact**: [Auswirkungen wenn es eintritt]

**Likelihood**: [Wahrscheinlichkeit]

**Mitigation-Strategie**:
1. [Präventive Maßnahme 1]
2. [Präventive Maßnahme 2]

**Contingency Plan**:
[Was tun wenn es eintritt?]

---

## 10. Abhängigkeiten

### Interne Abhängigkeiten

| Abhängigkeit | Team | Status | Impact if Delayed |
|--------------|------|--------|-------------------|
| [Feature/API] | [Team] | [Status] | [Impact] |

### Externe Abhängigkeiten

| Abhängigkeit | Vendor | Timeline | Risk |
|--------------|--------|----------|------|
| [Service/API] | [Vendor] | [ETA] | [Risk Level] |

### Blocking Issues

[Kritische Blocker die resolved werden müssen]

---

## 11. Timeline & Meilensteine

### Phasen

```text
Discovery ────▶ Design ────▶ Development ────▶ Testing ────▶ Launch
Week 1-2       Week 3-4      Week 5-8           Week 9       Week 10
```

### Detaillierter Zeitplan

| Phase | Aktivitäten | Deliverables | Datum | Owner |
|-------|-------------|--------------|-------|-------|
| **Discovery** | Research, PRD | Finalized PRD | [Datum] | PM |
| **Design** | Mockups, Specs | Design Specs | [Datum] | Design |
| **Development** | Sprint 1 | Backend APIs | [Datum] | Eng |
| **Development** | Sprint 2 | Frontend UI | [Datum] | Eng |
| **Testing** | QA, UAT | Test Reports | [Datum] | QA |
| **Launch** | Deploy, Monitor | Launch Metrics | [Datum] | PM |

### Meilensteine

- **M1**: PRD Approval - [Datum]
- **M2**: Design Approval - [Datum]
- **M3**: Development Complete - [Datum]
- **M4**: QA Sign-off - [Datum]
- **M5**: Production Launch - [Datum]
- **M6**: Success Metrics Review - [Datum]

---

## 12. Anhang

### Änderungshistorie

| Version | Datum | Autor | Änderungen |
|---------|-------|-------|-----------|
| 0.1 | [Datum] | [Name] | Initial Draft |
| 1.0 | [Datum] | [Name] | First Complete Version |

### Referenzen

- [User Research Report: Link]
- [Competitive Analysis: Link]
- [Technical Spike: Link]
- [Design Exploration: Link]

### Approvals

| Rolle | Name | Datum | Unterschrift/Approval |
|-------|------|-------|-----------------------|
| Product Owner | [Name] | [Datum] | ✅ |
| Engineering Lead | [Name] | [Datum] | ✅ |
| Design Lead | [Name] | [Datum] | ✅ |
| Legal/Compliance | [Name] | [Datum] | ✅ |

### Glossar

- **[Term]**: [Definition]
- **[Term]**: [Definition]

**Wann verwenden**:

- Standard neue Features
- Mittlere Komplexität
- Multiple Stakeholder
- 4-8 Wochen Entwicklung

## Template 3: Major Initiative PRD

Für große, strategische Projekte.

[Beinhaltet alle Elemente von Template 2, plus:]

```markdown
## Strategischer Kontext

### Vision

[Langfristige Vision]

### Strategic Alignment

**Company OKRs**:
- [OKR 1]: Wie trägt Feature bei?
- [OKR 2]: Wie trägt Feature bei?

**Product Strategy**:
[Wie passt es in größere Produkt-Roadmap?]

### Market Opportunity

**Market Size**:
- TAM: [Total Addressable Market]
- SAM: [Serviceable Addressable Market]
- SOM: [Serviceable Obtainable Market]

**Competitive Advantage**:
[Wie differenziert uns das?]

### Business Case

**Investment**:
- Engineering: [Person-Weeks]
- Design: [Person-Weeks]
- Estimated Cost: [EUR/USD]

**Expected Return**:
- Revenue Impact: [Projection]
- Cost Savings: [Projection]
- User Growth: [Projection]

**ROI Calculation**:
[Formula + Expected ROI]

## Go-to-Market Strategy

### Launch Plan

**Pre-Launch** (T-4 weeks):
- [Aktivität 1]
- [Aktivität 2]

**Launch** (T-0):
- [Aktivität 1]
- [Aktivität 2]

**Post-Launch** (T+2 weeks):
- [Aktivität 1]
- [Aktivität 2]

### Marketing & Communication

**Internal**:
- [Team Communication Plan]

**External**:
- [User Communication Plan]
- [Press/PR if applicable]

### Training & Documentation

- User Documentation: [Plan]
- Support Training: [Plan]
- Sales Enablement: [If B2B]

## Rollout Strategy

### Phased Rollout

| Phase | Audience | % Users | Duration | Criteria for Next Phase |
|-------|----------|---------|----------|-------------------------|
| Alpha | Internal | 100 employees | 1 week | No critical bugs |
| Beta | Early Adopters | 1% | 2 weeks | Metrics meet targets |
| GA | All Users | 100% | - | - |

### Feature Flags

[Which features behind flags, rollout plan]

### Rollback Plan

**Triggers for Rollback**:
- [Trigger 1: e.g., > 5% error rate]
- [Trigger 2: e.g., negative NPS]

**Rollback Procedure**:
1. [Step 1]
2. [Step 2]

## Long-term Roadmap

### V1 (This PRD)

[Summary]

### V2 (Q[X])

[Planned enhancements]

### V3+ (Future)

[Long-term vision]

## Monitoring & Iteration Plan

### Week 1 Post-Launch

- Daily metrics review
- Support ticket monitoring
- Bug triage

### Week 2-4 Post-Launch

- Weekly metrics review
- User feedback synthesis
- Iteration planning

### Post-Mortem

**Scheduled**: [Datum, 4 weeks post-launch]

**Participants**: [List]

**Format**: [Structured review of goals vs. actuals]
```

**Wann verwenden**:

- Strategische Initiativen
- Große Investments (>2 Monate Entwicklung)
- High business impact
- Executive visibility

## Template 4: Technical PRD

Für Platform/Infrastructure-Projekte.

```markdown
# Technical PRD: [Project Name]

[Standard PRD sections, plus:]

## Problem (Technical)

### Current State

**Architecture**:
[Aktuelle technische Architektur]

**Pain Points**:
- [Performance issue]
- [Scalability issue]
- [Maintenance issue]

**Technical Debt**:
[Relevantes Tech Debt]

### Proposed Solution (High-Level)

[Architektur-Überblick, nicht zu detailliert]

## Technical Requirements

### TR-1: [Requirement]

**Current**: [Aktueller Zustand]
**Target**: [Ziel-Zustand]
**Rationale**: [Warum wichtig?]

**Acceptance Criteria**:
- [ ] [Testbares Kriterium]

### Performance Requirements

| Metrik | Current | Target | Measurement |
|--------|---------|--------|-------------|
| Latency | [ms] | [ms] | [Method] |
| Throughput | [req/s] | [req/s] | [Method] |
| Uptime | [%] | [%] | [Method] |

### Compatibility Requirements

- Backward Compatibility: [Yes/No, Details]
- API Versioning: [Strategy]
- Migration Path: [Plan]

## Impact Assessment

### Systems Affected

| System | Impact | Downtime Required | Migration |
|--------|--------|-------------------|-----------|
| [System] | [High/Med/Low] | [Duration] | [Yes/No] |

### Data Migration

**Scope**: [What data needs migration]
**Volume**: [Size]
**Strategy**: [Online/Offline, Phased]
**Rollback**: [Plan]

## Testing Strategy

### Unit Tests

- Coverage Target: [%]
- New Tests: [Estimated count]

### Integration Tests

[Scope of integration testing]

### Performance Tests

- Load Tests: [Scenarios]
- Stress Tests: [Scenarios]
- Benchmarks: [What to benchmark]

### Chaos Engineering

[If applicable, chaos testing plans]
```

**Wann verwenden**:

- Infrastructure-Projekte
- Platform-Features
- Architecture-Änderungen
- Developer-facing Features

## Schnell-Referenz: Template-Wahl

| Projekt-Typ | Dauer | Komplexität | Template |
|-------------|-------|-------------|----------|
| Quick Enhancement | < 2 Wochen | Niedrig | Minimal MVP |
| Standard Feature | 4-8 Wochen | Mittel | Standard Feature |
| Major Initiative | > 2 Monate | Hoch | Major Initiative |
| Platform/Infra | Variabel | Mittel-Hoch | Technical |

## Template-Anpassung

**DO**:

- ✅ Template als Ausgangspunkt nutzen
- ✅ Nicht relevante Sektionen entfernen
- ✅ Projektspezifische Sektionen hinzufügen
- ✅ Auf Zielgruppe anpassen

**DON'T**:

- ❌ Sektionen nur ausfüllen um Vorlage zu folgen
- ❌ Irrelevante Informationen hinzufügen
- ❌ Kritische Sektionen weglassen
