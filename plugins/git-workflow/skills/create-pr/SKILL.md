---
name: create-pr
description: >
  Creates a pull request with GitHub CLI: new branch when on a protected branch, commits via the
  commit skill, formatting, a structured description with test plan, and issue links. Use when the
  user asks to "create a PR", "open a pull request", or "push this and open a PR".
argument-hint: "[--draft] [--no-format] [--target <branch>]"
allowed-tools:
  - Bash
  - Read
  - Glob
---

# Create Pull Request

## Options

- `--draft`: open a draft PR
- `--no-format`: skip formatting
- `--target <branch>`: base branch (default: the repository's default branch, usually `main`)

## Steps

1. **Branch.** Check `git branch --show-current`. On `main`, `master` or `develop`, never commit directly: create `<type>/<short-description>-<date>` (types: `feature`, `fix`, `docs`, `refactor`), for example `fix/login-redirect-2026-11-14`. On any other branch, stay on it. Honour a branch naming rule the repository documents.
2. **Changes.** Uncommitted changes go through the `commit` skill. Already committed changes are used as they are. Stop if there is nothing to put in a PR.
3. **Formatting** (unless `--no-format`). Run the formatter the project defines (Biome or Prettier, Ruff or Black, google-java-format, markdownlint). Commit formatting changes separately.
4. **Push** the branch with upstream tracking.
5. **PR.** Create it with `gh pr create`: a title of at most about 70 characters, a description from the template below, `--draft` when requested. Link the ticket the user names: `Closes <ID>` when the PR finishes it, `Refs <ID>` when the ticket stays open on purpose, and say why. Use the language the repository's commits and PRs use.
6. **Report** the PR URL and wait for the CI result only if the user asks for it.

## Description template

```markdown
## Description

What changed and why, in two or three sentences.

## Changes

- ...

## Test plan

- [ ] ...

## Breaking changes

None / ...
```

Keep PRs focused. If the diff is far above about 400 lines or mixes concerns, suggest splitting it.
