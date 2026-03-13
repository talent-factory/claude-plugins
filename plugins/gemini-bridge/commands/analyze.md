---
name: analyze
description: Delegate codebase or text analysis to Gemini 2.5 Pro (1M token context)
usage: /gemini-bridge:analyze [--vision <image_path>] <task_description>
---

# Gemini Bridge: Analyze

Delegate analysis tasks to Google Gemini 2.5 Pro when:
- Codebase exceeds ~150K tokens
- Multimodal input (screenshots, diagrams) is involved
- A second-model perspective adds value

## Usage

```
/gemini-bridge:analyze Analyze the entire src/ directory for architectural issues
/gemini-bridge:analyze --vision ./mockup.png Generate React component from this UI mockup
/gemini-bridge:analyze Find all security vulnerabilities in this FastAPI backend
```

## Workflow

1. Check bridge status with `gemini_status` tool
2. Collect relevant code/content into a single context string
3. Call `gemini_analyze_codebase` or `gemini_analyze_text` as appropriate
4. For images: use `gemini_analyze_image` with the file path
5. Return Gemini's analysis with source attribution

## When to Use vs. Claude Directly

| Use Gemini Bridge | Use Claude Directly |
|---|---|
| >150K token codebase | Normal-sized files |
| Screenshot → code generation | Text-only tasks |
| Independent second opinion | Tool use / agentic steps |
| PDF/diagram analysis | Code writing & refactoring |

## Notes

- Always attribute results: "Gemini 2.5 Pro analysis:"
- Gemini's output feeds back to Claude as context for further action
- Model-agnostic by design: swap model via `GEMINI_MODEL` env var without changing workflow
