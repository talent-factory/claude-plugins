---
name: create-prd
description: >
  Writes a Product Requirements Document (PRD) for a feature: problem, measurable objectives, user
  stories with acceptance criteria, prioritised requirements, scope boundaries and risks. Use when the
  user asks to "create a PRD", "write product requirements", or "specify this feature".
argument-hint: "<feature-description> [output-path]"
allowed-tools:
  - Read
  - Write
---

# Create PRD

Write `PRD.md` (or the given path) for the feature in `$ARGUMENTS`. If the description leaves the problem, the user or the success measure open, ask for them before writing.

## Structure

1. **Executive summary** (3 to 5 sentences): what, for whom, why, expected impact.
2. **Problem**: current state, who is affected, evidence, why now.
3. **Objectives and metrics**: SMART objectives; primary metric with baseline and target; guardrail metrics.
4. **Users and stories**: personas, stories ("As X, I want Y so that Z") with testable acceptance criteria.
5. **Functional requirements**, prioritised Must / Should / Could / Won't, with edge cases.
6. **Non-functional requirements**: performance, security and privacy, scalability, accessibility, reliability. State numbers.
7. **Out of scope**, with the reason for each exclusion.
8. **Risks**: likelihood, impact, mitigation, owner.
9. **Timeline and milestones**, dependencies, approvals.

Scale the document to the work: a change of under two weeks needs the summary, problem, stories, requirements and scope; a platform initiative needs all nine sections.

## Rules

- Describe the problem and the outcome, not the implementation. No architecture or code.
- Every objective has a number and a date; every requirement a priority and a rationale.
- Mark assumptions and open questions explicitly instead of inventing evidence or metrics.
- The next step is `/project-management:create-plan`, which reads this file.
