# Best Practices for Project Planning

Comprehensive guide for professional project planning with PRD-based task management in Linear.

## Fundamental Principles

### 1. PRD-Centric Planning

**Always derive from the PRD**:

- PRD as single source of truth
- All tasks derivable from PRD
- Complete PRD analysis before task creation
- PRD link in EPIC description

**DON'T**:

- Tasks without PRD reference
- Ad-hoc tasks without context
- Ignore feature creep

### 2. Consistency Above All

**Consistency checks before saving**:

- [ ] No duplicates
- [ ] No redundancies
- [ ] No contradictory overall picture
- [ ] Logical prioritization
- [ ] Correct dependencies

**DON'T**:

- Populate Linear without duplicate check
- Inconsistent priorities
- Contradictory requirements

### 3. Actionable Above All

**Every task must be implementable**:

- Clear description
- Unambiguous acceptance criteria
- No open questions
- All information provided

**DON'T**:

- Vague tasks ("Improve performance")
- Tasks requiring interpretation
- Missing acceptance criteria

## Workflow Best Practices

### PRD Analysis

**1. Read completely**:

```markdown
- [ ] Executive summary understood
- [ ] Problem statement clear
- [ ] Goals and metrics defined
- [ ] User stories reviewed
- [ ] Functional requirements (Must/Should/Could)
- [ ] Non-functional requirements
- [ ] Out of scope understood
- [ ] Risks identified
- [ ] Timeline realistic
```

**2. Group requirements**:

```typescript
const requirements = {
  mustHave: extractRequirements(prd, "must"),
  shouldHave: extractRequirements(prd, "should"),
  couldHave: extractRequirements(prd, "could"),
  wontHave: extractRequirements(prd, "won't"),
};
```

**3. Extract NFRs**:

```typescript
const nfrs = {
  performance: extractNFRs(prd, "performance"),
  security: extractNFRs(prd, "security"),
  scalability: extractNFRs(prd, "scalability"),
  usability: extractNFRs(prd, "usability"),
  accessibility: extractNFRs(prd, "accessibility"),
};
```

### EPIC Creation

**Best Practices**:

**DO**:

```yaml
EPIC:
  Title: "[Feature-Name]" (< 50 chars, descriptive)
  Description: |
    ## Executive Summary
    [3-5 sentences from PRD]

    ## Business Value
    - Why is this being built?
    - What impact does it have?
    - For whom is it important?

    ## Success Metrics
    - Metric 1: [Baseline → Target]
    - Metric 2: [Baseline → Target]

    ## Timeline
    - Phase 1: [Milestone]
    - Phase 2: [Milestone]

    ## Full PRD
    Link: [PRD path or URL]

  Status: planned
  Priority: high (based on Must-Have %)
  Labels: [epic, feature, tech-stack]
```

**DON'T**:

```yaml
EPIC:
  Title: "Feature" # Too vague
  Description: "Build feature X" # Too brief
  Status: in_progress # Not yet started!
  Priority: urgent # Everything is urgent → nothing is urgent
```

### Task Creation

**Best Practices**:

**DO**:

```markdown
Task: "[Concise Title]" (< 60 chars)

## Description

[Complete description: What, Why, How]

## Acceptance Criteria

- [ ] Criterion 1 (testable, measurable)
- [ ] Criterion 2 (testable, measurable)
- [ ] Criterion 3 (testable, measurable)

## Technical Notes

- Implementation details
- API endpoints
- Database schema
- Third-party dependencies

## Edge Cases

- Edge case 1: [How to handle?]
- Edge case 2: [How to handle?]

## Testing Requirements

- **Unit Tests**: [What to test?]
- **Integration Tests**: [What to test?]
- **E2E Tests**: [Which flows?]

## Dependencies

- **Depends on**: LIN-123, LIN-124
- **Blocks**: LIN-125

## Agent Recommendation

- **Agent**: `java-developer`
- **Rationale**: Spring Boot expertise required

## Definition of Done

- [ ] Code implemented
- [ ] Tests written (Coverage > 80%)
- [ ] Code review conducted
- [ ] Documented
- [ ] Deployed to staging
```

