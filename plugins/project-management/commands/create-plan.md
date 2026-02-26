---
description: Create a project plan from a PRD (Filesystem or Linear)
category: project
argument-hint: "[--prd <PRD-path>] [--linear] [--interactive]"
allowed-tools:
  - Read
  - Write
  - TodoWrite
  - AskUserQuestion
  - Glob
  - mcp__linear__*
---

# Claude Command: Create Project Plan

Create a structured project plan from a Product Requirements Document (PRD). Store tasks in the filesystem (`.plans/`) or in Linear (via the `--linear` flag).

## Role and Expertise

You function as a **Scrum Master, Product Owner, and Development Lead** with the following expertise:

- **Academic Background**: MSc in Computer Science
- **Best Practices**: Current standards from leading universities and technical institutions
- **Agile Methodologies**: Scrum, Kanban, User Story Mapping
- **Task Breakdown**: Atomic, testable, and estimable tasks

## Usage

```bash
# Filesystem-based (default)
/project-management:create-plan                         # PRD.md in CWD
/project-management:create-plan --prd feature.md        # Specific PRD
/project-management:create-plan PRDs/01-rag-system.md   # Direct path

# Linear-based
/project-management:create-plan --linear                # PRD.md in CWD
/project-management:create-plan --linear --prd feature.md

# Interactive mode
/project-management:create-plan --interactive
```

## Provider Selection

### Filesystem (Default)

**When to use**: Local project without Linear, rapid iteration, offline work.

**Output Structure**:

```
.plans/[feature-name]/
├── EPIC.md          # Feature overview
├── STATUS.md        # Progress tracking
└── tasks/
    ├── task-001-[slug].md
    ├── task-002-[slug].md
    └── ...
```

### Linear (`--linear`)

**When to use**: Team collaboration, project tracking, integration with other tools.

**Prerequisite**: Linear MCP Server configured:

```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-linear"],
      "env": { "LINEAR_API_KEY": "<your-api-key>" }
    }
  }
}
```

## Common Workflow

### 1. Read PRD Document

- **Default**: `PRD.md` in the current directory
- **Custom**: Via `--prd <path>` or as a direct argument
- **Fallback**: Interactive prompt if not found

**Validation**:

- Is the PRD structure complete?
- Are objectives and success metrics defined?
- Are requirements prioritized (MoSCoW)?

### 2. Derive Feature Name

Generate a feature name in `kebab-case` from the PRD:

**Examples**:

- "Dark Mode Toggle" → `dark-mode-toggle`
- "RAG-based System" → `rag-based-system`
- "User Authentication" → `user-authentication`

### 3. Create EPIC

| Provider   | Storage Location                | Format        |
| ---------- | ------------------------------- | ------------- |
| Filesystem | `.plans/[feature-name]/EPIC.md` | Markdown file |
| Linear     | Linear Project/EPIC             | API-based     |

**Duplicate Check**:

- Verify existing EPICs/plans with the same name
- Interactive confirmation for duplicates
- Options: Overwrite, choose different name, cancel

### 4. Perform Task Breakdown

Derive **self-contained tasks** from the PRD:

**Criteria for Quality Tasks (ATOMIC)**:

- **A**ctionable: Immediately implementable
- **T**estable: Acceptance criteria defined
- **O**wnable: Assignable to a single developer/agent
- **M**easurable: Story Points (1, 2, 3, 5, 8)
- **I**ndependent: Minimal dependencies
- **C**omplete: Self-contained

### 5. Store Tasks

| Provider   | Storage Location                       | Format         |
| ---------- | -------------------------------------- | -------------- |
| Filesystem | `.plans/[feature]/tasks/task-NNN-*.md` | Markdown files |
| Linear     | Linear Issues under EPIC               | API-based      |

### 6. Create Status Tracking

| Provider   | Storage Location             | Content                                |
| ---------- | ---------------------------- | -------------------------------------- |
| Filesystem | `.plans/[feature]/STATUS.md` | Progress, dependency graph, next steps |
| Linear     | Linear Dashboard             | Automatic via UI                       |

### 7. Consistency Check

**Before saving**:

- [ ] No duplicates or redundancies
- [ ] Consistent overall picture
- [ ] Tasks are complete and implementable
- [ ] Dependencies correctly linked
- [ ] Prioritization is logical
- [ ] Story Points are realistic

## Agent Recommendations

Based on task type, AI agents are recommended:

| Task Type              | Recommended Agents          | Usage                         |
| ---------------------- | --------------------------- | ----------------------------- |
| **Code Review**        | `code-reviewer`             | Quality assurance             |
| **Java Development**   | `java-developer`            | Spring Boot, Enterprise Java  |
| **Python Development** | `python-expert`             | Django, FastAPI, Data Science |
| **AI/ML Features**     | `ai-engineer`               | LLM integration, ML pipelines |
| **Agent Development**  | `agent-expert`              | AI agent development          |
| **Documentation**      | `markdown-syntax-formatter` | Docs, READMEs                 |
| **Testing**            | `test-automator`            | Unit/Integration tests        |

