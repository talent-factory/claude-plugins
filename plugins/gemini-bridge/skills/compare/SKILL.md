---
name: compare
description: >
  Uses Gemini 2.5 Pro as an independent technical reviewer to compare two
  approaches and validate design decisions. Implements the "propose with
  Claude, validate with Gemini" pattern. Activate when the user asks to
  "compare these two approaches", "get a second opinion on this design",
  "validate this architectural decision", "should we use X or Y", or
  "review these two options independently".
---

# Gemini Bridge: Compare

Use Gemini 2.5 Pro as an independent reviewer to compare technical approaches.
No single model has a monopoly on correctness — different architectures surface
different trade-offs.

## Workflow

### 1. Gather both approaches

Either:
- The user provides both approaches directly
- Claude proposes Approach A; the user or the codebase supplies Approach B
- Claude independently drafts both approaches before requesting Gemini's review

### 2. Verify the bridge

```python
gemini_status()
```

### 3. Request the comparison

```python
gemini_compare_approaches(
    problem=<problem_statement>,
    approach_a=<description_or_code_of_approach_a>,
    approach_b=<description_or_code_of_approach_b>,
    criteria=<optional_evaluation_criteria>
)
```

Good `criteria` examples: "performance at scale", "maintainability for a small team",
"migration risk", "alignment with existing patterns in this codebase".

### 4. Present and synthesise

Label Gemini's output clearly:

```markdown
**Independent review by Gemini 2.5 Pro**
[Gemini's structured comparison]
```

Then provide Claude's synthesis: which recommendation to follow, and why,
taking into account both perspectives and the specific project context.

## Why This Matters

Two models with different training data and architectures will notice
different strengths and failure modes in the same design. A disagreement
between Claude and Gemini is a signal to investigate further, not a
reason to pick a winner arbitrarily.
