# Skills and Agents Activation Guide

This guide explains how to activate and use skills and agents in Claude Code plugins.

## Agents

Agents are specialized AI assistants that handle complex, multi-step tasks autonomously. They are triggered automatically based on context or can be invoked manually.

### Automatic Activation

Agents activate automatically when Claude detects relevant context in your request. Each agent has triggering conditions defined in its `description` field.

**Example triggers:**

| Agent | Triggered by |
|-------|--------------|
| `java-developer` | Java performance questions, Spring Boot tasks |
| `python-expert` | Python refactoring, optimization tasks |
| `code-reviewer` | Code quality questions, PR reviews |
| `frontend-developer` | React/Next.js development tasks |

### Manual Activation via Task Tool

You can explicitly request an agent using the Task tool:

```
Use the java-developer agent to optimize this code
```

Claude will invoke:
```json
{
  "subagent_type": "development:java-developer",
  "prompt": "Optimize this code..."
}
```

### Agent Naming Convention

Agents are namespaced by plugin:

| Full Name | Plugin | Agent |
|-----------|--------|-------|
| `development:java-developer` | development | java-developer |
| `code-quality:python-expert` | code-quality | python-expert |
| `code-quality:frontend-developer` | code-quality | frontend-developer |
| `code-quality:code-reviewer` | code-quality | code-reviewer |
| `core:agent-expert` | core | agent-expert |
| `core:command-expert` | core | command-expert |
| `education:java-tutor` | education | java-tutor |

## Skills

Skills are reusable capabilities that can be invoked via commands, automatically triggered, or called directly.

### Activation Methods

#### 1. Via Command Flag

Some commands support a `--with-skills` flag to use an associated skill:

```bash
/commit --with-skills          # Uses professional-commit-workflow
/create-pr --with-skills       # Uses professional-pr-workflow
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
| `git-workflow:professional-commit-workflow` | git-workflow | professional-commit-workflow |
| `git-workflow:professional-pr-workflow` | git-workflow | professional-pr-workflow |
| `core:humanizer` | core | humanizer |
| `education:markdown-syntax-formatter` | education | markdown-syntax-formatter |
| `obsidian:tasknotes` | obsidian | tasknotes |

## Plugin-Specific Activation

### Git Workflow Plugin

**Skills:**

| Skill | Activation |
|-------|------------|
| `professional-commit-workflow` | `/commit --with-skills` |
| `professional-pr-workflow` | `/create-pr --with-skills` |

### Code Quality Plugin

**Agents:**

| Agent | Activation |
|-------|------------|
| `code-reviewer` | Automatic after code changes, or "review this code" |
| `python-expert` | Python-related questions, "optimize Python code" |
| `frontend-developer` | React/Next.js tasks, "create component" |

### Development Plugin

**Agent:**

| Agent | Activation |
|-------|------------|
| `java-developer` | Java/Spring Boot questions, "optimize Java performance" |

### Core Plugin

**Agents:**

| Agent | Activation |
|-------|------------|
| `agent-expert` | "Create an agent", "improve this agent" |
| `command-expert` | "Create a CLI command", "design command interface" |

**Skill:**

| Skill | Activation |
|-------|------------|
| `humanizer` | "Humanize this text", "remove AI patterns" |

### Education Plugin

**Agent:**

| Agent | Activation |
|-------|------------|
| `java-tutor` | Java learning questions, "explain this Java code" |

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
# Use java-developer agent for implementation
# Then use /commit --with-skills for fast, consistent commits
```

## Troubleshooting

### Agent Not Triggering

1. Check if the plugin is enabled in settings
2. Use explicit trigger phrases from agent description
3. Manually invoke via Task tool

### Skill Not Available

1. Verify plugin is installed and enabled
2. Check if skill is user-invocable (not all skills are)
3. Use associated command with `--with-skills` flag

## See Also

- [Agent Format Reference](agent-format.md)
- [Skill Format Reference](skill-format.md)
- [Plugin Development Guide](../development/plugin-development.md)
