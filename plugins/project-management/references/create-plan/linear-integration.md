# Linear Integration Guide

Comprehensive documentation for integration with Linear for EPIC and issue management.

## Overview

Linear serves as the central project management platform:

- **EPICs**: Represent PRD-based features/initiatives
- **Issues**: Individual, atomic tasks
- **Labels**: Categorization and filtering
- **Estimates**: Story point estimations
- **Dependencies**: Task relationships
- **Custom Fields**: Extended metadata (e.g., agent recommendations)

## Linear Hierarchy

```
Workspace (Organization)
└── Team
    └── Project (EPIC)
        ├── Issue 1
        ├── Issue 2
        └── Issue N
```

### EPIC Structure

**EPIC = PRD Feature**:

```yaml
Title: "[Feature-Name]"
Description: |
  ## Executive Summary
  [Adopted from PRD]

  ## Business Value
  [Why is this being built?]

  ## Success Metrics
  [Measurable goals]

  ## Timeline
  [Rough milestones]

  ## Full PRD
  Link: [PRD path or URL]
Status: planned | in_progress | completed | canceled
Priority: urgent | high | medium | low | no_priority
Estimate: [Sum of all issue estimates]
Labels: [epic, feature, ...]
```

### Issue Structure

**Issue = Atomic Task**:

```yaml
Title: "[Concise Task Description]"
Description: |
  ## Task Details
  [Complete description]

  ## Acceptance Criteria
  - [ ] Criterion 1
  - [ ] Criterion 2

  ## Technical Notes
  [Implementation hints]

  ## Agent Recommendation
  - Recommended agent: [agent-name]
  - Rationale: [Why this agent?]

  ## Dependencies
  - Depends on: LIN-XXX
  - Blocks: LIN-YYY

Parent: [EPIC-ID]
Status: backlog | todo | in_progress | done | canceled
Priority: urgent | high | medium | low | no_priority
Estimate: [1, 2, 3, 5, 8, 13, 21]
Labels: [feature, bug, documentation, ...]
Assignee: [Optional]
```

## Linear MCP Tools

### Available Tools

The Linear MCP server provides the following tools:

#### Project/EPIC Management

```typescript
// Create EPIC
mcp__linear__create_project({
  name: "Dark Mode Toggle",
  description: "Executive Summary + Full Description",
  state: "planned",
  priority: "high",
  teamId: "TEAM_ID",
});

// List EPICs
mcp__linear__list_projects({
  teamId: "TEAM_ID",
  status: "planned", // planned, in_progress, completed
});

// Get EPIC details
mcp__linear__get_project({
  projectId: "PROJECT_ID",
});

// Update EPIC
mcp__linear__update_project({
  projectId: "PROJECT_ID",
  name: "Updated Name",
  description: "Updated Description",
  state: "in_progress",
});
```

#### Issue Management

```typescript
// Create issue
mcp__linear__create_issue({
  title: "Implement UI Toggle Component",
  description: "Detailed description with acceptance criteria",
  projectId: "PROJECT_ID", // Link to EPIC
  priority: "high",
  estimate: 3, // Story Points
  labelIds: ["LABEL_ID_1", "LABEL_ID_2"],
  teamId: "TEAM_ID",
});

// List issues
mcp__linear__list_issues({
  projectId: "PROJECT_ID",
  status: "backlog", // backlog, todo, in_progress, done
  teamId: "TEAM_ID",
});

// Get issue details
mcp__linear__get_issue({
  issueId: "ISSUE_ID",
});

// Update issue
mcp__linear__update_issue({
  issueId: "ISSUE_ID",
  title: "Updated Title",
  description: "Updated Description",
  status: "in_progress",
  estimate: 5,
});

// Delete issue (for duplicates)
mcp__linear__delete_issue({
  issueId: "ISSUE_ID",
});
```

#### Label Management

```typescript
// List labels
mcp__linear__list_labels({
  teamId: "TEAM_ID",
});

// Create label
mcp__linear__create_label({
  name: "feature",
  color: "#4CAF50",
  teamId: "TEAM_ID",
});

// Assign labels to issue
mcp__linear__add_label_to_issue({
  issueId: "ISSUE_ID",
  labelId: "LABEL_ID",
});
```

#### Dependencies

```typescript
// Create dependency
mcp__linear__create_issue_relation({
  issueId: "ISSUE_ID",
  relatedIssueId: "RELATED_ISSUE_ID",
  type: "blocks", // blocks, blocked_by, related_to
});

// List dependencies
mcp__linear__list_issue_relations({
  issueId: "ISSUE_ID",
});
```

