# Development Plugin

## Version 2.0.0

Project initialisation and documentation synchronisation.

## Skills

| Invocation | What it does |
|---|---|
| `/development:init-project` | Sets up a new open source project: Git with `develop` to `main` branching, community files, GitHub templates, README, CI workflow, and optional Java (Gradle Kotlin DSL, Java 21, JUnit 5) or Python (uv) scaffolding. Options: `--git`, `--java`, `--uv`, `--name`, `--no-branching`, `--interactive`. |
| `update-documents` | Synchronises `CLAUDE.md`, `README.md` and `docs/` with deterministic, whitespace-tolerant rules (`config/sync_rules.json`). Activates on "sync the documentation". |

Rules baked into `init-project`: Java uses Gradle with the Kotlin DSL, never Maven; the initial commit goes through `/git-workflow:commit`.

## Installation

```json
{
  "extraKnownMarketplaces": {
    "talent-factory": {
      "source": { "source": "github", "repo": "talent-factory/claude-plugins" }
    }
  },
  "enabledPlugins": { "development@talent-factory": true }
}
```

## Changelog

### Version 2.0.0 (2026-11-14)

**Breaking:**

- `init-project` is one skill now (same invocation `/development:init-project`). The `--with-skills` flag is gone, and so are the command and the `professional-init-project` skill it duplicated.
- Removed the Python generators and scripts of `professional-init-project` (about 2.4k lines). Neither the command nor the skill ever called them.
- Removed the `java-developer` agent (a generic Java checklist).
- The plugin shrank from about 4.2k to about 0.7k lines.

### 1.3.1

- **Fix**: Added `keywords` and `license` fields to plugin.json
- **Fix**: Translated README and skill documentation to English
- **Fix**: Improved java-developer agent description

### 1.3.0

- **New**: `update-documents` skill for documentation synchronization
- **New**: Configurable sync rules between CLAUDE.md, README.md, and docs/
- **New**: Automatic sync status analysis with visual indicators

### 1.2.1

- **Fix**: Java projects now always use Gradle Kotlin DSL (not Maven)
- **Fix**: Initial commit now uses `/git-workflow:commit`
- **Improved**: Clearer step-by-step instructions in skill

### 1.2.0

- **New**: `--java` parameter for Java/Gradle Kotlin DSL projects
- **New**: `--with-skills` parameter for skill-based workflow
- **New**: `--no-branching` parameter to opt-out of develop/main strategy
- **New**: professional-init-project skill
- **Changed**: Git branching now uses develop → main by default
- **Changed**: Java projects use Gradle Kotlin DSL instead of Maven

### 1.1.0

- Initial release with init-project command
- java-developer agent

---

## Related Plugins

- **[Git Workflow](https://talent-factory.github.io/claude-plugins/plugins/git-workflow/)** - Professional commit and PR automation
- **[Code Quality](https://talent-factory.github.io/claude-plugins/plugins/code-quality/)** - Python and Frontend expert agents

---

## License

MIT License - see [LICENSE](https://github.com/talent-factory/claude-plugins/blob/main/LICENSE)

---

**Made with care by Talent Factory GmbH**
