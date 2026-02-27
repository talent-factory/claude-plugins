---
description: Validate agent files, YAML frontmatter (including color attribute), and best practices
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---

# Agent Validation Tool

This command validates Claude Code agents for:

- YAML frontmatter structure (including **color attribute**)
- Markdown syntax
- Agent-specific best practices
- Documentation completeness

## Usage

```bash
# Validate a specific agent
/core:check-agents agents/claude/agents/code-reviewer.md

# Or without path for interactive selection
/core:check-agents
```

## Validation Checks

### 1. YAML Frontmatter

**Required**:

- `name` (String, lowercase with hyphens, e.g., "code-reviewer")
- `description` (String, 1-200 characters)
- `color` (String, one of the permitted colors)

**Optional**:

- `category` (String, e.g., "quality-security", "specialized-domains")
- `model` (String: "sonnet", "opus", "haiku")
- `tools` (Array of tool names or comma-separated string)
- `allowed-tools` (Array of tool names)

**Format**:

```yaml
---
name: code-reviewer
description: Expert in code reviews with focus on quality and security
category: quality-security
model: sonnet
color: blue
tools: Read, Write, Grep
---
```

### 2. Color Attribute Validation

**Permitted colors**:

- `blue` - Default for code/development agents
- `green` - For testing/validation agents
- `red` - For security/critical agents
- `yellow` - For documentation agents
- `purple` - For research/analysis agents
- `orange` - For build/deployment agents
- `cyan` - For data/database agents
- `magenta` - For UI/UX agents

**Validation**:

- Color attribute must be present
- Color must be one of the permitted colors
- Color should match the category/function

**Recommendations**:

```yaml
# Good
name: code-reviewer
category: quality-security
color: blue

# Good
name: test-automator
category: testing
color: green

# Missing
name: markdown-formatter
category: specialized-domains
# NO color attribute!

# Wrong color
name: security-auditor
color: pink  # Not permitted
```

### 3. Markdown Structure

- Must begin with frontmatter
- At least one H1 heading (`# Agent Name`)
- Valid CommonMark format
- Clear sections (Role, Activation, Process, etc.)

**Recommended structure**:

```markdown
# Agent Name

[Brief description]

## Role / Core Expertise

[What the agent can do]

## Activation / Approach

[When and how the agent is used]

## Process / Workflow

[Step-by-step procedure]

## Deliverables / Output

[What the agent produces]
```

### 4. Agent-Specific Best Practices

**Name**:

- Lowercase with hyphens: `code-reviewer`
- No CamelCase or underscores: `CodeReviewer`, `code_reviewer`
- Descriptive and concise
- Matches filename (without `.md`)

**Description**:

- Short and concise (1-200 characters)
- Describes WHAT the agent does
- Optional: WHEN the agent should be used
- Optional: Proactive hint ("MUST BE USED when...", "Use PROACTIVELY...")
- **Language: English** (technical terms in English)

**Documentation (Markdown body)**:

- **Written primarily in English**
- Technical terms (e.g., "Code Review", "Testing") may remain in English
- Domain-specific terms (e.g., "Progressive Disclosure") in English permitted
- Consistent language within an agent

**Category** (optional, but recommended):

- Groups related agents
- Examples: `quality-security`, `specialized-domains`, `skill-builder`, `development`, `testing`

**Model** (optional):

- `sonnet` - Default (balanced)
- `opus` - Complex tasks
- `haiku` - Fast, simple tasks

## Validation Workflow

When executing this command, proceed as follows:

1. **Determine agent path**:
   - If no path provided: List all `.md` files in `claude/agents/` (recursive)
   - User selects agent or process all

2. **Read file**:
   - Use Read tool
   - Check whether file exists

3. **Parse YAML frontmatter**:
   - Extract first block between `---`
   - Check required fields: `name`, `description`, **`color`**
   - Validate optional fields: `category`, `model`, `tools`
   - Format validation (no syntax errors)

4. **Color attribute check**:
   - Is color attribute missing entirely?
   - Is color not in permitted colors?
   - Does color match the category/function?

5. **Validate Markdown**:
   - At least one H1 heading present
   - Name in H1 matches `name` in YAML (recommended)
   - Basic CommonMark structure

6. **Validate name**:
   - Lowercase with hyphens
   - Matches filename
   - Format: `[a-z][a-z0-9-]*`

