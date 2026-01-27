# Create Your First Pull Request with `/create-pr`

Learn how to create professional pull requests using the git-workflow plugin's `/create-pr` command.

**Duration**: 10 minutes
**Level**: Beginner
**Plugin**: git-workflow

---

## What You'll Learn

- How to use the `/create-pr` command
- Branch management and naming conventions
- Writing effective PR descriptions
- Code formatting integration
- Draft PR workflow

---

## Prerequisites

- Git repository with a remote on GitHub
- git-workflow plugin installed
- Changes committed (ideally via `/commit`)
- GitHub CLI (`gh`) installed and authenticated

---

## Step 1: Prepare Your Changes

Before creating a PR, you need committed changes. If you haven't committed yet, use `/commit` first:

```bash
# Make changes to your code
echo "function greet(name) { return 'Hello ' + name; }" > greet.js

# Commit using the git-workflow plugin
/commit
```

!!! tip "Integration with `/commit`"
    The `/create-pr` command does **not** create commits itself. If you have uncommitted changes, it will call `/commit` automatically.

---

## Step 2: Run `/create-pr`

In Claude Code, simply type:

```bash
/create-pr
```

Claude will guide you through the entire process:

1. **Check branch status** - Determine if you're on a protected branch
2. **Create feature branch** - If needed, with a descriptive name
3. **Format code** - Run project-specific formatters
4. **Push to remote** - Upload your branch
5. **Create the PR** - With title, description, and test plan

---

## Step 3: Understand Branch Management

The command handles branches automatically based on where you are:

=== "On Protected Branch (main/develop)"

    Claude creates a new feature branch for you:

    ```
    ⚠️ You're on 'develop' (protected branch)
    ✅ Creating branch: feature/add-greeting-function-2025-01-26
    ✅ Branch created and checked out
    ```

    Branch naming follows the convention: `<type>/<description>-<date>`

=== "On Feature Branch"

    Claude uses your existing branch:

    ```
    ✅ Already on feature branch: feature/add-greeting-function
    ✅ Using current branch for PR
    ```

### Branch Naming Convention

| Type | Prefix | Example |
|------|--------|---------|
| New feature | `feature/` | `feature/user-dashboard-2025-01-26` |
| Bug fix | `fix/` | `fix/login-crash-2025-01-26` |
| Documentation | `docs/` | `docs/api-reference-2025-01-26` |
| Refactoring | `refactor/` | `refactor/auth-module-2025-01-26` |

---

## Step 4: Code Formatting

Before the PR is created, Claude runs code formatters based on your project type:

=== "JavaScript/TypeScript"

    ```
    ✓ Biome formatting applied
    ✓ No issues found
    ```

=== "Python"

    ```
    ✓ Black formatting applied
    ✓ isort imports sorted
    ✓ Ruff checks passed
    ```

=== "Java"

    ```
    ✓ Google Java Format applied
    ✓ All files formatted
    ```

!!! note "Skip Formatting"
    Use `--no-format` if you want to skip automatic formatting:
    ```bash
    /create-pr --no-format
    ```

---

## Step 5: Review the PR Description

Claude generates a professional PR description with:

1. **Summary** - What changes were made and why
2. **Changes list** - Bullet points of all modifications
3. **Test plan** - Checklist for verifying the changes

Example PR output:

```markdown
## Beschreibung

Füge Greeting-Funktion mit Personalisierung hinzu.

## Änderungen

- Neue `greet()` Funktion in `greet.js`
- Unit Tests in `greet.test.js`
- Aktualisierte README mit Beispielen

## Test-Plan

- [ ] Manuelle Tests durchgeführt
- [ ] Automatische Tests laufen durch
- [ ] Code-Review bereit
```

---

## Step 6: Verify Your PR

After creation, Claude shows the PR URL:

```
✅ Pull Request created!

🔗 https://github.com/your-org/your-repo/pull/42
📝 Title: ✨ feat: Füge Greeting-Funktion hinzu
🎯 Target: main ← feature/add-greeting-function-2025-01-26
```

Click the link to review your PR on GitHub.

---

## Advanced Options

### Create a Draft PR

For work-in-progress changes that aren't ready for review:

```bash
/create-pr --draft
```

!!! info "When to Use Draft PRs"
    Draft PRs are great for:

    - Getting early feedback on your approach
    - Running CI/CD checks before the code is complete
    - Showing team members that you're working on something

### Specify Target Branch

By default, PRs target `main`. Change this with:

```bash
/create-pr --target develop
```

### Single Commit Mode

Squash all changes into one commit:

```bash
/create-pr --single-commit
```

### Use Professional Workflow Skill

For optimized performance with intelligent branch management:

```bash
/create-pr --with-skills
```

---

## Best Practices

### ✅ Do

- **Write clear PR titles** - Describe the "what" in under 50 characters
- **Explain the "why"** - The description should explain motivation, not just list changes
- **Keep PRs small** - Aim for 150-400 lines of changes
- **Self-review first** - Check your own diff before submitting
- **Link related issues** - Reference issues with `Fixes #123` or `Closes #456`
- **Use draft PRs** - For early feedback on work in progress

### ❌ Don't

- **Create huge PRs** - Large PRs are hard to review and more likely to have bugs
- **Mix unrelated changes** - Each PR should address one concern
- **Skip the description** - Reviewers need context to provide good feedback
- **Force push without warning** - Communicate with reviewers before rewriting history
- **Merge without CI passing** - Wait for all checks to complete

---

## Troubleshooting

### PR Creation Fails

**Problem**: `gh pr create` returns an error.

**Solution**:

1. Verify GitHub CLI is authenticated: `gh auth status`
2. Check remote is configured: `git remote -v`
3. Ensure branch is pushed: `git push -u origin HEAD`

### Branch Already Exists

**Problem**: The suggested branch name already exists.

**Solution**:

1. Claude will detect this and suggest an alternative name
2. Or delete the old branch if it's no longer needed: `git branch -d old-branch`

### Formatting Changes Detected

**Problem**: Code formatter modified files after your commit.

**Solution**:

1. Claude automatically commits formatting changes
2. These appear as a separate commit in your PR
3. To avoid this, run formatters before committing

---

## Complete Workflow Example

Here's the full workflow from change to PR:

```bash
# 1. Make your code changes
# ... edit files ...

# 2. Create a professional commit
/commit

# 3. Create the pull request
/create-pr

# Output:
# ✅ Branch: feature/add-greeting-function-2025-01-26
# ✅ Formatted: 2 files with Biome
# ✅ Pushed to origin
# ✅ PR created: https://github.com/your-org/your-repo/pull/42
```

---

## What's Next?

Now that you can create professional PRs, try:

1. **[PRD-Based Workflow](prd-workflow.md)** - Plan features before coding
2. **[Linear Integration](linear-integration.md)** - Connect with project management
3. **[Plugin Catalog](../plugins/index.md)** - Explore other plugins

---

## Related Resources

- **[Git Workflow Plugin](../plugins/git-workflow.md)** - Full plugin documentation
- **[Your First Commit](first-commit.md)** - Learn the commit workflow
- **[Conventional Commits Reference](../reference/conventional-commits.md)** - Commit message format
- **[Contributing Guide](../development/contributing.md)** - Contribute to this project