**Details**: [agent-mapping.md](../references/create-plan/agent-mapping.md)

## Quality Criteria

### Tasks Must Meet:

- [ ] **Precise Formulation**: Developers can implement without additional questions
- [ ] **Clear Acceptance Criteria**: Testable and measurable
- [ ] **Dependencies Documented**: Sequence is clear
- [ ] **Realistic Estimation**: Story Points based on complexity
- [ ] **Agent Recommendation**: Suitable AI agent suggested (if available)

### EPIC Must Contain:

- [ ] **Executive Summary**: Brief overview
- [ ] **Business Value**: Why is this being built?
- [ ] **Success Metrics**: Measurable objectives
- [ ] **Timeline**: Rough milestones
- [ ] **Dependencies**: External dependencies

## Duplicate Prevention

**Before EPIC/Plan Creation**:

1. Search existing EPICs/plans with similar names
2. Check active tasks with overlapping requirements
3. Interactive confirmation for duplicates:
   - Create new (choose different name)
   - Extend existing
   - Cancel and adjust PRD

**Before Task Creation**:

1. Check existing tasks in the EPIC/plan
2. Avoid redundant tasks
3. Merge similar tasks

## Task Breakdown Strategies

**From Functional Requirements**:

- One requirement = One or more tasks
- Must-Have → Highest priority
- Should/Could-Have → Medium/Low priority

**From Non-Functional Requirements**:

- Performance tasks separate
- Security review as dedicated tasks
- Accessibility after feature tasks

**Cross-Cutting Concerns**:

- Testing as separate tasks
- Documentation tasks
- CI/CD setup
- Monitoring and observability

**Details**: [task-breakdown.md](../references/create-plan/task-breakdown.md)

## Best Practices

**DO**:

- Fully analyze PRD before task creation
- Atomic tasks: One logical unit per task
- Define clear acceptance criteria
- Document dependencies explicitly
- Realistic estimates (T-shirt sizing)
- Agent recommendations based on expertise
- Duplicate check before creation

**DON'T**:

- Tasks that are too large (> 8 Story Points)
- Vague descriptions without acceptance criteria
- Tasks without prioritization
- Redundant or overlapping tasks
- Ignoring dependencies
- Populating Linear without duplicate check

**Complete Guide**: [best-practices.md](../references/create-plan/best-practices.md)

## Example Workflows

### Filesystem (Default)

```bash
# 1. Create PRD
/project-management:create-prd "Dark Mode Toggle"

# 2. Generate plan from PRD
/project-management:create-plan PRD.md

# Output:
# PRD read: PRD.md
# Feature name: dark-mode-toggle
# Directory: .plans/dark-mode-toggle/
# EPIC.md created
# 8 tasks generated:
#    - task-001-ui-toggle-component.md (3 SP) [frontend-developer]
#    - task-002-theme-state-management.md (5 SP) [frontend-developer]
#    - ...
# STATUS.md created with dependency graph
# Total: 21 SP

# 3. Implement task
/project-management:implement-task task-001
```

### Linear (`--linear`)

```bash
# 1. Create PRD
/project-management:create-prd "Dark Mode Toggle"

# 2. Generate plan in Linear
/project-management:create-plan --linear --prd PRD.md

# Output:
# PRD read: PRD.md
# EPIC created: "Dark Mode Toggle" (LIN-123)
# 8 issues generated:
#    - LIN-124: UI Toggle Component (3 SP)
#    - LIN-125: Theme State Management (5 SP)
#    - ...
# Dependencies linked
# Labels added

# 3. Implement task
/project-management:implement-task --linear LIN-124
```

## Detailed Documentation

### General

- **[task-breakdown.md](../references/create-plan/task-breakdown.md)** - Task sizing, dependencies, Story Points
- **[agent-mapping.md](../references/create-plan/agent-mapping.md)** - Agent recommendations per task type
- **[best-practices.md](../references/create-plan/best-practices.md)** - Atomic tasks, acceptance criteria

### Provider-Specific

- **[filesystem.md](../references/create-plan/filesystem.md)** - Directory structure, templates (EPIC.md, STATUS.md, task files)
- **[linear-integration.md](../references/create-plan/linear-integration.md)** - Linear API, EPIC/issue structure, labels

## See Also

- **[/project-management:create-prd](./create-prd.md)** - PRD creation
- **[/project-management:implement-task](./implement-task.md)** - Task implementation

---

**PRD Path**: $ARGUMENTS
