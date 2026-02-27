---
description: Validate command files, documentation, and best practices
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---

# Command Validation Tool

This command validates Claude Code commands for:

- YAML frontmatter structure
- Markdown syntax
- Documentation
- Best practices (Progressive Disclosure, naming conventions)

## Usage

```bash
# Validate a specific command
/core:check-commands agents/_shared/commands/commit.md

# Or without path for interactive selection
/core:check-commands
```

## Validation Checks

### 1. YAML Frontmatter

**Required**:

- `description` (String, 1-100 characters)
- `category` (String, must correspond to an existing folder)

**Optional**:

- `allowed-tools` (Array of tool names)

**Format**:

```yaml
---
description: Brief description of the command
category: develop
allowed-tools:
  - Read
  - Write
---
```

### 2. Markdown Structure

- Must begin with frontmatter
- At least one H1 heading (`# Title`)
- Valid CommonMark format
- No broken links to detail files

### 3. Documentation

**For extensive commands (Progressive Disclosure)**:

- Detail files in `references/<command-name>/`
- References in the main command to detail files via `../references/`

**Example structure**:

```text
_shared/
├── commands/
│   └── commit.md                    # Main command
└── references/
    └── commit/                      # Detail folder
        ├── pre-commit-checks.md
        ├── commit-types.md
        ├── best-practices.md
        └── troubleshooting.md
```

### 4. Best Practices

**Naming conventions**:

- Lowercase with hyphens: `check-commands.md`
- No CamelCase or underscores: `checkCommands.md`, `check_commands.md`

**Progressive Disclosure**:

- Main command: 50-250 lines (overview + workflow)
- Details: Extracted into separate files
- References: Links to detail files at the end

**Description**:

- Short and concise (1-100 characters)
- Describes WHAT the command does
- Imperative form: "Creates..." not "Create..."
- **Language: English** (technical terms in English)

**Documentation (Markdown body)**:

- **Written primarily in English**
- Technical terms remain in English
- Domain-specific terms in English permitted
- Consistent language within a command

## Validation Workflow

When executing this command, proceed as follows:

1. **Determine command path**:
   - If no path provided: List all `.md` files in `agents/_shared/commands/`
   - User selects command

2. **Read file**:
   - Use Read tool
   - Check whether file exists

3. **Parse YAML frontmatter**:
   - Extract first block between `---`
   - Check required fields: `description`
   - Validate optional fields: `allowed-tools`
   - Format validation (no syntax errors)

4. **Validate Markdown**:
   - At least one H1 heading present
   - No broken internal links
   - Basic CommonMark structure

5. **Documentation check**:
   - If command > 250 lines: Warning for Progressive Disclosure
   - If references exist: Check `../references/<command>/`
   - If references present: Verify file existence

6. **Best practices check**:
   - Filename: Lowercase with hyphens
   - Description: 1-100 characters

7. **Output report**:

   ```markdown
   ## Validation Report: /commit

   YAML Frontmatter: Valid
   Markdown Structure: Valid
   Documentation: Complete
   Best Practices: Compliant
   Progressive Disclosure: Implemented (85 lines main, 1246 lines details)

   ### Details:
   - Description: "Creates professional Git commits..." (Valid length)
   - Detail files: 4 found in references/commit/ (all referenced)
   - Naming: commit.md (compliant)

   Command is fully compliant!
   ```

   When issues are found:

   ```markdown
   ## Validation Report: /example

   YAML Frontmatter: Missing 'description' field
   Markdown Structure: No H1 heading found
   Best Practices: Compliant
   File size: 312 lines - consider Progressive Disclosure

   ### Issues to fix:
   1. Add 'description' field to YAML frontmatter
   2. Add H1 heading (# Title) at the beginning
   3. Consider splitting into main + detail files (>250 lines)

   ### Recommended actions:
   - Add description: "Brief command description"
   - Add # heading after frontmatter
   - Create detail folder: references/example/
   ```

## Error Handling

- **File not found**: Clear error message with path
- **YAML parse error**: Show line and error
- **Missing required fields**: List all missing fields

## Integration with Other Commands

This command is useful:

- **Before commit**: Validate commands before committing
- **After changes**: Ensure everything still works
- **New commands**: Verify initial setup

## Examples

**Successful validation**:

```text
/core:check-commands agents/_shared/commands/commit.md
-> All checks passed
```

**Failed validation**:

```text
/core:check-commands agents/_shared/commands/broken.md
-> 3 issues found (see report)
```

**Interactive selection**:

```text
/core:check-commands
-> Shows list of all commands
-> User selects
-> Validation runs
```

## Notes

- This command should itself follow best practices
- Can serve as a template for other validation commands
- Extensible for additional checks (e.g., security, performance)
