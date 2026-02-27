# Project Management Plugin

Comprehensive project management tools for PRD generation, project planning, task implementation with Linear integration and git worktree workflow.

## Version 2.6.0

**New in 2.6.0:**

- 📋 `/project-management:init-task` — Single-task creation with duplicate detection, ATOMIC validation, and mandatory Definition of Done
- 📄 Extended task template with Type, Plan, and Definition of Done fields

**Previous:**

- 🧠 Intelligent plugin orchestration for `/project-management:implement-task` (Superpowers brainstorm, agent routing, quality gate)
- ⚡ Skip options: `--skip-brainstorm`, `--skip-quality-gate`

- 🤖 `/project-management:implement-epic` - Fully autonomous EPIC implementation with parallel agents
- 🔄 Autonomous Loop Integration - Self-sustaining development loops via Stop hooks
- 👥 `epic-orchestrator` Agent - Coordinates parallel task agents
- 📊 Real-time progress tracking

## Commands

### `/project-management:create-prd`

Generate professional Product Requirements Documents (PRDs) for features and products.

**Features:**

- 📋 Comprehensive PRD structure with all essential sections
- 🎯 Goal-oriented format with clear objectives
- 👥 User personas and use cases
- 📊 Success metrics and KPIs
- 🔧 Technical requirements and constraints
- 🗺️ Implementation roadmap
- 📚 Extensive templates and best practices

**Usage:**

```bash
/project-management:create-prd
```

**PRD Sections:**

- Executive Summary
- Goals & Objectives
- User Personas
- User Stories & Use Cases
- Functional Requirements
- Non-Functional Requirements
- Technical Architecture
- Success Metrics
- Implementation Phases
- Risks & Mitigation

**References:**

