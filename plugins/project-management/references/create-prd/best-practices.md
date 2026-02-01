# PRD Best Practices

A Product Requirements Document (PRD) is a critical document in the product development process. The following best practices ensure the creation of high-quality PRDs.

## Fundamental Principles

### 1. User-Centric, Not Solution-Centric

**DO:**

```markdown
## Problem Statement

Users cannot effectively track their monthly expenses, resulting in budget overruns and financial uncertainty.

User Feedback:

- "I never know where my money went"
- "There is always too little left at the end of the month"
- "I need a better overview"
```

**DON'T:**

```markdown
## Solution

We will implement a dashboard with React and PostgreSQL that tracks transactions.
```

**Rationale**: PRDs focus on the WHY (problem) and WHAT (requirements), not on the HOW (implementation).

### 2. Measurable Objectives

**DO:**

```markdown
## Objectives

1. **User Engagement**:
   - 70% of users utilize the feature at least 3x/week
   - Average session duration: 5+ minutes

2. **Business Impact**:
   - 20% reduction in support tickets related to "finding transactions"
   - 15% increase in user retention after 3 months

3. **Technical Performance**:
   - Feature loads in < 2 seconds
   - 99.9% uptime
```

**DON'T:**

```markdown
## Objectives

- Users should be happier
- More engagement
- Better performance
```

### 3. Clear Delimitation (Out of Scope)

**DO:**

```markdown
## Delimitation (Out of Scope)

This PRD does **NOT** cover:

- Budgeting features (separate PRD in Q2)
- Multi-currency support (deferred to v2)
- Export to tax software (future consideration)
- Automatic categorization via ML (technical debt)

**Rationale**: Focus on core feature for initial launch. MVP approach with rapid user feedback.
```

**DON'T:**

```markdown
Everything else comes later.
```

### 4. User Stories with Context

**DO:**

```markdown
## User Stories

### US-1: Quick Expense Overview (Must-Have)

**As** Sarah (freelancer, 28, budget-conscious)
**I want to** see my expenses for the last 30 days at a glance
**So that** I can react in time before exceeding my budget

**Acceptance Criteria**:

- [ ] Dashboard displays total expenses for 7/30/90 days
- [ ] Visual comparison with previous month (±%)
- [ ] Top 3 expense categories prominently displayed
- [ ] Loads in < 2 seconds

**Context**:

- 60% of our users are freelancers with irregular income
- User research indicates: "Monthly overview" is the #1 request
- Mockup: Link to Figma
```

**DON'T:**

```markdown
## User Stories

As a user I want to see expenses.
```

## PRD Structure Best Practices

### Executive Summary

**Length**: 3-5 sentences, maximum 1 paragraph

**Content**:

- What is being built?
- For whom?
- Why is it important?
- Expected impact

**Example**:

```markdown
## Executive Summary

This PRD describes an expense dashboard for FinanceApp that provides users with an immediate overview of their monthly expenses. The primary target audience consists of freelancers and budget-conscious users (60% of our user base). The feature is intended to increase engagement by 20% and reduce support load by 15%. Estimated development time: 4 weeks, launch Q2.
```

### Problem Statement

**Structure**:

1. **Current State**: What is the problem?
2. **Impact**: Who is affected? To what extent?
3. **Evidence**: Data, feedback, metrics
4. **Opportunity**: Why address it now?

**Example**:

```markdown
## Problem Statement

### Current State

Users lack a quick overview of their expenses. They must scroll through transaction lists and calculate manually to understand where their money is going.

### Impact

- **User Frustration**: 45% indicate "unclear" in surveys
- **Support Load**: 120 tickets/month related to "finding expenses"
- **Churn Risk**: 25% of churned users cite "lack of overview" as the reason

### Evidence

- User Interviews (n=50): 92% desire a dashboard
- Analytics: Only 15% of users discover the report feature
- Competitor Analysis: All top 3 competitors have dashboards

### Opportunity

With the upcoming marketing push (Q2), now is the ideal time to improve retention through better UX.
```

### Functional Requirements

**Prioritization**: Must-Have, Should-Have, Nice-to-Have

**Format**: User-oriented, not technical

**Example**:

