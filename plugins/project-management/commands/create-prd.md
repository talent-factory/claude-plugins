---
description: Create a Product Requirements Document (PRD) for a product feature
category: project
argument-hint: "<feature-description> [output-path]"
allowed-tools:
  - Write
  - TodoWrite
  - Read
---

# Claude Command: Create PRD

Create a comprehensive, professional Product Requirements Document (PRD) based on industry best practices.

## Usage

```bash
/project-management:create-prd "Feature description"
/project-management:create-prd "Feature description" /path/to/output.md
```

**Examples**:

```bash
/project-management:create-prd "Add Dark Mode Toggle to settings"
/project-management:create-prd "AI-powered budgeting" docs/prds/budget-ai.md
```

## Workflow

1. **Analyze the Feature Description**
   - Understand scope and complexity
   - Identify project type (Feature, Initiative, Technical)
   - Select appropriate PRD template

2. **Create Structured PRD**
   - Executive Summary (Problem, Solution, Impact)
   - Problem Statement with evidence
   - Measurable objectives and success metrics
   - User Stories with acceptance criteria
   - Functional and non-functional requirements
   - Clear scope boundaries (Out of Scope)
   - Risk assessment with mitigation strategies
   - Timeline and milestones

3. **TodoWrite for Tracking**
   - Use TodoWrite to track PRD sections during creation
   - Ensure completeness

4. **Output**
   - Save PRD at the specified path
   - Default: `PRD.md` in the current directory

## PRD Fundamental Principles

### User-Centered, Not Solution-Centered

**Focus on**:

- **Problem**: What problem are we solving?
- **User**: For whom are we solving it?
- **Impact**: What value are we creating?

**NOT on**:

- Technical implementation
- Specific solution approaches
- Code/architecture details

### SMART Objectives

- **S**pecific: Clearly defined
- **M**easurable: Quantifiable
- **A**chievable: Realistic
- **R**elevant: Important for business/user
- **T**ime-bound: Clear timeframe

### Clear Prioritization

**MoSCoW Method**:

- **Must-Have**: Critical for MVP
- **Should-Have**: Important, not critical
- **Could-Have**: Nice-to-have
- **Won't-Have**: Explicitly excluded

## PRD Structure

### 1. Executive Summary (3-5 sentences)

What, For whom, Why, Impact, Timeline

### 2. Problem Statement

- Current state
- Problem description
- Impact (quantified)
- Evidence (data, research)
- Why now?

### 3. Objectives and Success Metrics

- Product objectives
- Business objectives
- Primary metrics (with baseline and target)
- Secondary metrics
- Guardrail metrics

### 4. User Stories and Personas

- Detailed personas (data-driven)
- User Stories (As X, I want Y so that Z)
- Acceptance criteria (testable)
- Context and rationale

### 5. Functional Requirements

- Ordered by priority (Must/Should/Could/Won't)
- Detailed description
- Acceptance criteria
- Edge cases
- User flows

### 6. Non-Functional Requirements

- Performance (speed, latency)
- Security and Privacy (GDPR, etc.)
- Scalability (growth)
- Usability and Accessibility (WCAG 2.1)
- Reliability (uptime, error rate)

### 7. Scope Boundaries (Out of Scope)

- What will NOT be built
- Rationale for exclusions
- Planned timeline for future features

### 8. Risk Assessment

- Risk matrix (Impact x Likelihood)
- Mitigation strategies
- Contingency plans
- Owner assignment

### 9. Timeline and Milestones

- Phase plan
- Key milestones
- Dependencies
- Approvals

## Template Selection

Based on project complexity:

| Type             | Duration   | Template         |
| ---------------- | ---------- | ---------------- |
| Small Feature    | < 2 weeks  | Minimal MVP      |
| Standard Feature | 4-8 weeks  | Standard Feature |
| Major Initiative | > 2 months | Major Initiative |
| Platform/Infra.  | Variable   | Technical PRD    |

**Details**: [templates.md](../references/create-prd/templates.md)

## Best Practices

**DO**:

- Focus on user needs and business value
- Define measurable, SMART objectives
- Write concrete acceptance criteria
- Include data and evidence
- Address risks proactively
- Communicate clear scope boundaries

**DON'T**:

- Prescribe technical implementation
- Use vague objectives ("more users")
- Include requirements without prioritization
- Add features without rationale
- Ignore out-of-scope items

**Complete Guide**: [best-practices.md](../references/create-prd/best-practices.md)

## Quality Criteria

### Content

- [ ] Executive Summary is concise (< 5 sentences)
- [ ] Problem is clearly defined with evidence
- [ ] Objectives are SMART
- [ ] User Stories include acceptance criteria
- [ ] Requirements are prioritized (Must/Should/Could)
- [ ] NFRs cover Performance, Security, Usability
- [ ] Success metrics include specific numbers
- [ ] Risks are identified with mitigation strategies
- [ ] "Out of Scope" is defined

### Format

- [ ] Consistent formatting
- [ ] Hierarchical structure
- [ ] Lists and tables for clarity
- [ ] Professional language

### Process

- [ ] Complete and actionable
- [ ] Understandable for all stakeholders
- [ ] No contradictions
- [ ] Realistic scope

## Additional Information

- **Best Practices**: [best-practices.md](../references/create-prd/best-practices.md)
  - Fundamental principles
  - Defining success metrics
  - Stakeholder management
  - Avoiding common mistakes

- **Templates**: [templates.md](../references/create-prd/templates.md)
  - Minimal MVP Template
  - Standard Feature Template
  - Major Initiative Template
  - Technical PRD Template

- **Sections Guide**: [sections-guide.md](../references/create-prd/sections-guide.md)
  - Detailed instructions for each section
  - Examples (Good vs. Bad)
  - Common mistakes per section
  - Writing tips

---

**Feature description**: $ARGUMENTS
