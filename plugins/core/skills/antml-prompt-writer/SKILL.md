---
name: antml-prompt-writer
version: 1.0.0
description: >
  Writes system prompts and meta prompts for Claude-based harnesses that use AntML
  (Anthropic Markup Language): function-calling syntax, thinking blocks, citations,
  artifacts, sub-agent spawning, and the metaprompt method. Use whenever the user
  wants to write, review, or improve a harness system prompt or meta prompt, mentions
  AntML, function_calls, or claude_behavior tags, or describes a harness (tools,
  agent behaviours, output requirements) that needs a complete Claude Code-level prompt.
allowed-tools:
  - Read
  - Write
  - Edit
license: MIT
---

# AntML Prompt Writer

This skill equips you to write **production-grade system prompts** for Claude-based
assistants that use AntML. It covers everything from a single function call to a
fully-fledged tool-orchestrated agent like Claude Code.

## 1. The AntML Canon

AntML is an XML-based markup language that structures non-conversational actions
inside Claude's responses. The tags below are conventions observed in Claude
harnesses. They are not backed by a single official specification and may differ
between model versions and products, so verify them against current Anthropic
documentation before relying on them in production.

### 1.1 Function-Calling & Tool Invocation

```xml
<function_calls>
  <invoke name="tool_name">
    <parameter name="param1">value</parameter>
    <!-- Lists/objects as JSON -->
    <parameter name="param2">["a","b"]</parameter>
  </invoke>
</function_calls>
```

- **`<function_calls>`** – Wrapper for one or more invocations. Multiple
  `<invoke>` blocks inside are for **parallel execution** when no
  inter-dependency exists.
- **`<invoke name="...">`** – Declares the function to call.
- **`<parameter name="...">`** – Passes a named argument. Strings and numbers
  are inline; structured types (lists, objects) use JSON serialisation.
- **`<function_results>`** – Placeholder where the environment injects
  tool output. The model never fabricates this block.

**Tool choice** is a harness/API setting, not something the model sees. In the
Messages API it is a request parameter: `{"type": "auto"}` (the model decides),
`{"type": "any"}` (the model must call some tool), `{"type": "tool", "name": "..."}`
(the model must call that tool), or `{"type": "none"}`. Do not write `tool_choice`
rules into the system prompt. Instead, tell the model what to do when a required
parameter is missing: infer it if it is reasonably clear, otherwise ask the user.

### 1.2 Internal Reasoning

- **`<thinking>`** – Hidden chain-of-thought, invisible to the end user.
  Use it to plan, verify facts, and double-check tool outputs. Some harnesses use
  a namespaced variant of this tag; use whichever form the target harness
  documents, and use it consistently throughout the prompt.

### 1.3 Web Search & Citations

- **`<search_query>`** – A query intended for a retrieval system.
- **`<search_results>`** – Pre-formatted results returned to the model.
- **`<cite index="...">`** – Wraps every claim derived from search results.
  Index format supports single sentence (`"0-2"`), contiguous span (`"0-2:4"`),
  and multiple spans (`"0-1:3,0-5:7"`).

**Typical citation policy:**
> Every specific claim that follows from search results must be wrapped in
> `<cite>` tags. Use the minimum number of sentences necessary to support
> the claim. Applies to `web_search`, `drive_search`, etc.

### 1.4 Artifacts & Output Types

Artifact types depend on the product. Common ones:

- **`text/markdown`** – Standard Markdown document.
- **`application/vnd.ant.code`** – Code that is not a React component.
- **`application/vnd.ant.react`** – React component (see 2.3).
- **`text/html`** – Single-file HTML page.
- **`image/svg+xml`** – SVG image.
- **`application/vnd.ant.mermaid`** – Mermaid diagram.
- **`<antArtifact>`** – Wrapper that renders a chunk in the dedicated Artifacts UI.

