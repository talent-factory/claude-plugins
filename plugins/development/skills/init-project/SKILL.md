---
name: init-project
description: >
  Initialises a new open source project: Git repository with a develop to main branching strategy,
  community files (LICENSE, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY), GitHub issue and PR templates,
  README, and optional Java (Gradle Kotlin DSL) or Python (uv) scaffolding. Use when the user asks to
  "initialise a project", "set up a new repository", or "start a new Java or Python project".
argument-hint: "[--git|--java|--uv] [--name <name>] [--no-branching] [--interactive]"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
---

# Init Project

## Options

- `--git` (default): plain Git project. `--java`: Java with Gradle. `--uv`: Python with uv.
- `--name <name>`: project name (default: the directory name).
- `--no-branching`: only `main`, no `develop`.
- `--interactive`: ask for type, name, license (MIT, Apache-2.0, GPL-3.0, BSD-3-Clause) and main language.

## Rules

1. **Java projects use Gradle with the Kotlin DSL (`build.gradle.kts`), never Maven.** Java 21 toolchain, JUnit 5, Gradle wrapper.
2. **The initial commit goes through `/git-workflow:commit`**, not a plain `git commit`, so it follows the commit format.
3. **Branching:** by default work happens on `develop` and `main` is created from it after the initial commit. With `--no-branching` the repository has only `main`.
4. Never overwrite existing files. If the directory already holds a project, list what would be added and ask first.

## Steps

1. **Type and name.** Resolve them from the options or the directory. Check the target directory first (`git status`, existing files).
2. **Git.** `git init`; `git checkout -b develop` (or `git branch -M main` with `--no-branching`).
3. **Language scaffold.**
   - `--java`: `settings.gradle.kts`, `build.gradle.kts` (Java plugin, toolchain 21, JUnit 5 via `useJUnitPlatform()`), `gradle.properties`, Gradle wrapper (`gradle wrapper`), `src/main/java` and `src/test/java` with a sample class and test.
   - `--uv`: `uv init` (install uv first if it is missing), then `src/<package>/` and `tests/` with `pytest` and `ruff` as dev dependencies.
4. **Project files.** `.gitignore` and `.gitattributes` for the language, `LICENSE` (chosen license, current year and the owner from `git config user.name`), `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md` (Contributor Covenant), `SECURITY.md`, `.github/ISSUE_TEMPLATE/` (bug, feature), `.github/PULL_REQUEST_TEMPLATE.md`, and a CI workflow for the language (`.github/workflows/ci.yml`). Pin GitHub Actions to current major versions.
5. **README.md** with name, one-line description, badges (license, CI), installation, quick start, documentation, contributing, license and support.
6. **Initial commit** with `/git-workflow:commit`. Unless `--no-branching`, then `git branch main` so `main` and `develop` start on the same commit, and stay on `develop`.
7. **Optional:** offer `gh repo create` and, once it exists, branch protection for `main` (pull request required, status checks, linear history). Do not push or create anything remote without the user's agreement.

## Report

List what was created, the branch layout and the next steps (first feature branch, CI secrets, branch protection).
