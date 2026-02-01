# PRD Sections: Detailed Guide

Comprehensive instructions for each section of a PRD with best practices, examples, and common mistakes.

## Executive Summary

### Purpose

Enable busy stakeholders to understand the essence in 30 seconds.

### Structure (3-5 Sentences)

1. **What** is being built?
2. **For whom** is it intended?
3. **Why** is it important?
4. **Expected Impact** (business/user)
5. **When** (timeline)

### Example: Good

```markdown
## Executive Summary

This PRD describes an AI-powered budgeting feature for FinanceApp that provides users with automatic expense categorization and budget suggestions. The primary target audience consists of the 2.5M active users who categorize manually (70% of our user base). The feature addresses the #1 user pain point from recent research and is expected to increase user engagement by 25% and reduce onboarding drop-off by 15%. Launch planned for Q2 2024 following 8-week development.
```

### Example: Poor

```markdown
## Executive Summary

We are building a new feature. It will be cool and users will like it. We are launching soon.
```

### Common Mistakes

- Too long (> 1 paragraph)
- Too vague (no concrete numbers)
- Too technical (implementation details)
- Missing business metrics

---

## Problem Statement

### Purpose

Establish clarity on WHY we are building. All stakeholders must understand the problem.

### Structure

1. **Current State**: What is the situation now?
2. **Problem Description**: What is the problem?
3. **Impact**: Who is affected? To what extent?
4. **Evidence**: Data supporting the problem
5. **Opportunity**: Why address it now?

### Writing Guidelines

**Concrete, not abstract**:

- "Users spend an average of 12 minutes on manual categorization"
- "Categorization is time-consuming"

**Quantified**:

- "45% of users abandon onboarding at the categorization step"
- "Many users abandon onboarding"

**Incorporate user quotes**:

```markdown
"I hate manually categorizing every transaction.
It takes forever!" - Sarah, 32, Freelancer
```

### Template

```markdown
## Problem Statement

### Current State

[Describe status quo neutrally]

Currently, users must manually categorize all transactions.
The app offers no automatic suggestions. New users see
an empty list and must build categories from scratch.

### The Problem

[Identify specific problem]

**For Users**:

- Time-intensive: avg. 12 minutes/day for categorization
- Frustrating: Repetitive, manual work
- Error-prone: 23% incorrect categorizations

**For Business**:

- Onboarding abandonment: 45% abandon at categorization
- Support load: 300 tickets/month related to "categorization"
- Churn risk: 18% of churned users cite "too complicated"

### Evidence

**Quantitative Data**:

- Analytics: Only 30% use categorization regularly
- Time-on-task: avg. 12 min. for 20 transactions
- Error rate: 23% require re-categorization

**Qualitative Research**:

- User interviews (n=50): 94% desire auto-categorization
- Support feedback: "Categorization" is #1 complaint
- NPS comments: 67 negative mentions (last 3 months)

**Competitive Analysis**:

- 5/5 top competitors have auto-categorization
- Market standard since 2022
- Users expect this feature

### Why Now?

**Strategic Timing**:

- Q2 marketing campaign: 500k new users expected
- Onboarding optimization is Q1 OKR
- Competitor X launches similar feature Q3

**Technical Readiness**:

- ML model already trained (accuracy: 89%)
- Infrastructure available
- Design system has components

**Business Impact**:

- Projected revenue impact: +EUR 250k/year (15% churn reduction)
- ROI: Break-even after 4 months
```

### Common Mistakes

- Describing solution instead of problem
- No data to substantiate claims
- Problem too small (not worth building)
- Problem too large (not solvable)

---

## Objectives & Success Metrics

### Purpose

Define how we measure success. Foundation for post-launch review.

### SMART Objectives

- **S**pecific: Clear what is being measured
- **M**easurable: Quantifiable
- **A**chievable: Realistic
- **R**elevant: Important for business/user
- **T**ime-bound: Clear timeframe

### Structure

````markdown
## Objectives & Success Metrics

### Product Objectives

