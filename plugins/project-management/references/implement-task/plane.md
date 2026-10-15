# Plane Integration Guide

Guide to working with Plane work items through the `plane-tf` MCP server (`mcp__plane-tf__*`) in `/project-management:implement-task --plane`.

## Overview

Plane is a provider next to the filesystem (default) and Linear (`--linear`). With `--plane`, the command:

- Resolves the work item from its identifier (e.g. `TF-792`)
- Reads states from the Plane project instead of hard-coding them
- Moves the work item to "In Progress" when implementation starts
- Moves it to "In Review" when the PR is ready
- Adds the `Closes <identifier>` line to the PR description so the item is closed when the PR merges

## Prerequisite: MCP Server

The server is registered at user scope:

```bash
claude mcp add --scope user plane-tf \
  -e PLANE_BASE_URL=https://plane.talent-factory.ch \
  -e PLANE_WORKSPACE_SLUG=tf \
  -e PLANE_API_KEY=<your-api-key> \
  -- uvx plane-mcp-server stdio
```

Never write the API key into the repository. It stays in the MCP configuration.

## Repository Configuration (CLAUDE.md)

Each repository declares its Plane project in its `CLAUDE.md`. The workspace slug comes from the MCP configuration, so it is not repeated here.

```markdown
## Plane Integration

- **Project**: `TF` (project identifier, not the UUID)
- **Status Override** (optional): only if the state names differ from the defaults
  - In Progress: `In Progress`
  - In Review: `In Review`
```

`Project` is the short identifier shown as the prefix of work item identifiers (`TF` in `TF-792`). The command resolves it to the project UUID with `project list`. Do not store UUIDs in `CLAUDE.md`.

If no `## Plane Integration` section exists, the command stops and asks for the project identifier. It does not guess.

## MCP Tools Used

### Resolve the project

```text
mcp__plane-tf__project  action=list
→ match identifier == "TF" → project id (UUID)
```

### Read the work item

```text
mcp__plane-tf__workitem  action=retrieve_by_identifier  workitem_identifier="TF-792"
→ id, name, description_html, state, labels, type
```

If `retrieve_by_identifier` is unavailable, list the project's items with `action=list` and a PQL filter, then match the sequence number.

### Read the states

Do not hard-code state UUIDs or names. Read them at runtime:

```text
mcp__plane-tf__state  action=list  project_id=<uuid>
→ [{ id, name, group }, ...]
```

State selection:

| Target | Rule |
| ------ | ---- |
| In Progress | Override name from `CLAUDE.md` if set, otherwise the first state in group `started` |
| In Review | Override name from `CLAUDE.md` if set, otherwise a `started` state named like "Review", otherwise the last `started` state |
| Done | Not set by the command (see "Closing" below) |

If the matching state cannot be determined unambiguously, the command lists the candidates and asks the user.

### Set the state

```text
mcp__plane-tf__workitem  action=update  project_id=<uuid>  workitem_id=<id>  state=<state uuid>
```

`update` changes only the fields you pass.

### Comment on progress

```text
mcp__plane-tf__workitem_comment  action=create  project_id=<uuid>  workitem_id=<id>
  comment_html="<p>Implementation started</p><ul><li>Branch: <code>feature/tf-792-...</code></li><li>Worktree: <code>.worktrees/task-tf-792/</code></li></ul>"
```

Comments are optional. Only write them at start and at PR creation.

## Branch Naming

Use the identifier in lower case, consistent with Linear:

```text
feature/tf-792-<description>
```

## Closing

The PR description contains a closing keyword for the work item:

```markdown
Closes TF-792
```

Use `Refs TF-792` instead only when the work item stays open on purpose (e.g. a production step or follow-up work). State the reason in the PR text.

The command does not set the Plane state to Done itself. Closing happens through the merged PR. Plane's GitHub integration, or the post-merge cleanup, moves the item to its completed state.

## Error Handling

| Error | Cause | Resolution |
| ----- | ----- | ---------- |
| `No module named 'fastmcp...'` | `plane-tf` server installation broken | Reinstall or refresh the server: `uvx --refresh plane-mcp-server` |
| Project identifier not found | `CLAUDE.md` value does not match Plane | Check identifier in Plane, fix `CLAUDE.md` |
| Ambiguous state | Several `started` states and no override | Ask user, then add override to `CLAUDE.md` |
| 401 / 403 | Invalid API key or missing permissions | Regenerate key, check workspace membership |
| Work item not found | Wrong identifier or archived item | Verify identifier, check archive |

## See Also

- [workflow.md](./workflow.md) - Complete workflow
- [linear.md](./linear.md) - Linear provider
- [filesystem.md](./filesystem.md) - Filesystem provider
