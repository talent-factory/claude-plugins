---
name: implement-task
description: >
  Implements one task end to end: reads it, analyses the code, works in its own git worktree with a
  draft PR, marks the task in progress, implements with tests, runs a quality gate and finalises
  the PR. Tasks come from .plans/ or from Plane. Use when the user asks to "implement task-001",
  "work on this task", or "implement PROJ-123".
argument-hint: "[task-id] [--plane] [--skip-brainstorm] [--skip-quality-gate]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Agent
  - AskUserQuestion
---

# Implement Task

## Task source

- **Filesystem (default):** `.plans/<feature>/tasks/task-NNN-*.md`, created by `create-plan` or `init-task` (format: [formats.md](../../references/formats.md)). Without an id, list the pending tasks whose `Requires` are completed and ask which one.
- **Plane (`--plane`):** a work item by identifier such as `PROJ-123`. Setup, tools and state handling: [plane.md](../../references/plane.md).

## Steps

1. **Read the task:** title, description, acceptance criteria, dependencies, type or labels. Stop if a required task is not completed.
2. **Understand the code** (skip with `--skip-brainstorm`). If the `brainstorming` skill of the superpowers plugin is available, use it for open design questions; otherwise read the files and tests the task touches and write down the approach in a few lines. Ask the user only about real ambiguity.
3. **Worktree and branch.** Work in `.worktrees/task-<id>/` so several tasks can run in parallel: `git worktree add -b <branch> .worktrees/task-<id> origin/<default-branch>`. Branch: `<prefix><task-id>-<slug>` (prefix from the type: `feature/`, `bugfix/`, `docs/`, `refactor/`, `test/`). Initialise submodules inside the worktree if the project has them.
4. **Mark the task in progress on the default branch, not in the worktree**, so other people see it at once. Filesystem: set `Status: in_progress` and `Updated` in the task file and STATUS.md, commit and push on the default branch. Plane: move the work item to the project's first `started` state (or the name configured in the repository's `CLAUDE.md`).
5. **Draft PR early** (`gh pr create --draft`) with the task reference, planned changes and a test plan, so CI starts and others can see the work.
6. **Implement** in the worktree. Write tests for each acceptance criterion. Commit in small steps with `/git-workflow:commit`. Pick a specialised agent only where one clearly fits the stack.
7. **Quality gate** (skip with `--skip-quality-gate`): run the project's tests, linters and type checks; review the full diff against the default branch (`/code-review` or a reviewer agent) and fix what it finds; walk through every acceptance criterion and the Definition of Done and show which test covers each. Do not continue with a failing check.
8. **Finalise the PR:** remove the draft prefix, describe what changed and how it was tested, add `Closes <id>` (or `Refs <id>` with the reason when the task stays open on purpose), run `gh pr ready`.
9. **Close the loop.** Filesystem: set the task to `completed` (or `needs_attention`) and update STATUS.md. Plane: move the item to the review state (Done is set after the merge, see plane.md). After the merge, clean up with `/git-workflow:post-merge-cleanup`.

## Rules

- One task per worktree, one PR per task.
- If something blocks you (missing dependency, unclear criterion, failing test you cannot fix), set the task to `blocked` or `needs_attention` with the reason instead of guessing.
- Never skip the status update in step 4: it prevents two people working on the same task.
