# Gemini Bridge Plugin

Model-agnostic bridge to Google Gemini 2.5 Pro for Claude Code. Enables long-context codebase analysis (1M tokens), multimodal vision, and independent model validation within your existing Claude Code workflow.

## Version 1.0.1

Gemini runs as an **MCP tool** — Claude calls it exactly like any other tool. No second terminal, no context switch, no workflow disruption.

## Commands

### `/gemini-bridge:analyze`

Delegate text or code analysis to Gemini's long-context model.

**Features:**

- 📝 Text prompts and second opinions
- 📦 Large codebase analysis (up to 1M tokens)
- 🔍 Security audits across entire repositories
- 🧠 Independent model validation

**Usage:**
```bash
/gemini-bridge:analyze Perform a full security audit of the src/ directory
/gemini-bridge:analyze Review this architecture for scalability issues
```

### `/gemini-bridge:compare`

Compare two technical approaches with Gemini as a neutral reviewer.

**Features:**

- ⚖️ Neutral comparison of two options
- 📊 Structured evaluation with criteria
- 🎯 Independent assessment (no anchoring to Claude's preference)

**Usage:**
```bash
/gemini-bridge:compare Should we use event sourcing or CQRS for the exam engine?
/gemini-bridge:compare Redis vs PostgreSQL for session storage
```

### `/gemini-bridge:vision`

Convert screenshots, diagrams, or PDFs into code or documentation.

**Features:**

- 🖼️ Screenshot to component conversion
- 📐 Diagram analysis and documentation
- 📄 PDF content extraction
- 🎨 UI mockup to React/Tailwind code

**Usage:**
```bash
/gemini-bridge:vision ./designs/dashboard-mockup.png "Generate a React + Tailwind component"
/gemini-bridge:vision ./docs/architecture.pdf "Summarize the key design decisions"
```

## Agents

All agents activate automatically based on context. See [Skills & Agents Activation Guide](../reference/skills-agents-activation.md) for details.

### Gemini Analyst

Sub-agent for delegating analysis tasks to Gemini.

**Activation:**
- Automatic: When tasks require long-context analysis or multimodal processing
- Manual: "Use gemini-analyst to review this codebase"

**Expertise:**
- 📦 Large codebase analysis
- 🖼️ Multimodal vision tasks
- 🔍 Security and architecture reviews
- 📊 Structured report generation

### Model Router

Orchestrator agent with capability-based routing logic.

**Activation:**
- Automatic: When tasks benefit from multi-model collaboration
- Manual: "Route this task to the best model"

**Routing Logic:**
```
Task                        → Model       → Reason
────────────────────────────────────────────────────
Entire repo analysis        → Gemini      1M context window
Write auth middleware       → Claude      Tool use expertise
Compare two approaches      → Gemini      Neutral review
Generate tests              → Claude      Code quality focus
Convert mockup to component → Gemini      Vision capability
```

## Skills

### Gemini Analyst Skill

Background knowledge for Claude on when and how to delegate to Gemini effectively.

## MCP Tools

The following tools are available to all Claude agents when the plugin is installed:

| Tool | Purpose |
|---|---|
| `gemini_status` | Check bridge connectivity and model info |
| `gemini_analyze_text` | Text prompts and second opinions |
| `gemini_analyze_codebase` | Large codebase analysis (up to 1M tokens) |
| `gemini_analyze_image` | Screenshot, diagram, and PDF analysis |
| `gemini_compare_approaches` | Neutral comparison of two technical options |

## Installation

### 1. Enable the Plugin

```json
{
  "enabledPlugins": {
    "gemini-bridge@talent-factory": true
  }
}
```

### 2. Install Python Dependencies

```bash
pip install google-genai fastmcp
# or with uv (recommended):
uv add google-genai fastmcp
```

### 3. Set API Key

```bash
# Get your key at: https://aistudio.google.com/app/apikey
export GEMINI_API_KEY="your-key-here"
```

### 4. Verify Connection

```bash
/gemini-bridge:analyze Check if the bridge is working
```

## Configuration

### Custom Model Version

```bash
export GEMINI_MODEL="gemini-2.5-flash-preview-04-17"  # Flash for cost savings
export GEMINI_MODEL="gemini-2.5-pro"                   # Default (Pro)
```

### Temperature Tuning

```python
gemini_analyze_text(prompt="...", temperature=0.7)  # More creative
gemini_analyze_text(prompt="...", temperature=0.0)  # Deterministic
```

## Security and Privacy

- **API key**: Stored as environment variable, never committed to git
- **Data**: Code content is sent to Google's Gemini API — review your data policies
- **`.gitignore`**: Ensure `.env` files with your API key are excluded

## Use Cases

### Large Codebase Security Review

```bash
/gemini-bridge:analyze Perform a full security audit of the src/ directory
```

Claude collects all source files, delegates to Gemini's 1M-token context, and returns a structured security report.

### Architecture Decision with Independent Review

```bash
/gemini-bridge:compare Should we use event sourcing or CQRS for the exam engine?
```

Claude prepares both approaches; Gemini evaluates them neutrally.

### UI Screenshot to Component

```bash
/gemini-bridge:vision ./designs/dashboard-mockup.png "Generate a React + Tailwind component"
```

### Teaching: Model-Agnostic AI Engineering

This plugin demonstrates the **model-agnostic pattern** in AI-Assisted Software Engineering courses:

1. **Separation of Concerns** — Routing logic in config, not code
2. **Capability-Based Routing** — Each model handles what it does best
3. **Multi-Model Validation** — Claude proposes, Gemini validates, Claude synthesizes

## Changelog

### Version 1.0.0 (2026-03-13)

- Initial release with 3 commands, 2 agents, 1 skill, and 5 MCP tools
- Google Gemini 2.5 Pro integration via `google-genai` SDK
- Multimodal vision support (images, PDFs)
- Configurable model via `GEMINI_MODEL` environment variable
- Comprehensive test suite (29 tests)

## License

MIT License - see [LICENSE](https://github.com/talent-factory/claude-plugins/blob/main/LICENSE) file for details.

---

**Made with care by Talent Factory GmbH**
