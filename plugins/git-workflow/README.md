# Git Workflow Plugin

## Version 3.0.0

Git workflows for Claude Code: Emoji Conventional Commits, pull requests, merge conflict resolution, post-merge cleanup, and the history of a PR description.

## Skills and commands

| Invocation | What it does |
|---|---|
| `/git-workflow:commit` | Runs the project's checks, stages the right files, splits unrelated changes and writes an English Emoji Conventional Commit. Options: `--no-verify`, `--skip-tests`. |
| `/git-workflow:create-pr` | Creates a branch when you are on a protected one, commits via `commit`, formats, pushes and opens the PR with `gh`. Options: `--draft`, `--no-format`, `--target <branch>`. |
| `/git-workflow:resolve-conflicts` | Analyses each conflict, resolves it by intent (lock files regenerated, imports merged, architectural conflicts handed back to you), runs tests and linters, reports. Options: `--dry-run`, `--no-tests`, `--strategy smart\|ours\|theirs`, `--target`. |
| `/git-workflow:post-merge-cleanup` | After a merge: removes the task's worktree, deletes local and remote branches, marks the task done (`STATUS.md` or a Plane work item). Options: `--dry-run`, `--keep-local`, `--no-status-update`. |
| `/git-workflow:pr-edit-history` | Shows the edit history of a PR description as a table (GraphQL `userContentEdits`). |
| `hunk-review` skill | Guides interactive diff review with the `hunkdiff` CLI. Activates on "review with hunk". |

The skills also activate from natural language ("commit this", "open a PR", "I have merge conflicts").

## Conventions

- **Commit format:** `<emoji> <type>(<scope>): <imperative description>`, in English. Types: `feat` ✨, `fix` 🐛, `docs` 📚, `style` 💎, `refactor` ♻️, `perf` ⚡, `test` 🧪, `chore` 🔧, `ci` 🚀, `security` 🔒, `deps` 📦.
- **No AI attribution lines** (`Co-Authored-By: Claude`, "Generated with Claude Code") unless the repository asks for them.
- **Protected branches** (`main`, `master`, `develop`) never receive direct commits; `create-pr` branches off as `<type>/<description>-<date>`.
- **Ticket links** in PR text: `Closes <ID>` when the PR finishes the ticket, `Refs <ID>` when it stays open on purpose.

## Installation

```json
{
  "extraKnownMarketplaces": {
    "talent-factory": {
      "source": { "source": "github", "repo": "talent-factory/claude-plugins" }
    }
  },
  "enabledPlugins": { "git-workflow@talent-factory": true }
}
```

Requirements: `git`, and the GitHub CLI `gh` for `create-pr`, `resolve-conflicts` (PR numbers) and `post-merge-cleanup`.

## Changelog

### Version 3.0.0 (2026-11-14)

**Breaking:**

- `commit`, `create-pr` and `resolve-conflicts` are skills now, with the same invocations (`/git-workflow:commit`, `/git-workflow:create-pr`, `/git-workflow:resolve-conflicts`). The `--with-skills` flag and the `--force-push` option of `commit` are gone.
- Removed the `professional-commit-workflow` and `professional-pr-workflow` skills, their Python scripts (about 1.9k lines), the validators and the duplicated `references/` and `docs/` trees. The model runs the checks of the project directly.
- `post-merge-cleanup` uses Plane instead of Linear.
- The plugin shrank from about 13.4k to about 1k lines.

### Version 2.4.2 (2026-11-14)

- Default merge target of `resolve-conflicts` is `main` instead of `develop` (trunk-based development)

### Version 2.4.1 (2026-11-14)

- Commit messages, PR descriptions, and generated descriptions are now written in English, in line with the repository language policy (commands `commit`, `create-pr`, `resolve-conflicts`, the `professional-commit-workflow` skill, its commit type catalogue, and fallback messages)

### Version 2.4.0 (2026-05-08)

**Minor Update:**

- ✨ Added `resolve-conflicts` skill for natural-language merge conflict resolution activation
- Now includes 4 commands and 5 professional workflow skills

### Version 2.3.0 (2026-05-07)

**Minor Update:**

- ✨ Added `hunk-review` skill for interactive terminal diff review sessions via Hunk CLI
- Adapted from [modem-dev/hunk](https://github.com/modem-dev/hunk) (MIT License)
- Now includes 4 commands and 4 professional workflow skills

### Version 2.2.2 (2026-02-27)

**Patch Update:**
- Added `keywords` and `license` fields to plugin.json
- Translated command and skill documentation to English
- Fixed Swiss German orthography (ss instead of ß)
- Updated command references to fully-qualified format

### Version 2.2.0 (2026-02-13)

**Minor Update:**

- ✨ Added `/git-workflow:resolve-conflicts` command for intelligent merge conflict resolution
- 📖 Added comprehensive reference documentation (strategies, best practices, troubleshooting)
- 🧠 Smart merge strategy with semantic code analysis
- 🔀 Support for `smart`, `ours`, and `theirs` strategies
- 🧪 Automated test and lint validation after resolution
- Now includes 4 commands and 3 professional workflow skills

### Version 2.1.0 (2026-02-03)

**Minor Update:**

- ✨ Added `post-merge-cleanup` skill for automated branch cleanup after merge
- Now includes 3 professional workflow skills

### Version 2.0.0 (2026-01-10)

**Major Update:**

- ✨ Added comprehensive reference documentation
- ✨ Integrated professional-commit-workflow skill
- ✨ Integrated professional-pr-workflow skill
- ✨ Added `/git-workflow:pr-edit-history` command
- 📚 Expanded commit types with emoji support
- 📚 Added troubleshooting guides
- 🔧 Enhanced pre-commit checks
- 🔧 Improved PR description generation

**Migration from 1.0.0:**

- All existing commands remain compatible
- New `--with-skills` flag optional
- References available for enhanced guidance

### Version 1.0.0

- Initial release with `/git-workflow:commit` and `/git-workflow:create-pr`

## Support

- **Issues:** [GitHub Issues](https://github.com/talent-factory/claude-plugins/issues)
- **Discussions:** [GitHub Discussions](https://github.com/talent-factory/claude-plugins/discussions)
- **Email:** support@talent-factory.ch

## Contributing

See [CONTRIBUTING.md](https://github.com/talent-factory/claude-plugins/blob/main/CONTRIBUTING.md) in the main repository.

## License

MIT License - see [LICENSE](https://github.com/talent-factory/claude-plugins/blob/main/LICENSE) file for details.

---

**Made with ❤️ by Talent Factory GmbH**
