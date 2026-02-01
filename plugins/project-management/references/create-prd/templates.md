# PRD Templates and Examples

Various PRD templates for different project types and complexity levels.

## Template 1: Minimal Viable PRD (MVP)

For small features or rapid iterations.

```markdown
# PRD: [Feature Name]

**Status**: Draft | Review | Approved
**Author**: [Name]
**Date**: [YYYY-MM-DD]
**Version**: 1.0

## tl;dr (Executive Summary)

[2-3 sentences: What, For whom, Why, Expected impact]

## Problem

[What problem are we solving? With evidence.]

## Objective

[1 primary, measurable objective]

- **Metric**: [What are we measuring?]
- **Target**: [Specific target value]
- **Timeline**: [By when?]

## User Story

As [Persona]
I want [Action]
So that [Benefit]

**Acceptance Criteria**:

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Out of Scope

- [What is not being built]
- [What is deferred to a later version]

## Success Metrics

- **Primary**: [Metric + Target]
- **Secondary**: [Metric + Target]

## Risks

- [Risk 1 + Mitigation]
- [Risk 2 + Mitigation]

## Timeline

- Design: [Date]
- Development: [Date]
- Launch: [Date]

## Approvals

- [ ] Product Owner
- [ ] Engineering Lead
- [ ] Design Lead
```

**When to use**:

- Small features (< 2 weeks development)
- Clear scope
- Few dependencies
- Experimental features

## Template 2: Standard Feature PRD

For typical new features.

````markdown
# Product Requirements Document: [Feature Name]

---

## Document Information

|----------------|---------------------------|
| **Status** | Draft / Review / Approved |
| **Author** | [Name, Team] |
| **Stakeholders**| [List] |
| **Created** | [Date] |
| **Last Updated** | [Date] |
| **Version** | 1.0 |
| **Target Release** | Q[X] YYYY |

---

## Executive Summary

[3-5 sentences summarizing:]

- What is being built?
- For whom?
- Why is it important?
- Expected business impact?
- Timeline?

---

## Table of Contents