```markdown
## Functional Requirements

### Must-Have (MVP)

#### FR-1: Expense Overview

**Description**: Dashboard displays aggregated expenses for the selected time period.

**Details**:

- Time periods: 7 days, 30 days, 90 days (tabs)
- Display: Total amount + comparison to previous period
- Visual: Trend graph (line chart)
- Load time: < 2 seconds

**Acceptance Criteria**:

- [ ] User can select time period
- [ ] Total amount is calculated correctly
- [ ] Trend graph shows daily totals
- [ ] Functions on mobile and desktop

**Dependencies**:

- Transaction data API (already available)
- Design system components

#### FR-2: Category Breakdown

**Description**: Display top categories with percentage values

**Details**:

- Show top 5 expense categories
- Percentage of total amount
- Clickable for details (link to transactions)

**Acceptance Criteria**:

- [ ] Categories sorted by amount
- [ ] Percentages sum to 100%
- [ ] Link navigates to filtered transactions

### Should-Have (Post-MVP)

#### FR-3: Budget Warnings

**Description**: Visual warning upon budget exceedance

**Details**:

- When expenses > 80% of monthly budget: Warning
- When expenses > 100%: Critical warning
- Configurable in settings

**Rationale**: High demand in user research (65%), but not critical for launch.

### Nice-to-Have (Future Consideration)

#### FR-4: Export as PDF

**Description**: Export dashboard as PDF

**Rationale**: Low user request (12%), high effort. Evaluate after launch based on feedback.
```

### Non-Functional Requirements

**Categories**: Performance, Security, Usability, Accessibility

**Example**:

```markdown
## Non-Functional Requirements

### Performance

- **NFR-1**: Dashboard loads in < 2s (p95)
- **NFR-2**: API response < 500ms
- **NFR-3**: Functions with 100k+ transactions

**Measurement**:

- Lighthouse Performance Score > 90
- Real User Monitoring (RUM) setup

### Security

- **NFR-4**: Sensitive financial data encrypted (AES-256)
- **NFR-5**: GDPR-compliant (data minimization)
- **NFR-6**: Audit log for data access

### Usability

- **NFR-7**: Mobile-first design (60% mobile traffic)
- **NFR-8**: Intuitive use without onboarding
- **NFR-9**: Error states clearly communicated

**Validation**: Usability testing with 10 users

### Accessibility

- **NFR-10**: WCAG 2.1 Level AA compliant
- **NFR-11**: Screen reader compatible
- **NFR-12**: Full keyboard navigation

**Tools**:

- Lighthouse Accessibility Audit
- axe DevTools
- Screen reader testing (NVDA, VoiceOver)
```

## Success Metrics

### SMART Metrics

**Specific, Measurable, Achievable, Relevant, Time-bound**

**DO:**

```markdown
## Success Metrics

### Primary Metrics (Launch + 4 Weeks)

1. **Feature Adoption**
   - **Metric**: % of active users visiting dashboard
   - **Target**: 60% within 4 weeks of launch
   - **Baseline**: N/A (new feature)
   - **Measurement**: Analytics event "dashboard_viewed"

2. **Engagement**
   - **Metric**: Average visits per week
   - **Target**: 3+ visits/week per active user
   - **Baseline**: N/A
   - **Measurement**: Analytics, tracked weekly

3. **User Satisfaction**
   - **Metric**: NPS Score for dashboard
   - **Target**: NPS > 40
   - **Baseline**: Overall App NPS = 35
   - **Measurement**: In-app survey (n > 100)

### Secondary Metrics (Launch + 8 Weeks)

4. **Support Impact**
   - **Metric**: Tickets related to "finding expenses"
   - **Target**: -20% reduction
   - **Baseline**: 120 tickets/month
   - **Measurement**: Support ticket tags

5. **Retention**
   - **Metric**: 90-day user retention
   - **Target**: +5% improvement
   - **Baseline**: 68% retention
   - **Measurement**: Cohort analysis

### Tracking Plan

| Metric           | Tool             | Frequency           | Owner        |
| ---------------- | ---------------- | ------------------- | ------------ |
| Dashboard Views  | Mixpanel         | Daily               | PM           |
| Session Duration | Google Analytics | Weekly              | PM           |
| NPS Survey       | In-App           | 2 weeks post-launch | UX           |
| Support Tickets  | Zendesk          | Weekly              | Support Lead |
```

**DON'T:**

```markdown
## Success Metrics

- Users are more satisfied
- Feature is used
- Support tickets decrease
```

## Risk Assessment

**Format**: Risk - Impact - Likelihood - Mitigation

**Example**:

