# Technical Reference

Comprehensive technical documentation for Claude Code plugin development and marketplace configuration.

---

## Quick Reference

<div class="grid cards" markdown>

-   :material-file-code:{ .lg .middle } **marketplace.json**

    ---

    Marketplace configuration schema and examples.

    [:octicons-arrow-right-24: Schema Reference](marketplace-json.md)

-   :material-puzzle:{ .lg .middle } **plugin.json**

    ---

    Plugin metadata and configuration format.

    [:octicons-arrow-right-24: Schema Reference](plugin-json.md)

-   :material-console:{ .lg .middle } **Command Format**

    ---

    Markdown format for command definitions.

    [:octicons-arrow-right-24: Format Guide](command-format.md)

-   :material-robot:{ .lg .middle } **Agent Format**

    ---

    Markdown format for agent definitions.

    [:octicons-arrow-right-24: Format Guide](agent-format.md)

-   :material-star:{ .lg .middle } **Skill Format**

    ---

    Directory structure and format for skills.

    [:octicons-arrow-right-24: Format Guide](skill-format.md)

-   :material-git:{ .lg .middle } **Conventional Commits**

    ---

    Emoji conventional commits reference.

    [:octicons-arrow-right-24: Commit Reference](conventional-commits.md)

</div>

---

## File Formats

### Configuration Files

| File | Purpose | Format | Required |
|------|---------|--------|----------|
| `marketplace.json` | Marketplace catalog | JSON | Yes (marketplace root) |
| `plugin.json` | Plugin metadata | JSON | Yes (per plugin) |
| `README.md` | Plugin documentation | Markdown | Yes (per plugin) |

### Plugin Components

| Component | Location | Format | Required |
|-----------|----------|--------|----------|
| Commands | `commands/*.md` | Markdown | Optional |
| Agents | `agents/*.md` | Markdown | Optional |
| Skills | `skills/*/` | Directory | Optional |
| References | `references/` | Markdown | Optional |

---

## Schema Versions

### Current Versions

- **Marketplace Schema**: 1.0.0
- **Plugin Schema**: 1.0.0
- **Command Format**: 1.0.0
- **Agent Format**: 1.0.0
- **Skill Format**: 1.0.0

---

## Tags Reference

### Common Tags

Use these standardized tags for better discoverability:

#### Development
- `git`, `workflow`, `commits`, `pull-requests`, `automation`
- `review`, `quality`, `refactoring`, `best-practices`
- `linting`, `formatting`, `testing`

#### Languages & Frameworks
- `python`, `java`, `javascript`, `typescript`, `react`
- `node`, `maven`, `gradle`, `npm`

#### Project Management
- `planning`, `prd`, `linear`, `agile`, `tasks`
- `project-management`, `task-management`

#### Education
- `education`, `teaching`, `learning`, `students`
- `tutorial`, `examples`

#### Utilities
- `utilities`, `validation`, `tools`, `development`
- `ci-automation`, `plugin-development`
- `productivity`, `integration`

---

## API Reference

### Claude Code Plugin API

Claude Code plugins interact with the Claude Code environment through:

1. **Commands**: User-invocable actions (e.g., `/commit`)
2. **Agents**: Specialized AI assistants with custom instructions
3. **Skills**: Reusable workflow templates
4. **References**: Documentation and best practices

### Marketplace API

The marketplace is indexed by Claude Code through:

```
https://github.com/talent-factory/claude-plugins
  └── .claude-plugin/marketplace.json
      └── plugins[]
          └── source: ./plugins/plugin-name
              └── .claude-plugin/plugin.json
```

---

## Validation Rules

### JSON Validation

All JSON files must:

- Be valid JSON syntax
- Include required fields
- Use correct data types
- Follow schema specifications

### Markdown Validation

Command and agent markdown files must:

- Have a title (H1 heading)
- Include required sections
- Use valid markdown syntax
- Follow format guidelines

### Directory Structure

Plugins must follow this structure:

```
plugins/plugin-name/
├── .claude-plugin/
│   └── plugin.json          ✅ Required
├── commands/                ⚠️ Optional but recommended
│   └── *.md
├── agents/                  ⚠️ Optional
│   └── *.md
├── skills/                  ⚠️ Optional
│   └── skill-name/
└── README.md                ✅ Required
```

---

## Best Practices

### Naming Conventions

- **Plugin names**: lowercase, hyphen-separated (e.g., `git-workflow`)
- **Command names**: lowercase, hyphen-separated (e.g., `create-pr`)
- **Agent names**: lowercase, hyphen-separated (e.g., `java-tutor`)
- **Skill names**: lowercase, hyphen-separated (e.g., `professional-commit-workflow`)

### Versioning

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

Example: `2.1.0`

---

## Next Steps

- **[Plugin Development](../development/plugin-development.md)** - Create plugins
- **[Contributing](../development/contributing.md)** - Contribute to marketplace
- **[Testing](../development/testing.md)** - Test your plugins

