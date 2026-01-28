# Skill Format Reference

Complete technical reference for creating skill definition files in Claude Code plugins.

---

## Overview

Skills are reusable, multi-step workflows that combine instructions, scripts, references, and assets into a cohesive capability. Unlike commands (single actions) or agents (specialized assistants), skills represent complete processes that Claude can execute, such as creating professional commits, managing tasks, or humanizing AI-generated text.

---

## Directory Structure

```
plugins/your-plugin/skills/your-skill/
├── SKILL.md              # Main skill definition (required)
├── scripts/              # Helper scripts (optional)
│   ├── script1.sh
│   └── script2.py
├── references/           # Documentation and guides (optional)
│   ├── guide.md
│   └── troubleshooting.md
└── assets/               # Templates and files (optional)
    ├── template.txt
    └── config.json
```

**Naming Convention**: Lowercase, hyphen-separated directory names (e.g., `professional-commit-workflow/`, `tasknotes/`)

---

## SKILL.md Structure

The `SKILL.md` file is the main definition and must include:

1. **Frontmatter** (YAML) - Metadata and configuration
2. **Title** (H1 heading) - Skill name
3. **Description** - Skill purpose and capabilities
4. **Purpose** section - When and why to use
5. **Workflow** section - Step-by-step process
6. **Resources** section - Available supporting files

---

## Basic Template

```markdown
---
name: your-skill
description: Brief description of skill purpose
version: 1.0.0
tags: [tag1, tag2, tag3]
author: Your Name
---

# Your Skill Name

This skill provides [primary capability]. It helps users [main benefit] by [approach].

## Purpose

Use this skill when you need to:

- Accomplish task 1
- Accomplish task 2
- Accomplish task 3

**When to use:**

- Scenario 1
- Scenario 2

**When NOT to use:**

- Scenario 1
- Scenario 2

## Workflow

Follow these steps to execute this skill:

### 1. Preparation

- Check prerequisite 1
- Verify prerequisite 2
- Gather required information

### 2. Execution

1. **Step 1**: Detailed action
   - Sub-action 1
   - Sub-action 2

2. **Step 2**: Detailed action
   - Sub-action 1
   - Sub-action 2

3. **Step 3**: Detailed action
   - Sub-action 1
   - Sub-action 2

### 3. Validation

- Verify outcome 1
- Confirm outcome 2
- Report results to user

## Resources

This skill includes the following resources:

### Scripts

- **scripts/script1.sh** - Purpose and usage
- **scripts/script2.py** - Purpose and usage

### References

- **references/guide.md** - Detailed guide
- **references/troubleshooting.md** - Common issues

### Assets

- **assets/template.txt** - Template file
- **assets/config.json** - Configuration example

## Examples

### Example 1: Basic Usage

**Scenario**: User wants to [goal]

**Process**:

1. Claude reads user request
2. Executes workflow steps 1-3
3. Uses script1.sh for automation
4. Returns result to user

**Outcome**: [Expected result]

### Example 2: Advanced Usage

**Scenario**: User wants to [complex goal]

**Process**:

1. Claude analyzes context
2. Adapts workflow based on conditions
3. Uses multiple scripts and references
4. Validates and reports

**Outcome**: [Expected result]

## Best Practices

### ✅ Do

- Follow the workflow sequence
- Validate inputs before processing
- Use provided scripts for automation
- Reference documentation when needed
- Report progress to user

### ❌ Don't

- Skip validation steps
- Ignore error conditions
- Modify workflow without understanding
- Assume user context without checking
```

## Troubleshooting

### Issue 1: [Common Problem]

**Symptoms**: Description of the problem

**Solution**:

1. Check condition 1
2. Verify condition 2
3. Apply fix

### Issue 2: [Common Problem]

**Symptoms**: Description of the problem

**Solution**:

