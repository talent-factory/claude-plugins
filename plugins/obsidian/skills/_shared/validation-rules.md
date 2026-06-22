# LLM-Wiki Validation Rules (shared)

Single source of truth for wiki validation. The deterministic rules are
implemented in `scripts/validate.py`; the semantic rules are applied by the
calling skill via LLM judgement. Skills MUST cite this file rather than
re-stating rules inline, to prevent drift.

## How to run the deterministic checks

```bash
python3 <plugin>/skills/_shared/scripts/validate.py \
  --vault-root <vault-root> [--target <file.md>] [--rules frontmatter,kindtype,deadlinks,asymmetric]
```

Output is a JSON array of findings: `{file, severity, rule, message, autofixable}`,
`severity ∈ {critical, minor}`. Exit code `1` when any finding is `critical`,
`0` otherwise, `2` when PyYAML is missing (fall back to the prose rules below).

## Severity policy

- **critical** — blocks plugin-driven writes until fixed or user-confirmed:
  missing/invalid frontmatter, missing required field, invalid `kind`/`type`.
- **minor** — reported, never blocks: dead links (may be legitimate forward
  references), asymmetric `related:` fields.

## Deterministic rules (validate.py)

1. **Frontmatter completeness.** Required for all: `kind, type, title, domain,
   status, tags, created`. Wiki pages also require `updated`; sources require
   `ingested` (not `updated`). `_wiki/log.md` is exempt. Missing `created`/`domain`
   are auto-fixable (derive `created` from git, set `domain` from the vault).
2. **`kind`/`type` consistency.** `kind: wiki` → `type ∈ {concept, tool, compare,
   hub, note, thinking}`. `kind: source` → `type ∈ {clipping, chat, note,
   transcript}`.
3. **Dead links.** Wikilinks `[[X]]` must resolve against `_wiki/`/`_raw/` basenames
   or vault media files. Normalize: strip alias (`[[T|a]]`, `[[T\|a]]`), strip
   `#anchor`, resolve full paths by basename, drop `.md`. Skip links inside inline
   code or fenced code blocks. Skip `log.md`, `lint-report-*.md`, `maintain-report-*.md`.
4. **Asymmetric `related:`.** If `A.related` resolves to wiki page `B`, then
   `B.related` must resolve back to `A`. Refs to non-wiki targets are ignored.
   Auto-fixable (add the missing back-reference).

## Semantic rules (LLM judgement, not in validate.py)

5. **Stale claims.** A wiki page whose `updated` is older than six months while a
   `sources:` entry has an `ingested` date newer than `last_synthesized`.
6. **Contradiction detection.** Pages that share an entity in `related:` but make
   conflicting claims. On ingest, this triggers Contradiction-Reconcile.
7. **Hub gaps.** Five or more pages sharing a tag/theme with no `type: hub` page.
8. **Source gaps.** A wiki page with empty `sources:` that asserts factual claims.
   `type: thinking` pages are EXEMPT — derived reasoning is not a factual assertion,
   so an empty `sources:` is allowed.

## Template compliance (semantic)

- `type: tool` → `## Setup` heading (informational only for hosted/hardware tools).
- `type: compare` → a table under `## Options` or `## Direktvergleich`.
- `type: hub` → all five sections: `## Overview`, `## Concepts`, `## Tools`,
  `## Compare Pages`, `## Related Hubs`.