1. **Improve User Engagement**
   - More users utilize categorization regularly
   - Longer session duration in app
   - Higher feature discovery

2. **Optimize Onboarding Experience**
   - Faster onboarding
   - Fewer abandonments
   - Better first-time UX

3. **Reduce Support Load**
   - Fewer support tickets
   - Increase self-service rate

### Business Objectives

- **Revenue**: Churn reduction - +EUR 250k ARR
- **Costs**: Reduce support costs by EUR 50k/year
- **Growth**: Increase onboarding completion rate

### Success Metrics

#### Primary Metrics (Launch + 4 Weeks)

| Metric                      | Description                            | Baseline     | Target   | Measurement            |
| --------------------------- | -------------------------------------- | ------------ | -------- | ---------------------- |
| **Feature Adoption**        | % users activating auto-categorization | 0%           | 60%      | Analytics Event        |
| **Categorization Accuracy** | % correctly categorized transactions   | 77% (manual) | 85%      | User Confirmation Rate |
| **Time-to-Categorize**      | avg. time for 20 transactions          | 12 min.      | < 2 min. | Event Timing           |

#### Secondary Metrics (Launch + 8 Weeks)

| Metric                    | Description                         | Baseline  | Target      | Measurement     |
| ------------------------- | ----------------------------------- | --------- | ----------- | --------------- |
| **Onboarding Completion** | % completing onboarding             | 55%       | 70%         | Funnel Analysis |
| **Support Tickets**       | Tickets related to "categorization" | 300/month | < 150/month | Zendesk Tags    |
| **NPS Impact**            | NPS score improvement               | 35        | 40+         | In-App Survey   |
| **Daily Active Users**    | % DAU using feature                 | N/A       | 40%         | Analytics       |

#### Guardrail Metrics

Metrics that must NOT be negatively impacted:

- Performance: App load time remains < 3s
- Accuracy: Categorization errors not > 20%
- Privacy: No user complaints about data usage

### Tracking Plan

**Analytics Events**:

```javascript
// Feature Activation
track("auto_categorization_enabled", {
  user_id: string,
  timestamp: datetime,
});

// Categorization
track("transaction_auto_categorized", {
  transaction_id: string,
  category: string,
  confidence: float,
  user_confirmed: boolean,
});

// Corrections
track("category_corrected", {
  transaction_id: string,
  old_category: string,
  new_category: string,
});
```
````

**Dashboard**: Link to Mixpanel Dashboard

**Review Schedule**:

- Week 1: Daily review (PM)
- Week 2-4: Weekly review (PM + Eng Lead)
- Week 8: Comprehensive post-mortem (all stakeholders)

````

### Common Mistakes

- Vague objectives ("more users")
- Too many metrics (loss of focus)
- Non-measurable objectives ("happier users")
- No baseline for comparison
- Unrealistic targets

---

## User Stories & Personas

### Purpose

Create empathy for users. Team understands WHO uses WHAT and WHY.

### Creating Personas

**Based on actual data**:

- User research
- Analytics segmentation
- Support feedback
- Sales/CS input

### Persona Template

```markdown
## Primary Personas

### Persona 1: "Budget-Conscious Sarah"

![Persona Image or Icon]

**Demographics**:
- Age: 28-35
- Occupation: Freelancer, knowledge work
- Income: EUR 3,000-4,500/month (variable)
- Tech-savviness: High
- Location: Urban, Germany

**Context & Behavior**:
- Uses 5+ finance apps
- Checks finances daily (routine)
- Prioritizes automation
- Mobile-first user (80% mobile)

**Pain Points**:
1. "I don't have time for manual work"
2. "I need a quick overview"
3. "Categorization is repetitive and annoying"

**Goals with App**:
- Automatic financial overview
- Low maintenance
- Insights without effort

**Quote**:
> "I want to quickly check in the morning with my coffee
> whether I'm on track. Not spend 10 minutes categorizing transactions."

**How to Measure Success for Sarah?**:
- Time-to-insight < 30 seconds
- Daily app usage
- High NPS score

**Segment Size**: 40% of our user base (~1M users)
````

### User Story Format

```markdown
## User Stories

