---
name: hunk-review
description: >
  This skill should be used when the user asks to "review code with hunk", "start a hunk review session",
  "add comments to a hunk diff", "annotate a diff with hunk", "use hunk for code review",
  or when the user mentions the `hunkdiff` CLI tool. Provides structured guidance for interacting
  with live Hunk diff review sessions via the daemon CLI.
---

# Hunk Review

> Adapted from [modem-dev/hunk](https://github.com/modem-dev/hunk/blob/main/skills/hunk-review/SKILL.md) — MIT License

## Overview

Hunk is an interactive terminal diff viewer designed for reviewing code changes, particularly
AI-generated ones. This skill controls live Hunk review sessions through the daemon CLI
(`hunk session`, `hunk comment`). Hunk itself runs as an interactive TUI — do not launch it
directly; interact with an already-running session instead.

**Installation:**
```bash
npm i -g hunkdiff
```

**Prerequisite:** A Hunk session must already be running (`hunk diff`, `hunk show`, or `hunk difftool`).

---

## Workflow

Follow this structured sequence for every review:

1. **Discover sessions** — identify available sessions and their repository roots
2. **Inspect structure** — understand files and hunks without loading full diffs
3. **Navigate** — move to the relevant file or hunk before commenting
4. **Reload** (if needed) — update session content when the diff changes
5. **Comment** — annotate specific hunks with focused, high-value notes

---

## Primary Commands

### 1. List Sessions

```bash
hunk session list
```

Returns all active sessions. Note the session ID or repository path — both can be used to target sessions in subsequent commands.

Most session commands accept either:
- `--repo <path>` — match by repository root directory
- `<session-id>` — explicit session identifier

### 2. Inspect Session Structure

```bash
hunk session review --json
```

Returns the full file and hunk structure as JSON without loading raw patch text.
Use this to understand the shape of the diff before navigating.

Add `--include-patch` **only** when examining actual diff content is essential:
```bash
hunk session review --json --include-patch
```

### 3. Navigate to a Location

**Absolute navigation** requires `--file` plus exactly one position target. Hunk indices are zero-based — the first hunk in a file is `--hunk 0`.

```bash
# Jump to a specific hunk index
hunk session navigate --file src/main.py --hunk 2

# Jump to a line in the new version
hunk session navigate --file src/main.py --new-line 42

# Jump to a line in the original version
hunk session navigate --file src/main.py --old-line 17
```

**Relative navigation** moves between already-annotated hunks:

```bash
hunk session navigate --next-comment
hunk session navigate --prev-comment
```

Always navigate before adding a comment — this ensures the user sees the
relevant code in the Hunk UI at the time the annotation appears.

### 4. Reload Session Content

Swap the diff content of a running session:

```bash
hunk session reload --repo . -- <command>
```

**Note:** Reloading replaces the session's diff content. Any comments attached to the previous diff are not preserved — re-apply them after reload using `hunk comment apply`.

Always include `--` before the nested command so its flags are not parsed by Hunk:

```bash
# Reload with the latest git diff
hunk session reload --repo . -- git diff HEAD

# Reload with a specific commit
hunk session reload --repo . -- git show abc1234
```

### 5. Add Comments

**Single comment:**

```bash
hunk comment add --file src/main.py --hunk 2 "Clarify the intent of this guard clause."
```

**Batch comments** (preferred for multiple annotations):

Pipe a JSON array to `comment apply` via stdin:

```bash
hunk comment apply --repo . <<'EOF'
[
  {
    "file": "src/auth.ts",
    "hunk": 1,
    "body": "This token is never invalidated on logout — potential session fixation risk."
  },
  {
    "file": "src/auth.ts",
    "hunk": 3,
    "body": "Prefer `crypto.timingSafeEqual` to avoid timing attacks."
  }
]
EOF
```

---

## Review Best Practices

### Prioritise Clarity Over Coverage

Avoid annotating every change. Focus on:
- **Intent** — is the purpose of the change clear?
- **Structure** — does the new code fit the existing architecture?
- **Risk** — are there security, correctness, or performance concerns?
- **Follow-ups** — what should be addressed before merging?

### Work in Narrative Order

Navigate through the diff in the order a reviewer would read it — typically top to bottom
within each file, critical files first — rather than strict alphabetical file order.

### Batch Where Possible

Prepare all comments for a file or section before calling `comment apply`.
Batching reduces CLI round-trips and produces a coherent annotation set.

### Minimal Patch Loading

Do not call `--include-patch` unless examining the actual diff text is necessary.
The JSON structure from `hunk session review --json` is sufficient for navigation
and batch-comment planning in most cases.

---

## Common Session Patterns

### Quick Annotation of a Git Diff

```bash
# Start Hunk (user runs this in a separate terminal)
hunk diff HEAD~1

# In this session: list and inspect
hunk session list
hunk session review --json

# Navigate and annotate
hunk session navigate --file src/api.py --hunk 0
hunk comment add --file src/api.py --hunk 0 "Missing input validation before DB write."
```

### Review a PR Locally

```bash
# Fetch PR diff and load into Hunk (user runs this)
gh pr diff 42 | hunk diff -

# Reload after new commits are pushed
hunk session reload --repo . -- gh pr diff 42
```

### Full Batch Review

```bash
# Inspect structure
hunk session review --json | jq '.files[].name'

# Prepare comments, then apply all at once
hunk comment apply --repo . < review-comments.json
```

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| `no session found` | No Hunk session running | Start Hunk in a separate terminal first |
| Navigation has no effect | Wrong `--file` path | Check exact path with `hunk session review --json` |
| `--` missing error | Nested command flags parsed by Hunk | Add `--` before the nested command |
| Comments not visible | Session was reloaded after commenting | Re-apply comments after reload |