## Workflow Implementation

### 1. Read PRD

```typescript
// Read PRD file
const prdContent = await read_file({ file_path: prdPath });

// Validate PRD structure
const prdData = parsePRD(prdContent);
validatePRDStructure(prdData);
```

### 2. Duplicate Check

```typescript
// Check existing EPICs
const existingProjects = await mcp__linear__list_projects({
  teamId: TEAM_ID,
  status: "planned,in_progress",
});

// Search for similar names
const duplicates = existingProjects.filter(
  (p) => similarity(p.name, prdData.title) > 0.8,
);

if (duplicates.length > 0) {
  // Interactive confirmation
  const userChoice = await askUserQuestion({
    question: "Similar EPIC found. What would you like to do?",
    options: ["Create new EPIC", "Extend existing EPIC", "Cancel"],
  });
}
```

### 3. Create EPIC

```typescript
// Create EPIC from PRD
const epic = await mcp__linear__create_project({
  name: prdData.title,
  description: formatEpicDescription(prdData),
  state: "planned",
  priority: mapPRDPriority(prdData.priority),
  teamId: TEAM_ID,
});

console.log(`EPIC created: ${epic.name} (${epic.identifier})`);
```

### 4. Task Breakdown

```typescript
// Derive tasks from PRD
const tasks = breakdownPRDToTasks(prdData);

// Categorize tasks
const categorizedTasks = {
  mustHave: tasks.filter((t) => t.priority === "must"),
  shouldHave: tasks.filter((t) => t.priority === "should"),
  couldHave: tasks.filter((t) => t.priority === "could"),
};
```

### 5. Create Issues

```typescript
// Create an issue for each task
for (const task of categorizedTasks.mustHave) {
  // Duplicate check
  const existingIssue = await checkForDuplicateIssue(task, epic.id);
  if (existingIssue) {
    console.log(`Duplicate found: ${existingIssue.identifier}`);
    continue;
  }

  // Prepare labels
  const labels = await getOrCreateLabels(task.labels, TEAM_ID);

  // Create issue
  const issue = await mcp__linear__create_issue({
    title: task.title,
    description: formatIssueDescription(task),
    projectId: epic.id,
    priority: mapPriority(task.priority),
    estimate: task.estimate,
    labelIds: labels.map((l) => l.id),
    teamId: TEAM_ID,
  });

  console.log(`Issue created: ${issue.identifier} - ${issue.title}`);
}
```

### 6. Link Dependencies

```typescript
// Create dependencies between issues
for (const task of tasks) {
  if (task.dependencies && task.dependencies.length > 0) {
    for (const depIdentifier of task.dependencies) {
      await mcp__linear__create_issue_relation({
        issueId: task.issueId,
        relatedIssueId: depIdentifier,
        type: "blocked_by",
      });
    }
  }
}
```

## Label Strategy

### Standard Labels

**Technology Stack**:

- `java` - Java/Spring Boot tasks
- `python` - Python/Django/FastAPI tasks
- `javascript` - JavaScript/TypeScript tasks
- `react` - React frontend
- `database` - Database-related tasks

**Task Type**:

- `feature` - New functionality
- `bug` - Bug fix
- `documentation` - Documentation
- `testing` - Test tasks
- `refactor` - Code refactoring
- `security` - Security tasks
- `performance` - Performance optimization

**Priority** (redundant to issue priority, but useful for filtering):

- `must-have` - Must-have features
- `should-have` - Should-have features
- `could-have` - Could-have features

**Agent Tags**:

- `agent:code-reviewer` - For code review tasks
- `agent:java-developer` - For Java tasks
- `agent:python-expert` - For Python tasks
- `agent:ai-engineer` - For AI/ML tasks

### Label Creation

```typescript
const standardLabels = [
  { name: "java", color: "#E76F00" },
  { name: "python", color: "#3776AB" },
  { name: "javascript", color: "#F7DF1E" },
  { name: "react", color: "#61DAFB" },
  { name: "feature", color: "#4CAF50" },
  { name: "bug", color: "#F44336" },
  { name: "documentation", color: "#FFC107" },
  { name: "testing", color: "#9C27B0" },
  { name: "must-have", color: "#D32F2F" },
  { name: "should-have", color: "#FF9800" },
  { name: "could-have", color: "#8BC34A" },
];

// Create labels (if not present)
for (const labelDef of standardLabels) {
  const existingLabel = existingLabels.find((l) => l.name === labelDef.name);
  if (!existingLabel) {
    await mcp__linear__create_label({
      name: labelDef.name,
      color: labelDef.color,
      teamId: TEAM_ID,
    });
  }
}
```