### Epic 1: Automatic Categorization

#### US-1.1: First Automatic Categorization

**Priority**: Must-Have
**Story Points**: 5
**Sprint**: 1

**As** Budget-conscious Sarah
**I want** my transactions to be automatically categorized
**So that** I don't waste time on manual categorization

**Context**:

- Sarah has 20-30 new transactions per week
- Currently spends 12 min./week on categorization
- She checks the app daily in the morning (8-9 AM)

**Acceptance Criteria**:

- [ ] New transactions are auto-categorized within 1 hour
- [ ] Categorization accuracy >= 85% (based on user corrections)
- [ ] User sees confidence level (High/Medium/Low)
- [ ] User can correct category with 1 tap
- [ ] Correction improves future predictions (ML feedback loop)

**User Flow**:

1. Sarah opens app in the morning
2. Sees new transactions with auto-categories
3. Review:
   - Correct - No action
   - Incorrect - Tap category - Select new - Confirm
4. Dashboard shows updated figures

**Edge Cases**:

- **New Merchant**: If merchant unknown - "Low Confidence"
- **Ambiguous**: e.g., "Amazon" (Shopping or Cloud) - Ask user
- **Offline**: Categorization occurs when online

**Dependencies**:

- ML model deployed (ML Team, Sprint 0)
- Transaction API updated (Backend, Sprint 1)
- UI components complete (Design, Sprint 0)

**Mockups**: [Link to Figma]

**Definition of Done**:

- [ ] Code reviewed & merged
- [ ] Unit tests (coverage >= 80%)
- [ ] QA testing passed
- [ ] Analytics events implemented
- [ ] Documentation updated
- [ ] Deployed to production
```

### Common Mistakes

- Personas based on intuition, not data
- User stories without acceptance criteria
- Too technical user stories ("As a system")
- Missing context/rationale
- No prioritization

---

## Functional Requirements

### Purpose

Describe WHAT is being built (not HOW).

### Structure by MoSCoW

- **M**ust-Have: Essential
- **S**hould-Have: Important, but not critical
- **C**ould-Have: Nice-to-Have
- **W**on't-Have: Explicitly excluded

### Template

```markdown
## Functional Requirements

### Must-Have (MVP - Launch Cannot Proceed Without)

#### FR-1: Automatic Categorization of New Transactions

**Description**:
System automatically categorizes new transactions based on ML model trained on historical data and user corrections.

**Functional Details**:

- Categorization occurs within 1 hour of transaction import
- 15 predefined categories (see Appendix A)
- Confidence level displayed: High (>90%), Medium (70-90%), Low (<70%)
- User can change category with 1-tap correction
- Correction feeds into training data (feedback loop)

**Behavior**:

| Scenario                 | System Behavior                          |
| ------------------------ | ---------------------------------------- |
| Known merchant           | Auto-categorize with "High" confidence   |
| Similar merchant         | Auto-categorize with "Medium" confidence |
| New merchant             | Best-guess with "Low" confidence         |
| Ambiguous (e.g., Amazon) | Ask user on first occurrence             |

**Edge Cases**:

1. **Split Transactions**: When user creates split, original category is transferred to splits

2. **Bulk Correction**: User changes category for merchant - System asks "Change all previous transactions too?"

3. **Offline Mode**: Transactions are cached and categorized when online

**User Interface**:
```

+-----------------------------+
| New Transactions |
| |
| Edeka Supermarket |
| Groceries (High) |
| -42.50 EUR |
| |
| ? Amazon.de |
| Shopping (Medium) |
| -89.99 EUR |
| [Category correct?] |
+-----------------------------+

```

**Acceptance Criteria**:
- [ ] New transactions are auto-categorized
- [ ] Confidence level is displayed
- [ ] User can correct with max. 2 taps
- [ ] Correction improves model (verified via testing)
- [ ] Works on iOS & Android
- [ ] Load time < 2 seconds

