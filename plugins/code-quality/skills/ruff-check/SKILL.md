---
name: ruff-check
description: >
  Lints and formats all Python files in the project using Ruff. Activates when
  the user asks to "lint my Python", "fix Python code style", "run ruff",
  "format my Python files", "check Python quality", or "fix linting errors".
  Installs Ruff if not present, auto-fixes resolvable issues, and reports
  remaining violations.
---

# Python Linting and Formatting with Ruff

Lint and auto-format all Python files in the project using Ruff — the fast,
all-in-one Python linter and formatter that replaces flake8, isort, and black.

## Workflow

### Step 1 — Install Ruff (if not present)

```bash
# Preferred: uv dev dependency
uv add --dev ruff 2>/dev/null || \
  # Fallback: pip
  pip install ruff
```

### Step 2 — Check for violations

```bash
ruff check .
```

Report the number of violations found and their categories.

### Step 3 — Auto-fix resolvable violations

```bash
ruff check --fix .
```

### Step 4 — Format code (replaces black)

```bash
ruff format .
```

### Step 5 — Final verification

```bash
ruff check . && ruff format --check .
```

Report outcome:
- `✓ No violations — all files clean.`
- List any remaining violations that require manual attention.

## Useful Options

| Flag | Purpose |
|---|---|
| `ruff check --select E,W` | Errors and warnings only |
| `ruff check --fix --unsafe-fixes` | Apply unsafe fixes as well |
| `ruff format --diff` | Preview formatting changes without applying |
| `ruff check --statistics` | Show count per rule |

## On Remaining Violations

For each violation that could not be auto-fixed:
1. Show the file path and line number
2. Explain what the rule requires
3. Suggest the manual fix
