# Code Quality Plugin

## Version 4.0.0

One skill: Python linting and formatting with Ruff.

## Skills

| Invocation | What it does |
|---|---|
| `/code-quality:ruff-check` | Installs Ruff if missing, runs `ruff check --fix` and `ruff format`, verifies, and reports the violations that need manual work. Also activates on "lint my Python", "run ruff", "fix code style". |

For code review use the built-in `/code-review` and `/security-review`, or the `pr-review-toolkit` and `feature-dev` plugins.

## Installation

```json
{
  "extraKnownMarketplaces": {
    "talent-factory": {
      "source": { "source": "github", "repo": "talent-factory/claude-plugins" }
    }
  },
  "enabledPlugins": { "code-quality@talent-factory": true }
}
```

## Changelog

### Version 4.0.0 (2026-11-14)

**Breaking:**

- Removed the agents `code-reviewer`, `python-expert` and `frontend-developer`: generic checklists and personas that current models follow without them. Reviews are covered by `/code-review` and `/security-review`.
- `ruff-check` is one skill now (same invocation `/code-quality:ruff-check`); the duplicate command is gone. The `--fix` argument of the command is not needed: the skill always applies safe fixes.
- The plugin shrank from about 600 to about 90 lines.

### Version 3.1.0 (2026-05-08)

- Added `ruff-check` skill for natural-language Python linting activation

### Version 3.0.2 (2026-02-27)

- Moved java-developer agent to development plugin
- Updated description to reflect current agent inventory
- Added `keywords` and `license` fields to plugin.json
- Translated agent descriptions and documentation to English

### Version 2.0.0 (2026-01-10)

- Added `/code-quality:ruff-check` command for Python linting
- Added code-reviewer agent for proactive reviews
- Added python-expert agent for Python development
- Added frontend-developer agent for Next.js/React development

### Version 1.0.0

- Initial release with `/code-quality:review` and `/code-quality:refactor` commands

## License

MIT License - see [LICENSE](https://github.com/talent-factory/claude-plugins/blob/main/LICENSE) file for details.

---

**Made with ❤️ by Talent Factory GmbH**
