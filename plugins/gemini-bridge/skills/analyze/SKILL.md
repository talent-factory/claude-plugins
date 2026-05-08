---
name: analyze
description: >
  Delegates codebase or text analysis to Google Gemini 2.5 Pro via the MCP
  bridge when the task exceeds Claude's practical context limit (~150K tokens)
  or when a second-model perspective adds value. Activate when the user asks
  to "analyze this codebase", "analyze with Gemini", "this is too large for
  Claude", "deep-dive the entire src/ directory", or requests analysis of a
  PDF or large document collection.
---

# Gemini Bridge: Analyze

Delegate analysis tasks to Gemini 2.5 Pro (up to 1M token context) when the
scope exceeds what Claude should handle directly.

## When to Use Gemini vs. Claude

| Situation | Route to |
|---|---|
| Codebase > 150K tokens | **Gemini** |
| Screenshot, diagram, or PDF input | **Gemini** (`gemini_analyze_image`) |
| Independent second opinion on a design decision | **Gemini** |
| Normal-sized files, tool use, code writing | **Claude directly** |

Quick token estimate: ~500 tokens per 400 lines of code; ~750 tokens per 600 words.

## Workflow

### 1. Verify the bridge

```python
gemini_status()
```

If the bridge is unavailable, inform the user and fall back to Claude's native analysis (with a note about the context limitation).

### 2. Collect content

Use `Read`, `Glob`, and `Grep` to gather the relevant files or text into a
single context string. Include only what is necessary for the analysis task.

### 3. Invoke the appropriate tool

**Large codebase analysis:**
```python
gemini_analyze_codebase(code_content=<collected_code>, task=<analysis_task>)
```

**Text / document analysis:**
```python
gemini_analyze_text(prompt=<task_description>, context=<collected_text>)
```

**Image / screenshot / PDF:**
```python
gemini_analyze_image(image_path=<path>, question=<task_description>)
```

### 4. Present the result

Always attribute Gemini's output clearly:

```markdown
**Analysis by Gemini 2.5 Pro**
[Gemini's response]
```

Then synthesise findings and suggest next steps using Claude's judgment.

## Model Configuration

The model is set via the `GEMINI_MODEL` environment variable. Changing this
variable does not require any workflow changes — all tools continue to work
unchanged. This is the model-agnostic design principle: routing logic lives in
configuration, not in code.
