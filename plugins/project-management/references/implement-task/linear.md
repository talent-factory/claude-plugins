# Linear Integration Guide

Guide to integrating the Linear MCP Server with Claude Code.

## Overview

The Linear MCP Server provides Claude Code with direct access to Linear data:

- Issue retrieval and search
- Status updates
- Comment creation
- Workflow management

## Installation

### 1. Generate Linear API Key

1. Navigate to Linear: https://linear.app
2. Go to **Settings** → **API**
3. Click **Create new API key**
4. **Select scopes**: `read`, `write`
5. Copy the API key

### 2. Configure MCP Server

**~/.config/claude/mcp_config.json**:

```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-linear"],
      "env": {
        "LINEAR_API_KEY": "${LINEAR_API_KEY}"
      }
    }
  }
}
```

### 3. Set Environment Variable

**~/.env**:

```bash
export LINEAR_API_KEY="lin_api_xxxxxxxxxxxxxxxxxxxxxxxx"
```

### 4. Verification

```bash
# In Claude Code:
"List my Linear issues"
"Show Linear team information"
```

## MCP Server Functions

### `linear_get_issue`

Retrieve issue details:

```javascript
linear_get_issue({ issueId: "PROJ-123" });
// → { id, identifier, title, description, state, assignee, labels }
```

### `linear_list_my_issues`

List assigned issues:

```javascript
linear_list_my_issues({ filter: "in_progress" });
// → Array of issue objects
```

### `linear_update_issue_state`

Modify issue status:

```javascript
linear_update_issue_state({ issueId: "PROJ-123", stateId: "state_inprogress" });
```

### `linear_create_comment`

Add a comment:

```javascript
linear_create_comment({ issueId: "PROJ-123", body: "Started implementation" });
```

### `linear_get_workflow_states`

Retrieve workflow states:

```javascript
linear_get_workflow_states({ teamId: "team_abc" });
// → [{ id: "state1", name: "Backlog" }, ...]
```

## Workflow State Mapping

**Standard Workflow**:

| State       | Definition       |
| ----------- | ---------------- |
| Backlog     | New issues       |
| Todo        | Scheduled        |
| In Progress | Currently active |
| In Review   | PR created       |
| Done        | Completed        |
| Canceled    | Discontinued     |

## Team and Project Setup

### Determine Team ID

```graphql
query GetTeams {
  teams {
    nodes {
      id
      name
      key
    }
  }
}
```

### Project Configuration in CLAUDE.md

```markdown
## Linear Integration

### Teams

- **Engineering**: `PROJ` (Team Key)
  - Team ID: `team_abc123`
  - Workflow: Backlog → In Progress → In Review → Done

### Status IDs

- Backlog: `state_backlog123`
- In Progress: `state_inprogress456`
- In Review: `state_review789`
- Done: `state_done012`
```

## API Rate Limits

- **Rate Limit**: 1,200 requests/hour
- **Burst**: 100 requests/minute

**Recommendations**:

- Utilize batching
- Cache frequently retrieved data
- Avoid unnecessary API calls

## Security

**API Key Protection**:

- Use environment variables
- Never commit to Git
- Add `.env` to `.gitignore`
- Rotate keys every 90 days

## Error Handling

| Error | Cause                    | Resolution         |
| ----- | ------------------------ | ------------------ |
| 401   | Invalid API key          | Generate a new key |
| 403   | Insufficient permissions | Verify scopes      |
| 404   | Issue does not exist     | Validate issue ID  |
| 429   | Rate limit exceeded      | Wait and retry     |

## Additional Resources

- **Linear API Documentation**: https://developers.linear.app/docs
- **GraphQL Schema**: https://studio.apollographql.com/public/Linear-API/home
- **Linear MCP Server**: https://github.com/modelcontextprotocol/servers

## See Also

- [workflow.md](./workflow.md) - Workflow examples
- [best-practices.md](./best-practices.md) - Best practices
- [troubleshooting.md](./troubleshooting.md) - Problem resolution
