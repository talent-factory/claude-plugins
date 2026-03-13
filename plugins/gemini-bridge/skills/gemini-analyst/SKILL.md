---
name: gemini-analyst
description: >
  Background knowledge for using the Gemini Bridge MCP tools effectively.
  Teaches Claude when and how to delegate to Gemini in a model-agnostic
  multi-agent setup. Claude-invocable only.
user-invocable: false
---

# Gemini Bridge: Usage Patterns

## When to Delegate to Gemini

### Token Budget Rule
Estimate token count before analysis:
- < 150K tokens → Claude handles directly
- > 150K tokens → Delegate to Gemini

Quick estimation: ~750 tokens per ~600 words, ~500 tokens per ~400 lines of code.

### Vision Rule
For image analysis tasks where Gemini's vision capabilities or extended context
provide an advantage, prefer `gemini_analyze_image`. Claude Code can also read
images natively via the Read tool, so use Gemini when the analysis requires
Gemini-specific strengths (e.g., large diagrams, complex OCR, PDF parsing).

### Validation Rule
For architecture decisions, security reviews, or critical design choices:
Use `gemini_compare_approaches` to get an independent assessment.
This implements the **"propose with Claude, validate with Gemini"** pattern.

## Tool Reference

```python
# Check bridge is working (do this once per session)
gemini_status()

# Short text prompts / second opinions
gemini_analyze_text(prompt, context=None, temperature=0.2)

# Large codebase analysis (up to 1M tokens with default model)
gemini_analyze_codebase(code_content, task, language=None)

# Image/screenshot/PDF analysis
gemini_analyze_image(image_path, question)

# Architecture/implementation comparison
gemini_compare_approaches(problem, approach_a, approach_b, criteria=None)
```

## Output Attribution Pattern

Always label Gemini's output clearly:

```markdown
**Analysis by Gemini 2.5 Pro**
[Gemini's response]
```

This is important for:
1. Transparency in multi-model workflows
2. Audit trails in educational settings
3. Debugging when models disagree

## Model-Agnostic Design Principle

The bridge is designed so that the **routing logic lives in agent configuration**,
not in application code. To swap Gemini for a different model:
1. Set the `GEMINI_MODEL` environment variable
2. All agents/commands continue working unchanged

This demonstrates to students: **good architecture is model-agnostic**.
