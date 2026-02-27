---
name: professional-commit-workflow
description: Creates professional git commits with automated pre-commit checks for Java, Python, React, and documentation projects. Generates emoji conventional commit messages and analyzes staging status. Produces atomic commits following best practices.
---

# Professional Commit Workflow

## Overview

This skill automates the complete Git commit workflow with professional quality checks and conventional commit messages. It replaces the `/git-workflow:commit` command with a reusable, distributable skill.

**Special Features:**
- Automatic project detection (Java, Python, React, Documentation)
- Pre-commit validation with project-specific tools
- Emoji Conventional Commits (feat, fix, docs, etc.)
- Intelligent staging analysis with automatic add
- Atomic commit recommendations for multiple logical changes
- Performance-optimized through modular validator architecture

## Prerequisites

**Required:**
- Git (version 2.0+)
- Python 3.8+

**Optional (for specific validations):**
- **Java**: Maven or Gradle
- **Python**: ruff, black, pytest, mypy
- **React/Node.js**: npm/pnpm/yarn/bun, ESLint, Prettier
- **Docs**: LaTeX, markdownlint, AsciiDoc

```bash
# Install Python dependencies
pip install -r requirements.txt --break-system-packages
```

## Usage Workflow

1. **User initiates commit**: "Create a commit" or "Commit the changes"

2. **Detect options**:
   - `--no-verify`: Skips pre-commit checks
   - `--skip-tests`: Skips tests only
   - `--force-push`: Force push after commit (use with caution!)

3. **Execute project detection**:
   ```bash
   python scripts/project_detector.py
   ```
   Automatically detects:
   - Java (Maven: pom.xml, Gradle: build.gradle)
   - Python (pyproject.toml, requirements.txt, setup.py)
   - React/Node.js (package.json with react/next/vite)
   - Documentation (*.tex, *.md, *.adoc)

4. **Pre-commit validation** (unless `--no-verify`):
   ```bash
   python scripts/main.py --validate-only
   ```
   Executes project-specific checks:
   - **Java**: Build, Tests, Checkstyle, SpotBugs
   - **Python**: Ruff, Black, pytest, mypy
   - **React**: ESLint, Prettier, TypeScript, Build
   - **Docs**: LaTeX compile, markdownlint

5. **Staging analysis**:
   ```bash
   python scripts/git_analyzer.py --analyze-staging
   ```
   - Checks `git status` for staged files
   - Automatically adds changes if necessary
   - Displays overview of files to be committed

6. **Diff analysis**:
   ```bash
   python scripts/git_analyzer.py --analyze-diff
   ```
   - Analyzes `git diff` for logical changes
   - Detects multiple features/fixes in a single commit
   - Recommends splitting when appropriate

7. **Generate commit message**:
   ```bash
   python scripts/commit_message.py --generate
   ```
   - Detects commit type from changes
   - Generates Emoji Conventional Commit
   - German, imperative description
   - Format: `<emoji> <type>: <description>`

8. **Create commit**:
   ```bash
   git commit -m "$(python scripts/commit_message.py --output)"
   ```
   - **IMPORTANT:** No "Co-Authored-By" or "Generated with" suffixes

9. **Optional: Offer push**:
   ```bash
   git push origin <branch>
   ```

## Main Script Usage

```bash
# Standard commit workflow
python scripts/main.py

# Validation only (no commit)
python scripts/main.py --validate-only

# Skip checks
python scripts/main.py --no-verify

# Skip tests
python scripts/main.py --skip-tests

# With force push
python scripts/main.py --force-push
```

## Output Structure

**Successful workflow:**
```text
Project detected: React/TypeScript
Pre-commit checks passed (3/3)
  ESLint: 0 errors
  TypeScript: Compilation successful
  Build: Successful
Staging analysis: 5 files ready
Commit type detected: feat
Commit created: feat: Add user dashboard with metrics
```

**On validation failures:**
```text
Pre-commit checks failed (1/3)
  ESLint: 0 errors
  TypeScript: 2 errors found
    - src/components/Dashboard.tsx:12 - Type 'string' is not assignable to type 'number'
  Build: Successful

Commit aborted. Please fix errors or use --no-verify.
```

## Configuration

### commit_types.json

Defines emoji mappings for Conventional Commits:

```json
{
  "feat": {"emoji": "✨", "description": "New functionality"},
  "fix": {"emoji": "🐛", "description": "Bug fix"},
  "docs": {"emoji": "📚", "description": "Documentation"}
}
```

### validation_rules.json

Project-specific validation rules:

```json
{
  "java": {
    "build": true,
    "tests": true,
    "checkstyle": true
  },
  "python": {
    "ruff": true,
    "black": true,
    "pytest": true,
    "mypy": true
  }
}
```

## Error Handling

**Validation errors:**
- Display detailed error message
- Offer `--no-verify` option
- Refer to [docs/troubleshooting.md](docs/troubleshooting.md)

**Git errors:**
- Check Git status (untracked, conflicts)
- Refer to Git troubleshooting
- Offer manual commands

**Tool not found:**
- Graceful degradation (skip)
- Warn user about missing validation
- Recommend tool installation

## Best Practices

**Atomic commits:**
- Each commit = one logical unit
- Separate features, fixes, refactorings
- No "WIP" or "misc changes" commits

**Meaningful messages:**
- Describe "what" and "why", not "how"
- Imperative form: "Add", not "Added"
- First line 72 characters or fewer
- No automatic signatures

**Code quality:**
- All checks passed before commit
- Tests pass
- Build successful
- No debug output or commented-out code

**Complete guidelines:** [docs/best-practices.md](docs/best-practices.md)

## References

- **[Pre-Commit Checks](docs/pre-commit-checks.md)**: Detailed check descriptions
- **[Commit Types](docs/commit-types.md)**: All emoji types with examples
- **[Best Practices](docs/best-practices.md)**: Comprehensive Git commit best practices
- **[Troubleshooting](docs/troubleshooting.md)**: Troubleshooting for common issues
