---
description: Validate command files (frontmatter fields, structure, file names)
category: validation
argument-hint: "[command-path-or-folder]"
allowed-tools:
  - Bash
  - Read
  - Glob
---

# Check Commands

Validate command files of a plugin with the bundled script, then explain what the findings mean.

## Steps

1. **Choose the target.** Use the given path (a file or a `commands/` folder). Without an argument, check every `commands/` folder of the current plugin or repository (`plugins/*/commands`).
2. **Run the validator:**

   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/validate_frontmatter.py" <path> --kind commands
   ```

   If it exits with code 2, PyYAML is missing: `pip install pyyaml`.
3. **Report** the findings grouped by file. For each one say what to change, and offer to apply the fix. Do not edit files unasked.

## What is checked

- Frontmatter block present and valid YAML.
- `description` present and not empty (one line, English, in the imperative).
- `allowed-tools` present (a list of tool names).
- No `name` or `usage` field: they break command registration. Optional: `category`, `argument-hint`, `model`, `disable-model-invocation`.
- File name lowercase kebab-case; at least one H1 heading in the body.

For skills use `/validate-marketplace --section skills`, which also checks name length, description length and triggers.
