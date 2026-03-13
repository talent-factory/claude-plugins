---
description: Use Gemini as an independent reviewer to compare two technical approaches
category: ai-engineering
argument-hint: "<comparison-question>"
allowed-tools:
  - Read
  - Glob
  - Grep
---

# Gemini Bridge: Compare

Use Gemini 2.5 Pro as an independent technical reviewer to compare approaches.
This implements the "propose with Claude, validate with Gemini" pattern.

## Usage

```
/gemini-bridge:compare Should we use FastAPI or Django for this REST API?
/gemini-bridge:compare Review these two database schemas for the user module
/gemini-bridge:compare Evaluate: event-driven vs. synchronous architecture for ExamCraft
```

## Workflow

1. Claude generates or gathers Approach A and Approach B
2. Call `gemini_compare_approaches` with both approaches and evaluation criteria
3. Present Gemini's structured comparison
4. Claude synthesizes final recommendation combining both perspectives

## Teaching Note (AI-Assisted Software Engineering)

This command demonstrates the **model-agnostic validation pattern**:
- No single model has monopoly on correctness
- Different model architectures surface different trade-offs
- Production systems benefit from multi-model review pipelines
- Students can observe how the same problem is framed differently by different models
