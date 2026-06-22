---
name: wiki-migrate-file
description: Migrates a legacy file from an Obsidian-based knowledge vault into the LLM-Wiki schema. Analyzes the file, proposes a split into raw and wiki content, writes target files with proper frontmatter, pulls cross-references, updates index and log, then deletes the original. Cluster mode handles thematic groups. Triggers when the user runs /wiki:migrate-file, asks to "migrate this legacy note", or wants to bulk-migrate a thematic cluster into the wiki.
---

# wiki-migrate-file

## When to invoke

- `/wiki:migrate-file <path>` — single legacy file inside the wiki root.
- `/wiki:migrate-file --cluster "<name>"` — thematic cluster (for pilot or batch migrations).

## Configuration

Same vault layout as `wiki-ingest`. Operates on files under `<wiki-root>/` that live outside `_raw/` and `_wiki/`.

## Workflow for a Single File

1. **Read the file** with the `Read` tool.

2. **Analyze the content:**
    - Has web-clipper frontmatter (URL, author)? → likely contains a source portion.
    - Has personal analysis (own headings, bullet lists, "Created:" markers)? → likely contains wiki content.
    - Determine: pure source / pure wiki / hybrid.
    - Determine `type:` (concept/tool/compare/hub for wiki; clipping/chat/note/transcript for source).

3. **Propose the migration plan to the user:**

    ```text
    File: <legacy-path>
    Detected: hybrid
      - Source portion: YouTube description with redirect URLs
      - Wiki portion:   personal setup notes

    Plan:
      - Source portion → _raw/clippings/2025-mcp-installer-youtube.md
      - Wiki portion   → _wiki/tools/MCP-Installer.md (kind: wiki, type: tool)
      - Cross-ref to existing _wiki/concepts/MCP.md (related: bidirectional)

    Confirm?
    ```

4. **After user confirmation:**
    - Write the source portion with `kind: source` frontmatter, `ingested: <today>`, `distilled_into: [<wiki-page>]`.
    - Write the wiki portion with `kind: wiki` frontmatter, template-compliant, `sources: [<raw-page>]`, `supersedes: ["<legacy-path>"]`, `last_synthesized: <today>`.
    - Maintain bidirectional cross-references to other wiki pages.

5. **Validate before finalizing (write-time gate).** Run the shared validator on each
   written target file:

   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/validate.py" \
     --vault-root "<wiki-root>/.." --target "<written-file>" \
     --rules frontmatter,kindtype,deadlinks,asymmetric
   ```

   Resolve all **critical** findings before deleting the original legacy file; list
   **minor** findings in the summary. On validator exit code 2, fall back to the
   deterministic rules in `${CLAUDE_PLUGIN_ROOT}/skills/_shared/validation-rules.md`.
   Never delete the original until the migrated file is free of critical findings.

6. **Update index and log** (see `wiki-ingest` skill, steps 6–7).

7. **Delete the legacy file** with `git rm`. Rationale: git history preserves the file, and the `supersedes:` field points to the old path.

8. **Run the markdown-syntax-formatter agent** (from the education plugin) on every touched file. If the education plugin is not installed, skip this step.

## Workflow for Cluster Mode

```text
/wiki:migrate-file --cluster "MCP"
```

1. **Identify the cluster:** find files thematically related to `<name>` via filename match, tag match, or an explicit user list.
2. **Show the cluster plan:** all detected files plus proposed migration targets, presented in a table. The user confirms or edits.
3. **Per file:** apply the single-file workflow steps 1, 2, 4, 5, 6, 7, and 8 — that is, read the file, analyze, then write/validate/update/cross-ref/log/format. Step 3 (the per-file confirmation prompt) is **skipped** because the cluster confirmation in step 2 above already covers it. Only **one** user confirmation up front; the skill then processes the cluster sequentially.
4. **Create a hub page** if the cluster contains five or more pages: `<wiki-root>/_wiki/concepts/<name>.md` with `type: hub`, listing all migrated pages in their respective hub sections.
5. **One commit at the end** with a suggested message.

## Edge Cases

- **File is genuinely source-only** (e.g., a raw clipping): place under `_raw/` only; do not create a wiki page unless the user requests one.
- **File is genuinely wiki-only** (e.g., personal analysis without a clipping): place under `_wiki/` only. An empty `sources:` field is acceptable when the content draws on the user's own knowledge.
- **File has no sensible schema mapping** (e.g., it is just a list of email addresses): ask the user whether to relocate it to a system folder, or to delete it.

## Output

- List of created, moved, and deleted files
- Number of new cross-references
- Log entry or entries
- In cluster mode: hub page if created
