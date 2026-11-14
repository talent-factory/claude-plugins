# Core Plugin

## Version 5.0.0

Validation for plugin commands and agents, plus a few standalone skills: text humanising, PDF to Markdown, AntML prompt writing, and the Ponytail minimalism skill.

## Commands

| Invocation | What it does |
|---|---|
| `/core:check-commands [path]` | Validates command files: frontmatter fields, structure, referenced files, language. |
| `/core:check-agents [path] [--fix]` | Validates agent files: frontmatter (`name`, `description`, `category`, `model` enum, `color`), structure, best practices. |

## Skills

| Skill | What it does |
|---|---|
| `humanizer` | Removes the signs of AI-written text (inflated wording, rule-of-three, vague attributions, em-dash overuse), based on Wikipedia's "Signs of AI writing". |
| `pdf-to-markdown` | Converts PDFs to Markdown: fast text extraction (PyMuPDF) or vision mode via the Anthropic API for complex layouts (`--use-api`, default model `claude-opus-5-5`). |
| `antml-prompt-writer` | Writes system prompts and meta prompts for Claude harnesses that use AntML (function calling, thinking, citations, sub-agents). |
| `ponytail` | Lazy-coding discipline: question the task, prefer the standard library and native features, one line before fifty. Levels `lite`, `full`, `ultra`. Modes: `/core:ponytail review` (diff review for over-engineering), `audit` (the same for the whole repository, ranked), `debt` (ledger of every `ponytail:` shortcut comment). |

The Ponytail skill is adapted from [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) (MIT).

## Installation

```json
{
  "extraKnownMarketplaces": {
    "talent-factory": {
      "source": { "source": "github", "repo": "talent-factory/claude-plugins" }
    }
  },
  "enabledPlugins": { "core@talent-factory": true }
}
```

## Changelog

### Version 5.0.0 (2026-11-14)

**Breaking:** the four Ponytail skills are one skill. `ponytail-review`, `ponytail-audit` and `ponytail-debt` became the modes `review`, `audit` and `debt` of `/core:ponytail` (`/core:ponytail review` and so on); their tags and output formats moved to `skills/ponytail/references/modes.md`, which is read only when a mode runs. The always-on discipline, levels and rules are unchanged. The skill count of the plugin drops from 7 to 4.

### Version 4.0.0 (2026-11-14)

**Breaking:**

- Removed the commands `check`, `run-ci`, `create-command`, `build-skill` and `package-skill`, the agents `command-expert` and `agent-expert`, and the four skill-builder agents with their README (about 3.6k lines). What they did (detect the project, run its checks and fix; scaffold a command or skill; package it) is default model behaviour, and the official `skill-creator` plugin covers building and evaluating skills.
- Kept: `check-commands`, `check-agents`, `humanizer`, `pdf-to-markdown`, `antml-prompt-writer` and the four Ponytail skills.
- The plugin shrank from about 6.6k to about 2.6k lines.

### Version 3.3.1 (2026-11-14)

- `pdf-to-markdown` default model is `claude-opus-5-5`; `check-commands` examples use existing paths

### Version 3.3.0 (2026-11-12)

**New Features:**
- Added the `antml-prompt-writer` skill: system-prompt and meta-prompt authoring for Claude-based harnesses with AntML, including a `<claude_behavior>` template, tool-use and citation rules, and the metaprompt method

### Version 3.2.0 (2026-06-25)

**New Features:**
- Added the **Ponytail** minimalism suite (four skills, adapted from [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail), MIT):
  - `ponytail` — always-on lazy-coding discipline with the seven-rung decision ladder and `lite`/`full`/`ultra` intensity levels
  - `ponytail-review` — diff review focused exclusively on over-engineering
  - `ponytail-audit` — repo-wide over-engineering audit with ranked findings
  - `ponytail-debt` — collects `ponytail:` shortcut comments into a tracked debt ledger
- Namespaced all invocation hints to the marketplace (`/core:ponytail*`), repointed the prose-style cross-reference to the `humanizer` skill, and added repo-standard frontmatter (`version`, `allowed-tools`, `license`)

### Version 3.1.3 (2026-02-27)

**Patch Update:**
- Added `keywords` and `license` fields to plugin.json
- Translated documentation and agent descriptions to English
- Improved skill-builder agent descriptions with contextual detail

### Version 3.1.0 (2026-02-06)

**New Features:**
- Added `pdf-to-markdown` skill for PDF to Markdown conversion
- Dual-mode support: fast (PyMuPDF) and vision (Claude Code analysis)
- LaTeX umlaut correction and Swiss German orthography

### Version 3.0.0 (2026-01-28)

**Breaking Change:**
- Moved `/development:init-project` command to development plugin
- Removed skill-builder agent system (available via `/core:build-skill` command)
- Updated documentation to English

### Version 2.1.0 (2026-01-19)

- Added Humanizer skill for removing AI writing patterns
- Added `/core:build-skill` and `/core:package-skill` commands

### Version 2.0.0 (2026-01-10)

- Added `/core:check` command for project validation
- Added `/core:create-command` for pattern-based command generation
- Added `/core:run-ci` for local CI execution
- Added agent-expert agent for agent development
- Added command-expert agent for CLI development
- Enhanced `/core:check-commands` with best practices validation
- Enhanced `/core:check-agents` with color attribute checking

### Version 1.0.0

- Initial release with `/core:check-commands` and `/core:check-agents`

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
