# PRD Best Practices

Ein Product Requirements Document (PRD) ist ein kritisches Dokument im Produktentwicklungsprozess. Hier sind die Best Practices für erstklassige PRDs.

## Grundprinzipien

### 1. Nutzerzentriert, nicht lösungszentriert

**DO ✅**:

```markdown
## Problemstellung

Benutzer können ihre monatlichen Ausgaben nicht effektiv nachverfolgen,
was zu Budgetüberschreitungen und finanzieller Unsicherheit führt.

Nutzerfeedback:
- "Ich weiß nie, wofür ich mein Geld ausgegeben habe"
- "Am Ende des Monats ist immer zu wenig übrig"
- "Ich brauche einen besseren Überblick"
```

**DON'T ❌**:

```markdown
## Lösung

Wir implementieren ein Dashboard mit React und PostgreSQL,
das Transaktionen trackt.
```

**Warum?**: PRDs fokussieren auf das WARUM (Problem) und WAS (Anforderungen), nicht auf das WIE (Implementierung).

### 2. Messbare Ziele

**DO ✅**:

```markdown
## Ziele

1. **Benutzer-Engagement**:
   - 70% der Nutzer verwenden das Feature mindestens 3x/Woche
   - Durchschnittliche Session-Dauer: 5+ Minuten

2. **Business Impact**:
   - 20% Reduktion in Support-Tickets zu "Transaktionen finden"
   - 15% Erhöhung der User-Retention nach 3 Monaten

3. **Technical Performance**:
   - Feature lädt in < 2 Sekunden
   - 99.9% Uptime
```

**DON'T ❌**:

```markdown
## Ziele

- Benutzer sollen glücklicher sein
- Mehr Engagement
- Bessere Performance
```

### 3. Klare Abgrenzung (Out of Scope)

**DO ✅**:

```markdown
## Abgrenzung (Out of Scope)

Diese PRD deckt **NICHT** ab:

- ❌ Budgetierungs-Features (separate PRD in Q2)
- ❌ Multi-Währungs-Support (erst in v2)
- ❌ Export zu Steuer-Software (Future Consideration)
- ❌ Automatische Kategorisierung via ML (Tech Debt)

**Warum**: Fokus auf Core-Feature für Initial Launch.
MVP-Ansatz mit schnellem User Feedback.
```

**DON'T ❌**:

```markdown
Alles andere kommt später.
```

### 4. User Stories mit Kontext

**DO ✅**:

```markdown
## User Stories

### US-1: Schneller Ausgaben-Überblick (Must-Have)

**Als** Sarah (Freelancerin, 28, Budget-bewusst)
**Möchte ich** auf einen Blick meine Ausgaben der letzten 30 Tage sehen
**Damit** ich rechtzeitig reagieren kann, bevor ich mein Budget überziehe

**Akzeptanzkriterien**:
- [ ] Dashboard zeigt Gesamt-Ausgaben für 7/30/90 Tage
- [ ] Visueller Vergleich zum Vormonat (±%)
- [ ] Top 3 Ausgaben-Kategorien prominent angezeigt
- [ ] Lädt in < 2 Sekunden

**Kontext**:
- 60% unserer Nutzer sind Freelancer mit unregelmäßigem Einkommen
- User Research zeigt: "Monatlicher Überblick" #1 Request
- Mockup: Link to Figma
```

**DON'T ❌**:

```markdown
## User Stories

Als Nutzer möchte ich Ausgaben sehen.
```

## PRD-Struktur Best Practices

### Executive Summary

**Länge**: 3-5 Sätze, maximal 1 Absatz

**Inhalt**:
- Was wird gebaut?
- Für wen?
- Warum ist es wichtig?
- Erwarteter Impact

**Beispiel**:

```markdown
## Executive Summary

Dieses PRD beschreibt ein Ausgaben-Dashboard für FinanceApp,
das Benutzern einen sofortigen Überblick über ihre monatlichen
Ausgaben gibt. Primäre Zielgruppe sind Freelancer und
Budget-bewusste Nutzer (60% unserer Nutzerbasis). Feature
soll Engagement um 20% steigern und Support-Last um 15%
reduzieren. Geschätzte Entwicklungszeit: 4 Wochen, Launch Q2.
```

### Problemstellung