- [Best Practices](https://github.com/talent-factory/claude-plugins/blob/main/plugins/project-management/references/create-prd/best-practices.md) - PRD quality guidelines
- [Sections Guide](https://github.com/talent-factory/claude-plugins/blob/main/plugins/project-management/references/create-prd/sections-guide.md) - Detailed section templates
- [Templates](https://github.com/talent-factory/claude-plugins/blob/main/plugins/project-management/references/create-prd/templates.md) - Ready-to-use PRD templates

### `/project-management:create-plan`

Transform PRDs into actionable project plans with task breakdown and Linear integration.

**Features:**

- 📋 Automatic task extraction from PRD
- 🎯 Task prioritization and dependencies
- 👥 Agent-to-task mapping
- 🔗 Linear issue creation and synchronization
- 📂 Filesystem-based plan management
- 🗂️ Hierarchical task organization

**Usage:**

```bash
/project-management:create-plan                    # From filesystem PRD
/project-management:create-plan --linear ISSUE-123 # From Linear issue
```

**Plan Structure:**

- High-level milestones
- Detailed task breakdown
- Agent assignment recommendations
- Dependency mapping
- Estimated complexity
- Priority levels

**References:**

- [Agent Mapping](https://github.com/talent-factory/claude-plugins/blob/main/plugins/project-management/references/create-plan/agent-mapping.md) - Agent selection guidelines
- [Best Practices](https://github.com/talent-factory/claude-plugins/blob/main/plugins/project-management/references/create-plan/best-practices.md) - Planning methodologies
- [Filesystem](https://github.com/talent-factory/claude-plugins/blob/main/plugins/project-management/references/create-plan/filesystem.md) - File-based plan storage
- [Linear Integration](https://github.com/talent-factory/claude-plugins/blob/main/plugins/project-management/references/create-plan/linear-integration.md) - Linear API usage
- [Task Breakdown](https://github.com/talent-factory/claude-plugins/blob/main/plugins/project-management/references/create-plan/task-breakdown.md) - Task decomposition strategies

### `/project-management:init-task`

Initialize a single task with duplicate detection, ATOMIC validation, and mandatory Definition of Done (Filesystem or Linear).

### `/project-management:implement-task`

Implement tasks with git worktree workflow, branch creation, and PR automation.

**Features:**

- 🌲 Git worktree creation for isolated development
- 🌿 Automatic branch creation and management
- 📝 Task status tracking
- 🔗 Linear issue synchronization
- 🚀 PR creation integration
- ✅ Completion verification

**Usage:**

```bash
/project-management:implement-task                 # From filesystem plan
/project-management:implement-task TASK-ID         # Specific task
/project-management:implement-task --linear ISSUE  # From Linear
```

**Workflow:**

1. Creates git worktree for task
2. Checks out new feature branch
3. Tracks implementation progress
4. Updates task status
5. Creates PR when complete
6. Synchronizes with Linear

**References:**

- [Best Practices](https://github.com/talent-factory/claude-plugins/blob/main/plugins/project-management/references/implement-task/best-practices.md) - Implementation guidelines
- [Filesystem](https://github.com/talent-factory/claude-plugins/blob/main/plugins/project-management/references/implement-task/filesystem.md) - Task file management
- [Linear](https://github.com/talent-factory/claude-plugins/blob/main/plugins/project-management/references/implement-task/linear.md) - Linear integration
- [Troubleshooting](https://github.com/talent-factory/claude-plugins/blob/main/plugins/project-management/references/implement-task/troubleshooting.md) - Common issues
- [Workflow](https://github.com/talent-factory/claude-plugins/blob/main/plugins/project-management/references/implement-task/workflow.md) - Complete workflow guide

### `/project-management:implement-epic`

**Autonomous, parallel EPIC implementation** using native Claude Code autonomous loops for self-sustaining development cycles.

**Features:**

- 🤖 **Fully Autonomous** - Initiates and coordinates all tasks independently
- 🔀 **Parallel Execution** - Multiple tasks simultaneously in separate worktrees
- 🔄 **Autonomous Loops** - Iterative cycles until success using Stop hooks
- 👀 **Auto-Review** - Automatic code reviews with fix loops
- 📊 **Live Tracking** - Real-time progress display
- 🛡️ **Fault Tolerance** - Blocked tasks are documented while others continue

**Usage:**

```bash
/project-management:implement-epic                              # Interactive selection
/project-management:implement-epic dark-mode-toggle             # Plan name
/project-management:implement-epic --linear PROJ-123            # Linear EPIC
/project-management:implement-epic feature-x --max-parallel 5   # With options
```

**Workflow:**

```
1. Load EPIC & analyze dependency graph
         ↓
2. Identify parallelizable tasks (no blockers)
         ↓
3. Per task: Start agent in dedicated worktree
         ↓
4. Autonomous loop for implementation (until TASK_COMPLETE)
         ↓
5. Autonomous loop for review (until REVIEW_COMPLETE)
         ↓
6. Update STATUS.md, start next tasks
         ↓
7. Repeat until all tasks complete
```

**Options:**

| Option             | Default | Description                 |
| ------------------ | ------- | --------------------------- |
| `--max-parallel`   | 3       | Maximum concurrent agents   |
| `--max-iterations` | 30      | Maximum iterations per task |
| `--skip-review`    | false   | Skip review phase           |
| `--dry-run`        | false   | Display analysis only       |

**References:**

- [Orchestrator Architecture](https://github.com/talent-factory/claude-plugins/blob/main/plugins/project-management/references/implement-epic/orchestrator-architecture.md) - Technical details
- [Autonomous Loop Integration](https://github.com/talent-factory/claude-plugins/blob/main/plugins/project-management/references/implement-epic/autonomous-loop-integration.md) - Loop configuration
- [Parallel Strategies](https://github.com/talent-factory/claude-plugins/blob/main/plugins/project-management/references/implement-epic/parallel-strategies.md) - Parallelization patterns
- [Troubleshooting](https://github.com/talent-factory/claude-plugins/blob/main/plugins/project-management/references/implement-epic/troubleshooting.md) - Common issues

### `/project-management:document-handoff`

Create handoff documentation before `/compact` for seamless context continuation.

**Features:**

- 📋 Captures current task state and progress
- 🔄 Ensures seamless context continuation after compaction
- 📝 Documents decisions, blockers, and next steps
- 🔗 Linear issue synchronization support

**Usage:**

```bash
/project-management:document-handoff
/project-management:document-handoff "Feature Implementation"
/project-management:document-handoff --linear-issue TF-177
```

**References:**

- [Best Practices](https://github.com/talent-factory/claude-plugins/blob/main/plugins/project-management/references/document-handoff/best-practices.md) - Handoff quality guidelines
- [Examples](https://github.com/talent-factory/claude-plugins/blob/main/plugins/project-management/references/document-handoff/examples.md) - Example handoff documents
- [Templates](https://github.com/talent-factory/claude-plugins/blob/main/plugins/project-management/references/document-handoff/templates.md) - Ready-to-use templates

## Agents

### `epic-orchestrator`

Coordinates the parallel implementation of all tasks within an EPIC.

**Capabilities:**

- Dependency graph analysis
- Agent lifecycle management
- Progress tracking
- Error recovery
- User escalation for blockers

## Installation

This plugin is part of the Talent Factory marketplace.

**Add to `.claude/settings.json`:**

```json
{
  "enabledPlugins": {
    "project-management@talent-factory": true
  }
}
```

## Project Structure

```
project-management/
├── .claude-plugin/
│   └── plugin.json
├── agents/
│   └── epic-orchestrator.md
├── commands/
│   ├── create-prd.md
│   ├── create-plan.md
│   ├── init-task.md
│   ├── implement-task.md
│   ├── implement-epic.md
│   └── document-handoff.md
├── references/
│   ├── create-prd/
│   │   ├── best-practices.md
│   │   ├── sections-guide.md
│   │   └── templates.md
│   ├── create-plan/
│   │   ├── agent-mapping.md
│   │   ├── best-practices.md
│   │   ├── filesystem.md
│   │   ├── linear-integration.md
│   │   └── task-breakdown.md
│   ├── init-task/
│   │   ├── duplicate-detection.md
│   │   ├── task-template.md
│   │   └── validation-rules.md
│   ├── implement-task/
│   │   ├── best-practices.md
│   │   ├── filesystem.md
│   │   ├── linear.md
│   │   ├── troubleshooting.md
│   │   └── workflow.md
│   ├── implement-epic/
│   │   ├── orchestrator-architecture.md
│   │   ├── autonomous-loop-integration.md
│   │   ├── parallel-strategies.md
│   │   └── troubleshooting.md
│   └── document-handoff/
│       ├── best-practices.md
│       ├── examples.md
│       └── templates.md
└── README.md
```

## Workflow Example

### Complete Feature Development

```bash
# 1. Create PRD
/project-management:create-prd
# Generates: docs/prd/feature-name.md

# 2. Create Project Plan
/project-management:create-plan
# Generates: docs/plans/feature-name-plan.md
# Creates Linear issues (if configured)

# 3. Implement Tasks
/project-management:implement-task TASK-1
# Creates worktree and branch
# Develops feature
# Creates PR when done

/project-management:implement-task TASK-2
# Repeat for each task
```

### With Linear Integration

```bash
# 1. Create PRD from Linear epic
/project-management:create-prd --linear EPIC-123

# 2. Generate plan with Linear sync
/project-management:create-plan --linear EPIC-123
# Creates sub-issues in Linear

# 3. Implement with Linear tracking
/project-management:implement-task --linear EPIC-123-1
# Updates Linear issue status automatically
```

## Best Practices

### PRD Creation

1. **Start with user needs** - Focus on solving real problems
2. **Define clear success metrics** - Measurable outcomes
3. **Include non-functional requirements** - Performance, security, scalability
4. **Document assumptions** - Be explicit about constraints
5. **Iterate with stakeholders** - Review and refine

### Project Planning

1. **Break down into small tasks** - Less than one day of work each
2. **Identify dependencies** - Critical path planning
3. **Assign appropriate agents** - Match skills to tasks
4. **Set realistic timelines** - Buffer for unknowns
5. **Track in Linear** - Central source of truth

### Task Implementation

1. **Use worktrees** - Isolated development environments
2. **Follow naming conventions** - `feature/`, `fix/`, etc.
3. **Commit frequently** - Small, atomic commits
4. **Update task status** - Keep plan current
5. **Create PRs early** - Enable collaboration

## Linear Integration

### Setup

```bash
# Set Linear API key
export LINEAR_API_KEY=your_key_here

# Or configure in .claude/settings.json
{
  "linear": {
    "apiKey": "your_key_here",
    "teamId": "your_team_id"
  }
}
```

### Features

- **Bi-directional sync** - Changes flow both ways
- **Issue creation** - Auto-create from tasks
- **Status updates** - Sync task completion
- **Comment tracking** - Add implementation notes
- **Label management** - Tag with component/priority

## Examples

### Example 1: New Feature

```bash
# User request: "Add OAuth login"

# Step 1: Create PRD
/project-management:create-prd

User: "We need OAuth login with Google and GitHub"

# Claude generates comprehensive PRD:
# - User personas (developers, end-users)
# - Use cases (sign up, sign in)
# - Technical requirements (OAuth2 flow)
# - Success metrics (signup conversion rate)
# - Security considerations

# Step 2: Create plan
/project-management:create-plan

# Claude generates:
# - 12 tasks broken down by milestone
# - Dependencies mapped
# - Agent assignments (backend-dev, security-expert)
# - Linear issues created

# Step 3: Implement first task
/project-management:implement-task TASK-1

# Claude:
# - Creates worktree: ../oauth-feature-task1
# - Checks out branch: feature/oauth-provider-setup
# - Guides implementation
# - Updates task status
# - Creates PR when complete
```

### Example 2: Bug Fix Project

```bash
# Linear issue: "Memory leaks in WebSocket connections"

# Create plan from Linear
/project-management:create-plan --linear BUG-456

# Implement fix
/project-management:implement-task --linear BUG-456-1

# Status automatically synced to Linear
```

## Requirements

- **Git:** Version 2.23+ (for worktree support)
- **Linear CLI:** Optional for Linear integration (`npm install -g @linear/cli`)
- **GitHub CLI:** Optional for automated PRs (`gh`)

## Troubleshooting

### PRD Generation

**Problem:** PRD too generic

- **Solution:** Provide more context about users and use cases

**Problem:** Missing technical details

- **Solution:** Explicitly request architecture and technical constraints

### Plan Creation

**Problem:** Tasks too large

- **Solution:** See [task-breakdown.md](https://github.com/talent-factory/claude-plugins/blob/main/plugins/project-management/references/create-plan/task-breakdown.md)

**Problem:** Linear sync fails

- **Solution:** Check API key and team ID in settings

### Task Implementation

**Problem:** Worktree creation fails

- **Solution:** See [troubleshooting.md](https://github.com/talent-factory/claude-plugins/blob/main/plugins/project-management/references/implement-task/troubleshooting.md)

**Problem:** Branch already exists

- **Solution:** Use different task ID or clean up old branches

## Changelog

### Version 2.5.0 (2026-02-26)

**Plugin Orchestration:**

- 🧠 Added plugin orchestration to `/project-management:implement-task` (Superpowers brainstorm, agent routing, quality gate)
- ⚡ Added skip options: `--skip-brainstorm`, `--skip-quality-gate`
- 📚 Added reference documentation: agent-routing, context-analysis, quality-gate

### Version 2.4.0 (2026-02-01)

**Documentation & Architecture:**

- 🌐 Complete documentation translation to professional English (academic level)
- 🔧 Removed external plugin dependency (ralph-wiggum)
- 🔄 Uses native Claude Code autonomous loops via Stop hooks
- 📚 Renamed `ralph-integration.md` to `autonomous-loop-integration.md`

### Version 2.3.0 (2026-02-01)

**Autonomous EPIC Implementation:**

- 🤖 Added `/project-management:implement-epic` command with autonomous loop integration
- 🔀 Parallel task execution with isolated worktrees
- 👥 Added `epic-orchestrator` agent for coordination
- 🔄 Autonomous implementation and review loops
- 📊 Real-time progress tracking and status updates
- 📚 Added 4 new reference documents for EPIC implementation

### Version 2.0.0 (2026-01-10)

**Major Update:**

- ✨ Added `/project-management:create-plan` command with Linear integration
- ✨ Added `/project-management:implement-task` command with worktree workflow
- 📚 Added comprehensive reference documentation (13 files)
- 🔗 Integrated Linear API for issue management
- 🌲 Added git worktree support for isolated development
- 📋 Enhanced PRD templates and best practices

**Migration from 1.0.0:**

- `/project-management:create-prd` remains compatible
- New commands optional but recommended
- Linear integration opt-in

### Version 1.0.0

- Initial release with `/project-management:create-prd`

## Support

- **Issues:** [GitHub Issues](https://github.com/talent-factory/claude-plugins/issues)
- **Discussions:** [GitHub Discussions](https://github.com/talent-factory/claude-plugins/discussions)
- **Email:** support@talent-factory.ch

## Contributing

See [CONTRIBUTING.md](https://github.com/talent-factory/claude-plugins/blob/main/CONTRIBUTING.md) in the main repository.

## License

MIT License - see [LICENSE](https://github.com/talent-factory/claude-plugins/blob/main/LICENSE) file for details.

---

**Made with ❤️ by Talent Factory GmbH**
