---
name: init-task
description: >
  Adds a single task to a plan or as a standalone task: duplicate detection against existing tasks,
  ATOMIC validation, and a mandatory Definition of Done. Use when the user asks to "add a task",
  "create a ticket for this", or "initialise a task" in a .plans/ based project.
argument-hint: "[title] [--plan <name>] [--standalone] [--type <type>] [--priority <p>] [--estimate <sp>]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
---

# Init Task

Create one task file in the right place. Format: [references/formats.md](../../references/formats.md).

## Steps

1. **Context.** Find plans with `Glob(".plans/*/EPIC.md")`. Use `--plan <name>`; if there is exactly one plan, use it; otherwise ask, or create a standalone task under `.plans/adhoc/` (`--standalone`).
2. **Duplicates.** Compare the title and description with the existing tasks of that plan (title words, acceptance criteria, files named). On a likely match show it and ask: create anyway, extend the existing task, or cancel.
3. **Collect the data** from arguments, asking only for what is missing: title, description or user story, 2 to 5 testable acceptance criteria, type, priority (must / should / could), estimate (1, 2, 3, 5, 8), dependencies, extra Definition-of-Done items.
4. **ATOMIC check.** Actionable, Testable, Ownable, Measurable, Independent, Complete. If the estimate is above 5 or the task covers several concerns, propose a split. If a criterion cannot be tested, rewrite it with the user.
5. **Write** `tasks/task-NNN-<slug>.md` with the next free number. The Definition of Done always contains: acceptance criteria verified, code reviewed, tests passing, documentation updated if applicable, plus the custom items.
6. **Update STATUS.md** (counts, story points, task list, dependency graph) and report the task path.