## Story Point Estimation

**Story Points** are based on complexity, not time:

| Story Points | Complexity        | Example                          |
| ------------ | ----------------- | -------------------------------- |
| **1**        | Trivial           | Configuration change             |
| **2**        | Simple            | Simple CRUD operation            |
| **3**        | Medium            | Feature with few edge cases      |
| **5**        | Complex           | Feature with multiple edge cases |
| **8**        | Very Complex      | Feature with many dependencies   |
| **13**       | Extremely Complex | Large refactoring/migration      |
| **21**       | Epic              | Too large, decompose!            |

**Rule of thumb**: Tasks > 8 SP should be decomposed into smaller tasks.

## Custom Fields

Linear allows custom fields for extended metadata:

```typescript
// Custom field for agent recommendations
await mcp__linear__create_custom_field({
  teamId: TEAM_ID,
  name: "Recommended Agent",
  type: "text",
  description: "AI agent recommended for this task",
});

// Set custom field
await mcp__linear__set_issue_custom_field({
  issueId: issue.id,
  customFieldId: CUSTOM_FIELD_ID,
  value: "java-developer",
});
```

## Error Handling

### Duplicate Detection

```typescript
function checkForDuplicateIssue(task, epicId) {
  const existingIssues = await mcp__linear__list_issues({
    projectId: epicId,
  });

  return existingIssues.find((issue) => {
    // Exact title match
    if (issue.title === task.title) return true;

    // Similarity > 90%
    if (similarity(issue.title, task.title) > 0.9) return true;

    return false;
  });
}
```

### Rate Limiting

Linear API has rate limits:

```typescript
// Throttle API calls
async function createIssuesWithThrottle(tasks, epicId) {
  for (const task of tasks) {
    await createIssue(task, epicId);
    await sleep(100); // 100ms pause between calls
  }
}
```

### Error Handling

```typescript
try {
  const issue = await mcp__linear__create_issue({...})
} catch (error) {
  if (error.code === "DUPLICATE") {
    console.log(`Issue already exists: ${task.title}`)
  } else if (error.code === "RATE_LIMIT") {
    console.log("Rate limit reached, waiting 60s...")
    await sleep(60000)
    // Retry
  } else {
    console.error(`Error creating issue: ${error.message}`)
    throw error
  }
}
```

## Best Practices

### EPIC Creation

**DO**:

- Include executive summary in EPIC description
- Link to complete PRD
- Set realistic timeline
- Communicate business value clearly

**DON'T**:

- Include technical implementation in EPIC
- Add too many details (belong in issues)
- Create EPICs without clear success metrics

### Issue Creation

**DO**:

- Clear, concise titles
- Comprehensive acceptance criteria
- Document dependencies
- Realistic estimates
- Add agent recommendations

**DON'T**:

- Vague descriptions
- Tasks too large (> 8 SP)
- Issues without acceptance criteria
- Ignore dependencies

### Label Usage

**DO**:

- Consistent label strategy
- Combine technology + type labels
- Agent tags for recommendations

**DON'T**:

- Too many labels per issue (max 5-7)
- Inconsistent label names
- Labels without clear meaning

## Troubleshooting

### "EPIC Not Found"

**Problem**: Issue cannot be linked to EPIC

**Solution**:

```typescript
// Verify EPIC ID
const epic = await mcp__linear__get_project({ projectId: EPIC_ID });
if (!epic) {
  console.error("EPIC does not exist!");
}
```

### "Label Not Found"

**Problem**: Label ID is invalid

**Solution**:

```typescript
// Retrieve labels again
const labels = await mcp__linear__list_labels({ teamId: TEAM_ID });
const labelMap = Object.fromEntries(labels.map((l) => [l.name, l.id]));
```

### "Rate Limit Exceeded"

**Problem**: Too many API calls

**Solution**:

- Implement throttling (100-200ms between calls)
- Use batch operations where possible
- On 429 error: wait 60s

---

**See also**:

- [task-breakdown.md](task-breakdown.md) - Task breakdown strategies
- [agent-mapping.md](agent-mapping.md) - Agent recommendations
- [best-practices.md](best-practices.md) - General best practices