```markdown
## Risk Assessment

### High Priority (Critical)

#### R-1: Performance with Large Data Volumes

- **Risk**: Dashboard slow for users with 50k+ transactions
- **Impact**: High (affects 15% power users)
- **Likelihood**: Medium (not reproduced in all tests)
- **Mitigation**:
  - Implement backend caching
  - Progressive loading for large datasets
  - Performance tests with production data
  - Fallback: Pagination for > 10k transactions

#### R-2: Privacy Concerns

- **Risk**: Users concerned about dashboard data storage
- **Impact**: High (can lead to churn)
- **Likelihood**: Low (based on existing features)
- **Mitigation**:
  - Transparent privacy notice
  - Opt-out option
  - GDPR review before launch
  - Clear communication: "No new data storage"

### Medium Priority

#### R-3: Categorization Accuracy

- **Risk**: Auto-categorization incorrect - dashboard inaccurate
- **Impact**: Medium (users can correct manually)
- **Likelihood**: Medium (known limitation)
- **Mitigation**:
  - Improve ML model training (pre-launch)
  - Simple re-categorization in UI
  - User feedback loop for training

### Low Priority

#### R-4: Browser Compatibility

- **Risk**: Chart library does not work in IE11
- **Impact**: Low (< 2% IE11 users)
- **Likelihood**: High
- **Mitigation**:
  - Polyfills
  - Graceful degradation (table instead of chart)
  - Sunset IE11 support Q3
```

## Stakeholder Management

### Approvals Matrix

```markdown
## Stakeholders & Approvals

| Role             | Name         | Responsibility        | Approval Required |
| ---------------- | ------------ | --------------------- | ----------------- |
| Product Owner    | Sarah Chen   | Final PRD approval    | Must              |
| Engineering Lead | Mike Johnson | Technical feasibility | Must              |
| Design Lead      | Anna Schmidt | UX/UI alignment       | Must              |
| Data/Analytics   | Tom Williams | Metrics definition    | Must              |
| Legal/Compliance | Legal Team   | GDPR review           | Must              |
| Marketing        | Jane Doe     | Go-to-market          | Informed          |
| Support Lead     | Chris Brown  | Support readiness     | Informed          |

**Approval Timeline**:

- Draft PRD: 2024-11-01
- Review period: 5 business days
- Final approval: 2024-11-08
- Kickoff: 2024-11-11
```

## Versioning & Updates

**Best Practice**: PRD is a living document

```markdown
## Change History

| Version | Date       | Author     | Changes                                             |
| ------- | ---------- | ---------- | --------------------------------------------------- |
| 1.0     | 2024-10-30 | Sarah Chen | Initial draft                                       |
| 1.1     | 2024-11-02 | Sarah Chen | Added NFR-10 (Accessibility) based on legal review  |
| 1.2     | 2024-11-05 | Sarah Chen | Reduced scope: Moved budget warnings to Should-Have |
| 2.0     | 2024-11-08 | Sarah Chen | Final approved version                              |

## Status: APPROVED (2024-11-08)
```

## Common Mistakes to Avoid

### Too Technical

```markdown
BAD: "Implement Redis caching with TTL of 3600s"
GOOD: "Dashboard data is cached for fast load time"
```

### Too Vague

```markdown
BAD: "Users should be able to see expenses"
GOOD: "Users see aggregated expenses for 7/30/90 days
with trend graph and top 5 categories"
```

### Missing Prioritization

```markdown
BAD: All features are "important"
GOOD: Clear Must/Should/Nice-to-Have classification with rationale
```

### No Metrics

```markdown
BAD: "Feature will be successful"
GOOD: "Success measured by 60% adoption within 4 weeks"
```

### No Delimitation

```markdown
BAD: Feature list without end
GOOD: Explicit "Out of Scope" section with justification
```

## Checklist: Quality PRD

Verify before finalization:

### Content

- [ ] Executive summary concise (< 5 sentences)
- [ ] Problem clearly defined with evidence
- [ ] Objectives SMART (specific, measurable, achievable)
- [ ] User stories with acceptance criteria
- [ ] Functional requirements prioritized
- [ ] NFRs for performance, security, usability
- [ ] Success metrics with concrete numbers
- [ ] Risks identified with mitigation
- [ ] "Out of Scope" clearly defined

### Format

- [ ] Consistent formatting
- [ ] Hierarchical headings
- [ ] Lists and tables for clarity
- [ ] Mockups/wireframes linked
- [ ] Technical terms explained

### Process

- [ ] Stakeholder input obtained
- [ ] Technical feasibility clarified
- [ ] Design alignment confirmed
- [ ] Legal/compliance review (if required)
- [ ] Approvals documented
- [ ] Versioning implemented

### Quality

- [ ] User-centric (not solution-centric)
- [ ] Understandable for all stakeholders
- [ ] No contradictions
- [ ] Realistic scope
- [ ] Actionable for development team
