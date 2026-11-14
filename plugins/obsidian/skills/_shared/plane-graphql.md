# Plane work items via GraphQL

How `today` and `weekly-review` read work items from a Plane instance through the `plane` MCP server. The caller decides which items it keeps (assignee, state, dates); this file covers fetching them. Every call passes `workspace: $PLANE_WORKSPACE`.

The self-hosted Plane edition has two limits that shape this step:

- **No PQL**, neither in `workitem list` nor in GraphQL `workItems(pql:)`. Both
  reject it with HTTP 400. Filter client-side.
- **No workspace-wide list.** `workitem list` and a root-level `workItems`
  without `project` return HTTP 404. Go through the projects instead.

GraphQL (`mcp__plane__graphql_query`) fetches all projects in one call:

1. `mcp__plane__member` with `action: me` → `me.id`.
2. One GraphQL query for every project:
   ```graphql
   { projects { id identifier
       workItems(first: 100) {
         hasNextPage nextCursor
         results { identifier name priority targetDate completedAt
                   state { name group } assignees { id } } } } }
   ```
   The result is large (all items, including done ones) and lands in a file.
   Filter it with `jq` or Python instead of reading it into context.
3. For every project with `hasNextPage: true`, page through it with
   `project(id:)`. **Keep going until `hasNextPage` is `false`**: open items
   (e.g. an old epic) often sit on the last page, so stopping early drops
   real work. Use a safety cap of 20 pages per project and note it in the
   terminal summary if the cap is hit.
   ```graphql
   { project(id: "<project id>") { identifier
       workItems(first: 100, after: "<nextCursor>") {
         hasNextPage nextCursor
         results { identifier name priority targetDate completedAt
                   state { name group } assignees { id } } } } }
   ```
   Notes for unattended runs:
   - Use the `nextCursor` the previous page returned (e.g. `100:1:0`, then
     `100:2:0`), never a guessed one.
   - A page may come back with `results` as a compact table string
     (`[N]{field,...}` header plus CSV-like rows) instead of a JSON array.
     Parse both forms.
   - On HTTP 429, wait 5 seconds and retry the same page, at most 2 times,
     before skipping it. If a page is skipped, say so in the terminal summary.

If the GraphQL tool is unavailable, fall back to REST: `mcp__plane__project`
`action: list`, then `mcp__plane__workitem` `action: list` per project with
`project_id` and `expand: state`. Note the REST assignee ids can differ from
`me.id`; compare via `expand: assignees` or skip the assignee check and say so.