**Struktur**:
1. **Aktueller Zustand**: Was ist das Problem?
2. **Auswirkungen**: Wen betrifft es? Wie stark?
3. **Evidenz**: Daten, Feedback, Metrics
4. **Opportunität**: Warum jetzt lösen?

**Beispiel**:

```markdown
## Problemstellung

### Aktueller Zustand

Nutzer haben keinen schnellen Überblick über ihre Ausgaben.
Sie müssen durch Transaktionslisten scrollen und manuell
rechnen, um zu verstehen, wo ihr Geld hingeht.

### Auswirkungen

- **Nutzer-Frustration**: 45% geben in Umfragen "unübersichtlich" an
- **Support-Last**: 120 Tickets/Monat zu "Ausgaben finden"
- **Churn-Risiko**: 25% der abgewanderten Nutzer nennen
  "fehlende Übersicht" als Grund

### Evidenz

- User Interviews (n=50): 92% wünschen Dashboard
- Analytics: Nur 15% der Nutzer entdecken Report-Feature
- Competitor Analysis: Alle Top-3-Wettbewerber haben Dashboard

### Opportunität

Mit bevorstehendem Marketing-Push (Q2) ist jetzt der ideale
Zeitpunkt, um Retention durch bessere UX zu verbessern.
```

### Funktionale Anforderungen

**Priorisierung**: Must-Have, Should-Have, Nice-to-Have

**Format**: User-orientiert, nicht technisch

**Beispiel**:

```markdown
## Funktionale Anforderungen

### Must-Have (MVP)

#### FR-1: Ausgaben-Übersicht

**Beschreibung**: Dashboard zeigt aggregierte Ausgaben für
gewählten Zeitraum.

**Details**:
- Zeiträume: 7 Tage, 30 Tage, 90 Tage (Tabs)
- Anzeige: Gesamtbetrag + Vergleich zum Vorperiode
- Visuell: Trend-Grafik (Line Chart)
- Ladezeit: < 2 Sekunden

**Akzeptanzkriterien**:
- [ ] Nutzer kann Zeitraum wählen
- [ ] Gesamtbetrag wird korrekt berechnet
- [ ] Trend-Grafik zeigt tägliche Summen
- [ ] Funktioniert auf Mobile und Desktop

**Abhängigkeiten**:
- Transaktionsdaten-API (bereits vorhanden)
- Design System Components

#### FR-2: Kategorien-Breakdown

**Beschreibung**: Top-Kategorien mit Prozentwerten anzeigen

**Details**:
- Zeige Top 5 Ausgaben-Kategorien
- Prozent vom Gesamtbetrag
- Klickbar für Details (Link zu Transaktionen)

**Akzeptanzkriterien**:
- [ ] Kategorien sortiert nach Höhe
- [ ] Prozente summieren sich zu 100%
- [ ] Link führt zu gefilterten Transaktionen

### Should-Have (Post-MVP)

#### FR-3: Budget-Warnungen

**Beschreibung**: Visuelle Warnung bei Budgetüberschreitung

**Details**:
- Wenn Ausgaben > 80% des Monatsbudgets: Warnung
- Wenn Ausgaben > 100%: Kritische Warnung
- Konfigurierbar in Settings

**Rationale**: Hohe Nachfrage in User Research (65%),
aber nicht kritisch für Launch.

### Nice-to-Have (Future Consideration)

#### FR-4: Export als PDF

**Beschreibung**: Dashboard als PDF exportieren

**Rationale**: Geringer User-Request (12%), hoher Aufwand.
Evaluieren nach Launch basierend auf Feedback.
```

### Nicht-funktionale Anforderungen

**Kategorien**: Performance, Security, Usability, Accessibility

**Beispiel**:

```markdown
## Nicht-funktionale Anforderungen

### Performance

- **NFR-1**: Dashboard lädt in < 2s (p95)
- **NFR-2**: API-Response < 500ms
- **NFR-3**: Funktioniert mit 100k+ Transaktionen

**Messung**:
- Lighthouse Performance Score > 90
- Real User Monitoring (RUM) Setup

### Security

- **NFR-4**: Sensible Finanzdaten verschlüsselt (AES-256)
- **NFR-5**: GDPR-konform (Daten-Minimierung)
- **NFR-6**: Audit-Log für Datenzugriffe

### Usability

- **NFR-7**: Mobile-First Design (60% Mobile-Traffic)
- **NFR-8**: Intuitive Nutzung ohne Onboarding
- **NFR-9**: Error States klar kommuniziert

**Validierung**: Usability-Testing mit 10 Nutzern

### Accessibility

- **NFR-10**: WCAG 2.1 Level AA konform
- **NFR-11**: Screen-Reader kompatibel
- **NFR-12**: Keyboard-Navigation vollständig

**Tools**:
- Lighthouse Accessibility Audit
- axe DevTools
- Screen Reader Testing (NVDA, VoiceOver)
```

