---
name: create-plan
description: >
  Turns a PRD into a file-based project plan under .plans/: an EPIC, atomic tasks with acceptance
  criteria, estimates and dependencies, and a STATUS file with a dependency graph. Use when the user
  asks to "create a plan from the PRD", "break this feature into tasks", or "plan the implementation".
argument-hint: "[--prd <path>] [--interactive]"
allowed-tools:
  - Read
  - Write
  - Glob
  - AskUserQuestion
---

# Create Plan

Read the PRD (`PRD.md` by default, or `--prd <path>`) and write the plan to `.plans/<feature-name>/`. File formats: [references/formats.md](../../references/formats.md).

## Steps

1. **Read and check the PRD.** It needs objectives, prioritised requirements and acceptance criteria. If something essential is missing, say what and ask; do not invent it.
2. **Feature name** in kebab-case from the PRD title. If `.plans/<name>/` exists, ask: extend it, choose another name, or cancel.
3. **EPIC.md** from the PRD summary, metrics, scope and risks.
4. **Break down into tasks.** Each task is atomic:
   - **A**ctionable (can start now), **T**estable (acceptance criteria), **O**wnable (one developer or agent), **M**easurable (1, 2, 3, 5 or 8 story points; split anything larger), **I**ndependent (few dependencies), **C**omplete (understandable without the PRD).
   - Record `Requires` and `Blocks` between tasks; no cycles.
   - Prefer vertical slices (a thin working path through the layers) over horizontal layers.
   - Name a suitable agent per task only if one is installed; leave the field empty otherwise.
5. **STATUS.md** with counts, story points, a Mermaid dependency graph and the tasks that can start immediately.
6. **Check before saving:** no duplicate or overlapping tasks, no dependency cycles, every Must requirement is covered by at least one task, estimates are plausible. Report the plan as a table: ID, title, SP, dependencies.

With `--interactive`, confirm the task list with the user before writing files.

## Next steps

`/project-management:implement-task <task-id>` for one task, `/project-management:implement-epic` for the whole plan, `/project-management:init-task` to add a task later.
