# Design: `/validate-marketplace` Command

**Date:** 2026-02-27
**Status:** Approved
**Replaces:** `/update-docs` command

## Overview

Rename and extend the existing `/update-docs` command to `/validate-marketplace`, adding comprehensive Anthropic Best Practices validation alongside the existing documentation synchronization. The command validates, reports, and auto-fixes plugin ecosystem compliance.

## Context

The Talent Factory Claude Code plugin marketplace requires consistent adherence to:
1. **Official Anthropic standards** for plugin.json, marketplace.json, agents, commands, and skills
2. **Project conventions** including English-only content at academic level
3. **Documentation consistency** across all files

The existing `/update-docs` command handles documentation synchronization but lacks standards validation.

## Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Integration approach | Integrated into existing command | Organic fit; validation before docs generation ensures correct output |
| Command name | `validate-marketplace` | Reflects expanded scope beyond documentation |
| Auto-fix behavior | Report + Auto-Fix with confirmation | Balance between efficiency and control |
| Language policy | English only, academic level | Open-source project targeting international audience |
| Skills migration | Warning + suggestion | Follows Anthropic recommendation without forced migration |

## Architecture

### 9-Step Validation Pipeline

```
Step 1: Extract Current State       → Build plugin inventory from authoritative sources
Step 2: Version Consistency         → Cross-file version synchronization
Step 2a: Detect Version Bumps       → Semantic versioning analysis for changed components
Step 3: Best Practices Audit        → Anthropic standards compliance check
Step 4: Language & Quality Audit    → English-only enforcement, academic level
Step 5: Skills Migration Check      → Commands → Skills migration warnings
Step 6: Update docs/plugins/        → Synchronize plugin documentation
Step 7: Update Plugin READMEs      → Synchronize plugin-level documentation
Step 8: Update CLAUDE.md           → Synchronize project overview
Step 9: Final Verification         → JSON validity, broken links, consistency
```

### Flags

| Flag | Description |
|------|-------------|
| `--verify` | Report only, no changes applied |
| `--section <name>` | Run specific section: `versions`, `best-practices`, `language`, `skills`, `docs`, `changelog` |
| `--fix` | Auto-fix without confirmation (default: prompt for confirmation) |

### Severity Levels

| Level | Meaning | Action |
|-------|---------|--------|
| `ERROR` | Must fix; violates required standards | Blocks clean report |
| `WARNING` | Should fix; violates recommended practices | Reported prominently |
| `INFO` | Nice to have; improvement suggestions | Listed in summary |

## Validation Rules

### Step 3: Best Practices Audit

#### 3.1 plugin.json Validation

| Rule | Severity | Auto-Fix | Reference |
|------|----------|----------|-----------|
| `name` present and kebab-case | ERROR | No | Anthropic plugin spec |
| `version` present and valid semver | ERROR | No | Anthropic plugin spec |
| `description` present | ERROR | No | Anthropic plugin spec |
| `author` as object `{name, email?, url?}` | WARNING | Yes (string → object) | Anthropic plugin spec |
| `keywords` array present | WARNING | No | Anthropic plugin spec |
| `license` valid SPDX identifier | WARNING | No | Anthropic plugin spec |
| No non-standard fields (e.g., `displayName`) | WARNING | Yes (remove) | Anthropic plugin spec |
| All paths relative with `./` prefix | ERROR | Yes (add prefix) | Anthropic plugin spec |
| `.claude-plugin/` contains ONLY `plugin.json` | ERROR | No | Anthropic plugin spec |

#### 3.2 marketplace.json Validation

| Rule | Severity | Auto-Fix | Reference |
|------|----------|----------|-----------|
| `$schema` field present | WARNING | Yes (add) | Anthropic marketplace spec |
| `metadata.pluginRoot` set | INFO | Yes (add) | Anthropic marketplace spec |
| Each plugin entry has `name` and `source` | ERROR | No | Anthropic marketplace spec |
| `category` field per plugin | WARNING | No | Anthropic marketplace spec |
| Version match with plugin.json | ERROR | Yes (sync from plugin.json) | Cross-file consistency |
| No reserved marketplace names used | ERROR | No | Anthropic marketplace spec |

#### 3.3 Agent Frontmatter Validation

| Rule | Severity | Auto-Fix | Reference |
|------|----------|----------|-----------|
| `name` present, lowercase kebab-case | ERROR | Yes (normalize) | Anthropic agent spec |
| `description` present | ERROR | No | Anthropic agent spec |
| `description` in third person, English | WARNING | No (report only) | Anthropic best practices |
| `description` includes triggering context | WARNING | No (report only) | Anthropic best practices |
| No non-standard fields (`author`, `version`, `tags` in agent) | WARNING | Yes (remove) | Anthropic agent spec |
| `tools` specified or documented as inherited | INFO | No | Anthropic agent spec |

