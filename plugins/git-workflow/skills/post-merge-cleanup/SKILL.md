---
name: post-merge-cleanup
description: >
  Cleans up after a merged PR: removes the task's worktree, deletes local and remote feature
  branches, and marks the task done (STATUS.md or a Plane work item). Use when the user says
  "clean up after merge", "the PR is merged", "delete the merged branch and worktree", or
  "mark the task as done after merge".
argument-hint: "<task-id> [--dry-run] [--keep-local] [--no-status-update]"
allowed-tools:
  - Bash
  - Read
  - Edit
  - Glob
---

# Post-Merge Cleanup

## Parameters

| Parameter | Description |
|---|---|
| `task_id` | Task identifier, e.g. `task-013` or `PROJ-123` |
| `--dry-run` | Show what would happen, change nothing |
| `--no-status-update` | Clean up git only |
| `--keep-local` | Keep the local branch, delete only the remote one |

## Steps

1. **Find the task source.** `task-NNN` means a `STATUS.md` below `.plans/` (`glob ".plans/**/STATUS.md"`). An identifier like `PROJ-123` means a Plane work item (`mcp__plane__workitem`, action `retrieve_by_identifier`, with the `workspace` the repository's `CLAUDE.md` names). If neither is found, say so and stop.
2. **Find the git assets** of the task: `git worktree list`, `git branch`, `git branch -r`, each filtered by the task id. Show them to the user. With `--dry-run`, stop here and list the planned actions.
3. **Safety check.** Confirm that a PR for the task was merged: `gh pr list --search "<task_id>" --state merged`. Without a merged PR, warn and continue only after explicit confirmation.
4. **Clean up**, skipping assets that do not exist:
   - `git worktree remove <path>` (if it has uncommitted changes, show them and ask; never use `--force` without confirmation)
   - `git branch -d <branch>` (if it is not fully merged, which is normal after a squash merge, ask before `-D`)
   - `git push origin --delete <branch>`
   - `git fetch --prune`
5. **Mark the task done** (unless `--no-status-update`):
   - **Plane:** read the project's states (`mcp__plane__state`, action `list`) and set the work item to the state in group `completed` (usually "Done") with `mcp__plane__workitem`, action `update`. Plane does not close work items on merge by itself.
   - **STATUS.md:** set the task row to completed, update the progress row if there is one, and move newly unblocked tasks into "Next steps". Formats and recognised status words: [docs/status-md-format.md](docs/status-md-format.md). Then commit with `✅ chore: Mark <task_id> as completed` and push.
6. **Report** what was removed and what was skipped. If the status update fails (permissions, wrong state name), say so; the git cleanup stays done.
