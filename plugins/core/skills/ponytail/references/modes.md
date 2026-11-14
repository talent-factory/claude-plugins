# Ponytail modes

Adapted from [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) (MIT License). All three modes read and report; none changes a file unless the user asks. They cover over-engineering and complexity only. Bugs, security and performance belong to a normal review. One small `assert`-based self-check or one `test_*.py` is not bloat; do not flag minimal tests. "normal mode" ends a mode.

## Tags (review and audit)

One per finding:

- `delete:` unused code, speculative feature, dead flexibility. Replacement: nothing.
- `stdlib:` hand-rolled thing the standard library ships. Name the function.
- `native:` dependency or code doing what the platform already does. Name the feature.
- `yagni:` abstraction with one implementation, config nobody sets, layer with one caller.
- `shrink:` same logic, fewer lines. Show the shorter form.

## review

Scope: the working diff (`git diff`, then `git diff --staged`). With no diff, ask which files or range to review.

Output, one line per finding: `L<line>: <tag> <what>. <replacement>.`

```
L42: yagni: factory with one product. Inline the constructor.
L88: stdlib: hand-rolled groupBy. itertools.groupby after sort.
L130: delete: unused `retryStrategy` flag, no caller sets it.
```

End with `net: -<N> lines possible.` Nothing to cut: `Lean already. Ship.`

## audit

Scope: the whole tree, skipping `node_modules`, `.git`, `target/`, `build/`, `dist/` and other build output. Hunt for: dependencies the stdlib or platform already ships, single-implementation interfaces, factories with one product, wrappers that only delegate, files exporting one thing, dead flags and config, hand-rolled stdlib.

Output, ranked with the biggest cut first, one line per finding: `<tag> <what to cut>. <replacement>. [path]`. End with `net: -<N> lines, -<M> deps possible.` Nothing to cut: `Lean already. Ship.`

## debt

Every deliberate shortcut carries a `ponytail:` comment naming its ceiling and upgrade path (`ponytail: <ceiling>, <upgrade path>`). Collect them so a deferral cannot quietly become permanent.

Scan: `grep -rnE '(#|//) ?ponytail:' .` (add other comment prefixes your stack uses; skip `node_modules`, `.git` and build output). The comment prefix keeps prose that merely mentions the convention out of the ledger.

Output, grouped by file, one row per marker: `<file>:<line>, <what was simplified>. ceiling: <limit>. upgrade: <trigger to revisit>.` Add `git blame -L<line>,<line>` when the user wants an owner per row. A marker that names no upgrade path gets the tag `no-trigger`; those are the ones that rot. End with `<N> markers, <M> with no trigger.` Nothing found: `No ponytail: debt. Clean ledger.`

To persist the ledger, ask first, then write it to a file such as `PONYTAIL-DEBT.md`.
