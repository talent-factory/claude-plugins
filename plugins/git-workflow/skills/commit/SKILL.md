---
name: commit
description: >
  Creates git commits as Emoji Conventional Commits with English messages, runs the project's own
  checks first, and splits unrelated changes into separate commits. Use when the user asks to
  "commit", "commit my changes", "create a commit", or after a finished change that should be committed.
argument-hint: "[--no-verify] [--skip-tests]"
allowed-tools:
  - Bash
  - Read
  - Glob
---

# Commit

Create a clean, atomic commit of the current changes.

## Options

- `--no-verify`: skip the pre-commit checks
- `--skip-tests`: run the checks but not the test suite

## Steps

1. **Checks** (unless `--no-verify`). Detect the project type from its files and run the checks the project already defines: lint, format check, type check, build, tests. Use the project's own scripts first (`package.json` scripts, `Makefile`, `pyproject.toml`, `build.gradle.kts`, `pom.xml`); otherwise the usual tools (Ruff or Black for Python, ESLint and `tsc` for JavaScript/TypeScript, Gradle or Maven for Java, markdownlint for docs). Stop and report failures. Do not commit over a failing check unless the user says so.
2. **Staging.** Run `git status` and `git diff`. If nothing is staged, stage the relevant files (name them, do not use `git add -A` blindly). Never stage secrets (`.env`, keys, credentials).
3. **Splitting.** If the diff mixes unrelated concerns (a feature plus a refactor, code plus unrelated docs), propose separate commits and create them one by one.
4. **Message.** Write `<emoji> <type>(<scope>): <imperative description>` in **English**, first line at most about 72 characters. Add a short body only when the reason is not obvious from the diff.
5. **Commit.** Create the commit. Offer to push; push only when the user agrees.

## Types

| Emoji | Type | Use for |
|---|---|---|
| ✨ | `feat` | new functionality |
| 🐛 | `fix` | bug fix |
| 📚 | `docs` | documentation |
| 💎 | `style` | formatting, no behaviour change |
| ♻️ | `refactor` | restructuring, no behaviour change |
| ⚡ | `perf` | performance |
| 🧪 | `test` | tests |
| 🔧 | `chore` | build, tooling, configuration |
| 🚀 | `ci` | CI/CD |
| 🔒 | `security` | security fixes |
| 📦 | `deps` | dependency updates |

Examples: `✨ feat(auth): Add OAuth2 login`, `🐛 fix: Resolve race condition in async handler`.

## Rules

- Messages describe the change only. Do not append `Co-Authored-By: Claude` or "Generated with Claude Code" lines unless the repository's own instructions ask for them.
- If a repository documents its own commit format, follow that instead of the table above.
- Do not amend, rebase or force-push without an explicit request.
