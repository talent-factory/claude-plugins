---
description: Create a new branch, commit changes, and open a pull request with automated commit splitting
category: develop
allowed-tools:
  - "Bash(git *)"
  - "Bash(gh *)"
  - "Bash(biome *)"
  - Read
  - Glob
---

# Claude Command: Create Pull Request

Automatically create a new branch, analyze changes, and create a professional pull request.

**All commit messages and PR descriptions are written in German.**

## Usage

Standard pull request:

```bash
/git-workflow:create-pr
```

With options:

```bash
/git-workflow:create-pr --draft          # Create draft PR
/git-workflow:create-pr --no-format      # Skip code formatting
/git-workflow:create-pr --single-commit  # All changes in one commit
/git-workflow:create-pr --target main    # Specify target branch (default: main)
/git-workflow:create-pr --with-skills    # Create a pull request using professional-pr-workflow
```

## Workflow

### With `--with-skills` Option

When `--with-skills` is used, the **professional-pr-workflow skill** is activated and the remaining command workflow is bypassed:

1. **Skill execution**: Use the professional-pr-workflow skill
   - Location: `../skills/professional-pr-workflow/`
   - Features: Intelligent branch management, code formatting, GitHub CLI integration
   - Integration with professional-commit-workflow for commits

2. **Skill details**: See [professional-pr-workflow README](../skills/professional-pr-workflow/README.md)

### Standard Workflow (without `--with-skills`)

1. **Check branch status** -- IMPORTANT
   - Check current branch: `git branch --show-current`
   - **Protected branches** (`main`, `master`, `develop`):
     - A new branch MUST be created
     - No commits directly on protected branches
   - **Feature branch** (e.g., `feature/xyz`, `bugfix/abc`):
     - No new branch needed, use current branch
   - Details: [commit-workflow.md](../references/create-pr/commit-workflow.md)

2. **Check changes**
   - Detect uncommitted or already committed changes
   - If uncommitted changes -> invoke `/git-workflow:commit`
   - If commits present -> use them
   - Details: [commit-workflow.md](../references/create-pr/commit-workflow.md)

3. **Create branch** (only when on protected branch)
   - Generate meaningful branch name: `<type>/<description>-<date>`
   - Check for existing branches
   - Create branch from current HEAD
   - Example: `feature/user-dashboard-2024-10-30`
   - **Skip** if already on feature branch

4. **Code formatting** (skip with `--no-format`)
   - **JavaScript/TypeScript**: Biome
   - **Python**: Black, isort, Ruff
   - **Java**: Google Java Format
   - **Markdown**: markdownlint
   - Details: [code-formatting.md](../references/create-pr/code-formatting.md)

5. **Create pull request**
   - Push branch to remote
   - Generate meaningful PR title
   - Create detailed PR description with test plan
   - Link relevant issues
   - Set appropriate labels
   - Template: [pr-template.md](../references/create-pr/pr-template.md)

## Integration with /commit

**Important**: This command does NOT create its own commits!

- **Uncommitted changes**: Invokes `/git-workflow:commit`
- **Existing commits**: Uses them for the PR
- **No commit duplication**: Commit logic only in `/git-workflow:commit`

**Workflow details**: [commit-workflow.md](../references/create-pr/commit-workflow.md)

## PR Template

```markdown
## Description

[Brief description of changes]

## Changes

- Change 1
- Change 2

## Test Plan

- [ ] Manual tests performed
- [ ] Automated tests pass
- [ ] Code review ready

## Breaking Changes

[If applicable]
```

**Complete template**: [pr-template.md](../references/create-pr/pr-template.md)

## Best Practices

- **Meaningful titles**: Describe the "what" in 50 characters
- **Detailed description**: Explain the "why" and "how"
- **Self-review**: Review your own changes before submission
- **Small PRs**: Keep PRs focused and reviewable (150-400 lines)
- **Clear commits**: Each commit should be independently comprehensible

**More best practices**: [pr-template.md](../references/create-pr/pr-template.md)

## Professional PR Workflow Skill

The `--with-skills` option uses the **professional-pr-workflow skill** for improved performance and extended features.

### Advantages vs. Standard Command

| Feature | Standard Command | Skill (`--with-skills`) |
|---------|------------------|------------------------|
| Performance | Standard | Optimized |
| Branch management | Manual | Intelligent |
| Code formatting | Optional | Integrated |
| GitHub CLI | Manual | Automated |
| Draft PR support | Basic | Extended |
| Dependencies | Python | Zero dependencies |

### Skill Features

- **Intelligent branch management**: Automatic branch creation with meaningful names
- **Integration with professional-commit-workflow**: Seamless commit integration
- **Code formatting**: Biome, Black, Prettier, Google Java Format
- **GitHub CLI integration**: Automatic PR creation with labels and templates
- **Draft PR support**: Extended draft PR functionality
- **Zero Python dependencies**: Only Python standard library

### Skill Usage

```bash
# Direct skill execution (alternative)
cd ../skills/professional-pr-workflow
python scripts/main.py

# Or via command with --with-skills
/git-workflow:create-pr --with-skills
```

**Skill documentation**: [professional-pr-workflow/README.md](../skills/professional-pr-workflow/README.md)

## Additional Information

- **Code Formatting**: [code-formatting.md](../references/create-pr/code-formatting.md)
- **Commit Workflow**: [commit-workflow.md](../references/create-pr/commit-workflow.md)
- **PR Template & Best Practices**: [pr-template.md](../references/create-pr/pr-template.md)
- **Troubleshooting**: [troubleshooting.md](../references/create-pr/troubleshooting.md)
