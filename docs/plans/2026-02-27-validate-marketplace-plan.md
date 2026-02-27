# Validate Marketplace Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Rename `/update-docs` to `/validate-marketplace` and add comprehensive Anthropic Best Practices validation with auto-fix capabilities alongside existing documentation synchronization.

**Architecture:** The existing command markdown file is replaced with a new, expanded command that adds Steps 3-5 (Best Practices Audit, Language Audit, Skills Migration Check) between the existing version consistency and documentation update steps. All validation rules are embedded directly in the command markdown as structured instructions for Claude.

**Tech Stack:** Markdown command file, YAML frontmatter, JSON (plugin.json, marketplace.json)

---

## Task 1: Create the new `/validate-marketplace` command

**Files:**
- Create: `.claude/commands/validate-marketplace.md`
- Delete: `.claude/commands/update-docs.md`

**Step 1: Write the new command file**

Create `.claude/commands/validate-marketplace.md` with the full 9-step validation pipeline. The command must include:

1. **Frontmatter** with description in English, allowed-tools list, and argument-hint
2. **Step 1: Extract Current State** (kept from update-docs)
3. **Step 2: Version Consistency** (kept from update-docs, including 2a version bumps)
4. **Step 3: Best Practices Audit** (NEW) - All rules from design doc sections 3.1-3.5
5. **Step 4: Language & Quality Audit** (NEW) - English-only enforcement
6. **Step 5: Skills Migration Check** (NEW) - Commands without skill equivalents
7. **Step 6-8: Documentation Updates** (kept from update-docs, renumbered)
8. **Step 9: Final Verification** (kept from update-docs, renumbered)
9. **Output format** with severity-coded report
10. **Error handling** section

The frontmatter must be:
```yaml
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
```

**Content structure:**

The body must follow this exact structure (all in English, academic level):

