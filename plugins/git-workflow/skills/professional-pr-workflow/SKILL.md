---
name: professional-pr-workflow
description: Automates pull request creation with branch management, code formatting, and integration with professional-commit-workflow. Supports GitHub CLI, automated PR descriptions, and project-specific formatters (Biome, Black, Prettier).
---

# Professional PR Workflow

## Overview

Automates the complete pull request workflow: branch creation, code formatting, commit integration, and PR creation via GitHub CLI.

**Features:**
- Intelligent branch management - detects protected branches
- Integration with professional-commit-workflow - no commit duplication
- Automatic code formatting (Biome, Black, Prettier, etc.)
- GitHub CLI integration - PR creation, labels, issue linking
- Meaningful PR descriptions with test plan
- Draft PR support - mark WIP PRs

## Prerequisites

**Required:**
- Git (2.0+)
- Python 3.8+
- GitHub CLI (`gh`) - installed and authenticated

**Optional (for code formatting):**
- **JavaScript/TypeScript**: Biome or Prettier
- **Python**: Black, isort, Ruff
- **Java**: Google Java Format
- **Markdown**: markdownlint

## Usage Workflow

1. **Check branch status**:
   - Protected branch (main/master/develop)? -> Create new branch
   - Feature branch? -> Use current branch

2. **Commit changes**:
   - Uncommitted changes? -> Invoke `professional-commit-workflow`
   - Already committed? -> Use existing commits

3. **Format code** (optional, skip with `--no-format`)

4. **Create PR**:
   - Push branch to remote
   - Generate PR title and description
   - Create PR via `gh pr create`

## Main Script Usage

```bash
# Standard PR workflow
python scripts/main.py

# Draft PR
python scripts/main.py --draft

# Without formatting
python scripts/main.py --no-format

# Single commit (all changes in one)
python scripts/main.py --single-commit

# Change target branch
python scripts/main.py --target develop
```

## Supported Formatters

### JavaScript/TypeScript
- **Biome** (preferred): `biome format --write .`
- **Prettier**: `prettier --write .`
- **ESLint**: `eslint --fix .`

### Python
- **Black**: `black .`
- **isort**: `isort .`
- **Ruff**: `ruff format .`

### Java
- **Google Java Format**: Via Maven/Gradle plugin

### Markdown
- **markdownlint**: `markdownlint --fix **/*.md`
- **mdformat**: `mdformat .`

## Output Example

```text
============================================================
  Professional PR Workflow
============================================================

Branch status: main (protected)
New branch created: feature/user-dashboard-2024-12-21

Code formatting:
  Biome: 5 files formatted
  ESLint: 0 errors

Branch pushed: origin/feature/user-dashboard-2024-12-21

PR created: #42
  https://github.com/user/repo/pull/42

PR workflow completed successfully
```

## Configuration

### pr_config.json

```json
{
  "protected_branches": ["main", "master", "develop"],
  "default_target": "main",
  "auto_delete_branch": false,
  "formatters": {
    "javascript": "biome",
    "python": "black",
    "java": "google-java-format"
  }
}
```

## Error Handling

**Branch errors**: Checks existing branches, offers alternative names
**Format errors**: Shows details, enables `--no-format` fallback
**GitHub CLI errors**: Checks authentication, shows gh setup instructions
**Push errors**: Retry logic, manual push commands

## References

- **[Code Formatting](docs/code-formatting.md)**: Formatter details
- **[Commit Workflow](docs/commit-workflow.md)**: Integration with commit skill
- **[PR Template](docs/pr-template.md)**: PR best practices
- **[Troubleshooting](docs/troubleshooting.md)**: Troubleshooting
