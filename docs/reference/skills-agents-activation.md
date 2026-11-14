# Skills and Agents Activation Guide

This guide explains how to activate and use skills and agents in Claude Code plugins.

## Agents

Agents are specialized AI assistants that handle complex, multi-step tasks autonomously. They are triggered automatically based on context or can be invoked manually.

### Automatic Activation

Agents activate automatically when Claude detects relevant context in your request. Each agent has triggering conditions defined in its `description` field.

**Example:** a code-review agent described as "use proactively after code changes" starts after you modify code. This marketplace currently ships no agents; the plugins consist of skills and a few commands.

### Manual Activation via Task Tool

You can explicitly request an agent using the Task tool:

```
Use the code-reviewer agent to review this change
```

Claude will invoke:
```json
{
  "subagent_type": "<plugin>:<agent-name>",
  "prompt": "Review this change..."
}
```

### Agent Naming Convention

Agents are namespaced by plugin:

| Full Name | Plugin | Agent |
|-----------|--------|-------|
| `<plugin>:<agent-name>` | `<plugin>` | `<agent-name>` |

## Skills

Skills are reusable capabilities that can be invoked via commands, automatically triggered, or called directly.

### Activation Methods

#### 1. Via Slash Command

Skills are invoked like commands, namespaced by plugin:

```bash
/git-workflow:commit
/git-workflow:create-pr --draft
```

#### 2. Automatic Triggering

Skills can activate automatically based on context:

| Skill | Auto-triggers when |
|-------|-------------------|
| `humanizer` | User asks to "humanize" or "make text more natural" |
| `markdown-syntax-formatter` | Formatting Markdown documents |
| `tasknotes` | Task management requests in Obsidian context |

#### 3. Direct Invocation

User-invocable skills can be called directly:

```bash
/markdown-syntax-formatter     # Direct skill invocation
```

### Skill Naming Convention

Skills are namespaced by plugin:

| Full Name | Plugin | Skill |
|-----------|--------|-------|
| `git-workflow:commit` | git-workflow | commit |
| `git-workflow:create-pr` | git-workflow | create-pr |
| `core:humanizer` | core | humanizer |
| `education:markdown-syntax-formatter` | education | markdown-syntax-formatter |
| `obsidian:tasknotes` | obsidian | tasknotes |

## Plugin-Specific Activation

### Git Workflow Plugin

**Skills:**

| Skill | Activation |
|-------|------------|
| `commit` | `/git-workflow:commit` |
| `create-pr` | `/git-workflow:create-pr` |
| `resolve-conflicts` | `/git-workflow:resolve-conflicts` |

### Code Quality, Development and Core Plugins

No agents. `ruff-check` and `update-documents` are skills; `check-commands` and `check-agents` are commands.

**Skill:**

| Skill | Activation |
|-------|------------|
| `humanizer` | "Humanize this text", "remove AI patterns" |

### Education Plugin

**Skill:**

| Skill | Activation |
|-------|------------|
| `markdown-syntax-formatter` | Markdown formatting, `/markdown-syntax-formatter` |

### Obsidian Plugin

**Skill:**

| Skill | Activation |
|-------|------------|
| `tasknotes` | "Show my tasks", "create a task", task management |

## Best Practices

### When to Use Agents

- Complex, multi-step tasks requiring domain expertise
- Tasks that benefit from specialized knowledge
- When you need consistent, high-quality output in a specific domain

### When to Use Skills

- Repetitive tasks that benefit from automation
- Tasks with well-defined inputs and outputs
- Performance-critical operations (skills are often faster)

### Combining Agents and Skills

Agents and skills can work together:

```bash
# Implement the change, then use /git-workflow:commit for consistent commits
```

## Troubleshooting

### Agent Not Triggering

1. Check if the plugin is enabled in settings
2. Use explicit trigger phrases from agent description
3. Manually invoke via Task tool

### Skill Not Available

1. Verify plugin is installed and enabled
2. Check if skill is user-invocable (not all skills are)
3. Invoke it explicitly as `/<plugin>:<skill>`

## See Also

- [Agent Format Reference](agent-format.md)
- [Skill Format Reference](skill-format.md)
- [Plugin Development Guide](../development/plugin-development.md)
