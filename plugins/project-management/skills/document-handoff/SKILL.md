---
name: document-handoff
description: >
  Writes a self-contained handoff document before /compact or the end of a session, so that a new
  agent with fresh context can continue the work. Use when the user says "prepare a handoff",
  "document before compact", "context is getting too large", "I need to hand this off", or "end of
  session notes".
argument-hint: "[task-name] [--output <dir>] [--plane <identifier>]"
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
---

# Document Handoff

Write a document that lets a fresh agent continue without any prior context. Skip it when the task finishes in minutes or only research was done.

## Parameters

| Parameter | Default | Description |
|---|---|---|
| `[task-name]` | derived from the git branch | Name used in the file name |
| `--output <dir>` | `.claude/handoffs/` | Output directory |
| `--plane <identifier>` | none | Add title, state and comments of this Plane work item (`mcp__plane__workitem`, `retrieve_by_identifier`) |

## Steps

1. **Gather.** `git branch --show-current`, `git status --short`, `git log --oneline -5`, `git diff --stat HEAD`, open TODO and FIXME markers in changed files, and the work item if `--plane` is given. Add what you know from the session itself: the goal, decisions, attempts.
2. **Write** `<output>/YYYY-MM-DD_<task-slug>.md` (create the directory) with these sections:
   - **Original task**: goal and agreed definition of done
   - **Completed**: concrete changes with file paths, commit hashes, PR numbers
   - **Failed attempts**: what was tried and the exact reason it failed, with error messages quoted verbatim
   - **Current state**: branch, uncommitted files, running services, environment specifics
   - **Next steps**: prioritised, with file paths and line numbers
   - **References**: key files, docs, patterns
   - **For the next agent**: two or three sentences: pick up here and do X
3. **Report** the path, the top three next steps and the continuation instruction:
   `Please read .claude/handoffs/YYYY-MM-DD_<task-slug>.md and continue with the next steps.`

## Quality

- Self-explanatory: every file reference has a path and, where it matters, a line number; no implicit assumptions.
- Actionable: "change line 123 in `src/auth/service.py`", not "adjust the auth code".
- No secrets. If a key or token was involved, name where it lives (variable name, file), never the value.
- The document is a working note: do not commit it unless the user asks.
