# 🌉 Gemini Bridge Plugin

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Plugin-blue)](https://claude.ai)
[![Gemini 2.5 Pro](https://img.shields.io/badge/Gemini-2.5%20Pro-orange)](https://ai.google.dev)

**Model-agnostic bridge to Google Gemini 2.5 Pro for Claude Code.**  
Enables long-context codebase analysis (1M tokens), multimodal vision, and 
independent model validation — seamlessly within your existing Claude Code workflow.

---

## 🎯 Why This Plugin?

| Problem | Solution |
|---|---|
| Codebase too large for Claude's context | Gemini handles up to 1M tokens |
| Need to analyze screenshots / diagrams | Gemini's multimodal vision |
| Want an independent model opinion | Model-agnostic validation pattern |
| Teaching model-agnostic AI engineering | Live routing example for students |

Gemini runs as an **MCP tool** — Claude calls it exactly like any other tool.  
No second terminal, no context switch, no workflow disruption.

---

## 🚀 Installation

### 1. Install the Plugin

In your project's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "talent-factory": {
      "source": {
        "source": "github",
        "repo": "talent-factory/claude-plugins"
      }
    }
  }
}
```

Then in Claude Code:
```
/plugin
→ Browse Plugins → talent-factory → gemini-bridge → Install
```

### 2. Install Python Dependencies

```bash
pip install google-generativeai fastmcp
# or with uv (recommended):
uv add google-generativeai fastmcp
```

### 3. Set API Key

```bash
# Get your key at: https://aistudio.google.com/app/apikey
export GEMINI_API_KEY="your-key-here"

# For persistent setup, add to your shell profile:
echo 'export GEMINI_API_KEY="your-key-here"' >> ~/.zshrc
```

### 4. Verify Connection

In Claude Code:
```
/gemini-bridge:analyze Check if the bridge is working
```

Claude will call `gemini_status` and confirm connectivity.

---

## 📦 What's Included

### Commands

| Command | Description |
|---|---|
| `/gemini-bridge:analyze` | Delegate text/code analysis to Gemini |
| `/gemini-bridge:compare` | Compare two approaches with Gemini as neutral reviewer |
| `/gemini-bridge:vision` | Convert screenshots/diagrams to code or docs |

### Agents

| Agent | Model | Role |
|---|---|---|
| `gemini-analyst` | Claude Sonnet 4.5 | Sub-agent for Gemini delegation |
| `model-router` | Claude Opus 4 | Orchestrator with routing logic |

### MCP Tools (available to all Claude agents)

| Tool | Purpose |
|---|---|
| `gemini_status` | Check bridge connectivity |
| `gemini_analyze_text` | Text prompts / second opinions |
| `gemini_analyze_codebase` | Large codebase analysis (up to 1M tokens) |
| `gemini_analyze_image` | Screenshot, diagram, PDF analysis |
| `gemini_compare_approaches` | Neutral comparison of two technical options |

---

## 💡 Usage Examples

### Large Codebase Security Review

```
/gemini-bridge:analyze Perform a full security audit of the src/ directory
```

Claude collects all source files, delegates to Gemini's 1M-token context,
and returns a structured security report.

### UI Screenshot to Component

```
/gemini-bridge:vision ./designs/dashboard-mockup.png "Generate a React + Tailwind component"
```

### Architecture Decision with Independent Review

```
/gemini-bridge:compare Should ExamCraft use event sourcing or CQRS for the exam engine?
```

Claude prepares both approaches; Gemini evaluates them neutrally.

### Multi-Agent Workflow

Claude Code (orchestrator) automatically routes tasks:

```
┌─────────────────────────────────┐
│   Claude Opus 4 (Orchestrator)  │
│   Decomposes task               │
└──────────────┬──────────────────┘
               │
    ┌──────────┼──────────────┐
    │          │              │