```markdown
# Validate Marketplace

Validates and synchronizes the plugin marketplace ecosystem. Performs comprehensive checks against Anthropic best practices, enforces English-only content at academic level, verifies version consistency, and synchronizes all documentation files.

## Usage

/validate-marketplace
/validate-marketplace --verify
/validate-marketplace --section best-practices
/validate-marketplace --section language
/validate-marketplace --fix

## Severity Levels

| Level | Meaning | Action |
|-------|---------|--------|
| ERROR | Violates required standards | Must fix; blocks clean report |
| WARNING | Violates recommended practices | Should fix; reported prominently |
| INFO | Improvement suggestion | Listed in summary |

## Process

### 1. Extract Current State
[Keep existing content from update-docs Step 1, translated to English]

### 2. Verify Version Consistency
[Keep existing content from update-docs Steps 2 and 2a, translated to English]

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

**Auto-fix procedure for `author`:**
If `author` is a string like `"Author Name"`, convert to `{"name": "Author Name"}`.

**Auto-fix procedure for non-standard fields:**
Remove fields not in the official schema: `name`, `version`, `description`, `author`, `homepage`, `repository`, `license`, `keywords`, `commands`, `agents`, `skills`, `hooks`, `mcpServers`, `outputStyles`, `lspServers`.

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
| `description` includes when to use / triggering context | WARNING | No (report only) |
| No non-standard fields in agent frontmatter | WARNING | Yes: remove `author`, `version`, `tags` if present |
| Standard fields only: `name`, `description`, `tools`, `disallowedTools`, `model`, `permissionMode`, `maxTurns`, `skills`, `mcpServers`, `hooks`, `memory`, `background`, `isolation`, `category`, `color` | WARNING | Yes: remove others |

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
| All `description` fields in frontmatter are in English | ERROR | No (report exact text requiring translation) |
| All README.md files are in English | ERROR | No (report file path) |
| All command body text is in English | ERROR | No (report file path and sample text) |
| All agent system prompts are in English | ERROR | No (report file path and sample text) |
| All skill SKILL.md body text is in English | ERROR | No (report file path and sample text) |
| Academic English level (no colloquialisms, informal expressions) | INFO | No (report only) |

**Detection heuristic for German text:**
Check for presence of German-specific patterns: umlauts in German words (ä, ö, ü combined with common German suffixes like -ung, -keit, -lich, -ieren), common German articles (der, die, das, ein, eine), and German conjunctions (und, oder, aber, wenn, dass).

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

**Commands with existing skill equivalents (no warning):**
Cross-reference `plugins/*/commands/*.md` names against `plugins/*/skills/*/` directory names.

### 6. Update docs/plugins/index.md
[Keep existing content from update-docs Step 3, translated to English]

### 7. Update Plugin-Specific Documentation
[Keep existing content from update-docs Steps 4 and 4a, translated to English]

### 8. Update Plugin READMEs and CLAUDE.md
[Keep existing content from update-docs Steps 5 and 6, translated to English]

### 9. Final Verification
[Keep existing content from update-docs Step 8, translated to English]
Add: verify that all auto-fixes from Step 3 produced valid files (re-parse JSON, re-validate YAML frontmatter).

## Output

**Summary report format:**

[Include the full output format from the design document]

## Error Handling

[Keep existing error handling from update-docs, translated to English]

## Related Commands

- `/core:check` - Validate individual plugin structure
- `/core:check-commands` - Validate command files in detail
- `/core:check-agents` - Validate agent files in detail
- `/git-workflow:commit` - Commit changes after validation
```

**Step 2: Delete the old command file**

Delete `.claude/commands/update-docs.md`.

**Step 3: Commit**

```bash
git add .claude/commands/validate-marketplace.md
git rm .claude/commands/update-docs.md
git commit -m "feat: replace /update-docs with /validate-marketplace command

Add comprehensive Anthropic Best Practices validation (Steps 3-5)
alongside existing documentation synchronization (Steps 6-9).
New checks: plugin.json schema, agent/command/skill frontmatter,
English-only enforcement, and skills migration recommendations."
```

---

## Task 2: Fix agent frontmatter violations

**Files:**
- Modify: `plugins/education/agents/java-tutor.md` (lines 1-7)
- Modify: `plugins/code-quality/agents/code-reviewer.md` (lines 1-7)
- Modify: `plugins/code-quality/agents/python-expert.md` (lines 1-7)
- Modify: `plugins/code-quality/agents/frontend-developer.md` (lines 1-6)
- Modify: `plugins/core/agents/command-expert.md` (lines 1-6)
- Modify: `plugins/core/agents/agent-expert.md` (lines 1-6)
- Modify: `plugins/development/skills/professional-init-project/SKILL.md` (lines 1-5)
- Modify: `plugins/development/skills/update-documents/SKILL.md` (lines 1-4)

**Step 1: Fix java-tutor.md**

Replace frontmatter:
```yaml
---
name: Java Tutor
description: Expert Java programming instructor for students
author: Talent Factory GmbH
version: 1.0.0
tags: [java, education, programming, teaching]
---
```
With:
```yaml
---
name: java-tutor
description: Expert Java programming instructor for students. Use proactively when students need guidance on Java concepts, object-oriented design, data structures, or debugging techniques.
color: blue
category: education
---
```

Changes: kebab-case name, removed non-standard fields (author, version, tags), added color and category, expanded description with triggering context.

**Step 2: Fix code-reviewer.md - translate description to English**

Replace frontmatter:
```yaml
---
name: code-reviewer
description: Experte für Code-Reviews. Überprüft Code proaktiv auf Qualität, Sicherheit und Wartbarkeit. Sofort nach dem Schreiben oder Ändern von Code verwenden.
category: quality-security
model: sonnet
color: blue
---
```
With:
```yaml
---
name: code-reviewer
description: Expert code reviewer. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code.
category: quality-security
model: sonnet
color: blue
---
```

**Step 3: Fix python-expert.md - translate description to English**

Replace frontmatter:
```yaml
---
name: python-expert
description: Schreibt idiomatischen Python-Code mit fortgeschrittenen Features wie Decorators, Generators und async/await. Optimiert Performance, implementiert Design Patterns und stellt umfassende Tests sicher. PROAKTIV verwenden für Python-Refactoring, Optimierung oder komplexe Python-Features.
category: language-specialists
model: sonnet
color: blue
---
```
With:
```yaml
---
name: python-expert
description: Writes idiomatic Python code leveraging advanced features such as decorators, generators, and async/await. Optimizes performance, implements design patterns, and ensures comprehensive test coverage. Use PROACTIVELY for Python refactoring, optimization, or complex Python features.
category: language-specialists
model: sonnet
color: blue
---
```

**Step 4: Fix frontend-developer.md - translate description to English**

Replace frontmatter:
```yaml
---
name: frontend-developer
description: Erstelle Next.js-Anwendungen mit React-Komponenten, shadcn/ui und Tailwind CSS. Experte für SSR/SSG, App Router und moderne Frontend Patterns. PROAKTIV verwenden für Next.js-Entwicklung, UI-Komponenten-Erstellung oder Frontend-Architektur.
category: development-architecture
color: magenta
---
```
With:
```yaml
---
name: frontend-developer
description: Builds Next.js applications with React components, shadcn/ui, and Tailwind CSS. Expert in SSR/SSG, App Router, and modern frontend patterns. Use PROACTIVELY for Next.js development, UI component creation, or frontend architecture.
category: development-architecture
color: magenta
---
```

**Step 5: Fix command-expert.md - translate description to English**

Replace frontmatter:
```yaml
---
name: command-expert
description: Erstelle CLI-Commands für Automatisierung und Tooling. PROAKTIV verwenden beim Entwerfen von Command-Line-Interfaces, Argument-Parsing oder Task-Automatisierung.
category: quality-security
color: cyan
---
```
With:
```yaml
---
name: command-expert
description: Creates CLI commands for automation and tooling. Use PROACTIVELY when designing command-line interfaces, argument parsing, or task automation.
category: quality-security
color: cyan
---
```

**Step 6: Fix agent-expert.md - translate description to English**

Replace frontmatter:
```yaml
---
name: agent-expert
category: specialized-domains
description: Erstelle und optimiere spezialisierte Claude Code Agents. Expertise in Agent-Design, Prompt Engineering, Domain-Modellierung und Best Practices für claude-code-templates System. PROAKTIV verwenden beim Entwerfen neuer Agents oder Verbessern bestehender.
color: purple
---
```
With:
```yaml
---
name: agent-expert
category: specialized-domains
description: Creates and optimizes specialized Claude Code agents. Expertise in agent design, prompt engineering, domain modeling, and best practices for the claude-code-templates system. Use PROACTIVELY when designing new agents or improving existing ones.
color: purple
---
```

**Step 7: Commit agent fixes**

```bash
git add plugins/education/agents/java-tutor.md plugins/code-quality/agents/code-reviewer.md plugins/code-quality/agents/python-expert.md plugins/code-quality/agents/frontend-developer.md plugins/core/agents/command-expert.md plugins/core/agents/agent-expert.md
git commit -m "fix: standardize agent frontmatter to Anthropic best practices

Translate all German descriptions to academic English.
Fix java-tutor: kebab-case name, remove non-standard fields, add color.
Ensure all agents have name, description, category, color."
```

---

## Task 3: Fix command frontmatter violations

**Files:**
- Modify: `plugins/git-workflow/commands/commit.md` (lines 1-6)
- Modify: `plugins/git-workflow/commands/create-pr.md` (lines 1-9)
- Modify: `plugins/git-workflow/commands/resolve-conflicts.md` (lines 1-9)
- Modify: `plugins/git-workflow/commands/pr-edit-history.md` (lines 1-5)
- Modify: `plugins/code-quality/commands/ruff-check.md` (lines 1-3)
- Modify: `plugins/education/commands/explain-code.md` (add frontmatter)
- Modify: `plugins/core/commands/check.md` (lines 1-5)
- Modify: `plugins/core/commands/check-commands.md` (lines 1-6)
- Modify: `plugins/core/commands/check-agents.md` (lines 1-6)
- Modify: `plugins/core/commands/build-skill.md` (lines 1-5)
- Modify: `plugins/core/commands/package-skill.md` (lines 1-5)
- Modify: `plugins/core/commands/create-command.md` (lines 1-5)
- Modify: `plugins/core/commands/run-ci.md` (lines 1-6)

**Step 1: Translate git-workflow command descriptions to English**

`commit.md`:
```yaml
description: Erstelle professionelle Git-Commits mit automatischen Checks für Java, Python und React Projekte
```
→
```yaml
description: Create professional git commits with automated checks for Java, Python, and React projects
```

`create-pr.md`:
```yaml
description: Erstelle einen neuen Branch, committe Änderungen und erstelle einen Pull Request mit automatischer Commit-Aufteilung
```
→
```yaml
description: Create a new branch, commit changes, and open a pull request with automated commit splitting
```

`resolve-conflicts.md`:
```yaml
description: Analysiere und loese Merge-Konflikte intelligent mit automatischer Test-Validierung
```
→
```yaml
description: Analyze and resolve merge conflicts intelligently with automated test validation
```

`pr-edit-history.md`:
```yaml
description: Zeige die Bearbeitungshistorie einer GitHub Pull Request Beschreibung
```
→
```yaml
description: Display the edit history of a GitHub pull request description
```

**Step 2: Fix ruff-check.md - add allowed-tools**

Replace:
```yaml
---
description: Lint und format alle Python-Dateien im Projekt mit Ruff
---
```
With:
```yaml
---
description: Lint and format all Python files in the project using Ruff
allowed-tools:
  - Bash
  - Read
  - Edit
---
```

**Step 3: Fix explain-code.md - add frontmatter**

Add YAML frontmatter at the beginning of the file:
```yaml
---
description: Explain code structure, logic, and design decisions for educational purposes
allowed-tools:
  - Read
  - Glob
  - Grep
---
```

**Step 4: Translate core command descriptions to English**

`check.md`:
```yaml
description: Führe Projekt-Checks aus und behebe Fehler ohne zu committen
```
→
```yaml
description: Run project checks and fix errors without committing
```

`check-commands.md`:
```yaml
description: Validiert Command-Dateien, Dokumentation und Best Practices
```
→
```yaml
description: Validate command files, documentation, and best practices
```

`check-agents.md`:
```yaml
description: Validiert Agenten-Dateien, YAML-Frontmatter (inkl. color-Attribut) und Best Practices
```
→
```yaml
description: Validate agent files, YAML frontmatter (including color attribute), and best practices
```

`build-skill.md`:
```yaml
description: Erstelle umfassende Claude Code Skills durch Elicitation-getriebene Entwicklung
```
→
```yaml
description: Build comprehensive Claude Code skills through elicitation-driven development
```

`package-skill.md`:
```yaml
description: Validiere und paketiere einen Claude Code Skill als verteilbare ZIP-Datei
```
→
```yaml
description: Validate and package a Claude Code skill as a distributable ZIP archive
```

`create-command.md`:
```yaml
description: Erstelle einen neuen Befehl nach existierenden Mustern und Organisationsstruktur
```
→
```yaml
description: Create a new command following existing patterns and organizational structure
```

`run-ci.md`:
```yaml
description: Führe CI-Checks aus und behebe alle Fehler bis alle Tests bestehen
```
→
```yaml
description: Run CI checks and fix all errors until all tests pass
```

**Step 5: Commit command fixes**

```bash
git add plugins/git-workflow/commands/*.md plugins/code-quality/commands/ruff-check.md plugins/education/commands/explain-code.md plugins/core/commands/*.md
git commit -m "fix: translate all command descriptions to English and add missing frontmatter

Translate German descriptions to academic English across all plugins.
Add missing frontmatter to explain-code.md.
Add missing allowed-tools to ruff-check.md."
```

---

## Task 4: Fix skill frontmatter violations

**Files:**
- Modify: `plugins/git-workflow/skills/professional-commit-workflow/SKILL.md` (lines 1-4)
- Modify: `plugins/git-workflow/skills/professional-pr-workflow/SKILL.md` (lines 1-4)
- Modify: `plugins/development/skills/professional-init-project/SKILL.md` (lines 1-5)
- Modify: `plugins/development/skills/update-documents/SKILL.md` (lines 1-4)
- Modify: `plugins/core/skills/humanizer/SKILL.md` (lines 1-11)

**Step 1: Translate git-workflow skill descriptions to English**

`professional-commit-workflow/SKILL.md`:
```yaml
description: Erstellt professionelle Git-Commits mit automatischen Pre-Commit-Checks für Java, Python, React und Dokumentation. Generiert Emoji Conventional Commit-Nachrichten und analysiert Staging-Status. Atomare Commits nach Best Practices.
```
→
```yaml
description: Creates professional git commits with automated pre-commit checks for Java, Python, React, and documentation projects. Generates emoji conventional commit messages and analyzes staging status. Produces atomic commits following best practices.
```

`professional-pr-workflow/SKILL.md`:
```yaml
description: Automatisiert Pull-Request-Erstellung mit Branch-Management, Code-Formatierung und Integration mit professional-commit-workflow. Unterstützt GitHub CLI, automatische PR-Beschreibungen und projektspezifische Formatter (Biome, Black, Prettier).
```
→
```yaml
description: Automates pull request creation with branch management, code formatting, and integration with professional-commit-workflow. Supports GitHub CLI, automated PR descriptions, and project-specific formatters (Biome, Black, Prettier).
```

**Step 2: Translate development skill descriptions to English**

`professional-init-project/SKILL.md`:
```yaml
description: Initialisiert Open-Source-Projekte mit GitHub Best Practices und Git-Branching-Strategie
```
→
```yaml
description: Initializes open-source projects with GitHub best practices and git branching strategy. Use when setting up new repositories with standardized configuration.
```

Also remove the non-standard `version` field from this skill's frontmatter.

`update-documents/SKILL.md`:
```yaml
description: Synchronisiert Dokumentation zwischen CLAUDE.md, README.md und docs/. Verwende diesen Skill um Dokumentations-Inkonsistenzen zu beheben.
```
→
```yaml
description: Synchronizes documentation between CLAUDE.md, README.md, and docs/. Use this skill to resolve documentation inconsistencies across project files.
```

**Step 3: Translate humanizer skill description to English**

`humanizer/SKILL.md`:
```yaml
description: |
  Entfernt Anzeichen von KI-generiertem Text. Verwende diesen Skill beim Bearbeiten oder
  Überprüfen von Texten, um sie natürlicher und menschlicher klingen zu lassen. Basiert
  auf Wikipedias umfassendem "Signs of AI writing" Leitfaden. Erkennt und behebt Muster wie:
  aufgeblasene Symbolik, Werbesprache, oberflächliche -ing-Analysen, vage Zuschreibungen,
  Gedankenstrich-Übernutzung, Dreierregel, KI-Vokabular, negative Parallelismen und
  übermässige Konjunktivphrasen.
```
→
```yaml
description: |
  Removes indicators of AI-generated text. Use this skill when editing or reviewing
  text to make it sound more natural and human. Based on Wikipedia's comprehensive
  "Signs of AI writing" guide. Detects and corrects patterns such as: inflated
  symbolism, promotional language, superficial -ing analyses, vague attributions,
  em-dash overuse, rule of three, AI vocabulary, negative parallelisms, and
  excessive subjunctive phrases.
```

**Step 4: Commit skill fixes**

```bash
git add plugins/git-workflow/skills/*/SKILL.md plugins/development/skills/*/SKILL.md plugins/core/skills/humanizer/SKILL.md
git commit -m "fix: translate all skill descriptions to English

Translate German SKILL.md descriptions to academic English.
Remove non-standard version field from professional-init-project."
```

---

## Task 5: Update marketplace.json with best-practice fields

**Files:**
- Modify: `.claude-plugin/marketplace.json`

**Step 1: Add $schema field and category per plugin**

Add `"$schema": "https://anthropic.com/claude-code/marketplace.schema.json"` as first field.

Add `category` field to each plugin entry:
- git-workflow: `"category": "development"`
- project-management: `"category": "productivity"`
- code-quality: `"category": "development"`
- education: `"category": "learning"`
- core: `"category": "development"`
- obsidian: `"category": "productivity"`
- development: `"category": "development"`

**Step 2: Commit marketplace.json update**

```bash
git add .claude-plugin/marketplace.json
git commit -m "fix: add schema reference and category fields to marketplace.json

Add $schema pointing to Anthropic's marketplace schema.
Add category field to all plugin entries per Anthropic best practices."
```

---

## Task 6: Translate agent and skill body content to English

**Files:**
- Modify: All agent `.md` files with German system prompts
- Modify: All skill `SKILL.md` files with German body content

**Step 1: Identify files with German body content**

Search all agent and skill files for German text patterns beyond the frontmatter. Focus on system prompt sections, workflow descriptions, and inline documentation.

**Step 2: Translate each file's body content**

For each file identified, translate the body (everything after the closing `---` frontmatter delimiter) to academic English. Preserve:
- Code blocks (do not translate)
- Technical terms
- File paths and command references
- YAML/JSON examples

**Step 3: Commit body translations**

```bash
git add plugins/*/agents/*.md plugins/*/skills/*/SKILL.md
git commit -m "fix: translate all agent and skill body content to English

Convert remaining German system prompts and skill instructions
to academic English for open-source international audience."
```

---

## Task 7: Update CLAUDE.md references

**Files:**
- Modify: `CLAUDE.md`

**Step 1: Update command reference**

Replace all references to `/update-docs` with `/validate-marketplace` in CLAUDE.md.

**Step 2: Update documentation language section**

Revise the "Documentation Language" section to reflect the new English-only policy. Remove the German exception clause or limit it to Swiss German orthography for user-facing UI strings only.

**Step 3: Commit CLAUDE.md update**

```bash
git add CLAUDE.md
git commit -m "docs: update CLAUDE.md for validate-marketplace command and English-only policy"
```

---

## Task 8: Add design document and plan to repository

**Files:**
- Add: `docs/plans/2026-02-27-validate-marketplace-design.md`
- Add: `docs/plans/2026-02-27-validate-marketplace-plan.md`

**Step 1: Commit planning documents**

```bash
git add docs/plans/2026-02-27-validate-marketplace-design.md docs/plans/2026-02-27-validate-marketplace-plan.md
git commit -m "docs: add validate-marketplace design and implementation plan"
```

---

## Execution Order

Tasks 1-5 can be partially parallelized:
- **Task 1** (new command) is independent
- **Tasks 2-4** (fix frontmatter) are independent of each other
- **Task 5** (marketplace.json) is independent
- **Task 6** (body translations) depends on Tasks 2-4 being done first (to avoid merge conflicts in same files)
- **Task 7** (CLAUDE.md) depends on Task 1 (needs to reference new command name)
- **Task 8** (docs) is independent

Recommended execution: Tasks 1+2+3+4+5 in parallel, then Task 6, then Task 7, then Task 8.
