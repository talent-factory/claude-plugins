# Linear Integration Guide

Anleitung zur Integration des Linear MCP Servers mit Claude Code.

## Übersicht

Der Linear MCP Server ermöglicht Claude Code direkten Zugriff auf Linear-Daten:

- Issue-Abruf und Suche
- Status-Updates
- Comment-Erstellung
- Workflow-Management

## Installation

### 1. Linear API Key generieren

1. Öffne Linear: https://linear.app
2. Gehe zu **Settings** → **API**
3. Klicke **Create new API key**
4. **Scopes auswählen**: `read`, `write`
5. API Key kopieren

### 2. MCP Server konfigurieren

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

### 3. Environment Variable setzen

**~/.env**:

```bash
export LINEAR_API_KEY="lin_api_xxxxxxxxxxxxxxxxxxxxxxxx"
```

### 4. Verifikation

```bash
# In Claude Code:
"List my Linear issues"
"Show Linear team information"
```

## MCP Server Funktionen

### `linear_get_issue`

Issue-Details abrufen:

```javascript
linear_get_issue({ issueId: "PROJ-123" })
// → { id, identifier, title, description, state, assignee, labels }
```

### `linear_list_my_issues`

Zugewiesene Issues auflisten:

```javascript
linear_list_my_issues({ filter: "in_progress" })
// → Array von Issue-Objekten
```

### `linear_update_issue_state`

Issue-Status ändern:

```javascript
linear_update_issue_state({ issueId: "PROJ-123", stateId: "state_inprogress" })
```

### `linear_create_comment`

Comment hinzufügen:

```javascript
linear_create_comment({ issueId: "PROJ-123", body: "Started implementation" })
```

### `linear_get_workflow_states`

Workflow-States abrufen:

```javascript
linear_get_workflow_states({ teamId: "team_abc" })
// → [{ id: "state1", name: "Backlog" }, ...]
```

## Workflow-States Mapping

**Standard-Workflow**:

| State | Bedeutung |
|-------|-----------|
| Backlog | Neue Issues |
| Todo | Geplant |
| In Progress | Wird bearbeitet |
| In Review | PR erstellt |
| Done | Abgeschlossen |
| Canceled | Abgebrochen |

## Team & Projekt Setup

### Team-ID ermitteln

```graphql
query GetTeams {
  teams {
    nodes { id, name, key }
  }
}
```

### Projekt-Konfiguration in CLAUDE.md

```markdown
## Linear Integration

### Teams
- **Engineering**: `PROJ` (Team-Key)
  - Team-ID: `team_abc123`
  - Workflow: Backlog → In Progress → In Review → Done

### Status-IDs
- Backlog: `state_backlog123`
- In Progress: `state_inprogress456`
- In Review: `state_review789`
- Done: `state_done012`
```

## API Rate Limits

- **Rate Limit**: 1.200 Requests/Stunde
- **Burst**: 100 Requests/Minute

**Empfehlungen**:
- ✅ Batching nutzen
- ✅ Caching für häufig abgerufene Daten
- ❌ Keine unnötigen API-Calls

## Security

**API Key Schutz**:
- ✅ Environment Variables nutzen
- ✅ Niemals in Git committen
- ✅ `.env` in `.gitignore`
- ✅ Key alle 90 Tage rotieren

## Error Handling

| Error | Ursache | Lösung |
|-------|---------|--------|
| 401 | API Key ungültig | Neuen Key generieren |
| 403 | Fehlende Permissions | Scopes prüfen |
| 404 | Issue existiert nicht | Issue-ID validieren |
| 429 | Rate Limit | Warten und Retry |

## Weiterführende Ressourcen

- **Linear API Docs**: https://developers.linear.app/docs
- **GraphQL Schema**: https://studio.apollographql.com/public/Linear-API/home
- **Linear MCP Server**: https://github.com/modelcontextprotocol/servers

## Siehe auch

- [workflow.md](./workflow.md) - Workflow-Beispiele
- [best-practices.md](./best-practices.md) - Best Practices
- [troubleshooting.md](./troubleshooting.md) - Problemlösungen

