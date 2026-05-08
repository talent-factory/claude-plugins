---
name: vision
description: >
  Transforms visual inputs (screenshots, UI mockups, architecture diagrams,
  whiteboard photos, PDFs) into code, documentation, or structured data using
  Gemini 2.5 Pro's multimodal capabilities. Activate when the user shares an
  image file and asks to "convert this mockup to code", "generate a component
  from this screenshot", "what does this diagram show", "extract this
  architecture", or "turn this whiteboard into code".
---

# Gemini Bridge: Vision

Transform visual inputs into code, documentation, or structured data using
Gemini 2.5 Pro's multimodal capabilities.

## Supported Inputs

| Format | Typical use case |
|---|---|
| PNG / JPG / WEBP | UI screenshots, mockups, whiteboard photos |
| GIF | Animated UI flows |
| PDF | Architecture documents, specifications, diagrams |

## Workflow

### 1. Confirm the image path

Verify the file exists and is readable:
```bash
ls -lh <image_path>
```

If the user has not provided a path, ask for it before proceeding.

### 2. Verify the bridge

```python
gemini_status()
```

### 3. Analyse the image

```python
gemini_analyze_image(
    image_path=<absolute_or_relative_path>,
    question=<task_description>
)
```

Craft the `question` to be as specific as possible. Examples:
- `"Generate a React TypeScript component matching this UI mockup exactly. Include all visible states and props."`
- `"Convert this UML class diagram to a Python dataclass hierarchy."`
- `"Extract the algorithm described on this whiteboard and implement it in Python with type hints."`
- `"Identify all UI components visible in this screenshot and list their props and interactions."`

### 4. Refine with Claude

Use Gemini's output as a scaffold. Claude then:
- Fills in implementation details Gemini left as stubs
- Adapts the output to the project's existing patterns and conventions
- Validates correctness and runs any available tests

Always attribute the initial analysis:

```markdown
**Initial analysis by Gemini 2.5 Pro**
[Gemini's output]

**Refined implementation**
[Claude's refined version]
```

## Common Use Cases

| Input | Output |
|---|---|
| UI mockup | React / Vue component with props |
| Architecture diagram | PlantUML / Mermaid diagram source |
| Whiteboard algorithm | Implemented function with tests |
| Legacy screenshot | Migration planning document |
| PDF specification | Structured data model or IaC template |