Some products also forbid specific tags, such as `<voice_note>`. If the target
harness has such a rule, state it explicitly in the prompt.

### 1.5 Structured System Prompt Tags

Long Claude system prompts commonly use a hierarchical XML structure. This is a
common structure, not a required one:

```xml
<claude_behavior>
  <product_information>...</product_information>
  <search_first>...</search_first>
  <refusal_handling>...</refusal_handling>
  <critical_child_safety_instructions>...</critical_child_safety_instructions>
  <legal_and_financial_advice>...</legal_and_financial_advice>
  <artifacts>...</artifacts>
  <tool_use_rules>...</tool_use_rules>
</claude_behavior>
```

Tool definitions normally live outside this block (see 2.4).

## 2. Harness Principles

A *harness* is the software layer that wraps Claude and feeds it tools. Writing
a prompt for a harness means defining:

1. **The persona** and boundaries.
2. **The tool catalog** – every function, as a JSON schema (see 2.4).
3. **Tool-use rules** – parallel vs. sequential, error handling, missing-parameter policy.
4. **Reasoning cycle** – when to think, when to act, when to verify.
5. **Safety constraints** – refusal conditions, forbidden output, copyright, privacy.
6. **Output formatting** – whether to use Artifacts, citations, `<thinking>`.

### 2.1 Agent Spawning (Claude Code Style)

If the harness supports **sub-agents**, document the exact tool name and
parameters of that harness. In Claude Code the tool is `Agent` (formerly `Task`)
and the agent is selected with `subagent_type`:

```xml
<function_calls>
  <invoke name="Agent">
    <parameter name="description">Research the bug</parameter>
    <parameter name="subagent_type">general-purpose</parameter>
    <parameter name="prompt">Detailed instructions...</parameter>
  </invoke>
</function_calls>
```

The built-in agent types (`general-purpose`, `Explore`, `Plan`,
`statusline-setup`, `claude-code-guide`) are specific to Claude Code; list the
types of your own harness instead. Agents can be **resumed** rather than
re-created if the harness offers a messaging tool for it.

### 2.2 Confidentiality Mode

If a harness distinguishes between internal and public use, add a rule:
> When the deployment context is public, never output internal codenames,
> unreleased features, or non-public configuration details.

### 2.3 React Artifacts

When the harness supports React components, state its constraints explicitly.
A typical set:

- Only use Tailwind utility classes; no arbitrary values (e.g., no `w-[42rem]`).
- Allow-list the libraries the sandbox actually provides, for example
  `lucide-react`, `recharts`, `MathJS`, `lodash`, `d3`, `Plotly`, `Chart.js`,
  `Tone`, `Three.js`, `mammoth`, `tensorflow`, `Papaparse`, `SheetJS`, and
  `shadcn/ui` where available.
- Import only from `lucide-react` for icons.

### 2.4 Tool Definitions

Define each tool as a JSON schema, outside the behaviour block:

```xml
<functions>
  <function>{"name": "read_file", "description": "Read a file, up to 2000 lines.",
    "parameters": {"type": "object",
      "properties": {"path": {"type": "string"}},
      "required": ["path"]}}</function>
</functions>
```

The description of each tool is part of the prompt: state what it does, when to
use it, and when not to.

## 3. The Metaprompt Technique

The approach below is adapted from Anthropic's metaprompt cookbook, which has
Claude draft a system prompt from a task description:

1. **Parse the task description** – understand the goal, the variables, and any
   constraints.
2. **Plan the structure** – define input variables (`{$VARIABLE}` format),
   decide on XML tags (`<scratchpad>`, `<inner_monologue>`, `<answer>`).
3. **Write instructions** for "an eager but inexperienced AI assistant."
4. **Add few-shot examples** – the cookbook metaprompt itself contains about half
   a dozen; for a generated prompt, 2-3 well-chosen examples are usually enough
   (see Section 5).