**Non-Goals (for this FR)**:
- Custom user categories (deferred to Should-Have)
- Sub-categories (future)
- Rule-based categorization (ML only)

**Dependencies**:
- ML model deployed & accessible via API
- Transaction import functional
- Category master data defined

**Test Strategy**:
- Unit tests: Model prediction logic
- Integration: API end-to-end
- E2E: User corrects category - Next transaction from same merchant correct
- Performance: 1000 transactions < 5s

**Mockups**: [Figma Link]

#### FR-2: Category Correction

[...]

### Should-Have (Post-MVP, before end of Q2)

#### FR-5: Custom User Categories

**Description**: Users can create their own categories

**Rationale for Should-Have**:
- Not critical for MVP
- 35% user request (not majority)
- Increases complexity (testing, migration)
- Can be added post-launch

[Details...]

### Could-Have (Backlog, re-evaluate post-launch)

#### FR-8: Category Rules

**Description**: User defines rule "All transactions from X - Category Y"

**Rationale for Could-Have**:
- Only 12% user request
- High implementation effort
- ML model should learn from corrections anyway
- Evaluate if needed based on post-launch feedback

### Won't-Have (Explicitly Excluded)

#### Sub-Categories

**Rationale**: Too complex for MVP, user research shows low value (8% request)

#### Auto-Tagging

**Rationale**: Separate feature, own PRD in Q3
```

### Common Mistakes

- Too technical ("Use Redis cache")
- No priority justification
- Unclear acceptance criteria
- Missing edge cases
- No user perspective

---

## Non-Functional Requirements (NFRs)

### Purpose

Define quality attributes: How good must it be?

### Categories

1. **Performance**: Speed, latency
2. **Scalability**: Growth, load
3. **Security**: Security, privacy
4. **Reliability**: Uptime, error rate
5. **Usability**: User-friendliness
6. **Accessibility**: Barrier-free access
7. **Maintainability**: Maintenance (for dev team)

### Template

```markdown
## Non-Functional Requirements

### Performance

**NFR-1: Response Time**

- **Requirement**: 95% of API requests < 500ms
- **Rationale**: Users expect immediate response, mobile-first
- **Measurement**: APM (Application Performance Monitoring)
- **Testing**: Load tests with 1000 concurrent users

**NFR-2: UI Responsiveness**

- **Requirement**: Time-to-interactive < 2 seconds
- **Rationale**: Mobile 3G connection minimum standard
- **Measurement**: Lighthouse Performance Score > 90
- **Testing**: Real device testing, throttled network

### Scalability

**NFR-3: User Load**

- **Requirement**: System functions at 100k DAU
- **Current**: 50k DAU
- **Growth**: +50k expected in Q2
- **Testing**: Load tests, stress tests

**NFR-4: Data Volume**

- **Requirement**: Performant with 1M+ transactions per user
- **Rationale**: Power users with multi-year data
- **Testing**: Test with production data samples

### Security & Privacy

**NFR-5: Data Encryption**

- **Requirement**: All PII encrypted at rest (AES-256)
- **Compliance**: GDPR, PCI-DSS (if applicable)
- **Audit**: Penetration testing before launch

**NFR-6: GDPR Compliance**

- **Requirement**: User can export & delete data
- **Timeline**: Must be ready at launch (legal requirement)
- **Validation**: Legal review

**NFR-7: ML Model Privacy**

- **Requirement**: Model training only with anonymized data
- **Rationale**: Privacy-first, no user identifiables
- **Validation**: Privacy impact assessment

### Reliability

**NFR-8: Availability**

- **Requirement**: 99.9% uptime (< 43 min. downtime/month)
- **Rationale**: Finance app, users check daily
- **Monitoring**: Uptime Robot, PagerDuty

**NFR-9: Error Rate**

- **Requirement**: < 0.1% error rate for categorization
- **Rationale**: Trust in auto-categorization is critical
- **Monitoring**: Sentry, error tracking

