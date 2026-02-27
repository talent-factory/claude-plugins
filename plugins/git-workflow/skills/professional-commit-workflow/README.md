# Professional Commit Workflow - Skill

Automates the complete Git commit workflow with professional quality checks and conventional commit messages for Java, Python, React, and documentation projects.

## Features

- ✅ **Automatic Project Detection** - Detects Java, Python, React, documentation
- ✅ **Pre-Commit Validation** - Build, tests, linting, type checking
- ✅ **Emoji Conventional Commits** - ✨ feat, 🐛 fix, 📚 docs, etc.
- ✅ **Intelligent Staging Analysis** - Automatic add when needed
- ✅ **Atomic Commit Recommendations** - Detects multiple logical changes
- ✅ **Performance Optimized** - Modular validator architecture
- ✅ **Reusable** - Works in any project
- ✅ **Zero Dependencies** - Uses only Python standard library

## Installation

### 1. Install Skill

```bash
# In Claude Code dotfiles
cd ~/.dotfiles/agents/claude/skills
git clone <this-repo> professional-commit-workflow

# Or: ZIP download and extract
unzip professional-commit-workflow.zip -d ~/.dotfiles/agents/claude/skills/
```

### 2. Python Dependencies (optional)

```bash
cd professional-commit-workflow
pip install -r requirements.txt --break-system-packages
```

**Note**: The skill works without additional Python packages. `requirements.txt` contains only optional tools for extended validation.

### 3. Make Skill Scripts Executable

```bash
chmod +x scripts/*.py
```

### 4. Use in Claude Code

The skill is automatically detected by Claude and can be used as follows:

```
Create a professional commit for the current changes
```

or

```
Run pre-commit checks and create a commit with emoji conventional commit format
```

## Usage

### Standard Workflow

```bash
# Via Python directly
python scripts/main.py

# Via Claude Code (recommended)
# Claude: "Create a commit with the professional-commit-workflow skill"
```

### With Options

```bash
# Skip checks
python scripts/main.py --no-verify

# Skip tests only
python scripts/main.py --skip-tests

# Validation only, no commit
python scripts/main.py --validate-only

# With force push (use with caution!)
python scripts/main.py --force-push
```

### Workflow Steps

1. **Project Detection**: Automatically detect Java/Python/React/Docs
2. **Git Status**: Analyze staging status, offer auto-add
3. **Pre-Commit Validation**: Project-specific checks
   - Java: Maven/Gradle build, tests, Checkstyle, SpotBugs
   - Python: Ruff, Black, isort, mypy, pytest
   - React: ESLint, Prettier, TypeScript, Jest/Vitest, build
   - Docs: LaTeX compile, markdownlint, AsciiDoc
4. **Diff Analysis**: Multiple changes? → Recommend atomic commits
5. **Commit Message**: Generate emoji conventional commit
6. **Create Commit**: Execute git commit
7. **Offer Push**: Optionally push to remote

## Project-Specific Validation

### Java Projects

**Detected by**: `pom.xml`, `build.gradle`, `build.gradle.kts`

**Checks**:
- ✅ Maven/Gradle compile
- ✅ Unit tests
- ✅ Checkstyle (if configured)
- ✅ SpotBugs (if configured)

**Example**:
```bash
# Maven
mvn compile
mvn test
mvn checkstyle:check

# Gradle
./gradlew build
./gradlew test
```

### Python Projects

**Detected by**: `pyproject.toml`, `requirements.txt`, `setup.py`

**Checks**:
- ✅ Ruff linting
- ✅ Black formatting
- ✅ isort import sorting
- ✅ mypy type checking (if configured)
- ✅ pytest tests

**Example**:
```bash
ruff check .
black --check .
isort --check-only .
mypy .
pytest
```

### React/Node.js Projects

**Detected by**: `package.json` with react/next/vue/svelte

**Checks**:
- ✅ ESLint
- ✅ Prettier formatting
- ✅ TypeScript compiler (if tsconfig.json exists)
- ✅ Tests (Jest/Vitest)
- ✅ Production build

**Example**:
```bash
npm run lint
npx prettier --check .
tsc --noEmit
npm test
npm run build
```

### Documentation Projects

**Detected by**: `*.tex`, `*.md` (>2 files), `*.adoc`

**Checks**:
- ✅ LaTeX compilation (pdflatex/xelatex)
- ✅ Markdown linting (markdownlint)
- ✅ AsciiDoc rendering (asciidoctor)

**Example**:
```bash
pdflatex main.tex
markdownlint **/*.md
asciidoctor *.adoc
```

## Configuration

### commit_types.json

Defines emoji mappings for conventional commits:

```json
{
  "feat": {
    "emoji": "✨",
    "description": "New functionality"
  },
  "fix": {
    "emoji": "🐛",
    "description": "Bug fix"
  }
}
```

**Full list**: See [config/commit_types.json](config/commit_types.json)

### validation_rules.json

Project-specific validation rules:

```json
{
  "python": {
    "checks": {
      "ruff": {"enabled": true, "timeout": 60},
      "pytest": {"enabled": true, "skippable": true}
    }
  }
}
```

**Full configuration**: See [config/validation_rules.json](config/validation_rules.json)

## Architecture