**DON'T**:

```markdown
Task: "Do stuff" # Too vague

## Description

Build feature X # No details

# No acceptance criteria

# No dependencies

# No agent recommendation
```

### Duplicate Prevention

**Strategy**:

**1. Before EPIC creation**:

```typescript
// Search for similar EPICs
const existingEPICs = await linear.listProjects({
  teamId: TEAM_ID,
  status: "planned,in_progress",
});

const similarEPICs = existingEPICs.filter((epic) => {
  return similarity(epic.name, newEPICName) > 0.7;
});

if (similarEPICs.length > 0) {
  // Interactive confirmation
  console.log("Similar EPICs found:");
  similarEPICs.forEach((epic) => {
    console.log(`  - ${epic.identifier}: ${epic.name}`);
  });

  const userChoice = await askUser("Do you wish to proceed?", [
    "Yes",
    "No, cancel",
    "Extend existing EPIC",
  ]);
}
```

**2. Before issue creation**:

```typescript
// Search for similar issues in EPIC
const existingIssues = await linear.listIssues({
  projectId: EPIC_ID,
});

const duplicates = existingIssues.filter((issue) => {
  // Exact title match
  if (issue.title === newIssueTitle) return true;

  // High similarity
  if (similarity(issue.title, newIssueTitle) > 0.85) return true;

  return false;
});

if (duplicates.length > 0) {
  console.log(`Duplicate found: ${duplicates[0].identifier}`);
  console.log("Skipping issue creation");
}
```

**3. Similarity check**:

```typescript
function similarity(str1: string, str2: string): number {
  // Levenshtein distance or other similarity metric
  const distance = levenshtein(str1.toLowerCase(), str2.toLowerCase());
  const maxLength = Math.max(str1.length, str2.length);
  return 1 - distance / maxLength;
}
```

### Prioritization

**MoSCoW Mapping to Linear Priorities**:

| MoSCoW          | Linear Priority    | Rationale               |
| --------------- | ------------------ | ----------------------- |
| **Must-Have**   | `urgent` or `high` | Critical for MVP        |
| **Should-Have** | `medium`           | Important, not critical |
| **Could-Have**  | `low`              | Nice-to-have            |
| **Won't-Have**  | No issues          | Out of scope            |

**Prioritization Algorithm**:

```typescript
function mapPriority(moscowPriority: string, businessValue: number): string {
  if (moscowPriority === "must") {
    return businessValue > 8 ? "urgent" : "high";
  }

  if (moscowPriority === "should") {
    return businessValue > 6 ? "high" : "medium";
  }

  if (moscowPriority === "could") {
    return "low";
  }

  // won't-have: Do not create issue
  return null;
}
```

**DON'T**:

- Mark everything as "urgent"
- Ignore priorities
- Create issues for Won't-Have items

### Estimation Best Practices

**T-Shirt Sizing to Story Points**:

| T-Shirt | Story Points | Duration | Example              |
| ------- | ------------ | -------- | -------------------- |
| **XS**  | 1            | < 2h     | Configuration change |
| **S**   | 2            | 2-4h     | Simple CRUD          |
| **M**   | 3-5          | 4-8h     | Standard feature     |
| **L**   | 8            | 1-2 days | Complex feature      |
| **XL**  | 13+          | 2+ days  | **TOO LARGE!**       |

**Estimation Factors**:

```typescript
function estimateTask(task: Task): number {
  let estimate = 2; // Baseline

  // Complexity
  if (task.hasMultipleEdgeCases) estimate += 1;
  if (task.isNewTechnology) estimate += 2;
  if (task.hasComplexAlgorithm) estimate += 2;

  // Uncertainty
  if (task.requirementsUnclear) estimate += 1;
  if (task.isUnknownCodebase) estimate += 1;

  // Dependencies
  if (task.dependencies.length > 2) estimate += 1;

  // Testing
  if (task.requiresE2ETests) estimate += 1;

  // Cap at 8 (anything > 8 should be split)
  return Math.min(estimate, 8);
}
```