**NFR-10: Data Loss Prevention**

- **Requirement**: Zero data loss
- **Strategy**: Backups, redundancy
- **RTO/RPO**: Recovery time < 1h, recovery point < 5 min.

### Usability

**NFR-11: Intuitive UI**

- **Requirement**: 90% of users understand feature without onboarding
- **Validation**: Usability testing (n >= 10)
- **Metrics**: Task success rate, time-on-task

**NFR-12: Error Messages**

- **Requirement**: Errors clearly communicated with recommended action
- **Example**: "Categorization failed. Please check your internet connection."
- **Validation**: Review with UX writer

### Accessibility

**NFR-13: WCAG 2.1 Compliance**

- **Requirement**: Level AA compliant
- **Rationale**: Inclusive design, legal in some markets
- **Testing**:
  - Automated: axe DevTools, Lighthouse
  - Manual: Screen reader testing (NVDA, VoiceOver)

**NFR-14: Keyboard Navigation**

- **Requirement**: All functions accessible via keyboard
- **Testing**: Manual keyboard-only testing

**NFR-15: Color Contrast**

- **Requirement**: Min. 4.5:1 for text, 3:1 for UI components
- **Tool**: Color Contrast Analyzer

### Maintainability

**NFR-16: Code Quality**

- **Requirement**: Test coverage >= 80%
- **Rationale**: Feature will be iterated, tests protect
- **Enforcement**: CI/CD pipeline checks

**NFR-17: Documentation**

- **Requirement**: API documented, Architecture Decision Records
- **Rationale**: Team scaling, knowledge transfer
- **Format**: OpenAPI Spec, ADRs in repo
```

### Common Mistakes

- Vague requirements ("must be fast")
- No measurable targets
- Unrealistic requirements
- NFRs forgotten (focus only on functionality)

---

## Out of Scope / Delimitation

### Purpose

Manage expectations. Clearly communicate what will NOT be built.

### Template

```markdown
## Delimitation (Out of Scope)

### Not in This Release

| Feature                    | Rationale                                  | Planned For     |
| -------------------------- | ------------------------------------------ | --------------- |
| **Custom User Categories** | Increases MVP complexity, only 35% request | Q2 post-launch  |
| **Sub-Categories**         | Low user value (8% request)                | Q3 if validated |
| **Bulk Edit**              | Nice-to-have, not critical                 | Backlog         |
| **ML Model Self-Learning** | Technically complex, separate initiative   | Q4 tech roadmap |

### Explicitly Excluded

- **Automatic Tagging**: Separate PRD, Q3 feature
- **Budget Integration**: Out of scope for categorization
- **Multi-Currency**: Already available, not part of this PRD
- **Historical Data Migration**: User data remains as is

**Rationale**: Focus on core feature (auto-categorization). MVP approach for rapid launch & user feedback.

### Delimitation from Other Projects

- **"Budget Alerts" PRD**: Uses categories, but separate initiative
- **"Reports V2" PRD**: Displays categories, but not part of this PRD

### Future Considerations

Features that MAY come later:

- **AI-Suggested Categories**: ML suggests new categories
- **Category Marketplace**: Users share category sets
- **Family Categories**: Shared categories for partners

**Decision**: Re-evaluate after launch based on:

- User feedback & feature requests
- Usage analytics
- Business priorities
```

### Common Mistakes

- Out-of-scope not documented
- Scope creep during development
- No rationale for exclusion
- Unclear future plans

---

## Risk Assessment

### Purpose

Proactively identify problems and plan mitigation.

### Risk Matrix

```
           Impact
         |  Low  | Medium |  High  |
---------+-------+--------+--------+
High     |       |        |        | Priority
Likelihood       |        |        |
Medium   |       |        |        |
         |       |        |        |
Low      |       |        |        |
```

### Template

```markdown
## Risk Assessment

### Risk Matrix

