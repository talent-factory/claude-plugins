---
name: document-handoff
description: >
  Creates comprehensive handoff documentation before a /compact operation,
  enabling a new agent with fresh context to seamlessly continue the work.
  Activate when the user says "prepare a handoff", "document before compact",
  "context is getting too large", "I need to hand this off", "create a handoff
  document", "end of session notes", or "document the current state for
  tomorrow". Supports --output and --linear-issue options.
---

# Document Handoff

Create a self-contained handoff document that gives a fresh agent everything it
needs to continue without any prior context.

## When to Use

**Use when:**
- Context window is approaching its limit and `/compact` is necessary
- Handing off to another developer or agent
- Interrupting a complex task mid-way
- Ending a working session and resuming the next day
- Multiple failed attempts have accumulated useful learning

**Skip when:**
- The task will finish in the next five minutes
- Only research was done — no implementation changes
- The task is trivial and the context is minimal

## Parameters

| Parameter | Default | Description |
|---|---|---|
| `[task-name]` | derived from git branch | Name for the handoff document |
| `--output <dir>` | `.claude/handoffs/` | Output directory |
| `--linear-issue <ID>` | — | Pull issue details from Linear (e.g. `TF-177`) |

## Workflow

### Step 1 — Gather information automatically

**Git status:**
```bash
git branch --show-current
git status --short
git log --oneline -5
git diff --stat HEAD
```

**TODO/FIXME in code:**
```bash
grep -rn "TODO\|FIXME\|HACK\|XXX" --include="*.py" --include="*.ts" \
  --include="*.java" . 2>/dev/null | head -20
```

**Linear issue (if `--linear-issue` is specified):**
Use `mcp__linear__get_issue` to retrieve title, description, status, comments.

### Step 2 — Structure the document

| Section | Content |
|---|---|
| **Original Task** | What was the goal? What definition of done was agreed? |
| **Already Completed** | Concrete changes made — file paths, commit hashes, PR numbers |
| **Failed Attempts** | What was tried, what failed, and the exact reason why |
| **Current State** | Git branch, uncommitted files, environment specifics, running services |
| **Next Steps** | Prioritised list with specific file paths and line numbers where relevant |
| **Important References** | Key files, docs, code patterns, external resources |
| **For the Next Agent** | 2–3 sentence executive summary: pick this up and do X next |

### Step 3 — Save the document

**Output path:**
```
.claude/handoffs/YYYY-MM-DD_<task-slug>.md
```

Examples:
- `.claude/handoffs/2026-05-08_auth-refactor.md`
- `.claude/handoffs/2026-05-08_rbac-regression-fix.md`

Create the directory if it does not exist: `mkdir -p .claude/handoffs/`

### Step 4 — Output summary

After saving:
1. Display the full path to the handoff file
2. Highlight the **top 3 next steps** in order
3. Print the continuation instruction:

```
To continue after /compact:
  "Please read .claude/handoffs/YYYY-MM-DD_<task-slug>.md and continue with the next steps."
```

## Quality Standards

A good handoff document is:

**Self-explanatory** — the next agent needs no prior knowledge. Every relevant
file path includes a line number. No implicit assumptions.

**Actionable** — "Modify line 123 in `src/auth/service.py`" not "adjust the
auth code". Next steps are prioritised and have clear acceptance criteria.

**Complete** — both successful *and* failed attempts are documented. Error
messages are quoted verbatim, not paraphrased. Dependencies and external
factors that affect the task are noted.

**Safe** — no API keys, passwords, tokens, or credentials. If any were
encountered, note their *location* (environment variable name or file path),
not their values.

## Handoff + Compact Sequence

```bash
# 1. Create the handoff
/project-management:document-handoff "My Task Name"

# 2. Compact the context
/compact

# 3. In the new session, load and continue
# "Please read .claude/handoffs/2026-05-08_my-task-name.md
#  and continue with the next steps."
```

## Additional Resources

- **`../references/document-handoff/templates.md`** — Full and minimal handoff templates
- **`../references/document-handoff/examples.md`** — Annotated real-world examples
- **`../references/document-handoff/best-practices.md`** — Effective handoff patterns and common mistakes
