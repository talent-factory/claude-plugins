---
description: Validate agent files (frontmatter fields, model values, colors)
category: validation
argument-hint: "[agent-path-or-folder]"
allowed-tools:
  - Bash
  - Read
  - Glob
---

# Check Agents

Validate agent definition files of a plugin with the bundled script, then explain what the findings mean.

## Steps

1. **Choose the target.** Use the given path (a file or an `agents/` folder). Without an argument, check every `agents/` folder of the current plugin or repository (`plugins/*/agents`). If there is none, say so.
2. **Run the validator:**

   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/validate_frontmatter.py" <path> --kind agents
   ```

   If it exits with code 2, PyYAML is missing: `pip install pyyaml`.
3. **Report** the findings grouped by file, say what to change, and offer to apply the fixes. Do not edit files unasked.

## What is checked

- Required: `name` (kebab-case, equal to the file name), `description`, `category`, `model`, `color`.
- `model` is one of `sonnet`, `opus`, `haiku`. Full model IDs such as `claude-opus-4` are rejected.
- `description` states what the agent does and when to use it, in the third person.
- `tools`, if present, restricts the available tools. Other standard fields: `disallowedTools`, `permissionMode`, `maxTurns`, `skills`, `mcpServers`, `hooks`, `memory`, `background`, `isolation`. Anything else is reported as non-standard.
- Suggested colors by function: `blue` development, `green` testing and quality, `red` security, `yellow` documentation, `purple` research, `orange` build and deployment, `cyan` data.
