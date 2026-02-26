---
description: Create handoff documentation before /compact for seamless continuation
category: project
argument-hint: "[task-name] [--output <dir>] [--linear-issue TF-XXX]"
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
  - TodoWrite
  - mcp__linear__*
---

# Claude Command: Document Handoff

Create comprehensive handoff documentation before a `/compact`, enabling a new agent with fresh context to seamlessly continue the work.

## Usage

```bash
# Default (task name derived from Git branch)
/project-management:document-handoff

# With explicit task name
/project-management:document-handoff "Feature Implementation"

# With custom output directory
/project-management:document-handoff "Task Name" --output docs/handoffs

# With Linear issue reference
/project-management:document-handoff --linear-issue TF-177
```

## When to Use

**Use when:**

- Context is becoming too large and `/compact` is necessary
- Handing off to another developer/agent
- Complex task needs to be interrupted
- Multiple failed attempts need to be documented
- At the end of a workday for the next session

**Do not use when:**

- Task will be completed in 5 minutes
- No relevant changes have been made
- Only research, no implementation
- Trivial task without significant context

## Workflow

### 1. Gather Information

Automatically collect relevant information:

**Capture Git Status:**

- Current branch and uncommitted changes
- Last 5 commits for context
- Modified files (staged and unstaged)

**Project Status:**

- Running services (Docker, etc.)
- TODO/FIXME comments in code
- Relevant environment variables

**Linear Integration (optional):**

- Retrieve issue details if `--linear-issue` is specified
- Linked issues and comments

### 2. Structure Documentation

Create handoff document with the following sections:

| Section                  | Content                                 |
| ------------------------ | --------------------------------------- |
| **Original Task**        | What should be achieved?                |
| **Already Completed**    | Changes, successful approaches          |
| **Failed Attempts**      | What did not work and why               |
| **Current State**        | Git status, modified files, environment |
| **Next Steps**           | Prioritized list with file paths        |
| **Important References** | Files, documentation, code patterns     |
| **For the Next Agent**   | Summary in 2-3 sentences                |

**Template**: [templates.md](../references/project-management:document-handoff/templates.md)

### 3. Save Documentation

**Output Directory:** `.claude/handoffs/`

**Filename Convention:** `YYYY-MM-DD_[task-slug].md`

Examples:

- `.claude/handoffs/2026-01-14_system-prompt-extraction.md`
- `.claude/handoffs/2026-01-14_rbac-regression-fix.md`

### 4. Output Summary

After creation:

- Display path to handoff file
- Highlight most important next steps
- Provide instructions for continuing after `/compact`

## Handoff Fundamental Principles

### Self-Explanatory

The next agent requires **no prior knowledge**:

- Complete context in the documentation
- No implicit assumptions
- All relevant file paths with line numbers

### Actionable

**Concrete action instructions**:

- "Modify line 123 in `file.py`" instead of "adjust code"
- Prioritized next steps
- Clear acceptance criteria

### Complete

**Document everything relevant**:

- Successful AND failed attempts
- Error messages with context
- Dependencies and external factors

## Quality Criteria

### Content

- [ ] Original task clearly described
- [ ] All changes documented
- [ ] Failed attempts with rationale
- [ ] Git status is current
- [ ] Next steps are prioritized
- [ ] File paths include line numbers

### Format

- [ ] Consistent Markdown structure
- [ ] Code blocks for commands and logs
- [ ] No secrets or credentials
- [ ] Professional language

## Workflow with Compact

```bash
# 1. Create handoff documentation
/project-management:document-handoff "Feature Implementation"

# 2. Compress context
/compact

# 3. New session: Load documentation
# "Please read .claude/handoffs/2026-01-14_feature-implementation.md
#  and continue with the next steps."
```

## Important Notes

1. **Execute before Compact**: The documentation is useless after compact if not created beforehand

2. **No Secrets**: Never include API keys, passwords, or tokens in handoff documentation

3. **Commit Git Changes**: Ideally commit all important changes before handoff

4. **Cleanup**: Regularly archive or delete old handoff documents

## Additional Information

- **Templates**: [templates.md](../references/project-management:document-handoff/templates.md)
  - Complete handoff template
  - Minimal template for quick handoffs

- **Examples**: [examples.md](../references/project-management:document-handoff/examples.md)
  - Minimal example
  - Complete example

- **Best Practices**: [best-practices.md](../references/project-management:document-handoff/best-practices.md)
  - Tips for effective handoffs
  - Avoiding common mistakes

## See Also

- **[/create-plan](./create-plan.md)** - Create project plan
- **[/implement-task](./implement-task.md)** - Implement task

---

**Task Name**: $ARGUMENTS
