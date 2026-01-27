# Command Format Reference

Complete technical reference for creating command definition files in Claude Code plugins.

---

## Overview

Commands are user-invocable actions defined in Markdown files. When a user types `/command-name` in Claude Code, the command's instructions guide Claude's behavior. Commands are the primary way users interact with plugins.

---

## Location

```
plugins/your-plugin/commands/your-command.md
```

**Naming Convention**: Lowercase, hyphen-separated (e.g., `create-pr.md`, `check-commands.md`)

---

## Required Structure

Every command file must include:

1. **Title** (H1 heading) - Command name
2. **Description** - What the command does
3. **Usage** section - How to invoke it
4. **Purpose** section - When and why to use it
5. **Instructions** section - Step-by-step guidance for Claude

---

## Basic Template

```markdown
# Command Name

Brief one-sentence description of what this command does.

## Usage

```
/command-name [options]
```

## Purpose

Explain when and why users should use this command. What problem does it solve?

## Instructions

Step-by-step instructions for Claude to follow:

1. First, do this
2. Then, do that
3. Finally, complete with this

## Examples

### Example 1: Basic Usage

```
/command-name
```

Expected outcome: Description of what happens.

### Example 2: With Options

```
/command-name --option value
```

Expected outcome: Description of what happens.

## Best Practices

- ✅ Do this
- ❌ Don't do that

## Troubleshooting

### Common Issue 1

**Problem**: Description of the problem

**Solution**: How to fix it
```

---

## Detailed Sections

### 1. Title (Required)

```markdown
# Create Pull Request
```

- **Format**: H1 heading (`#`)
- **Style**: Title case, descriptive
- **Length**: 2-5 words
- **Examples**:
    - ✅ `Create Pull Request`
    - ✅ `Check Commands`
    - ✅ `Build Skill`
    - ❌ `PR` (too short)
    - ❌ `Create a Pull Request for Your Changes` (too long)

### 2. Description (Required)

```markdown
Create professional pull requests with automated formatting and comprehensive descriptions.
```

- **Format**: Plain text paragraph
- **Length**: 1-2 sentences
- **Content**: Clear explanation of command purpose
- **Style**: Active voice, present tense

### 3. Usage Section (Required)

```markdown
## Usage

```
/create-pr [options]
```

**Options:**

- `--draft` - Create as draft PR
- `--target <branch>` - Target branch (default: main)
- `--no-format` - Skip code formatting
```

- **Format**: H2 heading (`##`)
- **Content**: Command syntax and available options
- **Code blocks**: Use triple backticks for command examples
- **Options**: List all available flags and arguments

### 4. Purpose Section (Required)

```markdown
## Purpose

Use this command when you need to:

- Create a pull request from your current branch
- Ensure code is properly formatted before PR
- Generate professional PR descriptions automatically
- Follow team PR conventions consistently

**When to use:**

- After committing changes to a feature branch
- When ready for code review
- Before merging work into main branch

**When NOT to use:**

- On protected branches (main, develop) - command will create feature branch first
- Without committed changes - use `/commit` first
```

- **Format**: H2 heading
- **Content**: Clear use cases and scenarios
- **Structure**: Bullet points for readability
- **Include**: When to use AND when not to use

### 5. Instructions Section (Required)

```markdown
## Instructions

Follow these steps to create a pull request:

1. **Check current branch**
   - Verify you're not on a protected branch (main, develop)
   - If on protected branch, create a feature branch with format: `<type>/<description>-<date>`
   - Types: feature/, fix/, docs/, refactor/

2. **Format code**
   - Detect project type (JavaScript, Python, Java)
   - Run appropriate formatter (Biome, Black, Google Java Format)
   - Commit formatting changes if any

3. **Push to remote**
   - Push current branch to origin
   - Set upstream tracking

4. **Generate PR description**
   - Analyze all commits on the branch
   - Create summary of changes
   - List modified files
   - Generate test plan checklist

5. **Create pull request**
   - Use GitHub CLI (`gh pr create`)
   - Set title from most recent commit
   - Use generated description
   - Target main branch (or specified with --target)
   - Mark as draft if --draft flag provided

6. **Confirm success**
   - Display PR URL
   - Show PR number
   - Confirm target branch
```

- **Format**: H2 heading
- **Content**: Detailed step-by-step process
- **Structure**: Numbered list with sub-bullets
- **Detail level**: Specific enough for Claude to execute
- **Include**: Decision points, error handling, edge cases

### 6. Examples Section (Recommended)

```markdown
## Examples

### Example 1: Basic PR Creation

```
/create-pr
```

**What happens:**

1. Checks you're on feature branch `feature/user-dashboard`
2. Formats code with Biome
3. Pushes to origin
4. Creates PR targeting main
5. Returns: `https://github.com/org/repo/pull/42`

### Example 2: Draft PR

```
/create-pr --draft
```

Creates a draft PR for early feedback without requesting reviews.

### Example 3: Custom Target Branch

```
/create-pr --target develop
```

Creates PR targeting `develop` instead of `main`.
```

- **Format**: H2 heading with H3 subheadings for each example
- **Content**: Real-world usage scenarios
- **Include**: Command, expected behavior, output
- **Variety**: Show different options and use cases

### 7. Best Practices Section (Recommended)

```markdown
## Best Practices

### ✅ Do

- **Keep PRs small** - Aim for 150-400 lines of changes
- **Write clear titles** - Describe the "what" in under 50 characters
- **Self-review first** - Check your own diff before submitting
- **Link issues** - Reference with `Fixes #123` or `Closes #456`

