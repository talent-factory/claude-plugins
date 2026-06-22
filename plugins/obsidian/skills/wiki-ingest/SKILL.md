---
name: wiki-ingest
description: Ingests a new source (web clipping, AI chat export, raw note, transcript) into an Obsidian-based LLM knowledge wiki. Files the source under _raw/, distills it into one or more _wiki/ pages, updates index and log, and pulls bidirectional cross-references. Triggers when the user asks to "ingest this source", "digest this clipping into the wiki", or runs /wiki:ingest while working in a configured wiki vault.
---

# wiki-ingest

## When to invoke

The user runs `/wiki:ingest <path-or-url-or-text>`, asks the assistant to "digest this source" or "ingest this clipping" while working in an Obsidian vault that follows the LLM-Wiki schema described below.

## Configuration

The skill expects the following vault layout. Default paths are shown; override via `wiki_root: <path>` in the vault's `CLAUDE.md`.

- `<wiki-root>/_raw/` — raw source files, organized by type subfolder
- `<wiki-root>/_wiki/` — distilled wiki pages
- `<wiki-root>/_wiki/index.md` — section-based index of all wiki pages
- `<wiki-root>/_wiki/log.md` — append-only operation log
- `<wiki-root>/_wiki/templates/` — frontmatter templates per source/wiki type

Default `<wiki-root>` is `Wiki/`.

## Inputs

One of:

- File path inside the vault (e.g., `Clippings/foo.md`)
- URL (web article — fetched via `WebFetch` first)
- Free text (a raw note pasted into the conversation)

## Workflow

1. **Detect source type:**
    - Markdown file with web-clipper frontmatter → `clipping`
    - File from an AI chat export folder → `chat`
    - File from a transcription folder → `transcript`
    - Free text or other → `note`

2. **Store the raw file** at `<wiki-root>/_raw/<type>/<YYYY-MM-DD>-<slug>.md`.
    - Slug: lowercase, dashes, max 60 characters, derived from the title or URL path.
    - Frontmatter follows the matching template in `<wiki-root>/_wiki/templates/`.
    - Required fields: `kind: source`, `type`, `title`, `domain`, `source_url` (if applicable), `ingested: <today>`, `distilled_into: []`.

3. **Identify topics and confirm with the user:**
    - Read the source and extract one to three main topics.
    - Read `<wiki-root>/_wiki/index.md` and check which wiki pages already exist.
    - Propose: "Topics are A, B. Plan: new page `_wiki/tools/X.md`, update `_wiki/concepts/Y.md`. Confirm?"
    - Wait for user confirmation or correction.

4. **Write or update wiki pages** using the matching template from `<wiki-root>/_wiki/templates/`.
    - Required wiki page fields: `kind: wiki`, `type` (concept/tool/compare/hub), `title`, `domain`, `status: active`, `tags`, `sources`, `related`, `created`, `updated`, `last_synthesized`.
    - Append the new raw file path to the wiki page's `sources:` field.
    - Append the touched wiki page paths to the raw file's `distilled_into:` field.

4a. **Validate before finalizing (write-time gate).** After writing each touched
    wiki/raw file, run the shared validator on it:

    ```bash
    python3 "${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/validate.py" \
      --vault-root "<wiki-root>" --target "<touched-file>" \
      --rules frontmatter,kindtype,deadlinks,asymmetric
    ```

    - **critical** findings: fix them (auto-fixable ones — `created`, `domain`,
      asymmetric back-refs — apply directly; others surface to the user with the
      finding text), then re-validate. Do NOT report the page as ingested while a
      critical finding remains.
    - **minor** findings: include them in the final summary; do not block.
    - Validator exit code 2 (PyYAML missing): fall back to the deterministic rules
      in `${CLAUDE_PLUGIN_ROOT}/skills/_shared/validation-rules.md` and continue.

5. **Pull cross-references:**
    - Grep the index for related topics: `grep -i "<topic>" <wiki-root>/_wiki/index.md`.
    - For each match, add the page bidirectionally to the `related:` field on both sides (asymmetric links are a lint error).
    - For critical cross-references (≥3 new connections per page), confirm with the user.

6. **Update the index** (`<wiki-root>/_wiki/index.md`):
    - Insert new wiki pages into the appropriate section (Concepts/Tools/Compare/Hubs).
    - Format: `- [[Title]] — one-liner | sources: N | updated: YYYY-MM-DD`.
    - Increment the Sources section counter.
    - Sort alphabetically within each section.

7. **Append a log entry** to `<wiki-root>/_wiki/log.md`:

    ```text
    ## [YYYY-MM-DD HH:MM] ingest | <source title>
    - source: _raw/<type>/<date>-<slug>.md
    - wiki touched: _wiki/<...>.md (new), _wiki/<...>.md (update)
    - cross-refs added: N
    - reconcile: <none | "<old> → <new>" | contradiction-flagged>
    ```

8. **Run the markdown-syntax-formatter agent** (from the education plugin) on every newly created or modified file. If the education plugin is not installed, skip this step.

## Edge Cases

- **Source already exists in `_raw/`** (path match): ask the user — skip / re-distill (re-validate existing wiki refs) / supersede (mark old as `status: deprecated`).
- **Wiki page on this topic already exists:** update instead of creating. When the
  new source contradicts an existing claim on the page (semantic rule 6 in
  `${CLAUDE_PLUGIN_ROOT}/skills/_shared/validation-rules.md`), run
  **Contradiction-Reconcile** before writing:
    1. Present both sides explicitly:
       `OLD: "<claim>" (sources: …)` vs. `NEW: "<claim>" (source: <new source>)`.
    2. Propose a concrete resolved wording, noting whether the old claim is
       superseded (and add a timeline note if the page tracks one).
    3. Ask the user to confirm.
       - **Confirm** → revise the page with the resolved wording; log
         `reconcile | <old> → <new>`.
       - **Reject** → do not overwrite; add a contradiction callout to the page
         (`> [!warning] Contradiction: …`) and log `contradiction-flagged`.
    Never silently overwrite a curated claim.
- **Source covers ≥3 distinct topics:** split into multiple wiki pages; all share the same source in `sources:`.
- **URL input:** fetch via `WebFetch` first, then handle as a markdown clipping.

## Output

The user receives:

- List of created and updated files
- Number of cross-references added
- Log entry preview
- Hint to run `/wiki:lint` if a cross-reference cluster (≥5 pages) lacks a hub page
- Validation summary: critical findings resolved, minor findings listed
