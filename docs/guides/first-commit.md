# Your First Commit with `/commit`

Learn how to create professional git commits using the git-workflow plugin's `/commit` command.

**Duration**: 5 minutes  
**Level**: Beginner  
**Plugin**: git-workflow

---

## What You'll Learn

- How to use the `/commit` command
- Understanding pre-commit checks
- Emoji conventional commit format
- Best practices for commit messages

---

## Prerequisites

- Git repository initialized
- git-workflow plugin installed
- Changes staged or unstaged in your repository

---

## Step 1: Make Some Changes

First, make some changes to your code:

```bash
# Example: Edit a file
echo "console.log('Hello, World!');" > hello.js

# Check status
git status
```

---

## Step 2: Use `/commit` Command

In Claude Code, simply type:

```bash
/commit
```

Claude will:

1. **Analyze your changes** - Review staged and unstaged files
2. **Run pre-commit checks** - Execute relevant tests and linters
3. **Suggest commit message** - Generate emoji conventional commit
4. **Stage and commit** - Complete the commit process

---

## Step 3: Review Pre-Commit Checks

The `/commit` command automatically runs checks based on your project type:

=== "JavaScript/Node.js"

    ```
    ✓ ESLint validation
    ✓ Prettier formatting
    ✓ TypeScript compilation (if applicable)
    ✓ Jest/Vitest tests
    ```

=== "Python"

    ```
    ✓ Ruff/Black formatting
    ✓ pytest tests
    ✓ mypy type checking
    ```

=== "Java"

    ```
    ✓ Maven/Gradle build
    ✓ Checkstyle validation
    ✓ JUnit tests
    ```

=== "Documentation"

    ```
    ✓ LaTeX compilation
    ✓ Markdown linting
    ```

---

## Step 4: Understand Commit Message Format

The `/commit` command uses **Emoji Conventional Commits**:

```
✨ feat: Add user authentication
│   │     │
│   │     └─ Description (imperative mood)
│   └─────── Type (feat, fix, docs, etc.)
└─────────── Emoji (visual indicator)
```

### Common Commit Types

| Emoji | Type | Usage |
|-------|------|-------|
| ✨ | `feat` | New features |
| 🐛 | `fix` | Bug fixes |
| 📚 | `docs` | Documentation changes |
| 💎 | `style` | Code formatting |
| ♻️ | `refactor` | Code restructuring |
| ⚡ | `perf` | Performance improvements |
| 🧪 | `test` | Testing |
| 🔧 | `chore` | Build/tools/config |

---

## Step 5: Review and Confirm

Claude will show you:

1. **Files changed** - What will be committed
2. **Pre-commit results** - All checks passed/failed
3. **Suggested commit message** - Emoji conventional format
4. **Confirmation prompt** - Approve or modify

Example output:

```
📝 Commit Summary
─────────────────
Files changed: 3
  M hello.js
  M package.json
  A tests/hello.test.js

Pre-commit checks: ✅ All passed

Suggested commit message:
✨ feat: Add hello world example with tests

Proceed with commit? (yes/no)
```

---

## Step 6: Complete the Commit

Type `yes` to confirm, and Claude will:

1. Stage all changes (if not already staged)
2. Create the commit with the message
3. Show commit hash and summary

```
✅ Commit successful!

Commit: abc1234
Message: ✨ feat: Add hello world example with tests
Files: 3 changed, 42 insertions(+), 5 deletions(-)
```

---

## Advanced Options

### Skip Pre-Commit Checks

If you need to commit quickly without checks:

```bash
/commit --no-verify
```

!!! warning "Use Sparingly"
    Skipping checks can lead to broken builds. Only use when necessary.

### Skip Tests Only

Run linters but skip time-consuming tests:

```bash
/commit --skip-tests
```


## Best Practices

### ✅ Do

- **Write clear descriptions** - Explain what and why
- **Use imperative mood** - "Add feature" not "Added feature"
- **Keep commits focused** - One logical change per commit
- **Run pre-commit checks** - Catch issues early
- **Review changes** - Verify what you're committing

### ❌ Don't

- **Commit broken code** - Always ensure tests pass
- **Mix unrelated changes** - Keep commits focused
- **Skip pre-commit checks** - Unless absolutely necessary
- **Use vague messages** - "Fix stuff" is not helpful
- **Commit sensitive data** - Check for secrets/credentials

---

## Troubleshooting

### Pre-Commit Checks Fail

**Problem**: Tests or linters fail during pre-commit.

**Solution**:

1. Review the error messages
2. Fix the issues in your code
3. Run `/commit` again

### Wrong Commit Type Suggested

**Problem**: Claude suggests wrong commit type.

**Solution**:

1. When prompted, modify the commit message
2. Choose the correct type from the list
3. Provide a better description

### Changes Not Detected

**Problem**: `/commit` doesn't see your changes.

**Solution**:

1. Verify changes exist: `git status`
2. Ensure you're in the repository root
3. Check if files are ignored in `.gitignore`

---

## What's Next?

Now that you've mastered basic commits, try:

1. **[Create Your First PR](create-first-pr.md)** - Learn pull request workflow
2. **[PRD-Based Workflow](prd-workflow.md)** - Plan before coding
3. **[Plugin Catalog](../plugins/index.md)** - Explore other plugins

---

## Related Resources

- **[Git Workflow Plugin](../plugins/git-workflow.md)** - Full plugin documentation
- **[Conventional Commits Reference](../reference/conventional-commits.md)** - Complete commit type list
- **[Contributing Guide](../development/contributing.md)** - Contribute to this project

