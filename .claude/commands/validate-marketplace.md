---
description: Validate and synchronize the entire marketplace ecosystem against Anthropic best practices, version consistency, language standards, and documentation completeness
argument-hint: "[--verify] [--section versions|best-practices|language|skills|docs|changelog] [--fix]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
---

# Validate Marketplace

Validates and synchronizes the plugin marketplace ecosystem. Performs comprehensive checks against Anthropic best practices, enforces English-only content at academic level, verifies version consistency, and synchronizes all documentation files.

## Usage

```bash
# Full validation and documentation update
/validate-marketplace

# Verify only (report without changes)
/validate-marketplace --verify

# Run specific section
/validate-marketplace --section best-practices
/validate-marketplace --section language
/validate-marketplace --section versions
/validate-marketplace --section skills
/validate-marketplace --section docs
/validate-marketplace --section changelog

# Auto-fix without confirmation prompts
/validate-marketplace --fix
```

## Severity Levels

| Level | Meaning | Action |
|-------|---------|--------|
| ERROR | Violates required standards | Must fix; blocks clean report |
| WARNING | Violates recommended practices | Should fix; reported prominently |
| INFO | Improvement suggestion | Listed in summary |

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

**Check that these locations match:**

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

### 2a. Detect Required Version Bumps

**IMPORTANT:** When plugin components have changed, recommend appropriate version bumps using Semantic Versioning.

**Analyze changes in each plugin:**

| Change Type | Version Bump | Examples |
|-------------|--------------|----------|
| **MAJOR** | X.0.0 | Breaking API changes, removed commands/skills, incompatible config changes |
| **MINOR** | x.Y.0 | New commands, new skills, new agents, new features, new CLI flags |
| **PATCH** | x.y.Z | Bug fixes, documentation updates, translation changes, refactoring |

**Detection rules:**

```
For each plugin with uncommitted or recent changes:

1. Check for NEW files in:
   - commands/*.md → MINOR (new command)
   - agents/*.md → MINOR (new agent)
   - skills/*/SKILL.md → MINOR (new skill)

2. Check for MODIFIED files:
   - SKILL.md with new features/flags → MINOR
   - SKILL.md with bug fixes only → PATCH
   - scripts/*.py with new functions → MINOR
   - scripts/*.py with fixes only → PATCH
   - README.md only → PATCH
   - Translation changes → PATCH (unless adding new language = MINOR)

3. Check for DELETED files:
   - Any command/agent/skill removed → MAJOR (breaking change)

4. Check for RENAMED files:
   - Command/skill renamed → MAJOR (breaking change)
```

**Report version bump recommendations:**

```
Version Bump Recommendations:
=============================

Plugin: obsidian (current: 1.0.1)
  Changes detected:
    - MODIFIED: skills/tasknotes/SKILL.md (new flags)
  Recommendation: MINOR bump → 1.1.0
  Reason: New features added
```

**Prompt user for confirmation:**

If version bumps are recommended, ask:
1. "Apply recommended version bumps? (Y/n)"
2. If declined, allow manual override

**Update all version locations:**

When a version bump is applied, update ALL of these files:
1. `plugins/NAME/.claude-plugin/plugin.json`
2. `.claude-plugin/marketplace.json`
3. `plugins/NAME/README.md`
4. `docs/plugins/index.md`

### 3. Best Practices Audit

#### 3.1 plugin.json Validation

For each `plugins/*/.claude-plugin/plugin.json`:

| Rule | Severity | Auto-Fix |
|------|----------|----------|
| `name` present and kebab-case (lowercase, hyphens only) | ERROR | No |
| `version` present and valid semver (MAJOR.MINOR.PATCH) | ERROR | No |
| `description` present and in English | ERROR | No |
| `author` as object `{name, email?, url?}` not string | WARNING | Yes: convert string to `{name: string}` |
| `keywords` array present | WARNING | No |
| `license` valid SPDX identifier | WARNING | No |
| No non-standard fields (e.g., `displayName`) | WARNING | Yes: remove field |
| All custom paths relative with `./` prefix | ERROR | Yes: add `./` prefix |
| `.claude-plugin/` directory contains ONLY `plugin.json` | ERROR | No |

**Standard plugin.json fields:** `name`, `version`, `description`, `author`, `homepage`, `repository`, `license`, `keywords`, `commands`, `agents`, `skills`, `hooks`, `mcpServers`, `outputStyles`, `lspServers`.