7. **Output report**

   **Compliant agent**:

   ```markdown
   ## Validation Report: code-reviewer

   YAML Frontmatter: Valid
   Color Attribute: blue (valid)
   Markdown Structure: Valid
   Name Convention: Valid
   Best Practices: Compliant

   ### Details:
   - Name: code-reviewer (matches filename)
   - Description: "Expert in code reviews..." (91 chars)
   - Category: quality-security
   - Model: sonnet
   - Color: blue (appropriate for code review)

   Agent is fully compliant!
   ```

   **Agent with missing color**:

   ```markdown
   ## Validation Report: markdown-syntax-formatter

   YAML Frontmatter: Valid (except color)
   Color Attribute: MISSING
   Markdown Structure: Valid
   Name Convention: Valid
   Best Practices: Partially compliant

   ### Issues to fix:
   1. REQUIRED: Add 'color' field to YAML frontmatter
      Recommended: color: yellow (documentation/formatting agent)

   ### Recommended fix:
   ```yaml
   ---
   name: markdown-syntax-formatter
   category: specialized-domains
   description: Converts text with visual formatting...
   color: yellow  # ADD THIS LINE
   ---
   ```

   ### Available colors

   - blue: Code/Development agents
   - green: Testing/Validation agents
   - red: Security/Critical agents
   - yellow: Documentation agents <- RECOMMENDED
   - purple: Research/Analysis agents
   - orange: Build/Deployment agents
   - cyan: Data/Database agents
   - magenta: UI/UX agents

   **Agent with invalid color**:

   ```markdown
   ## Validation Report: example-agent

   YAML Frontmatter: Valid (except color)
   Color Attribute: INVALID ("pink" not allowed)
   Markdown Structure: Valid
   Name Convention: Valid

   ### Issues to fix:
   1. Color "pink" is not in allowed colors list
      Change to one of: blue, green, red, yellow, purple, orange, cyan, magenta

   ### Recommended fix:
   Choose appropriate color based on agent function:
   - If code-related -> blue
   - If testing-related -> green
   - If security-related -> red
   - If documentation-related -> yellow
   - If research-related -> purple
   ```

8. **Bulk validation** (all agents):

   ```markdown
   ## Bulk Validation Report: claude/agents/

   Found 5 agent files:

   code-reviewer.md - Fully compliant
   markdown-syntax-formatter.md - Missing color
   skill-documenter-agent.md - Missing color
   skill-elicitation-agent.md - Missing color
   skill-generator-agent.md - Missing color

   ### Summary:
   - Total agents: 5
   - Compliant: 1 (20%)
   - Missing color: 4 (80%)
   - Invalid color: 0 (0%)
   - Other issues: 0 (0%)

   ### Agents needing color attribute:
   1. markdown-syntax-formatter.md -> Recommended: yellow
   2. skill-documenter-agent.md -> Recommended: yellow
   3. skill-elicitation-agent.md -> Recommended: purple
   4. skill-generator-agent.md -> Recommended: blue

   ### Quick fix script:
   Would you like me to add the recommended colors to all agents?
   ```

## Error Handling

- **File not found**: Clear error message with path
- **YAML parse error**: Show line and error
- **Missing required fields**: List all missing fields (including color!)
- **Invalid color**: Show permitted colors + recommendation

## Auto-Fix Option

After validation, optionally offer:

```text
Auto-fix available!

Should I automatically add the missing color attributes?
[Yes] Add recommended colors
[No] Show report only
[Manual] Show me what to do
```

If "Yes":

- Analyze agent function from `name` and `description`
- Select appropriate color
- Add `color: [color]` to YAML frontmatter
- Show diff before writing

## Integration with Other Commands

This command is useful:

- **Before commit**: Validate agents before committing
- **After changes**: Ensure all agents are compliant
- **New agents**: Verify initial setup
- **Bulk check**: Check all agents at once

## Examples

**Single agent with color**:

```text
/core:check-agents agents/claude/agents/code-reviewer.md
-> Fully compliant (color: blue)
```

**Single agent without color**:

```text
/core:check-agents agents/claude/agents/markdown-syntax-formatter.md
-> Missing color attribute
-> Recommended: yellow (documentation agent)
```

**Check all agents**:

```text
/core:check-agents
-> Found 5 agents, 4 missing color
-> [Show bulk report]
```

**With auto-fix**:

```text
/core:check-agents --fix
-> Fixed 4 agents, added color attributes
-> [Show changes]
```

## Color-Category Mapping

For orientation during auto-fix or manual assignment:

| Agent Type | Recommended Color | Examples |
|-----------|-------------------|----------|
| Code Review, Development | `blue` | code-reviewer, developer |
| Testing, Validation | `green` | test-automator, validator |
| Security, Critical | `red` | security-auditor, penetration-tester |
| Documentation, Writing | `yellow` | documenter, markdown-formatter |
| Research, Analysis | `purple` | researcher, analyst |
| Build, Deployment, CI/CD | `orange` | deployer, builder |
| Data, Database | `cyan` | data-engineer, db-optimizer |
| UI/UX, Design | `magenta` | ui-designer, ux-specialist |

**Keywords for auto-detection**:

- Blue: "code", "review", "developer", "engineer", "refactor"
- Green: "test", "validate", "check", "verify", "qa"
- Red: "security", "audit", "vulnerability", "pentest"
- Yellow: "document", "write", "markdown", "format", "guide"
- Purple: "research", "analyze", "investigate", "synthesize"
- Orange: "build", "deploy", "ci", "cd", "release"
- Cyan: "data", "database", "query", "etl", "pipeline"
- Magenta: "ui", "ux", "design", "interface", "accessibility"

## Notes

- This command should itself follow best practices
- Color attribute is now REQUIRED for all agents
- Auto-fix should intelligently suggest colors based on agent function
- When uncertain: Ask user which color is desired