## Erfolgsmetriken

### SMART Metrics

**Spezifisch, Messbar, Erreichbar, Relevant, Zeitgebunden**

**DO ✅**:

```markdown
## Erfolgsmetriken

### Primäre Metriken (Launch + 4 Wochen)

1. **Feature-Adoption**
   - **Metrik**: % der aktiven Nutzer, die Dashboard besuchen
   - **Ziel**: 60% innerhalb 4 Wochen nach Launch
   - **Baseline**: N/A (neues Feature)
   - **Messung**: Analytics Event "dashboard_viewed"

2. **Engagement**
   - **Metrik**: Durchschnittliche Besuche pro Woche
   - **Ziel**: 3+ Besuche/Woche pro aktiven Nutzer
   - **Baseline**: N/A
   - **Messung**: Analytics, tracked weekly

3. **User Satisfaction**
   - **Metrik**: NPS Score für Dashboard
   - **Ziel**: NPS > 40
   - **Baseline**: Overall App NPS = 35
   - **Messung**: In-App Survey (n > 100)

### Sekundäre Metriken (Launch + 8 Wochen)

4. **Support Impact**
   - **Metrik**: Tickets zu "Ausgaben finden"
   - **Ziel**: -20% Reduktion
   - **Baseline**: 120 Tickets/Monat
   - **Messung**: Support Ticket Tags

5. **Retention**
   - **Metrik**: 90-Tage User Retention
   - **Ziel**: +5% Verbesserung
   - **Baseline**: 68% retention
   - **Messung**: Cohort Analysis

### Tracking-Plan

| Metrik | Tool | Frequenz | Owner |
|--------|------|----------|-------|
| Dashboard Views | Mixpanel | Daily | PM |
| Session Duration | Google Analytics | Weekly | PM |
| NPS Survey | In-App | 2 weeks post-launch | UX |
| Support Tickets | Zendesk | Weekly | Support Lead |
```

**DON'T ❌**:

```markdown
## Erfolgsmetriken

- Nutzer sind zufriedener
- Feature wird verwendet
- Support-Tickets reduzieren sich
```

## Risikobewertung

**Format**: Risiko → Impact → Likelihood → Mitigation

**Beispiel**:

```markdown
## Risikobewertung

### Hohe Priorität (Kritisch)

#### R-1: Performance bei großen Datenmengen

- **Risiko**: Dashboard langsam bei Nutzern mit 50k+ Transaktionen
- **Impact**: Hoch (betrifft 15% Power-User)
- **Likelihood**: Mittel (nicht in allen Tests reproduziert)
- **Mitigation**:
  - Backend-Caching implementieren
  - Progressive Loading für große Datensätze
  - Performance-Tests mit Produktionsdaten
  - Fallback: Pagination bei > 10k Transaktionen

#### R-2: Datenschutz-Bedenken

- **Risiko**: Nutzer besorgt über Dashboard-Daten-Speicherung
- **Impact**: Hoch (kann zu Churn führen)
- **Likelihood**: Niedrig (basierend auf bestehenden Features)
- **Mitigation**:
  - Transparente Privacy-Notice
  - Opt-Out Option
  - GDPR-Review vor Launch
  - Clear Kommunikation: "Keine neue Datenspeicherung"

### Mittlere Priorität

#### R-3: Kategorisierung-Genauigkeit

- **Risiko**: Auto-Kategorisierung falsch → Dashboard ungenau
- **Impact**: Mittel (Nutzer können manuell korrigieren)
- **Likelihood**: Mittel (bekannte Limitierung)
- **Mitigation**:
  - ML-Modell-Training verbessern (pre-launch)
  - Einfache Re-Kategorisierung im UI
  - User Feedback Loop für Training

### Niedrige Priorität

#### R-4: Browser-Kompatibilität

- **Risiko**: Chart-Library funktioniert nicht in IE11
- **Impact**: Niedrig (< 2% IE11 Nutzer)
- **Likelihood**: Hoch
- **Mitigation**:
  - Polyfills
  - Graceful Degradation (Tabelle statt Chart)
  - Sunset IE11 Support Q3
```

