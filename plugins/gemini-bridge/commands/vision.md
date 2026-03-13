---
description: Convert screenshots, diagrams, or mockups to code/docs using Gemini's vision
category: ai-engineering
argument-hint: "<image-path> <task-description>"
allowed-tools:
  - Read
  - Bash
---

# Gemini Bridge: Vision

Transform visual inputs into code, documentation, or structured data using Gemini 2.5 Pro's multimodal capabilities.

## Usage

```
/gemini-bridge:vision ./mockup.png "Generate a React component matching this UI"
/gemini-bridge:vision ./architecture.jpg "Convert this diagram to a PlantUML class diagram"
/gemini-bridge:vision ./screenshot.png "Identify all UI components and their props"
/gemini-bridge:vision ./whiteboard.jpg "Extract the algorithm described and implement it in Python"
```

## Supported Formats

- PNG, JPG, WEBP, GIF — UI screenshots, diagrams, photos
- PDF — Architecture documents, specifications

## Workflow

1. Verify image path exists and is readable
2. Call `gemini_analyze_image` with path and task description
3. Claude Code uses Gemini's output to generate/refine code
4. Result is attributed to Gemini and further refined by Claude if needed

## Use Cases in Software Engineering Education

- Students photograph whiteboard designs → instant code scaffold
- UI mockups → React component stubs
- Legacy system screenshots → migration planning docs
- Architecture diagrams → IaC templates (Terraform, Docker Compose)