1. [Problem Statement](#problem-statement)
2. [Objectives & Success Metrics](#objectives--success-metrics)
3. [User Stories & Personas](#user-stories--personas)
4. [Functional Requirements](#functional-requirements)
5. [Non-Functional Requirements](#non-functional-requirements)
6. [Delimitation (Out of Scope)](#delimitation-out-of-scope)
7. [User Experience](#user-experience)
8. [Technical Considerations](#technical-considerations)
9. [Risk Assessment](#risk-assessment)
10. [Dependencies](#dependencies)
11. [Timeline & Milestones](#timeline--milestones)
12. [Appendix](#appendix)

---

## 1. Problem Statement

### Current State

[Describe the current situation]

### Problem Description

[What is the specific problem? Who is affected?]

### Impact

**User Impact**:

- [Impact 1 with data]
- [Impact 2 with data]

**Business Impact**:

- [Metric 1: e.g., churn rate]
- [Metric 2: e.g., support tickets]
- [Metric 3: e.g., revenue impact]

### Evidence & Research

**Quantitative**:

- Analytics: [Data]
- Metrics: [Numbers]

**Qualitative**:

- User interviews: [n=X, key findings]
- Support feedback: [Patterns]
- Surveys: [n=X, results]

**Market Analysis**:

- Competitor features: [Comparison]
- Industry trends: [Relevant trends]

### Why Now?

[Timing, opportunity, strategic importance]

---

## 2. Objectives & Success Metrics

### Product Objectives

1. **[Objective Name]**
   - Description: [Details]
   - Rationale: [Why important?]
   - Measurement: [How to measure?]

2. **[Objective Name]**
   - ...

### Business Objectives

- [Business objective 1 with context]
- [Business objective 2 with context]

### Success Metrics

#### Primary Metrics (Launch + 4 Weeks)

| Metric     | Baseline | Target   | Measurement Method | Owner  |
| ---------- | -------- | -------- | ------------------ | ------ |
| [Metric 1] | [Value]  | [Target] | [Tool/Method]      | [Name] |
| [Metric 2] | [Value]  | [Target] | [Tool/Method]      | [Name] |

#### Secondary Metrics (Launch + 8 Weeks)

| Metric     | Baseline | Target   | Measurement Method | Owner  |
| ---------- | -------- | -------- | ------------------ | ------ |
| [Metric 3] | [Value]  | [Target] | [Tool/Method]      | [Name] |
| [Metric 4] | [Value]  | [Target] | [Tool/Method]      | [Name] |

#### Guardrail Metrics

[Metrics that must not be negatively impacted]

---

## 3. User Stories & Personas

### Primary Personas

#### Persona 1: [Name]

**Demographics**:

- Role: [e.g., Freelancer]
- Age: [Range]
- Tech-savviness: [Level]

**Context**:

- [Relevant background]
- [Usage context]
- [Pain points]

**Goals**:

- [Goal 1]
- [Goal 2]

**Quote**: "[Typical user quote]"

### User Stories

#### Epic 1: [Epic Name]

**US-1.1: [Story Title]** (Priority: Must-Have)

**As** [Persona]
**I want** [Action/Feature]
**So that** [Benefit/Outcome]

**Acceptance Criteria**:

- [ ] [Specific, testable criterion 1]
- [ ] [Specific, testable criterion 2]
- [ ] [Specific, testable criterion 3]

**Context**:

- [Additional information]
- [User research findings]
- [Mockup links]

**Dependencies**:

- [Technical/feature dependencies]

**US-1.2: [Story Title]** (Priority: Should-Have)

[...]

---

## 4. Functional Requirements

### Must-Have (MVP)

#### FR-1: [Requirement Name]

**Description**: [Detailed description]

**Details**:

- [Specification 1]
- [Specification 2]
- [Specification 3]

**User Flow**:

1. User [Action]
2. System [Reaction]
3. User [Next action]

**Acceptance Criteria**:

- [ ] [Criterion 1]
- [ ] [Criterion 2]

**Edge Cases**:

- [Edge case 1 + Handling]
- [Edge case 2 + Handling]

**Dependencies**:

- [API, Service, Feature]

**Mockups**: [Link]

#### FR-2: [Requirement Name]

[...]

### Should-Have (Post-MVP)

#### FR-X: [Requirement Name]

**Rationale for Should-Have**: [Why not MVP?]

[...]

### Nice-to-Have (Future Consideration)

#### FR-Y: [Requirement Name]

**Rationale**: [Why later/maybe?]

[...]

---

## 5. Non-Functional Requirements

### Performance

- **NFR-1**: [Requirement with specific target]
  - Measurement: [How to test?]
  - Rationale: [Why important?]

### Security & Privacy

- **NFR-X**: [Security requirement]
  - Compliance: [GDPR, HIPAA, etc.]
  - Implementation: [High-level approach]

### Scalability

- **NFR-X**: [Scalability requirement]
  - Expected load: [Numbers]
  - Target: [Performance at load]

### Usability

- **NFR-X**: [Usability requirement]
  - Validation: [Usability testing plan]

### Accessibility

- **NFR-X**: WCAG 2.1 Level AA Compliance
  - Testing: [Tools & methods]

### Reliability

- **NFR-X**: [Uptime, error rate requirements]
  - Monitoring: [How to monitor?]

---

## 6. Delimitation (Out of Scope)

### Not in This Release

| Feature     | Rationale | Planned For |
| ----------- | --------- | ----------- |
| [Feature 1] | [Reason]  | [Q/Version] |
| [Feature 2] | [Reason]  | [Q/Version] |

### Explicitly Excluded

- **[Feature]**: [Detailed justification]
- **[Feature]**: [Detailed justification]

---

## 7. User Experience

### User Flows

[Visual user flow diagrams or links]

### Wireframes/Mockups

- [Mockup 1: Screen Name] - [Link]
- [Mockup 2: Screen Name] - [Link]

### Interaction Patterns

[Description of important interactions]

### Mobile Considerations

[Specific mobile UX requirements]

---

## 8. Technical Considerations

**Note**: Focus on WHAT, not HOW. Technical decisions are the responsibility of the development team.

### Systems Affected

- [System 1]: [Type of change]
- [System 2]: [Type of change]

### APIs Required

- [API 1]: [Purpose]
- [API 2]: [Purpose]

### Data Model

[New entities, important changes - high level]

### Third-Party Integrations

- [Service 1]: [Purpose, licensing considerations]

### Performance Considerations

[Critical performance aspects]

### Security Considerations

[Important security aspects]

---

## 9. Risk Assessment

| ID  | Risk   | Impact | Likelihood | Mitigation | Owner  |
| --- | ------ | ------ | ---------- | ---------- | ------ |
| R-1 | [Risk] | H/M/L  | H/M/L      | [Strategy] | [Name] |
| R-2 | [Risk] | H/M/L  | H/M/L      | [Strategy] | [Name] |

### Details for High-Priority Risks

#### R-1: [Risk Name]

**Description**: [Detailed description]

**Impact**: [Effects if it occurs]

**Likelihood**: [Probability]

**Mitigation Strategy**:

1. [Preventive measure 1]
2. [Preventive measure 2]

**Contingency Plan**:
[What to do if it occurs?]

---

## 10. Dependencies

### Internal Dependencies

| Dependency    | Team   | Status   | Impact if Delayed |
| ------------- | ------ | -------- | ----------------- |
| [Feature/API] | [Team] | [Status] | [Impact]          |

### External Dependencies

| Dependency    | Vendor   | Timeline | Risk         |
| ------------- | -------- | -------- | ------------ |
| [Service/API] | [Vendor] | [ETA]    | [Risk Level] |

### Blocking Issues

[Critical blockers that must be resolved]

---

## 11. Timeline & Milestones

### Phases

```text
Discovery -----> Design -----> Development -----> Testing -----> Launch
Week 1-2        Week 3-4       Week 5-8           Week 9        Week 10
```
````

### Detailed Schedule

| Phase           | Activities      | Deliverables   | Date   | Owner  |
| --------------- | --------------- | -------------- | ------ | ------ |
| **Discovery**   | Research, PRD   | Finalized PRD  | [Date] | PM     |
| **Design**      | Mockups, Specs  | Design Specs   | [Date] | Design |
| **Development** | Sprint 1        | Backend APIs   | [Date] | Eng    |
| **Development** | Sprint 2        | Frontend UI    | [Date] | Eng    |
| **Testing**     | QA, UAT         | Test Reports   | [Date] | QA     |
| **Launch**      | Deploy, Monitor | Launch Metrics | [Date] | PM     |

### Milestones

- **M1**: PRD Approval - [Date]
- **M2**: Design Approval - [Date]
- **M3**: Development Complete - [Date]
- **M4**: QA Sign-off - [Date]
- **M5**: Production Launch - [Date]
- **M6**: Success Metrics Review - [Date]

---

## 12. Appendix

### Change History

| Version | Date   | Author | Changes                |
| ------- | ------ | ------ | ---------------------- |
| 0.1     | [Date] | [Name] | Initial draft          |
| 1.0     | [Date] | [Name] | First complete version |

### References

- [User Research Report: Link]
- [Competitive Analysis: Link]
- [Technical Spike: Link]
- [Design Exploration: Link]

### Approvals

| Role             | Name   | Date   | Signature/Approval |
| ---------------- | ------ | ------ | ------------------ |
| Product Owner    | [Name] | [Date] |                    |
| Engineering Lead | [Name] | [Date] |                    |
| Design Lead      | [Name] | [Date] |                    |
| Legal/Compliance | [Name] | [Date] |                    |

### Glossary

- **[Term]**: [Definition]
- **[Term]**: [Definition]

````

**When to use**:

- Standard new features
- Medium complexity
- Multiple stakeholders
- 4-8 weeks development

## Template 3: Major Initiative PRD

For large, strategic projects.

[Includes all elements from Template 2, plus:]

```markdown
## Strategic Context

### Vision

[Long-term vision]

### Strategic Alignment

**Company OKRs**:
- [OKR 1]: How does the feature contribute?
- [OKR 2]: How does the feature contribute?

**Product Strategy**:
[How does it fit into the larger product roadmap?]

### Market Opportunity

**Market Size**:
- TAM: [Total Addressable Market]
- SAM: [Serviceable Addressable Market]
- SOM: [Serviceable Obtainable Market]

**Competitive Advantage**:
[How does this differentiate us?]

### Business Case

**Investment**:
- Engineering: [Person-weeks]
- Design: [Person-weeks]
- Estimated cost: [EUR/USD]

**Expected Return**:
- Revenue impact: [Projection]
- Cost savings: [Projection]
- User growth: [Projection]

**ROI Calculation**:
[Formula + expected ROI]

## Go-to-Market Strategy

### Launch Plan

**Pre-Launch** (T-4 weeks):
- [Activity 1]
- [Activity 2]

**Launch** (T-0):
- [Activity 1]
- [Activity 2]

**Post-Launch** (T+2 weeks):
- [Activity 1]
- [Activity 2]

### Marketing & Communication

**Internal**:
- [Team communication plan]

**External**:
- [User communication plan]
- [Press/PR if applicable]

### Training & Documentation

- User documentation: [Plan]
- Support training: [Plan]
- Sales enablement: [If B2B]

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

**Scheduled**: [Date, 4 weeks post-launch]

**Participants**: [List]

**Format**: [Structured review of goals vs. actuals]
````

**When to use**:

- Strategic initiatives
- Large investments (>2 months development)
- High business impact
- Executive visibility

## Template 4: Technical PRD

For platform/infrastructure projects.

```markdown
# Technical PRD: [Project Name]

[Standard PRD sections, plus:]

## Problem (Technical)

### Current State

**Architecture**:
[Current technical architecture]

**Pain Points**:

- [Performance issue]
- [Scalability issue]
- [Maintenance issue]

**Technical Debt**:
[Relevant tech debt]

### Proposed Solution (High-Level)

[Architecture overview, not too detailed]

## Technical Requirements

### TR-1: [Requirement]

**Current**: [Current state]
**Target**: [Target state]
**Rationale**: [Why important?]

**Acceptance Criteria**:

- [ ] [Testable criterion]

### Performance Requirements

| Metric     | Current | Target  | Measurement |
| ---------- | ------- | ------- | ----------- |
| Latency    | [ms]    | [ms]    | [Method]    |
| Throughput | [req/s] | [req/s] | [Method]    |
| Uptime     | [%]     | [%]     | [Method]    |

### Compatibility Requirements

- Backward compatibility: [Yes/No, details]
- API versioning: [Strategy]
- Migration path: [Plan]

## Impact Assessment

### Systems Affected

| System   | Impact         | Downtime Required | Migration |
| -------- | -------------- | ----------------- | --------- |
| [System] | [High/Med/Low] | [Duration]        | [Yes/No]  |

### Data Migration

**Scope**: [What data needs migration]
**Volume**: [Size]
**Strategy**: [Online/Offline, phased]
**Rollback**: [Plan]

## Testing Strategy

### Unit Tests

- Coverage target: [%]
- New tests: [Estimated count]

### Integration Tests

[Scope of integration testing]

### Performance Tests

- Load tests: [Scenarios]
- Stress tests: [Scenarios]
- Benchmarks: [What to benchmark]

### Chaos Engineering

[If applicable, chaos testing plans]
```

**When to use**:

- Infrastructure projects
- Platform features
- Architecture changes
- Developer-facing features

## Quick Reference: Template Selection

| Project Type      | Duration   | Complexity  | Template         |
| ----------------- | ---------- | ----------- | ---------------- |
| Quick Enhancement | < 2 weeks  | Low         | Minimal MVP      |
| Standard Feature  | 4-8 weeks  | Medium      | Standard Feature |
| Major Initiative  | > 2 months | High        | Major Initiative |
| Platform/Infra    | Variable   | Medium-High | Technical        |

## Template Customization

**DO**:

- Use template as starting point
- Remove non-relevant sections
- Add project-specific sections
- Adapt to target audience

**DON'T**:

- Fill sections just to follow template
- Add irrelevant information
- Omit critical sections
