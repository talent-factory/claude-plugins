---
description: Update all documentation to reflect current plugin versions and structure
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Update Documentation

Synchronizes all documentation files with the current state of the marketplace and plugins. Ensures version consistency across all files.

## Usage

```bash
# Full documentation update
/update-docs

# Verify only (no changes)
/update-docs --verify

# Update specific section
/update-docs --section plugins
/update-docs --section changelog
/update-docs --section readme
```

## Process

### 1. Extract Current State

**Read authoritative sources:**

1. `.claude-plugin/marketplace.json` - Plugin versions and descriptions
2. `plugins/*/plugin.json` - Individual plugin metadata
3. `plugins/*/commands/*.md` - Available commands
4. `plugins/*/agents/*.md` - Available agents
5. `plugins/*/skills/*/` - Available skills

**Build plugin inventory:**

```json
{
  "plugin-name": {
    "version": "X.Y.Z",
    "description": "...",
    "commands": ["cmd1", "cmd2"],
    "agents": ["agent1"],
    "skills": ["skill1"],
    "tags": ["tag1", "tag2"]
  }
}
```

### 2. Verify Version Consistency

**Check these locations match:**

| File | Field |
|------|-------|
| `plugins/NAME/.claude-plugin/plugin.json` | `version` |
| `.claude-plugin/marketplace.json` | `plugins[name].version` |
| `plugins/NAME/README.md` | Version section |
| `docs/plugins/NAME.md` | Version in header/table |
| `docs/plugins/index.md` | Plugin table |
| `CHANGELOG.md` | Latest entry for plugin |

**Report inconsistencies:**

```
Version Mismatch Detected:
  Plugin: code-quality
  - marketplace.json: 3.0.0
  - plugin.json: 3.0.0
  - docs/plugins/index.md: 2.0.0 ← OUTDATED
  - README.md: 2.0.0 ← OUTDATED
```

### 3. Update docs/plugins/index.md

**Update plugin table:**

```markdown
| Plugin | Version | Commands | Agents | Skills | Tags |
|--------|---------|----------|--------|--------|------|
| [Git Workflow](git-workflow.md) | X.Y.Z | N | N | N | tags |
```

**Update feature sections:**

- Add missing plugins
- Remove deleted plugins
- Update command/agent lists
- Update descriptions

### 4. Update Plugin-Specific Docs

For each plugin in `docs/plugins/`:

1. Update version number
2. Update command list
3. Update agent list with activation instructions
4. Update skill list with activation instructions
5. Update feature descriptions
6. Verify all internal links

### 4a. Verify Skills and Agents Documentation

**Each plugin doc must include for agents:**

```markdown
## Agents

### agent-name

Description of the agent.

**Activation:**
- Automatic: Triggered when [conditions]
- Manual: Use Task tool with `subagent_type: "plugin:agent-name"`

**Expertise:**
- Area 1
- Area 2
```

**Each plugin doc must include for skills:**

```markdown
## Skills

### skill-name

Description of the skill.

**Activation:**
- Via command: `/command --with-skills`
- Direct invocation: The skill activates automatically when [conditions]
- Manual: `/skill-name` (if user-invocable)

**Features:**
- Feature 1
- Feature 2
```

**Check for missing activation instructions:**

```bash
# Find agents without activation docs
for doc in docs/plugins/*.md; do
  if grep -q "## Agents" "$doc"; then
    if ! grep -qi "activation\|trigger\|invoke" "$doc"; then
      echo "Missing activation: $doc"
    fi
  fi
done
```

### 5. Update Plugin READMEs

For each `plugins/*/README.md`:

1. Sync version with plugin.json
2. Update command documentation
3. Update agent documentation
4. Update installation instructions

### 6. Update CLAUDE.md

**Sections to update:**

1. **Repository Overview** - Plugin count and descriptions
2. **Plugin Types** - List of all plugins with commands
3. **Key Files** - File paths and purposes
4. **Common Tasks** - Accurate command references

### 7. Update CHANGELOG.md

**Add entries for changes:**

```markdown
## [Unreleased]

### Changed

- Updated documentation to reflect current plugin structure
- Synchronized version numbers across all files

### Plugins

#### plugin-name X.Y.Z
- Description of changes
```

### 8. Final Verification

**Run consistency checks:**

```bash
# Verify all plugin.json files are valid JSON
for f in plugins/*/.claude-plugin/plugin.json; do
  jq . "$f" > /dev/null || echo "Invalid: $f"
done

# Verify marketplace.json
jq . .claude-plugin/marketplace.json > /dev/null

# Check for broken internal links in docs
grep -r "](.*\.md)" docs/ | grep -v "http"
```

## Files Updated

### Always Updated

| File | Updates |
|------|---------|
| `docs/plugins/index.md` | Plugin table, versions, commands |
| `CLAUDE.md` | Plugin overview, command references |
| `plugins/*/README.md` | Version, features |

### Conditionally Updated

| File | Condition |
|------|-----------|
| `docs/plugins/*.md` | If plugin changed |
| `CHANGELOG.md` | If `--changelog` flag |
| `docs/getting-started/*.md` | If installation changed |

## Validation Rules

### Version Format

- Must follow Semantic Versioning: `MAJOR.MINOR.PATCH`
- No leading zeros: `1.0.0` not `01.00.00`
- No suffixes unless pre-release: `1.0.0-beta.1`

### Command Documentation

Each command must have:
- Description in frontmatter
- Usage section with examples
- Process section with steps

### Agent Documentation

Each agent must have:
- name, description, model, color in frontmatter
- Triggering examples in description
- System prompt with responsibilities

## Output

**Summary report:**

```
Documentation Update Complete
=============================

Files Updated: 8
- docs/plugins/index.md
- docs/plugins/code-quality.md
- docs/plugins/core.md
- docs/plugins/development.md (NEW)
- plugins/code-quality/README.md
- plugins/core/README.md
- plugins/development/README.md
- CLAUDE.md

Version Synchronization:
- code-quality: 2.0.0 → 3.0.0
- core: 2.1.0 → 3.0.0
- development: NEW (1.1.0)

Warnings:
- docs/plugins/development.md does not exist (create it)

Next Steps:
1. Review changes with `git diff`
2. Commit with `/commit`
```

## Error Handling

**Missing plugin documentation:**

```
Warning: No documentation found for plugin 'development'
Action: Create docs/plugins/development.md from template
```

**Broken links:**

```
Error: Broken link in docs/plugins/index.md
  Line 15: [Core Utilities](core.md) → File not found
Action: Verify file exists or update link
```

**Invalid JSON:**

```
Error: Invalid JSON in plugins/core/.claude-plugin/plugin.json
  Line 5: Unexpected token
Action: Fix JSON syntax before continuing
```

## Related Commands

- `/core:check` - Validate plugin structure
- `/core:check-commands` - Validate command files
- `/core:check-agents` - Validate agent files
- `/git-workflow:commit` - Commit documentation changes
