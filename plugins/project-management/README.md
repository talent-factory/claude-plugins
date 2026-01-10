# Project Management Plugin

Comprehensive project management tools for PRD generation, project planning, task implementation with Linear integration and git worktree workflow.

## Version 2.0.0

**Major Update:** Now includes `/create-plan` and `/implement-task` commands with comprehensive references and Linear integration.

## Commands

### `/create-prd`

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
/create-prd
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
- [Best Practices](./references/create-prd/best-practices.md) - PRD quality guidelines
- [Sections Guide](./references/create-prd/sections-guide.md) - Detailed section templates
- [Templates](./references/create-prd/templates.md) - Ready-to-use PRD templates

### `/create-plan`

Transform PRDs into actionable project plans with task breakdown and Linear integration.

**Features:**
- 📋 Automatic task extraction from PRD
- 🎯 Task prioritization and dependencies
- 👥 Agent-to-task mapping
- 🔗 Linear issue creation and syncing
- 📂 Filesystem-based plan management
- 🗂️ Hierarchical task organization

**Usage:**
```bash
/create-plan                    # From filesystem PRD
/create-plan --linear ISSUE-123 # From Linear issue
```

**Plan Structure:**
- High-level milestones
- Detailed task breakdown
- Agent assignment recommendations
- Dependency mapping
- Estimated complexity
- Priority levels

**References:**
- [Agent Mapping](./references/create-plan/agent-mapping.md) - Agent selection guidelines
- [Best Practices](./references/create-plan/best-practices.md) - Planning methodologies
- [Filesystem](./references/create-plan/filesystem.md) - File-based plan storage
- [Linear Integration](./references/create-plan/linear-integration.md) - Linear API usage
- [Task Breakdown](./references/create-plan/task-breakdown.md) - Task decomposition strategies

### `/implement-task`

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
/implement-task                 # From filesystem plan
/implement-task TASK-ID         # Specific task
/implement-task --linear ISSUE  # From Linear
```

**Workflow:**
1. Creates git worktree for task
2. Checks out new feature branch
3. Tracks implementation progress
4. Updates task status
5. Creates PR when complete
6. Syncs with Linear

**References:**
- [Best Practices](./references/implement-task/best-practices.md) - Implementation guidelines
- [Filesystem](./references/implement-task/filesystem.md) - Task file management
- [Linear](./references/implement-task/linear.md) - Linear integration
- [Troubleshooting](./references/implement-task/troubleshooting.md) - Common issues
- [Workflow](./references/implement-task/workflow.md) - Complete workflow guide

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
├── commands/
│   ├── create-prd.md
│   ├── create-plan.md
│   └── implement-task.md
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
│   └── implement-task/
│       ├── best-practices.md
│       ├── filesystem.md
│       ├── linear.md
│       ├── troubleshooting.md
│       └── workflow.md
└── README.md
```

## Workflow Example

### Complete Feature Development

```bash
# 1. Create PRD
/create-prd
# Generates: docs/prd/feature-name.md

# 2. Create Project Plan
/create-plan
# Generates: docs/plans/feature-name-plan.md
# Creates Linear issues (if configured)

# 3. Implement Tasks
/implement-task TASK-1
# Creates worktree and branch
# Develops feature
# Creates PR when done

/implement-task TASK-2
# Repeat for each task
```

### With Linear Integration

```bash
# 1. Create PRD from Linear epic
/create-prd --linear EPIC-123

# 2. Generate plan with Linear sync
/create-plan --linear EPIC-123
# Creates sub-issues in Linear

# 3. Implement with Linear tracking
/implement-task --linear EPIC-123-1
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

1. **Break down into small tasks** - < 1 day of work each
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
/create-prd

User: "We need OAuth login with Google and GitHub"

# Claude generates comprehensive PRD:
# - User personas (developers, end-users)
# - Use cases (sign up, sign in)
# - Technical requirements (OAuth2 flow)
# - Success metrics (signup conversion rate)
# - Security considerations

# Step 2: Create plan
/create-plan

# Claude generates:
# - 12 tasks broken down by milestone
# - Dependencies mapped
# - Agent assignments (backend-dev, security-expert)
# - Linear issues created

# Step 3: Implement first task
/implement-task TASK-1

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
/create-plan --linear BUG-456

# Implement fix
/implement-task --linear BUG-456-1

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
- **Solution:** Explicitly ask for architecture and technical constraints

### Plan Creation

**Problem:** Tasks too large
- **Solution:** See [task-breakdown.md](./references/create-plan/task-breakdown.md)

**Problem:** Linear sync fails
- **Solution:** Check API key and team ID in settings

### Task Implementation

**Problem:** Worktree creation fails
- **Solution:** See [troubleshooting.md](./references/implement-task/troubleshooting.md)

**Problem:** Branch already exists
- **Solution:** Use different task ID or clean up old branches

## Changelog

### Version 2.0.0 (2026-01-10)

**Major Update:**
- ✨ Added `/create-plan` command with Linear integration
- ✨ Added `/implement-task` command with worktree workflow
- 📚 Added comprehensive reference documentation (13 files)
- 🔗 Integrated Linear API for issue management
- 🌲 Added git worktree support for isolated development
- 📋 Enhanced PRD templates and best practices

**Migration from 1.0.0:**
- `/create-prd` remains compatible
- New commands optional but recommended
- Linear integration opt-in

### Version 1.0.0

- Initial release with `/create-prd`

## Support

- **Issues:** [GitHub Issues](https://github.com/talent-factory/claude-plugins/issues)
- **Discussions:** [GitHub Discussions](https://github.com/talent-factory/claude-plugins/discussions)
- **Email:** support@talent-factory.ch

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) in the main repository.

## License

MIT License - see [LICENSE](../../LICENSE) file for details.

---

**Made with ❤️ by Talent Factory GmbH**
