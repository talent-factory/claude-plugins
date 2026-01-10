# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a **Claude Code plugin marketplace** maintained by Talent Factory GmbH. It hosts 5 professional plugins distributed via GitHub for software development, education, and project management. The repository serves as both a marketplace configuration and a development workspace for plugin contributors.

**Target Users:** Students, software developers, educators, and development teams.

## Architecture

### Marketplace Structure

The repository uses a two-level architecture:

1. **Marketplace Level** (`.claude-plugin/marketplace.json`):
   - Defines the "talent-factory" marketplace
   - Lists all available plugins with metadata
   - Indexed by Claude Code's plugin system

2. **Plugin Level** (`plugins/[name]/`):
   - Each plugin is self-contained
   - Standard structure: `.claude-plugin/plugin.json`, `commands/`, `agents/`, `README.md`
   - Commands are Markdown files defining user-invocable functionality
   - Agents are Markdown files defining specialized AI assistants

### Plugin Types

- **git-workflow**: Git operations (`/commit`, `/create-pr`)
- **project-management**: PRD generation (`/create-prd`)
- **code-quality**: Code review and refactoring
- **education**: Teaching aids with Java Tutor agent
- **tf-core**: Plugin validation tools (`/check-commands`, `/check-agents`)

### How Plugins Work

```
User adds marketplace → Claude Code indexes marketplace.json →
User selects plugins → Plugins installed → Commands available as /command-name
```

Installation config in `.claude/settings.json`:
```json
{
  "extraKnownMarketplaces": {
    "talent-factory": {
      "source": { "source": "github", "repo": "talent-factory/claude-plugins" }
    }
  },
  "enabledPlugins": {
    "git-workflow@talent-factory": true
  }
}
```

## Development Commands

### Testing Plugins Locally

```bash
# Test a single plugin
claude --plugin-dir ./plugins/PLUGIN-NAME

# Test all plugins (entire marketplace)
claude --plugin-dir .

# Inside Claude Code, validate structure
/check-commands  # Validates command markdown files
/check-agents    # Validates agent definitions
```

### Validation

The repository has no build/compile step. Validation is done via GitHub Actions:

```bash
# Validation happens automatically on:
# - Push to main/develop
# - Pull requests
# - Manual workflow dispatch

# Checks performed:
# - JSON syntax in plugin.json files
# - Required fields (name, version, displayName)
# - Directory structure compliance
# - README presence
# - Markdown link validity
# - Secret scanning
# - Branch naming conventions (feature/, fix/, docs/, refactor/)
# - Commit message format (Conventional Commits with emoji)
```

### Branch Workflow

**Important Branch Protection Rules:**

- **main**: Production releases only
  - Requires 1 approval
  - All CI checks must pass
  - Linear history enforced
  - No direct pushes (even for admins)

- **develop**: Integration branch
  - Maintainer (dsenften) can push directly
  - All other contributors must use PRs
  - Requires 1 approval for PRs
  - All CI checks must pass

- **Feature branches**: Use naming convention
  - `feature/description` - New features
  - `fix/description` - Bug fixes
  - `docs/description` - Documentation
  - `refactor/description` - Code refactoring

### Commit Format

Use Emoji Conventional Commits (German imperative):

```
🎉 feat: Füge Python Tutor Agent hinzu
🐛 fix: Behebe Commit-Validierungsfehler
📚 docs: Aktualisiere Installation-Guide
♻️ refactor: Vereinfache PR-Template
🧪 test: Ergänze Plugin-Struktur-Tests
```

**Important:** Do NOT add these suffixes to commits:
- ❌ "Co-Authored-By: Claude"
- ❌ "Generated with Claude Code"

## Plugin Development Workflow

### Creating a New Plugin

1. **Structure**:
   ```
   plugins/your-plugin/
   ├── .claude-plugin/plugin.json
   ├── commands/your-command.md
   ├── agents/your-agent.md (optional)
   └── README.md
   ```

2. **plugin.json** must include:
   ```json
   {
     "name": "your-plugin",
     "version": "1.0.0",
     "displayName": "Your Plugin",
     "description": "Brief description",
     "keywords": ["tag1", "tag2"],
     "author": "Name",
     "license": "MIT"
   }
   ```

3. **Update marketplace.json**:
   Add entry to `.claude-plugin/marketplace.json` plugins array

4. **Command files** (Markdown):
   - Title with clear name
   - Usage section with examples
   - Purpose and when to use
   - Step-by-step instructions
   - Best practices and warnings