**Auto-fix procedure for `author`:**
If `author` is a string like `"Author Name"`, convert to `{"name": "Author Name"}`.

**Auto-fix procedure for non-standard fields:**
Remove any field not in the standard fields list above.

#### 3.2 marketplace.json Validation

For `.claude-plugin/marketplace.json`:

| Rule | Severity | Auto-Fix |
|------|----------|----------|
| `$schema` field present pointing to Anthropic schema | WARNING | Yes: add `"$schema": "https://anthropic.com/claude-code/marketplace.schema.json"` |
| `metadata.pluginRoot` set for cleaner source paths | INFO | No |
| Each plugin entry has `name` and `source` | ERROR | No |
| `category` field per plugin entry | WARNING | No |
| Plugin version matches corresponding `plugin.json` version | ERROR | Yes: sync from plugin.json |
| Marketplace name not in reserved list | ERROR | No |

**Reserved marketplace names:** `claude-code-marketplace`, `claude-code-plugins`, `claude-plugins-official`, `anthropic-marketplace`, `anthropic-plugins`, `agent-skills`, `life-sciences`.

#### 3.3 Agent Frontmatter Validation

For each `plugins/*/agents/*.md`:

| Rule | Severity | Auto-Fix |
|------|----------|----------|
| `name` present, lowercase kebab-case | ERROR | Yes: lowercase and hyphenate |
| `description` present | ERROR | No |
| `description` in English | ERROR | No (report with exact text) |
| `description` in third person (no "I", "you", "we") | WARNING | No (report only) |
| `description` includes when-to-use or triggering context | WARNING | No (report only) |
| No non-standard fields in agent frontmatter | WARNING | Yes: remove non-standard fields |

**Standard agent frontmatter fields:** `name`, `description`, `tools`, `disallowedTools`, `model`, `permissionMode`, `maxTurns`, `skills`, `mcpServers`, `hooks`, `memory`, `background`, `isolation`, `category`, `color`.

**Auto-fix procedure for name normalization:**
Convert to lowercase, replace spaces with hyphens: `"Java Tutor"` → `"java-tutor"`.

#### 3.4 Command Frontmatter Validation

For each `plugins/*/commands/*.md`:

| Rule | Severity | Auto-Fix |
|------|----------|----------|
| YAML frontmatter delimiters (`---`) present | ERROR | No (too complex for auto-fix) |
| `description` field present in frontmatter | ERROR | No |
| `description` in English | ERROR | No (report with exact German text) |
| `allowed-tools` field present | WARNING | No |
| `argument-hint` present when command body references `$ARGUMENTS` | INFO | No |

#### 3.5 Skill SKILL.md Validation

For each `plugins/*/skills/*/SKILL.md`:

| Rule | Severity | Auto-Fix |
|------|----------|----------|
| `SKILL.md` file exists in skill directory | ERROR | No |
| `name` in frontmatter is kebab-case, max 64 characters | ERROR | Yes: normalize |
| `name` does not contain reserved words ("anthropic", "claude") | ERROR | No |
| `description` present, max 1024 characters | ERROR | No |
| `description` in English | ERROR | No (report with exact text) |
| `description` states both what it does AND when to use it | WARNING | No (report only) |
| `description` in third person | WARNING | No (report only) |
| SKILL.md under 500 lines | WARNING | No (report line count) |
| Supporting file references max one level deep from SKILL.md | INFO | No (report only) |

### 4. Language and Quality Audit

Scan all plugin component files for non-English content:

| Rule | Severity | Auto-Fix |
|------|----------|----------|
| All `description` fields in frontmatter are in English | ERROR | No (report exact text) |
| All README.md files are in English | ERROR | No (report file path) |
| All command body text is in English | ERROR | No (report file path and sample) |
| All agent system prompts are in English | ERROR | No (report file path and sample) |
| All skill SKILL.md body text is in English | ERROR | No (report file path and sample) |
| Academic English level (no colloquialisms) | INFO | No (report only) |

**Detection heuristic for German text:**
Check for German-specific patterns: umlauts combined with German suffixes (-ung, -keit, -lich, -ieren), common German articles (der, die, das, ein, eine), and German conjunctions (und, oder, aber, wenn, dass).

**Report format:**
```
[E040] plugins/git-workflow/commands/commit.md
  Field: description
  Current: "Erstelle professionelle Git-Commits mit automatischen Checks..."
  Required: English translation at academic level
```

### 5. Skills Migration Check