**DON'T**:

- Overly optimistic estimates
- Forget testing effort
- Fail to split tasks > 8 SP

### Dependency Management

**Dependency Types**:

**Blocking**:

```yaml
Task A: "Implement Backend API"
Task B: "Implement Frontend UI"

Relation: Task B depends on Task A (blocked_by)
  Task A blocks Task B (blocks)
```

**Related**:

```yaml
Task A: "Implement User Login"
Task B: "Implement User Registration"

Relation: Task A related to Task B (related_to)
```

**Best Practices**:

**DO**:

- Document dependencies explicitly
- Visualize (graph)
- Enable parallel work
- Identify critical path

**DON'T**:

- Long dependency chains (> 3 levels)
- Circular dependencies
- Add dependencies after task creation

### Agent Recommendations

**Always specify**:

```markdown
## Agent Recommendation

**Recommended Agent**: `java-developer`

**Rationale**:
Spring Boot REST controller with service layer logic.
Enterprise Java pattern expertise required.

**Alternative Agents**:

- `python-expert` (if Python rewrite is desired)

**Multi-Agent Workflow** (if complex):

1. `java-developer` - Implementation (5 SP)
2. `code-reviewer` - Quality review (2 SP)
3. `test-automator` - E2E tests (3 SP)
```

**DON'T**:

- Omit agent recommendation
- Assign wrong agent
- Provide no rationale

## Quality Criteria

### EPIC Quality

**Checklist**:

- [ ] **Title**: Clear and concise (< 50 chars)
- [ ] **Executive Summary**: 3-5 sentences
- [ ] **Business Value**: Why and impact
- [ ] **Success Metrics**: Measurable goals
- [ ] **Timeline**: Rough milestones
- [ ] **PRD Link**: Full PRD linked
- [ ] **Status**: `planned` (initial)
- [ ] **Priority**: Based on MoSCoW
- [ ] **Labels**: epic, feature, tech-stack

### Task Quality

**Checklist**:

- [ ] **Atomic**: One logical unit
- [ ] **Actionable**: Immediately implementable
- [ ] **Testable**: Acceptance criteria defined
- [ ] **Ownable**: Assignable to one person
- [ ] **Measurable**: Estimate 2-8 SP
- [ ] **Independent**: Minimal dependencies
- [ ] **Complete**: All information provided
- [ ] **Described**: Full description
- [ ] **Agent-Mapped**: Recommended agent
- [ ] **Labeled**: Technology + type labels
- [ ] **DoD**: Definition of done defined

### Plan Quality

**Overall assessment**:

- [ ] **Completeness**: All PRD requirements covered?
- [ ] **Consistency**: No contradictions?
- [ ] **Realism**: Timeline realistic?
- [ ] **Testability**: All tasks testable?
- [ ] **Prioritization**: MoSCoW correctly mapped?
- [ ] **Dependencies**: All identified?
- [ ] **Resources**: Sufficient developers/time?

## Common Errors

### PRD Not Read Completely

**Problem**: Tasks missing or inconsistent

**Symptom**:

```yaml
PRD: "Must-Have: Dark Mode with Accessibility Features"

Tasks:
  - "Implement Dark Mode Toggle" # Correct
  # Accessibility missing!
```

**Solution**: Complete PRD analysis before task breakdown

### Tasks Too Large

**Problem**: Tasks > 8 SP

**Symptom**:

```yaml
Task: "Implement complete User Authentication System" (21 SP) # Incorrect
```

**Solution**: Decompose into atomic tasks:

```yaml
Tasks:
  - "User Registration" (5 SP) # Correct
  - "Login/Logout" (3 SP) # Correct
  - "Password Reset" (3 SP) # Correct
  - "Session Management" (5 SP) # Correct
  - "MFA" (8 SP) # Correct
```

### Vague Acceptance Criteria

**Problem**: Not testable

**Incorrect**:

```markdown
## Acceptance Criteria

- Feature works
- No bugs
```

**Correct**:

```markdown
## Acceptance Criteria

- [ ] User can toggle Dark Mode in Settings
- [ ] Theme persists in LocalStorage
- [ ] Theme applies to all components
- [ ] Keyboard accessible (Tab navigation)
- [ ] Screen reader announces theme change
```

### Dependencies Ignored

**Problem**: Tasks in wrong order

**Example**:

```yaml
Tasks:
  - "E2E Tests" (created first) # Incorrect
  - "Feature Implementation" (created second) # Incorrect

# E2E tests cannot run before feature!
```

**Solution**:

```yaml
Tasks:
  - "Feature Implementation" (LIN-123) # Correct
  - "E2E Tests" (LIN-124, depends on LIN-123) # Correct
```

### Duplicates Not Checked

**Problem**: Redundant issues

**Example**:

```yaml
Existing:
  - LIN-123: "Implement Dark Mode"

New (Duplicate):
  - LIN-456: "Add Dark Mode Feature" # Incorrect
```

**Solution**: Duplicate check before creation

### Inconsistent Prioritization

**Problem**: Contradictory priorities

**Example**:

```yaml
EPIC Priority: low
Tasks:
  - Task 1: Priority urgent # Incorrect
  - Task 2: Priority urgent # Incorrect


# If EPIC is low, tasks cannot be urgent!
```

**Solution**: Consistent priorities (EPIC to tasks)

## Communication and Collaboration

### With Stakeholders

**EPIC as Communication Tool**:

- Executive summary for management
- Success metrics for product owner
- Timeline for stakeholders
- PRD link for details

**DON'T**:

- Technical details in EPIC
- Too many details (belong in issues)

### With Developers

**Issues as Work Units**:

- Clear description (no interpretation needed)
- All information provided
- Acceptance criteria testable
- Agent recommendation helpful

**DON'T**:

- Vague descriptions
- Missing information
- Interpretation required

### With QA/Testing

**Testing Requirements**:

- Unit tests: What to test?
- Integration tests: Which scenarios?
- E2E tests: Which flows?
- Acceptance criteria as test cases

**DON'T**:

- Testing as afterthought
- Vague test requirements
- Untestable acceptance criteria

## Maintenance and Updates

### Updating the Plan

**During Implementation**:

- Add new tasks (if necessary)
- Adjust estimates (based on actuals)
- Update dependencies
- Keep status current

**DON'T**:

- Treat plan as static
- Fail to document changes
- Ignore scope creep

### Post-Mortem

**After Completion**:

- Compare actual vs. estimated
- Identify bottlenecks
- Document lessons learned
- Improve process

**Template**:

```markdown
## Post-Mortem: [EPIC-Name]

### Summary

- Estimated effort: [X SP]
- Actual effort: [Y SP]
- Delta: [Y-X SP] (+/-Z%)

### What Went Well

- [Point 1]
- [Point 2]

### What Could Be Improved

- [Point 1]
- [Point 2]

### Lessons Learned

- [Lesson 1]
- [Lesson 2]

### Action Items

- [ ] Action 1
- [ ] Action 2
```

## Checklists

### Before Plan Creation

- [ ] PRD read completely
- [ ] Requirements understood
- [ ] Scope clearly defined
- [ ] Timeline realistic
- [ ] Resources available

### During Plan Creation

- [ ] EPIC created with complete description
- [ ] Duplicate check performed
- [ ] All Must-Have tasks created
- [ ] Should/Could-Have tasks prioritized
- [ ] Dependencies identified
- [ ] Agent recommendations added
- [ ] Labels consistent
- [ ] Estimates realistic

### After Plan Creation

- [ ] Consistency check performed
- [ ] No duplicates
- [ ] Completeness verified
- [ ] Dependencies linked
- [ ] Plan shared with team
- [ ] Questions clarified

---

**See also**:

- [linear-integration.md](linear-integration.md) - Linear API details
- [task-breakdown.md](task-breakdown.md) - Task breakdown strategies
- [agent-mapping.md](agent-mapping.md) - Agent recommendations
