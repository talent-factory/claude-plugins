# Plane Integration Guide

Guide to working with Plane work items through the `plane` MCP server (`mcp__plane__*`) in `/project-management:implement-task --plane`.

## Overview

Plane is a provider next to the filesystem (default) and Linear (`--linear`). With `--plane`, the command:

- Resolves the work item from its identifier (e.g. `PROJ-123`)
- Reads states from the Plane project instead of hard-coding them
- Moves the work item to "In Progress" when implementation starts
- Moves it to "In Review" when the PR is ready
- Adds the `Closes <identifier>` line to the PR description so the item is closed when the PR merges

## Prerequisite: MCP Server

One `plane` MCP server serves all workspaces. Every call passes the workspace slug (the first path segment of the Plane URL) in the `workspace` parameter. Register the server once at user scope according to the documentation of the Plane MCP server (`uvx plane-mcp-server`), with your Plane base URL and API key.

Never write the API key into the repository. It stays in the MCP configuration.

## Repository Configuration (CLAUDE.md)

Each repository declares its Plane project in its `CLAUDE.md`. Add the workspace slug as `workspace:` to this section so that the command can pass it to every MCP call.

```markdown
## Plane Integration

- **Workspace**: `<workspace-slug>`
- **Project**: `PROJ` (project identifier, not the UUID)
- **Status Override** (optional): only if the state names differ from the defaults
  - In Progress: `In Progress`
  - In Review: `In Review`
```

`Project` is the short identifier shown as the prefix of work item identifiers (`PROJ` in `PROJ-123`). The command resolves it to the project UUID with `project list`. Do not store UUIDs in `CLAUDE.md`.

If no `## Plane Integration` section exists, the command stops and asks for the project identifier. It does not guess.

## MCP Tools Used

### Resolve the project

```text
mcp__plane__project  workspace=<slug>  action=list
→ match identifier == "TF" → project id (UUID)
```

### Read the work item

```text
mcp__plane__workitem  workspace=<slug>  action=retrieve_by_identifier  workitem_identifier="PROJ-123"
→ id, name, description_html, state, labels, type
```

If `retrieve_by_identifier` is unavailable, list the project's items with `action=list` and a PQL filter, then match the sequence number.

### Read the states

Do not hard-code state UUIDs or names. Read them at runtime:

```text
mcp__plane__state  workspace=<slug>  action=list  project_id=<uuid>
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
mcp__plane__workitem  workspace=<slug>  action=update  project_id=<uuid>  workitem_id=<id>  state=<state uuid>
```

`update` changes only the fields you pass.

### Comment on progress

```text
mcp__plane__workitem_comment  workspace=<slug>  action=create  project_id=<uuid>  workitem_id=<id>
  comment_html="<p>Implementation started</p><ul><li>Branch: <code>feature/proj-123-...</code></li><li>Worktree: <code>.worktrees/task-proj-123/</code></li></ul>"
```

Comments are optional. Only write them at start and at PR creation.

## Branch Naming

Use the identifier in lower case, consistent with Linear:

```text
feature/proj-123-<description>
```

## Closing

The PR description contains a closing keyword for the work item:

```markdown
Closes PROJ-123
```

Use `Refs PROJ-123` instead only when the work item stays open on purpose (e.g. a production step or follow-up work). State the reason in the PR text.

The command does not set the Plane state to Done itself. A `Closes` keyword only closes GitHub issues; it does not change a Plane work item. Move the item to its completed state manually in Plane, unless the workspace has a Plane–GitHub integration configured that does this on merge (verify this in Plane before relying on it).

## Error Handling

| Error | Cause | Resolution |
| ----- | ----- | ---------- |
| `No module named 'fastmcp...'` | `plane` server installation broken | Reinstall or refresh the server: `uvx --refresh plane-mcp-server` |
| Project identifier not found | `CLAUDE.md` value does not match Plane | Check identifier in Plane, fix `CLAUDE.md` |
| Ambiguous state | Several `started` states and no override | Ask user, then add override to `CLAUDE.md` |
| 401 / 403 | Invalid API key or missing permissions | Regenerate key, check workspace membership |
| Work item not found | Wrong identifier or archived item | Verify identifier, check archive |

## See Also

- [workflow.md](./workflow.md) - Complete workflow
- [linear.md](./linear.md) - Linear provider
- [filesystem.md](./filesystem.md) - Filesystem provider