1. Check condition 1
2. Verify condition 2
3. Apply fix
```

---

## Frontmatter (Required)

The YAML frontmatter at the top of SKILL.md contains skill metadata:

```yaml
---
name: professional-commit-workflow
description: Create professional git commits with emoji conventional commits format
version: 2.0.0
tags: [git, commits, workflow, automation]
author: Talent Factory GmbH
license: MIT
---
```

### Frontmatter Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Skill identifier (lowercase, hyphen-separated, max 64 chars) |
| `description` | string | Yes | What the skill does and when to use it. Claude uses this for skill selection. Max 1024 chars. Use `>` for multiline YAML. Write in third person. |
| `version` | string | No | Skill version (semantic versioning) |
| `allowed-tools` | list | No | Tools Claude can use without asking permission (e.g., Read, Write, Edit, Grep, Glob, Bash) |
| `disable-model-invocation` | boolean | No | Set `true` to prevent automatic loading. Manual-only via `/name`. Default: `false` |
| `user-invocable` | boolean | No | Set `false` to hide from `/` menu. Background knowledge only. Default: `true` |
| `argument-hint` | string | No | Hint for autocomplete (e.g., `[filename]`, `[issue-number]`) |
| `tags` | array | No | Keywords for discoverability |
| `author` | string | No | Skill creator |
| `license` | string | No | License type (MIT, Apache-2.0, etc.) |

---

## Detailed Sections

### 1. Title and Introduction (Required)

```markdown
# Professional Commit Workflow

This skill provides a comprehensive workflow for creating professional git commits using emoji conventional commits format. It helps developers maintain consistent, meaningful commit history by automating commit message formatting, validation, and best practices enforcement.
```

- **Format**: H1 heading followed by introduction paragraph
- **Content**: Clear explanation of skill purpose and benefits
- **Length**: 2-4 sentences
- **Style**: Present tense, active voice

### 2. Purpose Section (Required)

```markdown
## Purpose

Use this skill when you need to:

- Create git commits that follow conventional commits standard
- Ensure commit messages are clear and descriptive
- Automate commit message formatting with emoji prefixes
- Validate commit messages before committing
- Maintain consistent commit history across team

**When to use:**

- After making code changes that need to be committed
- When working on feature branches
- Before creating pull requests
- During code review iterations

**When NOT to use:**