For each command in `plugins/*/commands/*.md`, check whether a corresponding skill exists in `plugins/*/skills/`:

| Rule | Severity | Auto-Fix |
|------|----------|----------|
| Command has a corresponding skill directory with SKILL.md | WARNING | No |
| Suggest skill directory path and SKILL.md template | INFO | No |

**Report format:**
```
Skills Migration Recommendations:
  [W050] code-quality:ruff-check
    Status: No skill equivalent found
    Suggestion: Create plugins/code-quality/skills/ruff-check/SKILL.md
    Priority: Medium

  [W051] education:explain-code
    Status: No skill equivalent found
    Suggestion: Create plugins/education/skills/explain-code/SKILL.md
    Priority: Medium
```

**Exclude from warning:** Commands that already have a corresponding skill directory (cross-reference command filenames against skill directory names within the same plugin).

### 6. Update docs/plugins/index.md

**Update plugin table:**

```markdown
| Plugin | Version | Commands | Agents | Skills | Tags |
|--------|---------|----------|--------|--------|------|
| [Git Workflow](git-workflow.md) | X.Y.Z | N | N | N | tags |
```

**Update feature sections:**

- Add missing plugins
- Remove deleted plugins
- Update command/agent/skill lists
- Update descriptions

### 7. Update Plugin-Specific Documentation

For each plugin in `docs/plugins/`:

1. Update version number
2. Update command list
3. Update agent list with activation instructions
4. Update skill list with activation instructions
5. Update feature descriptions
6. Verify all internal links

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
- Direct invocation: Activates automatically when [conditions]
- Manual: `/skill-name` (if user-invocable)

**Features:**
- Feature 1
- Feature 2
```

**Check for missing activation instructions:**

For each plugin doc containing an "Agents" section, verify that activation/trigger/invoke instructions are present.

### 8. Update Plugin READMEs and CLAUDE.md

**For each `plugins/*/README.md`:**

1. Sync version with plugin.json
2. Update command documentation
3. Update agent documentation
4. Update installation instructions

**For `CLAUDE.md`:**

1. **Repository Overview** - Plugin count and descriptions
2. **Plugin Types** - List of all plugins with commands
3. **Key Files** - File paths and purposes
4. **Common Tasks** - Accurate command references

### 9. Final Verification

**Run consistency checks:**

1. Verify all plugin.json files are valid JSON
2. Verify marketplace.json is valid JSON
3. Check for broken internal links in docs
4. Re-validate any files that were auto-fixed in Step 3

## Output

**Summary report:**

```
Marketplace Validation Report
==============================

Step 1: Extract Current State
  Plugins found: N
  Commands: N | Agents: N | Skills: N

Step 2: Version Consistency
  ✓ All versions synchronized
  (or list mismatches)

Step 3: Best Practices Audit
  ERRORS: N
    [E001] file: description of issue
           Auto-fixed: description of fix (if applicable)
  WARNINGS: N
    [W001] file: description of issue
  INFO: N
    [I001] file: suggestion

Step 4: Language & Quality Audit
  ERRORS: N
    [E040] file: field/section in German
  INFO: N
    [I040] file: style suggestion

Step 5: Skills Migration Check
  WARNINGS: N
    [W050] plugin:command - No skill equivalent
           Suggestion: Create path/to/SKILL.md

Step 6-8: Documentation Updates
  Files Updated: N
  - list of files

Step 9: Final Verification
  ✓ All JSON files valid
  ✓ No broken internal links
  (or list issues)

Summary:
  Total Findings: N (E errors, W warnings, I info)
  Auto-Fixed: N
  Manual Action Required: N

Next Steps:
  1. Review changes with `git diff`
  2. Address manual findings
  3. Commit with `/git-workflow:commit`
```

## Error Handling

**Missing plugin documentation:**

```
Warning: No documentation found for plugin 'plugin-name'
Action: Create docs/plugins/plugin-name.md from template
```

**Broken links:**

```
Error: Broken link in docs/plugins/index.md
  Line N: [Link Text](target.md) → File not found
Action: Verify file exists or update link
```

**Invalid JSON:**

```
Error: Invalid JSON in plugins/name/.claude-plugin/plugin.json
  Line N: Unexpected token
Action: Fix JSON syntax before continuing
```

## Related Commands

- `/core:check` - Validate individual plugin structure
- `/core:check-commands` - Validate command files in detail
- `/core:check-agents` - Validate agent files in detail
- `/git-workflow:commit` - Commit changes after validation
