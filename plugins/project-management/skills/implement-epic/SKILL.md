---
name: implement-epic
description: >
  Implements all tasks of a .plans/ EPIC in dependency order, running independent tasks in parallel
  as subagents in separate git worktrees, with a review pass and a STATUS.md update after each wave.
  Use when the user asks to "implement the whole epic", "run all tasks of the plan", or "implement
  the plan in parallel".
argument-hint: "<plan-name> [--max-parallel <n>] [--dry-run]"
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

# Implement EPIC

Runs the plan in `.plans/<plan-name>/` (format: [formats.md](../../references/formats.md)). This costs many tokens, because every task gets its own agent. State the number of pending tasks and the planned waves before starting, and let the user confirm. `--dry-run` stops after that overview.

## Steps

1. **Analyse.** Read EPIC.md, STATUS.md and all task files. Build the dependency graph from the `Requires` fields. Stop on cycles or on tasks that require a missing task. Group the pending tasks into **waves**: wave 1 has no open dependency, wave 2 depends only on wave 1, and so on. Show the waves.
2. **Run a wave.** Start one subagent per task, at most `--max-parallel` at a time (default 3), each in its own worktree (`isolation: "worktree"` or `git worktree add` as in `implement-task`). Brief each agent completely, because it starts without context: task file, acceptance criteria, Definition of Done, branch name, and the instruction to follow the `implement-task` steps 3 to 8 (worktree, draft PR, implementation with tests, quality gate, PR ready). Do not mark tasks in progress from the agents; the orchestrator does that on the default branch before the wave starts.
3. **Collect results.** For each task note: PR URL, tests passed, open questions. A task that fails its quality gate after two attempts becomes `needs_attention` with the reason; do not retry endlessly.
4. **Update STATUS.md** after each wave: task statuses, counts, story points, the graph. Commit it on the default branch.
5. **Next wave.** Tasks whose dependencies are completed (merged, or at least PR ready if the user chose to stack branches) start next. Tasks that depend on a `needs_attention` task stay pending and are listed as blocked.
6. **Report.** Per task: status and PR; then total, open problems and the order in which to merge. Merging stays with the user.

## Rules

- A task's files should not overlap with another task of the same wave. If two tasks of a wave touch the same files, run them one after the other.
- Merge conflicts are not solved silently: set the task to `needs_attention`, or use `/git-workflow:resolve-conflicts` with the user.
- Stop and ask when the plan, not the code, looks wrong (contradicting tasks, impossible dependencies).
