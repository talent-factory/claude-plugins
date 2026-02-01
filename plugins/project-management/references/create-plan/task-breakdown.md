# Task Breakdown Strategies

Comprehensive guide for decomposing PRD requirements into atomic, actionable tasks.

## Fundamental Principles

### What Constitutes a "Good" Task?

A good task fulfills the **ATOMIC** criteria:

- **A**ctionable: Immediately implementable without further clarification
- **T**estable: Clear acceptance criteria
- **O**wnable: Assignable to one person/agent
- **M**easurable: Progress measurable (story points)
- **I**ndependent: Minimally dependent on other tasks
- **C**omplete: Self-contained

### Task Size

**Ideal Size**: 2-5 story points (1-2 days of work)

| Story Points | Description            | Example                          |
| ------------ | ---------------------- | -------------------------------- |
| **1**        | Trivial, < 2h          | Config change, typo fix          |
| **2**        | Simple, 2-4h           | Simple CRUD, CSS adjustment      |
| **3**        | Standard, 4-8h         | Feature with few edge cases      |
| **5**        | Complex, 1-2 days      | Feature with multiple edge cases |
| **8**        | Very complex, 2-3 days | Large feature, many dependencies |
| **13+**      | **TOO LARGE!**         | Decompose into smaller tasks     |

**Rule of thumb**: Tasks > 8 SP should be decomposed.

## Breakdown Strategies

### 1. From Functional Requirements

**PRD Section**: Functional Requirements (MoSCoW-prioritized)

#### Strategy

Each requirement is decomposed into **1-N tasks**:

**Example Requirement**:

> **Must-Have**: User can toggle Dark Mode in Settings

**Breakdown**:

1. **UI Toggle Component** (3 SP)
   - Toggle switch in Settings page
   - Visual feedback on toggle
   - Accessibility (ARIA labels)

2. **Theme State Management** (5 SP)
   - Store state (Context/Redux)
   - Implement theme provider
   - Propagate theme changes

3. **CSS Variables Setup** (2 SP)
   - Define CSS variables for Light/Dark
   - Convert all components to use variables
   - Theme-specific styles

4. **Local Storage Persistence** (2 SP)
   - Save theme preference
   - Restore on load
   - Fallback to system theme

#### Mapping to Tasks

```typescript
function breakdownFunctionalRequirement(requirement) {
  const tasks = [];

  // Pattern 1: UI Component Task
  if (requirement.hasUI) {
    tasks.push({
      title: `Implement ${requirement.name} UI Component`,
      type: "frontend",
      estimate: estimateUIComplexity(requirement),
      labels: ["feature", "ui"],
      agent: "react-developer",
    });
  }

  // Pattern 2: Backend Logic Task
  if (requirement.hasBackendLogic) {
    tasks.push({
      title: `Implement ${requirement.name} Backend Logic`,
      type: "backend",
      estimate: estimateBackendComplexity(requirement),
      labels: ["feature", "backend"],
      agent: "java-developer" || "python-expert",
    });
  }

  // Pattern 3: State Management Task
  if (requirement.hasStateManagement) {
    tasks.push({
      title: `Implement ${requirement.name} State Management`,
      type: "state",
      estimate: 3,
      labels: ["feature", "state-management"],
      agent: "react-developer",
    });
  }

  // Pattern 4: Persistence Task
  if (requirement.hasPersistence) {
    tasks.push({
      title: `Implement ${requirement.name} Persistence`,
      type: "persistence",
      estimate: 2,
      labels: ["feature", "database"],
      agent: "java-developer",
    });
  }

  return tasks;
}
```

### 2. From Non-Functional Requirements

**PRD Section**: Non-Functional Requirements (NFRs)

#### Performance Tasks

**Example NFR**:

> **Performance**: Page must load in < 2s

**Breakdown**:

1. **Performance Baseline** (2 SP)
   - Measure current load time
   - Identify bottlenecks
   - Generate Lighthouse report

2. **Code Splitting** (5 SP)
   - Implement lazy loading
   - Route-based code splitting
   - Optimize bundle size

3. **Image Optimization** (3 SP)
   - Responsive images
   - WebP format
   - Lazy loading

4. **Caching Strategy** (5 SP)
   - Service worker
   - HTTP caching
   - LocalStorage/IndexedDB

#### Security Tasks

**Example NFR**:

> **Security**: OWASP Top 10 Compliance

**Breakdown**:

1. **Security Audit** (3 SP)
   - OWASP Top 10 check
   - Dependency audit
   - Security scan (SAST)

2. **Input Validation** (5 SP)
   - XSS prevention
   - SQL injection prevention
   - CSRF protection

3. **Authentication Hardening** (8 SP)
   - Password policy
   - MFA implementation
   - Session management

