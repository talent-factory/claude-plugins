---
name: wiki-think
description: Argues with your notes in an Obsidian-based LLM knowledge wiki — challenges assumptions (devil's advocate), surfaces non-obvious connections, or asks Socratic questions. Optionally saves the result as a wiki page. Triggers when the user runs /wiki:think, asks to "challenge this note", "poke holes in my thinking", "find connections between my notes", or "ask me Socratic questions about X".
---

# wiki-think

## When to invoke

The user runs `/wiki:think <topic-or-page> [--mode challenge|connect|socratic] [--save]`,
or asks the assistant to challenge a note, find connections across notes, or ask
probing questions about a topic in the wiki.

## Configuration

Same vault layout as `wiki-ingest`. Default mode (no `--mode`) is `challenge`.
Modes are combinable: `--mode challenge,connect`.

## Workflow

1. **Load context (index-first).** Read `<wiki-root>/_wiki/index.md`, identify the
   page(s) matching the topic, and read them plus their directly `related:` pages.
2. **Apply the requested mode(s)** using `references/thinking-modes.md`:
   - `challenge` — surface weak assumptions, counter-examples, and blind spots.
   - `connect` — find non-obvious links between distant pages; propose new
     cross-references or a hub theme.
   - `socratic` — ask a short sequence of probing questions instead of answering.
3. **Output to terminal** by default.
4. **`--save`** → write `<wiki-root>/_wiki/thinking/<slug>.md` with frontmatter
   `kind: wiki, type: thinking`, `sources:` set to the referenced page paths,
   `related:` set to those pages (bidirectional — add the back-reference on each).
   Then run the write-time validation gate:

    ```bash
    python3 "${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/validate.py" \
      --vault-root "<wiki-root>/.." --target "<thinking-file>" \
      --rules frontmatter,kindtype,deadlinks,asymmetric
    ```

    Resolve critical findings before finalizing. `type: thinking` is exempt from
    the empty-`sources:` semantic rule, so a thinking page with no sources is valid.

## Output

- Terminal: the challenge / connections / questions for the chosen mode(s).
- With `--save`: the created `thinking/<slug>.md` path and any cross-references added.
