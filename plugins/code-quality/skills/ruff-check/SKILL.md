---
name: ruff-check
description: >
  Lints and formats all Python files of the project with Ruff: installs it if missing, auto-fixes what
  can be fixed, formats, and reports the violations that need manual work. Use when the user asks to
  "lint my Python", "fix Python code style", "run ruff", "format my Python files", or "fix linting errors".
allowed-tools:
  - Bash
  - Read
  - Edit
---

# Ruff Check

Ruff replaces flake8, isort and black in one tool.

1. **Install** if `ruff --version` fails: `uv add --dev ruff`, otherwise `pip install ruff`. Respect an existing Ruff configuration (`pyproject.toml`, `ruff.toml`); do not add one unasked.
2. **Check:** `ruff check .` and report the number of violations by rule.
3. **Fix:** `ruff check --fix .` (safe fixes only), then `ruff format .`.
4. **Verify:** `ruff check . && ruff format --check .`.
5. **Report.** Clean: "No violations, all files formatted." Otherwise, for each remaining violation give file and line, what the rule requires and the manual fix, and apply it when it is clearly correct.

Useful flags: `ruff check --statistics` (counts per rule), `ruff format --diff` (preview), `ruff check --fix --unsafe-fixes` (only when the user asks, and review the diff afterwards).