### ❌ Don't

- **Create huge PRs** - Large PRs are hard to review
- **Mix unrelated changes** - Each PR should address one concern
- **Skip the description** - Reviewers need context
- **Force push without warning** - Communicate with reviewers first
```

- **Format**: H2 heading with H3 subheadings for Do/Don't
- **Content**: Actionable advice
- **Structure**: Bullet points with bold labels
- **Balance**: Equal number of do's and don'ts

### 8. Troubleshooting Section (Recommended)

```markdown
## Troubleshooting

### PR Creation Fails

**Problem**: `gh pr create` returns an error

**Solution**:

1. Verify GitHub CLI is authenticated: `gh auth status`
2. Check remote is configured: `git remote -v`
3. Ensure branch is pushed: `git push -u origin HEAD`

### Branch Already Exists

**Problem**: The suggested branch name already exists

**Solution**:

1. Claude will detect this and suggest an alternative name
2. Or delete the old branch if no longer needed: `git branch -d old-branch`
```

- **Format**: H2 heading with H3 subheadings for each issue
- **Content**: Common problems and solutions
- **Structure**: Problem/Solution pairs
- **Include**: Commands to diagnose and fix

### 9. References Section (Optional)

```markdown
## References

This command uses the following reference documentation:

- [PR Template](../references/create-pr/pr-template.md) - PR description structure
- [Code Formatting](../references/create-pr/code-formatting.md) - Formatter details
- [Troubleshooting](../references/create-pr/troubleshooting.md) - Extended troubleshooting

**Related Commands:**

- `/commit` - Create commits before PR
- `/pr-edit-history` - View PR description changes
```

- **Format**: H2 heading
- **Content**: Links to related documentation
- **Include**: Reference files, related commands, external resources

---

## Advanced Features

### Options and Flags

Document command options clearly:

```markdown
## Options

| Flag | Description | Default | Example |
|------|-------------|---------|---------|
| `--draft` | Create as draft PR | false | `/create-pr --draft` |
| `--target <branch>` | Target branch | main | `/create-pr --target develop` |
| `--no-format` | Skip formatting | false | `/create-pr --no-format` |
| `--single-commit` | Squash commits | false | `/create-pr --single-commit` |
```

### Conditional Logic

Include decision trees for complex commands:

```markdown
## Instructions

1. **Determine branch strategy**
   - IF on protected branch (main, develop):
     - Create new feature branch
     - Checkout new branch
   - ELSE IF on feature branch:
     - Use current branch
   - ELSE:
     - Ask user for confirmation

2. **Handle uncommitted changes**
   - IF unstaged changes exist:
     - Call `/commit` command
     - Wait for commit completion
   - ELSE IF no commits on branch:
     - Error: "No changes to create PR from"
   - ELSE:
     - Proceed with PR creation
```

### Integration with Other Commands

Reference other commands when appropriate:

```markdown
## Prerequisites

Before using this command:

1. Ensure changes are committed (use `/commit` if needed)
2. Verify GitHub CLI is installed and authenticated
3. Confirm you're in a git repository

**Automatic integration:**

- If uncommitted changes detected, `/commit` is called automatically
- If formatting needed, appropriate formatter is invoked
```

---

## Best Practices for Command Design

### Writing Instructions

✅ **Do**:

- Be specific and actionable
- Use numbered steps for sequential actions
- Include error handling
- Specify exact commands to run
- Explain WHY, not just WHAT

❌ **Don't**:

- Use vague language like "handle the files"
- Skip error cases
- Assume Claude knows your conventions
- Write instructions for humans (write for Claude)

### Example: Good vs. Bad Instructions

**❌ Bad**:

```markdown
## Instructions

1. Check the branch
2. Format the code
3. Create the PR
```

**✅ Good**:

```markdown
## Instructions

1. **Check current branch**
   - Run: `git branch --show-current`
   - IF branch is "main" or "develop":
     - Create feature branch: `git checkout -b feature/<description>-$(date +%Y-%m-%d)`
   - ELSE:
     - Continue with current branch

2. **Format code**
   - Detect project type by checking for:
     - `package.json` → JavaScript (use Biome)
     - `pyproject.toml` → Python (use Black)
     - `pom.xml` → Java (use Google Java Format)
   - Run formatter: `<formatter-command>`
   - IF files changed:
     - Stage changes: `git add .`
     - Commit: `git commit -m "💎 style: Format code"`

3. **Create pull request**
   - Generate description from commits: `git log main..HEAD --oneline`
   - Create PR: `gh pr create --title "<title>" --body "<description>"`
   - Display PR URL to user
```

---

## Validation Checklist

Before submitting a command file, verify:

- [ ] Title is clear and descriptive
- [ ] Description explains purpose in 1-2 sentences
- [ ] Usage section shows command syntax
- [ ] Purpose section explains when to use
- [ ] Instructions are detailed and actionable
- [ ] At least 2 examples provided
- [ ] Best practices included
- [ ] Common issues documented in troubleshooting
- [ ] Markdown syntax is valid
- [ ] Code blocks use proper syntax highlighting
- [ ] Links to references work correctly

---

## Related Resources

- **[Agent Format](agent-format.md)** - Agent definition format
- **[Skill Format](skill-format.md)** - Skill definition format
- **[Plugin Development](../development/plugin-development.md)** - Complete development guide
- **[Best Practices](../development/best-practices.md)** - Plugin development best practices