4. **Security Testing** (5 SP)
   - Penetration testing
   - Security unit tests
   - Vulnerability scanning

#### Accessibility Tasks

**Example NFR**:

> **Accessibility**: WCAG 2.1 Level AA

**Breakdown**:

1. **Accessibility Audit** (2 SP)
   - Axe/Lighthouse scan
   - Keyboard navigation test
   - Screen reader test

2. **Semantic HTML** (3 SP)
   - ARIA labels
   - Heading hierarchy
   - Landmark regions

3. **Keyboard Navigation** (3 SP)
   - Optimize tab order
   - Focus states
   - Skip links

4. **Accessibility Testing** (3 SP)
   - Automated tests (axe-core)
   - Manual testing
   - Screen reader testing

### 3. Cross-Cutting Concerns

Tasks relevant across multiple features:

#### Testing

**Breakdown**:

1. **Unit Tests** (3 SP per feature)
   - Component tests
   - Function tests
   - Edge cases

2. **Integration Tests** (5 SP per feature)
   - API integration
   - Component integration
   - E2E happy path

3. **E2E Tests** (5 SP)
   - User flows
   - Critical paths
   - Cross-browser

#### Documentation

**Breakdown**:

1. **Code Documentation** (2 SP)
   - JSDoc/JavaDoc
   - README updates
   - Architecture docs

2. **User Documentation** (3 SP)
   - User guide
   - Tutorials
   - FAQ

3. **API Documentation** (3 SP)
   - OpenAPI/Swagger
   - Endpoint descriptions
   - Example requests

#### DevOps/Infrastructure

**Breakdown**:

1. **CI/CD Pipeline** (5 SP)
   - Build pipeline
   - Test integration
   - Deployment automation

2. **Monitoring and Observability** (5 SP)
   - Logging setup
   - Metrics collection
   - Alerting

3. **Infrastructure as Code** (8 SP)
   - Terraform/CloudFormation
   - Environment setup
   - Configuration management

## Dependency Management

### Dependency Types

**Blocking**: Task A must complete before Task B can start
**Related**: Tasks share code/context
**Sequential**: Logical ordering

### Dependency Mapping

```typescript
// Example: Dark Mode Feature
const tasks = [
  {
    id: "T1",
    title: "CSS Variables Setup",
    dependencies: [], // No dependencies
  },
  {
    id: "T2",
    title: "Theme State Management",
    dependencies: ["T1"], // Blocked by T1
  },
  {
    id: "T3",
    title: "UI Toggle Component",
    dependencies: ["T2"], // Blocked by T2
  },
  {
    id: "T4",
    title: "Local Storage Persistence",
    dependencies: ["T2"], // Blocked by T2
  },
  {
    id: "T5",
    title: "Unit Tests",
    dependencies: ["T3", "T4"], // Blocked by T3 and T4
  },
];

// Visualization:
//     T1
//     ↓
//     T2
//    ↙ ↘
//  T3   T4
//    ↘ ↙
//     T5
```

### Minimizing Dependencies

**DO**:

- Design tasks as independently as possible
- Define interfaces/contracts early
- Enable parallel work

**DON'T**:

- Long dependency chains (> 3 levels)
- Circular dependencies
- Unnecessary dependencies

## Story Point Estimation

### Estimation Factors

**Complexity**:

- Number of edge cases
- Algorithm complexity
- New vs. familiar technology

**Uncertainty**:

- Clear requirements?
- Familiar codebase?
- Familiar tools/frameworks?

**Effort**:

- Coding effort
- Testing effort
- Review effort
- Documentation effort

### Planning Poker

Team-based estimation:

1. **Present task**: PO explains task
2. **Clarify questions**: Team asks questions
3. **Private estimation**: Each person selects story points
4. **Simultaneous reveal**: All show estimates
5. **Discuss**: When there are large differences
6. **Reach consensus**: Team agrees

### Estimation Examples

#### Example 1: Simple CRUD

**Task**: "User can edit profile"

**Analysis**:

- Known pattern (CRUD)
- Clear requirements
- Few edge cases

**Estimation**: **3 SP**

#### Example 2: Complex Authentication

**Task**: "Implement MFA with TOTP"

**Analysis**:

- New technology (TOTP)
- Security-critical
- Many edge cases (device lost, backup codes)

**Estimation**: **8 SP**

#### Example 3: Performance Optimization

**Task**: "Reduce page load time by 50%"

**Analysis**:

- Unclear requirements (where to optimize?)
- High uncertainty
- Many potential bottlenecks

**Estimation**: **13 SP** → **TOO LARGE, DECOMPOSE!**

**Better Breakdown**:

1. Performance baseline (2 SP)
2. Bottleneck analysis (3 SP)
3. Specific optimizations (3-5 SP each)

## Task Templates

### Feature Task Template

