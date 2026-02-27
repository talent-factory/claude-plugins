---
description: Display the edit history of a GitHub pull request description
category: github
allowed-tools: Bash
---

# Display Pull Request Edit History

Retrieve the complete edit history of a pull request description and display it in a formatted table.

## Usage

Standard (interactive - prompts for parameters):

```bash
/git-workflow:pr-edit-history
```

With parameters:

```bash
/git-workflow:pr-edit-history owner/repo#123
```

Or specified individually:

```bash
/git-workflow:pr-edit-history --owner anthropics --repo claude-code --pr 456
```

## Workflow

1. **Determine parameters**:
   - If no parameters provided, prompt the user for:
     - Repository owner (e.g., "anthropics")
     - Repository name (e.g., "claude-code")
     - Pull request number (e.g., "123")
   - If provided in format `owner/repo#pr`, parse the parameters
   - If provided individually (`--owner`, `--repo`, `--pr`), use those

2. **Execute GitHub GraphQL query**:
   - Use `gh api graphql` to retrieve the edit history
   - Query:
     ```graphql
     query {
       repository(owner: "OWNER", name: "REPO") {
         pullRequest(number: PR_NUMBER) {
           userContentEdits(first: 100) {
             nodes {
               editedAt
               editor {
                 login
               }
             }
           }
         }
       }
     }
     ```

3. **Process data**:
   - Parse the JSON response
   - Extract editedAt (timestamp) and editor.login (username)
   - Sort by timestamp (oldest first)

4. **Format table**:
   - Create a Markdown table with the following columns:
     - `#` (sequential number)
     - `Edited At (UTC)` (timestamp in readable format)
     - `Editor` (username)
   - Format timestamps as: `YYYY-MM-DD HH:MM:SS`
   - Example:
     ```
     | #  | Edited At (UTC)     | Editor    |
     |----|---------------------|-----------|
     | 1  | 2025-12-01 00:08:34 | dsenften  |
     | 2  | 2025-12-01 15:57:21 | dsenften  |
     | 3  | 2025-12-01 16:24:33 | dsenften  |
     ```

5. **Output**:
   - Display the table
   - Add summary:
     - Total number of edits
     - Time span (first to last edit)
     - List of editors (unique)

## Error Handling

- **gh CLI not installed**: Inform user that `gh` CLI must be installed
- **Not authenticated**: Point to `gh auth login`
- **Repository not found**: Verify owner and repo name
- **PR not found**: Verify PR number
- **No edit history**: Report that the PR description was never edited
- **More than 100 edits**: Note that only the first 100 are displayed

## Examples

### Example 1: Interactive Usage
```bash
/git-workflow:pr-edit-history
# Prompts for: Owner? Repo? PR number?
# Displays table
```

### Example 2: Compact Syntax
```bash
/git-workflow:pr-edit-history anthropics/claude-code#789
```

### Example 3: Explicit Parameters
```bash
/git-workflow:pr-edit-history --owner anthropics --repo claude-code --pr 789
```

## Extended Options

The user can optionally specify additional options:

- `--limit N`: Limit to the last N edits (default: all up to 100)
- `--json`: Output as JSON instead of table
- `--export FILE`: Export table to file (Markdown or CSV)

## Technical Details

- **GraphQL API**: Uses GitHub GraphQL API v4
- **Rate limits**: Observes GitHub API rate limits (5000 requests/hour for authenticated requests)
- **Authentication**: Uses the authentication of the `gh` CLI
- **Timezone**: All timestamps are displayed in UTC

## Notes

- The initial creation of the PR description does not count as an edit
- Only manual edits are displayed (no automatic updates)
- Bot edits (e.g., from GitHub Actions) are also displayed