#### 3.4 Command Frontmatter Validation

| Rule | Severity | Auto-Fix | Reference |
|------|----------|----------|-----------|
| YAML frontmatter present | ERROR | No (too complex) | Anthropic command spec |
| `description` present | ERROR | No | Anthropic command spec |
| `description` in English | ERROR | No (report only) | Project convention |
| `allowed-tools` present | WARNING | No | Anthropic command spec |
| `argument-hint` when command accepts arguments | INFO | No | Anthropic command spec |

#### 3.5 Skill Frontmatter Validation

| Rule | Severity | Auto-Fix | Reference |
|------|----------|----------|-----------|
| `SKILL.md` present in skill directory | ERROR | No | Anthropic skill spec |
| `name` kebab-case, max 64 characters | ERROR | Yes (normalize) | Anthropic skill spec |
| `name` does not contain "anthropic" or "claude" | ERROR | No | Anthropic skill spec |
| `description` present, max 1024 characters | ERROR | No | Anthropic skill spec |
| `description` states what AND when | WARNING | No (report only) | Anthropic best practices |
| `description` in third person | WARNING | No (report only) | Anthropic best practices |
| SKILL.md under 500 lines | WARNING | No (report only) | Anthropic best practices |
| Supporting files max one level deep | INFO | No (report only) | Anthropic best practices |

### Step 4: Language & Quality Audit

| Rule | Severity | Auto-Fix | Reference |
|------|----------|----------|-----------|
| All descriptions in English | ERROR | No (manual) | Project convention |
| All README.md content in English | ERROR | No (manual) | Project convention |
| No German text in frontmatter fields | ERROR | No (report only) | Project convention |
| Academic English level in descriptions | INFO | No (report only) | Project convention |
| Swiss German orthography where German remains (transition) | WARNING | No | Project convention |

### Step 5: Skills Migration Check

| Rule | Severity | Auto-Fix | Reference |
|------|----------|----------|-----------|
| Command without skill equivalent | WARNING | No | Anthropic recommendation |
| Suggest skill directory + SKILL.md template | INFO | Yes (generate template) | Anthropic recommendation |

## Output Format

```
Marketplace Validation Report
==============================

Step 1: Extract Current State
  Plugins found: 7
  Commands: 25 | Agents: 14 | Skills: 9

Step 2: Version Consistency
  ✓ All versions synchronized

Step 3: Best Practices Audit
  ERRORS: 3
    [E001] education/agents/java-tutor.md: name "Java Tutor" → kebab-case required
           Auto-fixed: "java-tutor"
    [E002] education/commands/explain-code.md: Missing YAML frontmatter
    [E003] code-quality/commands/ruff-check.md: Missing allowed-tools field

  WARNINGS: 5
    [W001] core/agents/command-expert.md: Missing tools specification
    [W002] education/agents/java-tutor.md: Non-standard fields (author, version, tags)
           Auto-fixed: removed non-standard fields
    ...

Step 4: Language & Quality Audit
  ERRORS: 12
    [E010] git-workflow/commands/commit.md: Description in German
    [E011] git-workflow/commands/create-pr.md: Description in German
    ...

Step 5: Skills Migration Check
  WARNINGS: 4
    [W020] code-quality:ruff-check - No skill equivalent
           Suggestion: Create skills/ruff-check/SKILL.md
    ...

Step 6-8: Documentation Updates
  Files Updated: 8
  ...

Step 9: Final Verification
  ✓ All JSON files valid
  ✓ No broken internal links

Summary:
  Total Findings: 24 (3 errors, 9 warnings, 12 info)
  Auto-Fixed: 5
  Manual Action Required: 19

Next Steps:
  1. Review changes with `git diff`
  2. Address manual findings
  3. Commit with `/git-workflow:commit`
```

## Current Findings (Snapshot 2026-02-27)

### Critical (ERROR)
1. `education/commands/explain-code.md` - Missing YAML frontmatter entirely
2. `education/agents/java-tutor.md` - Name in Title Case, non-standard fields
3. `code-quality/commands/ruff-check.md` - Missing `allowed-tools`
4. 12+ command/agent descriptions in German instead of English

### Important (WARNING)
5. 4 agents missing `tools` field specification
6. `marketplace.json` missing `$schema` field
7. 4 commands without skill equivalents
8. Some descriptions not in third person

### Informational (INFO)
9. `metadata.pluginRoot` not set in marketplace.json
10. Some commands missing `argument-hint`

## Files Affected

| File | Change |
|------|--------|
| `.claude/commands/update-docs.md` | Delete (replaced) |
| `.claude/commands/validate-marketplace.md` | Create (new command) |
| All command/agent/skill frontmatter | Update (English descriptions, standards compliance) |
| `.claude-plugin/marketplace.json` | Update (add $schema, category fields) |
| Various plugin.json files | Update (remove non-standard fields) |