```markdown
## Task: [Feature-Name]

### Description

[Brief description of the functionality]

### Acceptance Criteria

- [ ] Criterion 1 (testable, measurable)
- [ ] Criterion 2
- [ ] Criterion 3

### Technical Notes

- Implementation details
- API endpoints
- Database schema

### Edge Cases

- Edge case 1
- Edge case 2

### Testing Requirements

- Unit tests: [What to test?]
- Integration tests: [What to test?]
- E2E tests: [Which flows?]

### Dependencies

- Depends on: [Task-IDs]
- Blocks: [Task-IDs]

### Agent Recommendation

- **Agent**: [agent-name]
- **Rationale**: [Why this agent?]

### Estimate

**Story Points**: [1, 2, 3, 5, 8]
```

### Bug Task Template

```markdown
## Task: Fix [Bug-Name]

### Description

[What is broken?]

### Steps to Reproduce

1. Step 1
2. Step 2
3. Observe error

### Expected Behavior

[What should happen?]

### Actual Behavior

[What actually happens?]

### Root Cause

[Cause of the bug]

### Fix Description

[How will it be fixed?]

### Testing Requirements

- Unit tests: [New tests?]
- Regression tests: [Which flows to retest?]

### Estimate

**Story Points**: [1, 2, 3]
```

### Documentation Task Template

```markdown
## Task: Document [Feature-Name]

### Description

[What should be documented?]

### Documentation Scope

- [ ] User guide
- [ ] API documentation
- [ ] Architecture docs
- [ ] Code comments

### Target Audience

[Developers, users, admin, etc.]

### Deliverables

- File 1: [Path]
- File 2: [Path]

### Estimate

**Story Points**: [2, 3]
```

## Common Errors

### Tasks Too Large

**Problem**: Tasks > 8 SP

**Example**:

> "Implement user authentication system" (21 SP)

**Solution**: Decompose into:

1. User registration (5 SP)
2. Login/logout (3 SP)
3. Password reset (3 SP)
4. Session management (5 SP)
5. MFA (8 SP)

### Vague Descriptions

**Problem**: Unclear requirements

**Incorrect**:

> "Improve performance"

**Correct**:

> "Reduce page load time from 5s to < 2s through code splitting and image optimization"

### Missing Acceptance Criteria

**Problem**: Not testable

**Incorrect**:

> "Implement dark mode"

**Correct**:

> "Implement dark mode"
>
> - [ ] Toggle present in Settings
> - [ ] Theme changes on toggle
> - [ ] Preference saved in LocalStorage
> - [ ] Theme restored on load

### Ignoring Dependencies

**Problem**: Tasks in wrong order

**Example**:

- Task 1: "Implement E2E tests"
- Task 2: "Implement feature"

**Problem**: E2E tests cannot be implemented before the feature!

**Solution**: Make dependencies explicit:

- Task 1: "Implement feature"
- Task 2: "Implement E2E tests" (depends on Task 1)

## Best Practices

### DO

**Atomic Tasks**:

- One logical unit per task
- 2-5 SP ideal
- Self-contained

**Clear Descriptions**:

- What should be built?
- Why is it being built?
- How is success measured?

**Testable Acceptance Criteria**:

- Measurable and verifiable
- Checkbox format
- No interpretation needed

**Realistic Estimates**:

- Use planning poker
- Consider historical data
- When uncertain: estimate higher

**Document Dependencies**:

- Identify blocking tasks
- Enable parallel work
- Visualize (graph)

### DON'T

**Tasks Too Large**:

- > 8 SP should be decomposed
- Multiple logical units should be decomposed

**Vague Requirements**:

- No clear acceptance criteria
- Interpretation needed
- Scope creep possible

**Ignore Constraints**:

- Forget NFRs
- Omit cross-cutting concerns
- Treat testing as afterthought

**Unrealistic Estimates**:

- Too optimistic
- Ignore dependencies
- Underestimate testing effort

## Checklist: Is My Task Good?

Before creating a task in Linear:

- [ ] **Atomic**: One logical unit?
- [ ] **Actionable**: Immediately implementable?
- [ ] **Testable**: Acceptance criteria defined?
- [ ] **Ownable**: Assignable to one person?
- [ ] **Measurable**: Estimate provided (2-8 SP)?
- [ ] **Independent**: Minimally dependent?
- [ ] **Complete**: Self-contained?
- [ ] **Described**: Full description?
- [ ] **Agent-Mapped**: Recommended agent specified?
- [ ] **Labeled**: Labels for categorization?

If **all points** are checked: Task is ready!

---

**See also**:

- [linear-integration.md](linear-integration.md) - Linear API details
- [agent-mapping.md](agent-mapping.md) - Agent recommendations
- [best-practices.md](best-practices.md) - General best practices