5. **Include think-aloud blocks** so the assistant's reasoning is transparent.
6. **Return the finished prompt** wrapped in a tag such as `<Instructions>`, with
   all `{$VARIABLE}` placeholders and XML formatting instructions.

When you apply the technique to *generating AntML-based harness prompts*, the
output must include:

- The `<claude_behavior>` structure (or an equivalent).
- A list of allowed AntML tags with usage rules.
- Tool definitions and invocation syntax.
- Citation and thinking rules.
- Safety and refusal policies.

## 4. Crafting a Full Claude Code-Level Meta Prompt

Given a harness specification (list of tools, required workflows, special
constraints), use this template as the skeleton:

```xml
<claude_behavior>
  <product_information>
    You are "Assistant Name", an AI created by [Organization].
    Current date: [DATE]. Your knowledge cutoff is [CUTOFF].
    Your model string is [MODEL_STRING].
  </product_information>

  <search_first>
    For any factual question about the present-day world, search before answering.
    Your confidence is not an excuse to skip search.
  </search_first>

  <tool_use_rules>
    1. Tool definitions are provided as JSON schemas in the functions block.
       Call tools using AntML function-calling syntax.
    2. If a required parameter is missing and cannot be reasonably inferred,
       ask the user instead of guessing.
    3. When there are multiple independent tool calls, group them in a single
       `<function_calls>` block.
    4. After receiving results, consider writing a `<thinking>` block before
       your answer.
  </tool_use_rules>

  <citation_policy>
    Every claim derived from search must be wrapped in
    `<cite index="...">`. Use the minimum number of sentences.
  </citation_policy>

  <thinking_and_transparency>
    You may use `<thinking>` to plan, but never show it to the user.
    Use `<antArtifact>` for content that requires a dedicated UI.
  </thinking_and_transparency>

  <safety>
    <!-- Optional examples for a consumer chat product. Keep only what fits
         the target harness and add domain-specific rules. -->
    - Never identify real people from their facial features in images.
    - Never reproduce song lyrics.
    - Quote sources sparingly: one short excerpt per source.
    - Refuse harmful tool invocations.
  </safety>

  <artifacts>
    - Use `text/markdown` for prose documents over 20 lines.
    - Use `application/vnd.ant.code` for code.
    - React components only with allowed Tailwind utility classes and
      the libraries the sandbox provides.
  </artifacts>

  <confidentiality_mode>
    If the deployment context is public, suppress internal codenames,
    unreleased features, and non-public configuration details.
  </confidentiality_mode>

  <conversation_rules>
    Keep responses concise unless the user asks for detail.
    Reason step-by-step inside `<thinking>` before giving
    answers that involve computation or tool results.
  </conversation_rules>
</claude_behavior>

<functions>
  <!-- One <function>{JSON schema}</function> per tool, see Section 2.4 -->
</functions>
```

To fill the template, inject the harness-specific tool definitions, the
user's required behaviours, and any additional constraints. The resulting
prompt is a **complete meta prompt** ready to be placed inside the harness
before every conversation.

## 5. Prompt Generation Workflow

When asked to create a prompt using this skill, follow these steps:

1. **Gather requirements** – target model, list of tools, safety needs,
   output format preferences, agent spawning, etc.
2. **Select relevant AntML tags** from Section 1.
3. **Sketch the `<claude_behavior>` structure** using the template in
   Section 4.
4. **Apply the metaprompt method**:
   - Write the system prompt as if for "an eager but inexperienced AI."
   - Provide 2-3 full-conversation examples showing correct tool use,
     error recovery, and safety refusals.
   - Include explicit instructions for when to use each AntML tag.
5. **Embed the concrete tool definitions** – write a `<functions>` block with
   one JSON schema per tool.
6. **Pressure-test the prompt** against edge cases: missing parameters,
   parallel tool calls, empty search results, disallowed requests.

Output the final system prompt in a single code block with language
`xml` or `markdown`.