```text
professional-commit-workflow/
├── SKILL.md                      # Skill definition for Claude Code
├── README.md                     # This file
├── requirements.txt              # Python dependencies (optional)
│
├── scripts/                      # Executable scripts
│   ├── main.py                   # Main orchestrator
│   ├── commit_message.py         # Commit message generator
│   ├── project_detector.py       # Project type detection
│   ├── git_analyzer.py           # Git status analysis
│   ├── utils.py                  # Utility functions
│   └── validators/               # Project validators
│       ├── base_validator.py     # Base class
│       ├── java_validator.py     # Java (Maven, Gradle)
│       ├── python_validator.py   # Python (Ruff, Black, pytest)
│       ├── react_validator.py    # React/Node.js (ESLint, TS)
│       └── docs_validator.py     # Documentation (LaTeX, MD)
│
├── config/                       # Configuration files
│   ├── commit_types.json         # Emoji conventional commits
│   └── validation_rules.json     # Validation rules
│
└── docs/                         # Migrated documentation
    ├── best-practices.md         # Git commit best practices
    ├── commit-types.md           # All commit types
    ├── pre-commit-checks.md      # Check descriptions
    └── troubleshooting.md        # Troubleshooting
```

## Examples

### Successful Python Commit

```text
$ python scripts/main.py

============================================================
  Professional Commit Workflow
============================================================

✓ Project types detected: python
✓ 3 files ready for commit
  - src/api/routes.py
  - tests/test_routes.py
  - README.md

============================================================
  Pre-Commit Validation
============================================================

✓ Ruff Linting: No linting errors
✓ Black Formatting: Code correctly formatted
✓ pytest: All tests passed

Validation result: 3/3 checks passed

============================================================
  Diff Analysis
============================================================

ℹ️  Files changed: 3
ℹ️  Insertions: +47
ℹ️  Deletions: -12

============================================================
  Commit Message
============================================================

ℹ️  Generated: ✨ feat: Add API routes for user management
Use commit message? [Y/n] y

============================================================
  Create Commit
============================================================

✓ Commit created: ✨ feat: Add API routes for user management

============================================================
  Push to Remote
============================================================

Push to 'main'? [Y/n] y
✓ Push to 'main' successful

✅ Commit workflow completed successfully
```

### On Validation Errors

```text
============================================================
  Pre-Commit Validation
============================================================

✓ Ruff Linting: No linting errors
✗ Black Formatting: Formatting errors found
    src/api/routes.py would be reformatted
✓ pytest: All tests passed

Validation result: 2/3 checks passed

❌ Pre-commit checks failed
ℹ️  Fix the errors or use --no-verify to skip
```

## Troubleshooting

### Tool Not Found

**Problem**: "Command 'ruff' not found"

**Solution**: Install the tool or skip the check

```bash
# Install tool
pip install ruff

# Or: Skip check
python scripts/main.py --no-verify
```

### Tests Failing

**Problem**: Tests are not passing

**Solutions**:

1. **Fix tests** (recommended)
2. **Skip tests**: `--skip-tests`
3. **Skip all checks**: `--no-verify`

```bash
python scripts/main.py --skip-tests
```

### Build Errors

**Problem**: Maven/Gradle/npm build fails

**Solution**: See [docs/troubleshooting.md](docs/troubleshooting.md)

### Multiple Logical Changes

**Problem**: Skill warns about multiple changes in one commit

**Solution**: Create atomic commits

```bash
# Split changes
git reset
git add src/feature-a/
git commit -m "✨ feat: Feature A"

git add src/feature-b/
git commit -m "✨ feat: Feature B"
```

## Best Practices

### Atomic Commits

✅ **Good**: One commit = one logical change
```
✨ feat: Add user authentication
🧪 test: Add tests for authentication
📚 docs: Document auth API
```

❌ **Bad**: Everything in one commit
```
✨ feat: Auth, tests, docs, bugfixes and refactoring
```

### Commit Messages

✅ **Good**: Imperative, descriptive, <72 characters
```
✨ feat: Add dark mode toggle
🐛 fix: Resolve memory leak in WebSocket connections
```

❌ **Bad**: Past tense, vague
```
feat: Added stuff
fix: bug
```

### Code Quality

✅ **Before every commit**:
- [ ] Linting passed
- [ ] Tests successful
- [ ] Build successful
- [ ] No debug output
- [ ] No secrets

**Full best practices**: [docs/best-practices.md](docs/best-practices.md)

## Documentation

- **[Pre-Commit Checks](docs/pre-commit-checks.md)** - Detailed check descriptions
- **[Commit Types](docs/commit-types.md)** - All emoji types with examples
- **[Best Practices](docs/best-practices.md)** - Git commit best practices
- **[Troubleshooting](docs/troubleshooting.md)** - Troubleshooting guide

## Migration from /git-workflow:commit Command

If you have been using the `/git-workflow:commit` command:

1. **Install skill** (see above)
2. **Use Claude**: "Create a commit with the professional-commit-workflow skill"
3. **Optional**: Disable `/git-workflow:commit` command or keep it for legacy projects

**Advantages**:
- ✅ Reusable across projects
- ✅ No duplication of command files
- ✅ Easy updates (only update skill)
- ✅ Distributable to other users

## License

MIT License - See [LICENSE](LICENSE) for details.

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).

## Version

**Version**: 1.0.0
**Author**: talent-factory
**Refactored from**: `/git-workflow:commit` command
**Date**: 2024-12-21