- For merge commits (use git's default merge message)
- For automated commits from CI/CD
- When rebasing or amending commits (use git commands directly)
```

- **Format**: H2 heading with bullet points
- **Content**: Clear use cases and scenarios
- **Include**: When to use AND when not to use
- **Structure**: Organized by context

### 3. Workflow Section (Required)

```markdown
## Workflow

Follow these steps to create a professional commit:

### 1. Analyze Changes

1. **Check git status**
   - Run: `git status`
   - Identify modified, added, and deleted files
   - Categorize changes by type (feature, fix, docs, etc.)

2. **Review diff**
   - Run: `git diff` for unstaged changes
   - Run: `git diff --staged` for staged changes
   - Understand the scope and impact of changes

3. **Determine commit type**
   - Based on changes, select appropriate type:
     - ✨ `feat` - New feature
     - 🐛 `fix` - Bug fix
     - 📚 `docs` - Documentation
     - ♻️ `refactor` - Code refactoring
     - 🧪 `test` - Tests
     - 🎨 `style` - Formatting
     - ⚡ `perf` - Performance
     - 🔧 `chore` - Maintenance

### 2. Generate Commit Message

1. **Create description**
   - Use German imperative form (e.g., "Füge hinzu", "Behebe", "Aktualisiere")
   - Keep under 50 characters
   - Be specific and descriptive
   - Start with verb

2. **Format message**
   - Structure: `<emoji> <type>: <description>`
   - Example: `✨ feat: Füge Benutzer-Dashboard hinzu`
   - Validate format matches conventional commits

3. **Add body (if needed)**
   - Explain WHY, not WHAT (code shows what)
   - Reference issues: `Fixes #123`
   - List breaking changes: `BREAKING CHANGE: ...`

### 3. Stage and Commit

1. **Stage files**
   - Run: `git add <files>` for specific files
   - Or: `git add .` for all changes
   - Verify with: `git status`

2. **Create commit**
   - Run: `git commit -m "<message>"`
   - If body needed: `git commit -m "<message>" -m "<body>"`
   - Verify commit created: `git log -1`

3. **Validate commit**
   - Check commit message format
   - Verify files included
   - Confirm commit hash generated
```

- **Format**: H2 heading with H3 subheadings for phases
- **Content**: Detailed step-by-step process
- **Structure**: Numbered steps with sub-bullets
- **Include**: Commands to run, decision points, validation steps

### 4. Resources Section (Required)

```markdown
## Resources

This skill includes the following resources:

### Scripts

- **scripts/validate-commit-msg.sh** - Validates commit message format against conventional commits standard
- **scripts/generate-changelog.py** - Generates changelog from commit history
- **scripts/check-branch.sh** - Verifies current branch is appropriate for commits

### References

- **references/conventional-commits.md** - Complete guide to conventional commits format
- **references/emoji-guide.md** - Emoji prefix reference for all commit types
- **references/german-imperative.md** - Guide to German imperative verb forms
- **references/troubleshooting.md** - Common issues and solutions

### Assets

- **assets/commit-template.txt** - Template for commit messages
- **assets/pre-commit-hook** - Git hook for automatic validation
- **assets/commitlint.config.js** - Configuration for commitlint tool
```

- **Format**: H2 heading with H3 subheadings for categories
- **Content**: List all supporting files with descriptions
- **Include**: Purpose and usage for each file
- **Organization**: Group by type (scripts, references, assets)

### 5. Examples Section (Recommended)

```markdown
## Examples

### Example 1: Feature Commit

**Scenario**: User added a new user dashboard component

**Process**:

1. Claude analyzes changes: new React component, tests, and documentation
2. Determines commit type: `feat` (new feature)
3. Generates message: `✨ feat: Füge Benutzer-Dashboard-Komponente hinzu`
4. Stages files: `src/components/UserDashboard.tsx`, `src/components/UserDashboard.test.tsx`, `docs/components.md`
5. Creates commit with generated message
6. Validates commit format
7. Reports: `Created commit abc1234: ✨ feat: Füge Benutzer-Dashboard-Komponente hinzu`

**Outcome**: Professional commit with proper format, all relevant files included

### Example 2: Bug Fix with Issue Reference

**Scenario**: User fixed a login validation bug (issue #42)

**Process**:

1. Claude analyzes changes: modified validation logic in auth service
2. Determines commit type: `fix` (bug fix)
3. Generates message: `🐛 fix: Behebe Login-Validierungsfehler`
4. Adds body: `Fixes #42\n\nValidierung prüft jetzt korrekt auf leere Passwörter`
5. Stages files: `src/services/auth.service.ts`
6. Creates commit with message and body
7. Validates format and issue reference
8. Reports: `Created commit def5678: 🐛 fix: Behebe Login-Validierungsfehler (Fixes #42)`

**Outcome**: Bug fix commit with issue reference and explanation

### Example 3: Documentation Update

**Scenario**: User updated API documentation

**Process**:

1. Claude analyzes changes: modified README.md and API docs
2. Determines commit type: `docs` (documentation)
3. Generates message: `📚 docs: Aktualisiere API-Dokumentation`
4. Stages files: `README.md`, `docs/api/endpoints.md`
5. Creates commit
6. Validates format
7. Reports: `Created commit ghi9012: 📚 docs: Aktualisiere API-Dokumentation`

**Outcome**: Documentation commit with appropriate emoji and type
```

- **Format**: H2 heading with H3 subheadings for each example
- **Content**: Real-world usage scenarios
- **Include**: Scenario, process steps, outcome
- **Variety**: Show different commit types and situations

---

## Supporting Files

### Scripts Directory

Scripts automate parts of the workflow:

**Example: scripts/validate-commit-msg.sh**

```bash
#!/bin/bash
# Validates commit message format

MESSAGE="$1"

# Check format: <emoji> <type>: <description>
if ! echo "$MESSAGE" | grep -qE '^[^ ]+ (feat|fix|docs|style|refactor|test|chore|perf): .+$'; then
    echo "Error: Invalid commit message format"
    echo "Expected: <emoji> <type>: <description>"
    exit 1
fi

# Check description length
DESCRIPTION=$(echo "$MESSAGE" | sed 's/^[^ ]* [^:]*: //')
if [ ${#DESCRIPTION} -gt 50 ]; then
    echo "Warning: Description exceeds 50 characters (${#DESCRIPTION})"
fi

echo "Commit message format valid"
exit 0
```

### References Directory

References provide detailed documentation:

**Example: references/conventional-commits.md**

```markdown
# Conventional Commits Reference

Complete guide to conventional commits format used in this project.

## Format

```
<emoji> <type>: <description>

[optional body]

[optional footer]
```

## Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
...
```

### Assets Directory

Assets provide templates and configuration:

**Example: assets/commit-template.txt**

```yaml
---
name: professional-commit-workflow
description: Create professional git commits with emoji conventional commits format
version: 2.0.0
tags: [git, commits, workflow, automation]
author: Talent Factory GmbH
license: MIT
---
```
<emoji> <type>: <description>

# Why this change is needed:
#

# What this change does:
#

# Breaking changes (if any):
#

# Issues closed:
# Fixes #
```

- **Format**: H1 heading followed by introduction paragraph
- **Content**: Clear explanation of skill purpose and benefits
- **Length**: 2-4 sentences
- **Style**: Present tense, active voice

### 2. Purpose Section (Required)

```markdown
## Purpose

Use this skill when you need to:

- Create git commits that follow conventional commits standard
- Ensure commit messages are clear and descriptive
- Automate commit message formatting with emoji prefixes
- Validate commit messages before committing
- Maintain consistent commit history across team

**When to use:**

- After making code changes that need to be committed
- When working on feature branches
- Before creating pull requests
- During code review iterations

**When NOT to use:**

- For merge commits (use git's default merge message)
- For automated commits from CI/CD
- When rebasing or amending commits (use git commands directly)
```

- **Format**: H2 heading with bullet points
- **Content**: Clear use cases and scenarios
- **Include**: When to use AND when not to use
- **Structure**: Organized by context

### 3. Workflow Section (Required)

```markdown
## Workflow

Follow these steps to create a professional commit:

### 1. Analyze Changes

1. **Check git status**
   - Run: `git status`
   - Identify modified, added, and deleted files
   - Categorize changes by type (feature, fix, docs, etc.)

2. **Review diff**
   - Run: `git diff` for unstaged changes
   - Run: `git diff --staged` for staged changes
   - Understand the scope and impact of changes

3. **Determine commit type**
   - Based on changes, select appropriate type:
     - ✨ `feat` - New feature
     - 🐛 `fix` - Bug fix
     - 📚 `docs` - Documentation
     - ♻️ `refactor` - Code refactoring
     - 🧪 `test` - Tests
     - 🎨 `style` - Formatting
     - ⚡ `perf` - Performance
     - 🔧 `chore` - Maintenance

### 2. Generate Commit Message

1. **Create description**
   - Use German imperative form (e.g., "Füge hinzu", "Behebe", "Aktualisiere")
   - Keep under 50 characters
   - Be specific and descriptive
   - Start with verb

2. **Format message**
   - Structure: `<emoji> <type>: <description>`
   - Example: `✨ feat: Füge Benutzer-Dashboard hinzu`
   - Validate format matches conventional commits

3. **Add body (if needed)**
   - Explain WHY, not WHAT (code shows what)
   - Reference issues: `Fixes #123`
   - List breaking changes: `BREAKING CHANGE: ...`

### 3. Stage and Commit

1. **Stage files**
   - Run: `git add <files>` for specific files
   - Or: `git add .` for all changes
   - Verify with: `git status`

2. **Create commit**
   - Run: `git commit -m "<message>"`
   - If body needed: `git commit -m "<message>" -m "<body>"`
   - Verify commit created: `git log -1`

3. **Validate commit**
   - Check commit message format
   - Verify files included
   - Confirm commit hash generated
```

- **Format**: H2 heading with H3 subheadings for phases
- **Content**: Detailed step-by-step process
- **Structure**: Numbered steps with sub-bullets
- **Include**: Commands to run, decision points, validation steps

### 4. Resources Section (Required)

```markdown
## Resources

This skill includes the following resources:

### Scripts

- **scripts/validate-commit-msg.sh** - Validates commit message format against conventional commits standard
- **scripts/generate-changelog.py** - Generates changelog from commit history
- **scripts/check-branch.sh** - Verifies current branch is appropriate for commits

### References

- **references/conventional-commits.md** - Complete guide to conventional commits format
- **references/emoji-guide.md** - Emoji prefix reference for all commit types
- **references/german-imperative.md** - Guide to German imperative verb forms
- **references/troubleshooting.md** - Common issues and solutions

### Assets

- **assets/commit-template.txt** - Template for commit messages
- **assets/pre-commit-hook** - Git hook for automatic validation
- **assets/commitlint.config.js** - Configuration for commitlint tool
```

- **Format**: H2 heading with H3 subheadings for categories
- **Content**: List all supporting files with descriptions
- **Include**: Purpose and usage for each file
- **Organization**: Group by type (scripts, references, assets)

### 5. Examples Section (Recommended)

```markdown
## Examples

### Example 1: Feature Commit

**Scenario**: User added a new user dashboard component

**Process**:

1. Claude analyzes changes: new React component, tests, and documentation
2. Determines commit type: `feat` (new feature)
3. Generates message: `✨ feat: Füge Benutzer-Dashboard-Komponente hinzu`
4. Stages files: `src/components/UserDashboard.tsx`, `src/components/UserDashboard.test.tsx`, `docs/components.md`
5. Creates commit with generated message
6. Validates commit format
7. Reports: `Created commit abc1234: ✨ feat: Füge Benutzer-Dashboard-Komponente hinzu`

**Outcome**: Professional commit with proper format, all relevant files included

### Example 2: Bug Fix with Issue Reference

**Scenario**: User fixed a login validation bug (issue #42)

**Process**:

1. Claude analyzes changes: modified validation logic in auth service
2. Determines commit type: `fix` (bug fix)
3. Generates message: `🐛 fix: Behebe Login-Validierungsfehler`
4. Adds body: `Fixes #42\n\nValidierung prüft jetzt korrekt auf leere Passwörter`
5. Stages files: `src/services/auth.service.ts`
6. Creates commit with message and body
7. Validates format and issue reference
8. Reports: `Created commit def5678: 🐛 fix: Behebe Login-Validierungsfehler (Fixes #42)`

**Outcome**: Bug fix commit with issue reference and explanation

### Example 3: Documentation Update

**Scenario**: User updated API documentation

**Process**:

1. Claude analyzes changes: modified README.md and API docs
2. Determines commit type: `docs` (documentation)
3. Generates message: `📚 docs: Aktualisiere API-Dokumentation`
4. Stages files: `README.md`, `docs/api/endpoints.md`
5. Creates commit
6. Validates format
7. Reports: `Created commit ghi9012: 📚 docs: Aktualisiere API-Dokumentation`

**Outcome**: Documentation commit with appropriate emoji and type
```

- **Format**: H2 heading with H3 subheadings for each example
- **Content**: Real-world usage scenarios
- **Include**: Scenario, process steps, outcome
- **Variety**: Show different commit types and situations

---

## Supporting Files

### Scripts Directory

Scripts automate parts of the workflow:

**Example: scripts/validate-commit-msg.sh**

```bash
#!/bin/bash
# Validates commit message format

MESSAGE="$1"

# Check format: <emoji> <type>: <description>
if ! echo "$MESSAGE" | grep -qE '^[^ ]+ (feat|fix|docs|style|refactor|test|chore|perf): .+$'; then
    echo "Error: Invalid commit message format"
    echo "Expected: <emoji> <type>: <description>"
    exit 1
fi

# Check description length
DESCRIPTION=$(echo "$MESSAGE" | sed 's/^[^ ]* [^:]*: //')
if [ ${#DESCRIPTION} -gt 50 ]; then
    echo "Warning: Description exceeds 50 characters (${#DESCRIPTION})"
fi

echo "Commit message format valid"
exit 0
```

### References Directory

References provide detailed documentation:

**Example: references/conventional-commits.md**

```markdown
# Conventional Commits Reference

Complete guide to conventional commits format used in this project.

## Format

```
<emoji> <type>: <description>

[optional body]

[optional footer]
```

## Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
...
```

### Assets Directory

Assets provide templates and configuration:

**Example: assets/commit-template.txt**

```
<emoji> <type>: <description>

# Why this change is needed:
#

# What this change does:
#

# Breaking changes (if any):
#

# Issues closed:
# Fixes #
```

---

## Best Practices for Skill Design

### Workflow Design

✅ **Do**:

- Break workflow into clear phases
- Include validation at each step
- Provide decision points for different scenarios
- Specify exact commands to run
- Include error handling

❌ **Don't**:

- Create overly complex workflows
- Skip validation steps
- Assume context without checking
- Use vague instructions
- Ignore edge cases

### Resource Organization

✅ **Do**:

- Group related files logically
- Document each resource's purpose
- Keep scripts focused and reusable
- Provide complete examples in references
- Use clear, descriptive filenames

❌ **Don't**:

- Mix unrelated resources
- Create monolithic scripts
- Skip documentation for scripts
- Use cryptic filenames
- Duplicate information across files

### Example: Good vs. Bad Skill Structure

**❌ Bad**:

```
skills/commit/
├── SKILL.md              # Vague instructions
└── script.sh             # Does everything, poorly documented
```

**✅ Good**:

```
skills/professional-commit-workflow/
├── SKILL.md              # Clear, detailed workflow
├── scripts/
│   ├── validate-commit-msg.sh    # Single responsibility
│   ├── generate-changelog.py     # Well-documented
│   └── check-branch.sh           # Focused task
├── references/
│   ├── conventional-commits.md   # Complete guide
│   ├── emoji-guide.md            # Quick reference
│   └── troubleshooting.md        # Common issues
└── assets/
    ├── commit-template.txt       # Reusable template
    └── pre-commit-hook           # Ready to use
```

---

## Real-World Examples

### Example 1: Professional Commit Workflow Skill

From the git-workflow plugin:

**Directory Structure**:

```
plugins/git-workflow/skills/professional-commit-workflow/
├── SKILL.md
├── scripts/
│   └── validate-commit-msg.sh
├── references/
│   ├── conventional-commits.md
│   ├── emoji-guide.md
│   └── troubleshooting.md
└── assets/
    └── commit-template.txt
```

**Key Features**:

- Comprehensive workflow for creating professional commits
- Automated validation of commit message format
- Detailed references for conventional commits and emoji usage
- Template for consistent commit messages
- Troubleshooting guide for common issues

### Example 2: TaskNotes Skill

From the obsidian plugin:

**Directory Structure**:

```
plugins/obsidian/skills/tasknotes/
├── SKILL.md
├── references/
│   ├── api-reference.md
│   ├── query-syntax.md
│   └── examples.md
└── assets/
    └── query-templates.json
```

**Key Features**:

- Integration with Obsidian TaskNotes Plugin API
- Natural language task management
- Comprehensive API reference
- Query syntax documentation
- Example queries for common scenarios

### Example 3: Humanizer Skill

From the core plugin:

**Directory Structure**:

```
plugins/core/skills/humanizer/
├── SKILL.md
└── references/
    ├── humanization-guide.md
    └── examples.md
```

**Key Features**:

- Transforms AI-generated text to sound more human
- Detailed guide on humanization techniques
- Examples of before/after transformations
- No scripts needed (pure text transformation)

---

## Validation Checklist

Before submitting a skill, verify:

- [ ] SKILL.md includes frontmatter with name, description, version
- [ ] Title clearly identifies the skill
- [ ] Introduction explains purpose and benefits
- [ ] Purpose section explains when to use (and when not to)
- [ ] Workflow section provides detailed, actionable steps
- [ ] Resources section lists all supporting files
- [ ] At least 2 examples provided showing different scenarios
- [ ] All scripts are executable and include comments
- [ ] All scripts have clear, single responsibilities
- [ ] All references are complete and well-organized
- [ ] All assets are properly formatted and documented
- [ ] Directory structure follows naming conventions
- [ ] Markdown syntax is valid
- [ ] Code examples use proper syntax highlighting
- [ ] No duplicate or redundant information

---

## Testing Your Skill

### Local Testing

1. **Create skill directory**:
   ```bash
   mkdir -p plugins/your-plugin/skills/your-skill
   cd plugins/your-plugin/skills/your-skill
   ```

2. **Add SKILL.md and resources**:
   ```bash
   touch SKILL.md
   mkdir -p scripts references assets
   ```

3. **Test with Claude Code**:
   ```bash
   claude --plugin-dir ./plugins/your-plugin
   ```

4. **Verify skill is loaded**:
   - Check that skill appears in plugin capabilities
   - Test workflow steps manually
   - Verify scripts execute correctly
   - Validate references are accessible

### Integration Testing

1. **Test with real scenarios**:
   - Execute complete workflow from start to finish
   - Test edge cases and error conditions
   - Verify all resources are used correctly

2. **Validate outputs**:
   - Check that workflow produces expected results
   - Verify error messages are clear
   - Confirm validation steps work correctly

3. **User experience**:
   - Ensure workflow is intuitive
   - Verify instructions are clear
   - Check that examples match real usage

---

## Best Practices for Skill Design

### Workflow Design

✅ **Do**:

- Break workflow into clear phases
- Include validation at each step
- Provide decision points for different scenarios
- Specify exact commands to run
- Include error handling

❌ **Don't**:

- Create overly complex workflows
- Skip validation steps
- Assume context without checking
- Use vague instructions
- Ignore edge cases

### Resource Organization

✅ **Do**:

- Group related files logically
- Document each resource's purpose
- Keep scripts focused and reusable
- Provide complete examples in references
- Use clear, descriptive filenames

❌ **Don't**:

- Mix unrelated resources
- Create monolithic scripts
- Skip documentation for scripts
- Use cryptic filenames
- Duplicate information across files

### Example: Good vs. Bad Skill Structure

**❌ Bad**:

```
skills/commit/
├── SKILL.md              # Vague instructions
└── script.sh             # Does everything, poorly documented
```

**✅ Good**:

```
skills/professional-commit-workflow/
├── SKILL.md              # Clear, detailed workflow
├── scripts/
│   ├── validate-commit-msg.sh    # Single responsibility
│   ├── generate-changelog.py     # Well-documented
│   └── check-branch.sh           # Focused task
├── references/
│   ├── conventional-commits.md   # Complete guide
│   ├── emoji-guide.md            # Quick reference
│   └── troubleshooting.md        # Common issues
└── assets/
    ├── commit-template.txt       # Reusable template
    └── pre-commit-hook           # Ready to use
```

---

## Real-World Examples

### Example 1: Professional Commit Workflow Skill

From the git-workflow plugin:

**Directory Structure**:

```
plugins/git-workflow/skills/professional-commit-workflow/
├── SKILL.md
├── scripts/
│   └── validate-commit-msg.sh
├── references/
│   ├── conventional-commits.md
│   ├── emoji-guide.md
│   └── troubleshooting.md
└── assets/
    └── commit-template.txt
```

**Key Features**:

- Comprehensive workflow for creating professional commits
- Automated validation of commit message format
- Detailed references for conventional commits and emoji usage
- Template for consistent commit messages
- Troubleshooting guide for common issues

### Example 2: TaskNotes Skill

From the obsidian plugin:

**Directory Structure**:

```
plugins/obsidian/skills/tasknotes/
├── SKILL.md
├── references/
│   ├── api-reference.md
│   ├── query-syntax.md
│   └── examples.md
└── assets/
    └── query-templates.json
```

**Key Features**:

- Integration with Obsidian TaskNotes Plugin API
- Natural language task management
- Comprehensive API reference
- Query syntax documentation
- Example queries for common scenarios

### Example 3: Humanizer Skill

From the core plugin:

**Directory Structure**:

```
plugins/core/skills/humanizer/
├── SKILL.md
└── references/
    ├── humanization-guide.md
    └── examples.md
```

**Key Features**:

- Transforms AI-generated text to sound more human
- Detailed guide on humanization techniques
- Examples of before/after transformations
- No scripts needed (pure text transformation)

### Example 4: Markdown Syntax Formatter Skill

From the education plugin:

**Directory Structure**:

```
plugins/education/skills/markdown-syntax-formatter/
├── SKILL.md
├── swiss-german-conventions.md
└── linter-exceptions.md
```

**Key Features**:

- Converts visual formatting into proper Markdown syntax
- Fixes heading hierarchies and document structure
- Progressive disclosure with two reference files loaded on demand
- Swiss German orthography support for German-language documents
- Context-aware linter exception handling
- Uses `allowed-tools` to declare Read, Write, Edit, Grep, Glob permissions
- Multiline `description` with trigger keywords for automatic activation

**Why this is a good example for BSc students**:

This skill demonstrates several important patterns:

1. **Progressive disclosure**: Core instructions stay in SKILL.md (207 lines), detailed conventions live in separate reference files that load only when needed
2. **Separation of concerns**: Language conventions and linter exceptions are isolated into their own files
3. **Discoverability**: The description includes both what the skill does ("Converts text...") and when to use it ("Use this skill when formatting...")
4. **No scripts needed**: Pure instruction-based skill without code dependencies

---

## Validation Checklist

Before submitting a skill, verify:

- [ ] SKILL.md includes frontmatter with name, description, version
- [ ] Title clearly identifies the skill
- [ ] Introduction explains purpose and benefits
- [ ] Purpose section explains when to use (and when not to)
- [ ] Workflow section provides detailed, actionable steps
- [ ] Resources section lists all supporting files
- [ ] At least 2 examples provided showing different scenarios
- [ ] All scripts are executable and include comments
- [ ] All scripts have clear, single responsibilities
- [ ] All references are complete and well-organized
- [ ] All assets are properly formatted and documented
- [ ] Directory structure follows naming conventions
- [ ] Markdown syntax is valid
- [ ] Code examples use proper syntax highlighting
- [ ] No duplicate or redundant information

---

## Testing Your Skill

### Local Testing

1. **Create skill directory**:
   ```bash
   mkdir -p plugins/your-plugin/skills/your-skill
   cd plugins/your-plugin/skills/your-skill
   ```

2. **Add SKILL.md and resources**:
   ```bash
   touch SKILL.md
   mkdir -p scripts references assets
   ```

3. **Test with Claude Code**:
   ```bash
   claude --plugin-dir ./plugins/your-plugin
   ```

4. **Verify skill is loaded**:
   - Check that skill appears in plugin capabilities
   - Test workflow steps manually
   - Verify scripts execute correctly
   - Validate references are accessible

### Integration Testing

1. **Test with real scenarios**:
   - Execute complete workflow from start to finish
   - Test edge cases and error conditions
   - Verify all resources are used correctly

2. **Validate outputs**:
   - Check that workflow produces expected results
   - Verify error messages are clear
   - Confirm validation steps work correctly

3. **User experience**:
   - Ensure workflow is intuitive
   - Verify instructions are clear
   - Check that examples match real usage

---

## Related Resources

- **[Command Format](command-format.md)** - Command definition format
- **[Agent Format](agent-format.md)** - Agent definition format
- **[Plugin Development](../development/plugin-development.md)** - Complete development guide
- **[Best Practices](../development/best-practices.md)** - Plugin development best practices
- **[Conventional Commits](conventional-commits.md)** - Commit message format reference