┌───▼───┐  ┌──▼──────┐  ┌───▼────────────┐
│Claude │  │ Claude  │  │ Gemini 2.5 Pro  │
│Sonnet │  │ Sonnet  │  │ (via MCP tool)  │
│Coding │  │ Testing │  │ Large Context   │
└───────┘  └─────────┘  └────────────────┘
```

---

## 🎓 Teaching: Model-Agnostic AI Engineering

This plugin is designed to demonstrate the **model-agnostic pattern** 
in AI-Assisted Software Engineering courses.

### Key Concepts Illustrated

**1. Separation of Concerns**
```python
# Routing logic in config, not code:
# agents/model-router.md → decides WHO handles what
# gemini_bridge/server.py → HOW to call Gemini
# Your application → doesn't know or care which model ran
```

**2. Capability-Based Routing**
```
Task                          → Best Model        → Why
─────────────────────────────────────────────────────────
Entire repo analysis          → Gemini             1M context
Write auth middleware         → Claude             tool use
Compare Redis vs PostgreSQL   → Gemini             neutral review
Generate tests                → Claude             code quality
Convert mockup to component   → Gemini             vision
```

**3. Multi-Model Validation Pattern**
```
Claude proposes → Gemini validates → Claude synthesizes
```
Demonstrates that no single model is authoritative.

### Classroom Exercise

Ask students to:
1. Add a new routing rule to `agents/model-router.md`
2. Swap Gemini for a different model by setting `GEMINI_MODEL` env var only
3. Observe that agents/commands are unchanged → **model-agnostic confirmed**

---

## ⚙️ Configuration

### Custom Model Version

Set the `GEMINI_MODEL` environment variable:
```bash
export GEMINI_MODEL="gemini-2.5-flash-preview-04-17"  # Use Flash for cost savings
export GEMINI_MODEL="gemini-2.5-pro"    # Default (Pro)
```

### Temperature Tuning

```python
# In gemini_analyze_text(), pass temperature (0.0-2.0):
gemini_analyze_text(prompt="...", temperature=0.7)  # More creative
gemini_analyze_text(prompt="...", temperature=0.0)  # Deterministic
```

### Using with Claude Code Max Plan

No additional configuration needed. The MCP bridge runs as a local subprocess.
Your Claude Code Max plan handles Claude's side; Gemini API key handles Gemini's side.

---

## 🔒 Security & Privacy

- **API key**: stored as environment variable, never committed to git
- **Data**: code content is sent to Google's Gemini API — review your data policies
- **`.gitignore`**: ensure `.env` files with your API key are excluded

```gitignore
# Add to .gitignore:
.env
.env.local
```

---

## 🛠️ Development & Contributing

```bash
git clone https://github.com/talent-factory/claude-plugins
cd claude-plugins/plugins/gemini-bridge

# Install dev dependencies
uv sync --extra dev

# Run tests
pytest tests/

# Lint
ruff check .
```

### Plugin Structure

```
gemini-bridge/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata
├── .mcp.json                # MCP server configuration
├── commands/
│   ├── analyze.md           # /gemini-bridge:analyze
│   ├── compare.md           # /gemini-bridge:compare
│   └── vision.md            # /gemini-bridge:vision
├── agents/
│   ├── gemini-analyst.md    # Sub-agent for delegation
│   └── model-router.md      # Orchestrator with routing logic
├── skills/
│   └── gemini-analyst/
│       └── SKILL.md         # Background knowledge for Claude
├── gemini_bridge/
│   ├── __init__.py
│   └── server.py            # FastMCP server (5 tools)
├── pyproject.toml
└── README.md
```

---

## 📋 Roadmap

- [ ] Streaming support for long analyses
- [ ] Gemini 2.5 Flash for cost-optimized tasks  
- [ ] Token count estimator (pre-routing decision helper)
- [ ] Parallel Claude + Gemini calls with synthesis agent
- [ ] Integration with `project-management` plugin (auto-route large EPICs)

---

## 📄 License

MIT License — see [LICENSE](../../LICENSE) for details.

---

**Talent Factory GmbH** · [talent-factory.ch](https://talent-factory.ch) · [@talent-factory](https://github.com/talent-factory)

*Part of the [claude-plugins](https://github.com/talent-factory/claude-plugins) collection*