## Stakeholder-Management

### Approvals Matrix

```markdown
## Stakeholder & Approvals

| Rolle | Name | Verantwortung | Approval Required |
|-------|------|---------------|-------------------|
| Product Owner | Sarah Chen | Final PRD Approval | ✅ Must |
| Engineering Lead | Mike Johnson | Technical Feasibility | ✅ Must |
| Design Lead | Anna Schmidt | UX/UI Alignment | ✅ Must |
| Data/Analytics | Tom Williams | Metrics Definition | ✅ Must |
| Legal/Compliance | Legal Team | GDPR Review | ✅ Must |
| Marketing | Jane Doe | Go-to-Market | ℹ️ Informed |
| Support Lead | Chris Brown | Support Readiness | ℹ️ Informed |

**Approval Timeline**:
- Draft PRD: 2024-11-01
- Review Period: 5 business days
- Final Approval: 2024-11-08
- Kickoff: 2024-11-11
```

## Versionierung & Updates

**Best Practice**: PRD ist lebendiges Dokument

```markdown
## Änderungshistorie

| Version | Datum | Autor | Änderungen |
|---------|-------|-------|-----------|
| 1.0 | 2024-10-30 | Sarah Chen | Initial Draft |
| 1.1 | 2024-11-02 | Sarah Chen | Added NFR-10 (Accessibility) based on Legal Review |
| 1.2 | 2024-11-05 | Sarah Chen | Reduced Scope: Moved Budget-Warnings to Should-Have |
| 2.0 | 2024-11-08 | Sarah Chen | Final Approved Version |

## Status: ✅ APPROVED (2024-11-08)
```

## Häufige Fehler vermeiden

### ❌ Zu technisch

```markdown
BAD: "Implementiere Redis-Caching mit TTL von 3600s"
GOOD: "Dashboard-Daten werden gecacht für schnelle Ladezeit"
```

### ❌ Zu vage

```markdown
BAD: "Nutzer sollen Ausgaben sehen können"
GOOD: "Nutzer sehen aggregierte Ausgaben für 7/30/90 Tage
       mit Trend-Grafik und Top-5-Kategorien"
```

### ❌ Fehlende Priorisierung

```markdown
BAD: Alle Features sind "wichtig"
GOOD: Klare Must/Should/Nice-to-Have Einteilung mit Rationale
```

### ❌ Keine Metrics

```markdown
BAD: "Feature wird erfolgreich sein"
GOOD: "Erfolg gemessen an 60% Adoption in 4 Wochen"
```

### ❌ Keine Abgrenzung

```markdown
BAD: Feature-Liste ohne Ende
GOOD: Explizite "Out of Scope" Sektion mit Begründung
```

## Checkliste: Gutes PRD

Vor Finalisierung prüfen:

### Inhalt
- [ ] Executive Summary prägnant (< 5 Sätze)
- [ ] Problem klar definiert mit Evidenz
- [ ] Ziele SMART (spezifisch, messbar, erreichbar)
- [ ] User Stories mit Akzeptanzkriterien
- [ ] Funktionale Anforderungen priorisiert
- [ ] NFRs für Performance, Security, Usability
- [ ] Erfolgsmetriken mit konkreten Zahlen
- [ ] Risiken identifiziert mit Mitigation
- [ ] "Out of Scope" klar definiert

### Format
- [ ] Konsistente Formatierung
- [ ] Überschriften hierarchisch
- [ ] Listen & Tabellen für Übersicht
- [ ] Mockups/Wireframes verlinkt
- [ ] Technische Begriffe erklärt

### Prozess
- [ ] Stakeholder-Input eingeholt
- [ ] Technische Feasibility geklärt
- [ ] Design-Alignment bestätigt
- [ ] Legal/Compliance Review (falls nötig)
- [ ] Approvals dokumentiert
- [ ] Versionierung implementiert

### Qualität
- [ ] Nutzer-zentriert (nicht lösungs-zentriert)
- [ ] Verständlich für alle Stakeholder
- [ ] Keine Widersprüche
- [ ] Realistischer Scope
- [ ] Actionable für Entwicklungsteam
