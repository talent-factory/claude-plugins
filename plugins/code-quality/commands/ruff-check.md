---
description: Lint and format all Python files in the project using Ruff
allowed-tools:
  - Bash
  - Read
  - Edit
---

# Python Code Linting and Formatting with Ruff

This workflow runs Ruff linting and formatting on all Python files in the project.

1. Install Ruff if not present (prefer uv when available)

```bash
# With uv (preferred)
uv add --dev ruff

# Fallback with pip
pip install ruff
```

2. Run linting on all Python files

```bash
ruff check .
```

3. Automatically fix resolvable linting issues

```bash
ruff check --fix .
```

4. Format code (replaces black)

```bash
ruff format .
```

5. Final check - both linting and formatting

```bash
ruff check . && ruff format --check .
```

## Additional Options

- `ruff check --select E,W` - Errors and warnings only
- `ruff check --fix --unsafe-fixes` - Apply unsafe fixes as well
- `ruff format --diff` - Show changes without applying them
- `ruff check --statistics` - Show statistics on issues found