5. **Agent files** (Markdown, optional):
   - Metadata section (name, description, version, tags)
   - Expertise areas
   - Approach/methodology
   - Example interactions
   - Response format guidelines

### Testing Your Plugin

```bash
# Local testing
cd /path/to/claude-plugins
claude --plugin-dir ./plugins/your-plugin

# In Claude Code session:
/your-command

# Validate structure
/check-commands
/check-agents
```

### Submitting Changes

1. Fork repository
2. Create feature branch: `git checkout -b feature/add-your-plugin`
3. Make changes
4. Test locally
5. Commit with conventional format
6. Push and create PR
7. CI/CD will automatically:
   - Validate JSON syntax
   - Check directory structure
   - Scan for secrets
   - Label PR by size and type
   - Require 1 approval

## Key Files & Their Purpose

- **`.claude-plugin/marketplace.json`**: Marketplace catalog - lists all plugins
- **`plugins/*/plugin.json`**: Individual plugin metadata
- **`plugins/*/commands/*.md`**: User-invocable commands (accessed via `/command-name`)
- **`plugins/*/agents/*.md`**: Specialized AI assistant definitions
- **`.github/workflows/validate-plugins.yml`**: Main CI/CD pipeline
- **`.github/workflows/branch-protection.yml`**: Enforces development standards
- **`docs/PLUGIN_DEVELOPMENT.md`**: Comprehensive contributor guide
- **`.github/BRANCH_PROTECTION_SETUP.md`**: GitHub settings configuration

## GitHub Actions Workflows

### validate-plugins.yml
Runs on: PR/push to main/develop

Jobs:
- **validate-structure**: JSON validity, required fields, directory compliance
- **validate-documentation**: README presence, markdown links
- **security-scan**: Trivy scan, secret detection
- **test-plugins**: Structure verification
- **summary**: Aggregates results, fails if any validation fails

### branch-protection.yml
Runs on: PR to main/develop

Validates:
- Branch naming (must use feature/, fix/, docs/, refactor/)
- Commit messages (Conventional Commits format)
- PR description length (warns if <50 chars)
- PR size (warns if >1000 changes)
- Approval status

### pr-labels.yml
Auto-labels PRs based on:
- Changed files (plugin:*, documentation, infrastructure)
- PR size (size/xs through size/xl)
- Commit type (enhancement, bug, refactoring)

### Other Workflows
- **greetings.yml**: Welcomes first-time contributors
- **stale.yml**: Closes inactive issues (60 days) and PRs (30 days)

## Common Tasks

### Add a New Command to Existing Plugin

1. Create `plugins/PLUGIN-NAME/commands/new-command.md`
2. Write command definition in Markdown
3. Test: `claude --plugin-dir ./plugins/PLUGIN-NAME`
4. Verify: `/new-command` works in Claude Code
5. Commit and PR

### Update Plugin Version

1. Update `version` in `plugins/PLUGIN-NAME/.claude-plugin/plugin.json`
2. Update corresponding entry in `.claude-plugin/marketplace.json`
3. Update `CHANGELOG.md` with changes
4. Follow semantic versioning (MAJOR.MINOR.PATCH)

### Add a New Plugin to Marketplace

1. Create plugin structure in `plugins/new-plugin/`
2. Write `plugin.json`, commands, README
3. Add entry to `.claude-plugin/marketplace.json`
4. Test locally: `claude --plugin-dir ./plugins/new-plugin`
5. Validate: `/check-commands` and `/check-agents`
6. Create PR with complete documentation

## Special Considerations

### Branch Protection Bypass
Only the maintainer (dsenften) can push directly to `develop`. This is enforced via GitHub branch protection with `enforce_admins: false` for develop only.

### Conventional Commits with Emoji
This project uses emoji prefixes on commit types. The `/commit` command in git-workflow plugin generates these automatically. If committing manually, follow the format in CONTRIBUTING.md.

### No Build Step
This repository contains only configuration files (JSON, Markdown). There are no compilation, transpilation, or build artifacts. Validation is purely structural and syntactic.

### Plugin Distribution
Users don't clone this repository. Instead, Claude Code fetches plugin definitions from GitHub when the marketplace is added to settings. Changes propagate when Claude Code refreshes the marketplace index.

### Educational Context
The education plugin (Java Tutor agent) is tailored for FFHS (Fernfachhochschule Schweiz) and TSBE students. It references Swiss computer science curriculum and teaching methodologies specific to those institutions.
