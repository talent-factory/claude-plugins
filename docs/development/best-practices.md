# Best Practices

Follow these guidelines to create high-quality plugins that are easy to use, maintain, and extend.

---

## Plugin Design

### Keep Plugins Focused

Each plugin should have a clear, well-defined purpose. Don't create "kitchen sink" plugins that try to do everything.

=== "✅ Good"

    ```
    plugins/git-workflow/     → Git operations only
    plugins/code-quality/     → Code review and linting
    plugins/education/        → Teaching and learning
    ```

=== "❌ Bad"

    ```
    plugins/everything/       → Git, review, teaching, deployment, ...
    ```

### Follow Semantic Versioning

Use [SemVer](https://semver.org/) for all plugin versions:

| Change | Version Bump | Example |
|--------|-------------|---------|
| Breaking changes | Major | `1.0.0` → `2.0.0` |
| New features (backwards compatible) | Minor | `1.0.0` → `1.1.0` |
| Bug fixes | Patch | `1.0.0` → `1.0.1` |

Update versions in both `plugin.json` and `marketplace.json` simultaneously.

### Provide Complete READMEs

Every plugin README should include:

1. **Title and description** - What the plugin does
2. **Commands overview** - Table of all available commands
3. **Installation** - How to enable the plugin
4. **Usage examples** - Real-world scenarios
5. **Configuration** - Any required setup (e.g., MCP servers)

---

## Command Design

### Use Clear, Action-Oriented Names

Commands should be verbs in kebab-case:

| ✅ Good | ❌ Bad |
|---------|--------|
| `commit` | `git-stuff` |
| `create-pr` | `pr` |
| `check-commands` | `validator` |
| `create-prd` | `prd` |

### Keep Commands Focused

Each command should do one thing well. If a command does too much, split it into multiple commands.

=== "✅ Good"

    ```bash
    /commit          # Create a commit
    /create-pr       # Create a pull request
    ```

=== "❌ Bad"

    ```bash
    /git-everything  # Commits, creates PR, pushes, deploys...
    ```

### Write Clear Instructions

Claude follows your command instructions literally. Be specific:

=== "✅ Clear"

    ```markdown
    ## Instructions

    1. Run `git status` to check for changes
    2. If no changes exist, inform the user and stop
    3. Analyze the diff with `git diff`
    4. Generate a commit message using Emoji Conventional Commits format
    5. Stage all changes with `git add`
    6. Create the commit
    ```

=== "❌ Vague"

    ```markdown
    ## Instructions

    Make a commit with a good message.
    ```

### Define Allowed Tools

Use YAML frontmatter to restrict which tools a command can use:

```yaml
---
description: Create professional git commits
allowed-tools:
  - "Bash(git *)"
  - Read
  - Glob
---
```

This prevents commands from performing unintended operations.

### Support Arguments

For commands that accept input, define arguments clearly:

```yaml
---
description: Create a PRD
argument-hint: "<feature description> [output path]"
---
```

And reference them in the instructions with `$ARGUMENTS`.

---

## Agent Design

### Define Clear Expertise

Each agent should have a well-defined domain of expertise:

| ✅ Focused | ❌ Too Broad |
|-----------|-------------|
| Java development expert | General programming helper |
| Code review specialist | Everything reviewer |
| Markdown formatting | Document processor |

### Use Appropriate Colors

Follow the color convention for agent types:

| Color | Domain |
|-------|--------|
| `blue` | Development/coding |
| `green` | Testing/quality |
| `purple` | Architecture/design |
| `orange` | Education/learning |
| `red` | Security/critical |

### Include Interaction Examples

Show how the agent should respond in different scenarios:

```markdown
## Examples

### Example: User asks about Spring Boot

User: "How do I create a REST controller?"

You should:
1. Explain the @RestController annotation
2. Show a minimal working example
3. Explain request mapping
4. Mention common pitfalls
```

---

## Documentation

### Use References for Details

Keep command files concise by moving detailed documentation to `references/`:

```text
commands/
  commit.md              → Main command (concise)
references/commit/
  best-practices.md      → Detailed best practices
  commit-types.md        → Full list of commit types
  troubleshooting.md     → Common problems and solutions
```

Link from commands to references:

```markdown
**Details**: [best-practices.md](../references/commit/best-practices.md)
```

### Write for Your Audience

| Audience | Write in | Example |
|----------|----------|---------|
| Users | Simple, task-oriented language | "Run `/commit` to create a commit" |
| Developers | Technical, detailed language | "The YAML frontmatter defines the tool permissions scope" |
| Contributors | Process-oriented language | "Fork the repo, create a feature branch, submit a PR" |

### Keep Documentation in Sync

When you modify a command, update:

- [ ] The command file itself
- [ ] The plugin README
- [ ] Related reference files
- [ ] Marketplace description (if scope changed)

---

## Security

### Never Hardcode Secrets

```yaml
# ❌ Never do this
env:
  API_KEY: "sk-1234567890abcdef"

# ✅ Use environment variables
env:
  LINEAR_API_KEY: "<your-api-key>"
```

### Restrict Tool Access

Only grant tools that a command actually needs:

```yaml
# ✅ Minimal permissions
allowed-tools:
  - "Bash(git *)"
  - Read

# ❌ Too permissive (no restrictions)
# (omitting allowed-tools grants access to everything)
```

### Ask Before Destructive Operations

Commands should confirm before performing irreversible actions:

```markdown
## Instructions

Before running `git push --force`:
1. Show the user what will be force-pushed
2. Warn about potential data loss
3. Ask for explicit confirmation
```

---

## User Experience

### Provide Sensible Defaults

Commands should work with minimal input:

```bash
/commit                    # Works with defaults
/commit --no-verify        # Override when needed
/create-plan               # Reads PRD.md from CWD
/create-plan --prd my.md   # Custom input when needed
```

### Give Clear Feedback

Commands should inform users about what's happening:

```markdown
## Instructions

After each step, show the user what was done:

✅ Pre-commit checks passed
✅ 3 files staged
✅ Commit created: abc1234
✅ Message: ✨ feat: Add user dashboard
```

### Handle Errors Gracefully

```markdown
## Error Handling

If no changes are detected:

1. Run `git status` to verify
2. Show the user: "No changes to commit"
3. Suggest: "Make changes first, then run /commit again"

If tests fail:

1. Show the failing test output
2. Suggest fixes if possible
3. Offer: "Use /commit --no-verify to skip checks"
```

---

## Performance

### Keep Prompts Concise

Long command files consume more tokens. Structure them efficiently:

- Use bullet points instead of paragraphs
- Reference details in `references/` instead of inlining
- Avoid repeating information

### Use Skills for Complex Logic

For commands with significant logic (formatters, validators), consider using Skills with Python scripts:

```text
skills/professional-commit-workflow/
├── SKILL.md
├── config/
│   └── commit_types.json
└── scripts/
    ├── main.py
    └── git_analyzer.py
```

Benefits:

- Faster execution
- Lower token consumption
- Reusable across plugins

---

## Naming Conventions

### Files

| Component | Convention | Example |
|-----------|-----------|---------|
| Command files | kebab-case | `create-pr.md` |
| Agent files | kebab-case | `java-tutor.md` |
| Plugin directories | kebab-case | `git-workflow/` |
| Reference directories | kebab-case | `commit-types.md` |

### Identifiers

| Component | Convention | Example |
|-----------|-----------|---------|
| Plugin name | kebab-case | `"name": "git-workflow"` |
| Command name | kebab-case | `"name": "create-pr"` |
| Agent name | kebab-case | `"name": "java-tutor"` |
| Branch names | type/description | `feature/add-dark-mode` |

### Commit Messages

Follow the [Emoji Conventional Commits](../reference/conventional-commits.md) format:

```
✨ feat: Füge Benutzer-Dashboard hinzu
🐛 fix: Behebe Speicherleck in API
📚 docs: Aktualisiere Installationsanleitung
🔧 chore: Aktualisiere Dependencies
```

---

## Checklist Before Submission

- [ ] Plugin has a clear, focused purpose
- [ ] `plugin.json` is valid with all required fields
- [ ] Version follows semantic versioning
- [ ] README is comprehensive with usage examples
- [ ] All commands have YAML frontmatter
- [ ] Commands have `allowed-tools` defined
- [ ] Agent colors follow the convention
- [ ] No secrets or credentials in any file
- [ ] Tested locally with `claude --plugin-dir`
- [ ] `/check-commands` and `/check-agents` pass
- [ ] Marketplace entry updated (if new plugin)
- [ ] CHANGELOG updated

---

## Related Resources

- **[Plugin Development](plugin-development.md)** - Create plugins
- **[Testing](testing.md)** - Test your plugins
- **[CI/CD](ci-cd.md)** - Automated validation
- **[Contributing](contributing.md)** - Submission process
- **[Conventional Commits](../reference/conventional-commits.md)** - Commit format reference
