---
name: wiki-query
description: Answers a question against an Obsidian-based LLM knowledge wiki. Performs index-first search, reads relevant pages, synthesizes an answer with citations, and optionally files the synthesis back as a new wiki page. Triggers when the user runs /wiki:query or asks a question that should be answered from the curated wiki rather than from raw sources.
---

# wiki-query

## When to invoke

The user runs `/wiki:query <question>`, or asks a question that should be answered from the curated `<wiki-root>/_wiki/` rather than from raw sources or web search.

## Configuration

Same vault layout as `wiki-ingest`.

## Inputs

A natural-language question (German or English).

## Workflow

1. **Index-first search:**
    - Read `<wiki-root>/_wiki/index.md`.
    - Identify top candidates by filename match, tags, and one-liner match (heuristic, no embeddings).
    - Take at most five to seven candidates as the initial set.

2. **Full-text fallback:**
    - If the index yields no good matches: `grep -ril "<keyword>" "<wiki-root>/_wiki/"` for terms from the question.
    - Add the top five hits.

3. **Read the pages:**
    - Load all candidates with the `Read` tool.
    - Extract the relevant sections.

4. **Synthesize with citations:**
    - Write the answer; format citations as `[[Page#Heading]]`.
    - Use multi-citations for claims supported by multiple sources.
    - Name contradictions explicitly ("X says A, Y says B").

5. **Propose answer format:**
    - Default: inline (chat reply).
    - On request: a new `_wiki/compare/<name>.md` page, a table, a cheatsheet, or Marp slides.

6. **Filing-back prompt:**
    - "Should I file this synthesis as `_wiki/compare/<proposed-name>.md`?"
    - Default: no. On yes: create the page using the `wiki-compare.md` template, populate `sources:` with all consulted pages, update index and log, run `markdown-syntax-formatter`.

7. **Knowledge-gap hint:**
    - If the answer is incomplete: "Sources X, Y would help here — should I prepare `/wiki:ingest` for them?" — or offer a web search with user approval.

## Edge Cases

- **No index entries match:** fall back to full text. If full text also finds nothing, state plainly that the wiki has nothing on this topic, plus a suggestion of what to ingest.
- **Synthesized answer would exceed approximately 300 words:** offer the filing-back option more prominently.
- **Question is actually an ingest** ("digest this for me"): forward to `/wiki:ingest`.

## Output

Answer with citations, plus an optional pointer to the filed synthesis page.