| ID  | Risk                 | Impact | Likelihood | Priority | Owner      |
| --- | -------------------- | ------ | ---------- | -------- | ---------- |
| R-1 | ML accuracy too low  | High   | Medium     | High     | ML Lead    |
| R-2 | Performance at scale | Medium | Low        | Low      | Eng Lead   |
| R-3 | Privacy concerns     | High   | Low        | Medium   | PM + Legal |

### Detailed Risk Analysis

#### R-1: ML Model Accuracy Below Target (High Priority)

**Risk Description**:
ML model does not achieve the target 85% accuracy in production.
Model was trained with synthetic data and may perform worse with real user data.

**Impact**: High

- User trust in auto-categorization decreases
- More manual corrections - poor UX
- Negative NPS, potentially churn
- Feature adoption < target

**Likelihood**: Medium

- Model in testing: 89% accuracy
- But: Test data != production data
- New merchants/edge cases in production

**Mitigation Strategy** (Proactive):

1. **Pre-Launch**:
   - [ ] Test with production data sample (anonymized)
   - [ ] A/B test: 10% user beta (2 weeks before launch)
   - [ ] Calibrate confidence thresholds

2. **Launch**:
   - [ ] Phased rollout: 1% - 10% - 50% - 100%
   - [ ] Real-time model monitoring (accuracy, confidence distribution)
   - [ ] Weekly model retraining with user corrections

3. **Post-Launch**:
   - [ ] User feedback loop: "Was this categorization helpful?"
   - [ ] Manual review of low-confidence predictions
   - [ ] Continuous model improvement

**Contingency Plan** (If it occurs):

- **Trigger**: Accuracy < 80% for 3 consecutive days
- **Action**:
  1. Feature flag OFF for new users (existing can continue)
  2. Emergency model retraining with production data
  3. Bring in ML expert for deep dive
  4. Communication: Transparent with users ("We are still improving")
- **Timeline**: 5 days for fix
- **Rollback**: If not fixable in 1 week - Rollback, re-plan

**Owner**: ML Lead (Primary), PM (Secondary)

**Status**: Mitigation in progress (pre-launch testing underway)

---

#### R-2: Performance Degradation at High Scale (Low Priority)

**Risk**: System slow at 100k+ concurrent categorization requests

**Impact**: Medium

- User experience suffers (slow categorization)
- Potentially timeouts
- Negative impact on NFR-1 (response time)

**Likelihood**: Low

- Load tests show performance OK up to 150k users
- Current: 50k DAU, growth to 100k takes 6+ months
- Time for scaling if needed

**Mitigation**:

- Load tests in CI/CD
- Auto-scaling configured
- Performance monitoring (APM)
- Fallback: Async categorization if load high

**Owner**: Engineering Lead

---

#### R-3: Privacy/GDPR Concerns (Medium Priority)

**Risk**: Users concerned about data usage for ML training

**Impact**: High (if it occurs)

- PR problem
- Trust loss
- Potentially legal issues

**Likelihood**: Low

- Privacy impact assessment completed
- Legal sign-off obtained
- Transparently communicated in privacy policy

**Mitigation**:

- Privacy notice before feature activation
- Opt-out option available
- Model training only with anonymized data
- Clear communication in UI

**Owner**: PM + Legal Lead

### Risk Review Schedule

- **Pre-Launch**: Weekly risk review (PM, Eng Lead, ML Lead)
- **Launch Week**: Daily monitoring
- **Post-Launch**: Bi-weekly review until metrics stable
```

### Common Mistakes

- Risks not documented
- No mitigation plans
- Unrealistic risk assessment
- No owner assigned
- No contingency plans

---

## Additional Important Sections

### Timeline & Milestones

- Realistic time estimates
- Include buffer (15-20%)
- Consider dependencies
- Clearly defined milestones

### Appendix

- Mockups/wireframes
- Technical specs (links)
- Research reports (links)
- Competitive analysis
- Glossary for technical terms

### Approval & Sign-off

- All stakeholders listed
- Clear approval process
- Timeline for reviews
- Documented approvals
