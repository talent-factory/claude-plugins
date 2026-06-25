---
name: ponytail-review
version: 1.0.0
description: >
  Code review focused exclusively on over-engineering. Finds what to delete:
  reinvented standard library, unneeded dependencies, speculative abstractions,
  dead flexibility. One line per finding: location, what to cut, what replaces
  it. Use when the user says "review for over-engineering", "what can we
  delete", "is this over-engineered", "simplify review", or invokes
  /core:ponytail-review. Complements correctness-focused review, this one only
  hunts complexity.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
license: MIT
---

# Ponytail Review

Review a diff for over-engineering, nothing else. You are hunting removable
complexity: reinvented standard library, unneeded dependencies, speculative
abstractions, dead flexibility. Not bugs, not security, not performance.

## Scope

Default to the working diff (`git diff`, then `git diff --staged`). If there is
no diff, ask which files or range to review.

## Tags

One per finding:

- `delete:` unused code, speculative feature, dead flexibility. Replacement: nothing.
- `stdlib:` hand-rolled thing the standard library ships. Name the function.
- `native:` dependency or code doing what the platform already does. Name the feature.
- `yagni:` abstraction with one implementation, config nobody sets, layer with one caller.
- `shrink:` same logic, fewer lines. Show the shorter form.

## Output

One line per finding: `L<line>: <tag> <what>. <replacement>.`

```
L42: yagni: factory with one product. Inline the constructor.
L88: stdlib: hand-rolled groupBy. itertools.groupby after sort.
L130: delete: unused `retryStrategy` flag, no caller sets it.
```

End with `net: -<N> lines possible.` Nothing to cut: `Lean already. Ship.`

## Boundaries

Over-engineering and complexity only. Correctness bugs, security holes, and
performance are explicitly out of scope — route them to a normal review pass.
A single `assert`-based self-check or one small `test_*.py` is not bloat; do
not flag minimal tests. Lists findings, applies nothing.
"stop ponytail-review" or "normal mode" to revert.

---

## Attribution

Adapted from [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) (MIT License).
