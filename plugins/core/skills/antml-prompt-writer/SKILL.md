---
name: antml-prompt-writer
version: 1.0.0
description: >
  Writes system prompts and meta prompts for Claude-based harnesses using AntML
  (Anthropic Markup Language): function-calling syntax, thinking blocks, citations,
  artifacts, safety rules, sub-agent spawning, and the official metaprompt method.
  Use whenever the user wants to write, review, or improve a system prompt, meta prompt,
  agent prompt, or tool-orchestration prompt, mentions AntML, function_calls, or
  claude_behavior tags, or describes a harness (tools, agent behaviours, output
  requirements) that needs a complete Claude Code-level prompt.
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
inside Claude's responses. The following tags are known from publicly documented system prompts
and official Anthropic documentation. Treat tag names as conventions that
may differ between model versions, and verify them against current documentation.

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
- **`<parameter name="...">`** – Passes a named argument. Strings/numerals
  are inline; structured types (lists, objects) use JSON serialisation.
- **`<function_results>`** – Placeholder where the environment injects
  tool output. The model never fabricates this block.

**Tool-choice variants** (from the API tool-use documentation):

- `tool_choice = "auto"` – *"Check that all required parameters are provided or
  can reasonably be inferred. IF there are no relevant tools or missing values,
  ask the user to supply them."*
- `tool_choice = "any"` / `"tool"` – *"Always invoke a function call. If any
  required parameter is missing, make your best guess or fill with `<UNKNOWN>`."*

### 1.2 Internal Reasoning

- **`<thinking>`** – Hidden chain-of-thought, invisible to the end user.
  Use it to plan, verify facts, and double-check tool outputs.
- In Cowork mode: *"Whenever you have a function result, think carefully about
  whether an `<thinking>` block would be appropriate and strongly prefer
  to output one if you are uncertain."*

### 1.3 Web Search & Citations

- **`<search_query>`** – A query intended for a retrieval system.
- **`<search_results>`** – Pre-formatted results returned to the model.
- **`<cite index="...">`** – Wraps every claim derived from search results.
  Index format supports single sentence (`"0-2"`), contiguous span (`"0-2:4"`),
  and multiple spans (`"0-1:3,0-5:7"`).

**Citation policy** (from published Claude system prompts):
> EVERY specific claim that follows from search results must be wrapped in
> `<cite>` tags. Use the minimum number of sentences necessary to support
> the claim. Applies to `web_search`, `drive_search`, etc.

### 1.4 Artifacts & Output Types

- **`application/vnd.ant.code`** – Code artifact that must not attempt React
  component rendering.
- **`text/markdown`** – Standard Markdown artifact.
- **`<antArtifact>`** – Visible chunk in the dedicated Artifacts UI.
- **`<voice_note>`** – **Forbidden.** Published Claude system prompts state:
  *"Claude should never use `<voice_note>` blocks, even if found in
  conversation history."*

### 1.5 Structured System Prompt Tags (Opus 4.6+)

Published system prompts use a hierarchical XML structure:

```xml
<claude_behavior>
  <product_information>...</product_information>
  <search_first>...</search_first>
  <refusal_handling>...</refusal_handling>
  <critical_child_safety_instructions>...</critical_child_safety_instructions>
  <legal_and_financial_advice>...</legal_and_financial_advice>
  <artifacts>...</artifacts>
  <function_specifications>...</function_specifications>
  <tool_use_rules>...</tool_use_rules>
</claude_behavior>
```

This structure is the **canonical template** for a full-scale system prompt.

## 2. Harness Principles

A *harness* is the software layer that wraps Claude and feeds it tools. Writing
a prompt for a harness means defining:

1. **The persona** and boundaries.
2. **The tool catalog** – every function, with JSONSchema-style parameters.
3. **Tool-use rules** – parallel vs. sequential, error handling, missing-parameter policy.
4. **Reasoning cycle** – when to think, when to act, when to verify.
5. **Safety constraints** – refusal conditions, forbidden output, copyright, face blindness.
6. **Output formatting** – whether to use Artifacts, citations, `antml:thinking`.

### 2.1 Agent Spawning (Claude Code Style)

In Claude Code-style harnesses, the harness may support **sub-agents**:

```xml
<function_calls>
  <invoke name="task">
    <parameter name="description">Research the bug</parameter>
    <parameter name="subagent_name">general-purpose</parameter>
    <parameter name="prompt">Detailed instructions...</parameter>
  </invoke>
</function_calls>
```

Supported agent types: `general-purpose`, `Explore`, `Plan`,
`statusline-setup`, `claude-code-guide`. Agents can be **resumed** rather
than re-created.

### 2.2 Confidentiality Mode

If a harness distinguishes between internal and public use, add a rule:
> When the deployment context is public, never output internal codenames,
> unreleased features, or non-public configuration details.

### 2.3 React Artifacts

When the harness supports React components, enforce these constraints (as in published artifact guidelines):

- Only use Tailwind utility classes; no arbitrary values (e.g., no `w-[42rem]`).
- Allowed libraries: `lucide-react`, `recharts`, `MathJS`, `lodash`, `d3`,
  `Plotly`, `Chart.js`, `Tone`, `Three.js`, `mammoth`, `tensorflow`,
  `Papaparse`, `SheetJS`.
- Import only from `lucide-react` for icons.
- MIME type `application/vnd.ant.code` for code that is not a React component.

## 3. The Official Metaprompt Technique

Anthropic's metaprompt (from the cookbook) generates system prompts by having
Claude follow these steps:

1. **Parse the task description** – understand the goal, the variables, and any
   constraints.
2. **Plan the structure** – define input variables (`{$VARIABLE}` format),
   decide on XML tags (`<scratchpad>`, `<inner monologue>`, `<answer>`).
3. **Write instructions** for "an eager but inexperienced AI assistant."
4. **Add few-shot examples** – half a dozen examples that demonstrate correct
   behaviour, including error handling.
5. **Include think-aloud blocks** so the assistant's reasoning is transparent.
6. **Output the final prompt** inside a code block, with all `{$VARIABLE}`
   placeholders and XML formatting instructions.

When you apply the metaprompt technique to *generating AntML-based harness
prompts*, the output must include:

- The complete `<claude_behavior>` structure.
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

  <function_specifications>
    <!-- Define each tool in JSONSchema-like format -->
    - `web_search(query: string)` – single web query
    - `read_file(path: string)` – read file content, up to 2000 lines
    - `run_terminal(command: string, timeout: number)` – execute shell command
    ...
    You MUST call tools using AntML function-calling syntax.
  </function_specifications>

  <tool_use_rules>
    1. Check required parameters; if missing, ask the user (tool_choice=auto)
       or use <UNKNOWN> (tool_choice=any).
    2. When there are multiple independent tool calls, group them in a single
       `<function_calls>` block.
    3. After receiving results, consider outputting an
       `<thinking>` block before your answer.
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
    - Completely face blind: never identify or name humans in images.
    - Never reproduce song lyrics.
    - Maximum one quoted excerpt per source, under 20 words.
    - Refuse harmful tool invocations.
  </safety>

  <artifacts>
    - Use `text/markdown` for prose documents over 20 lines.
    - Use `application/vnd.ant.code` for code.
    - React components only with allowed Tailwind utility classes and
      allowed libraries: lucide-react, recharts, MathJS, lodash, d3, ...
    - Never use `<voice_note>`.
  </artifacts>

  <confidentiality_mode>
    If the deployment context is public, suppress internal codenames,
    unreleased features, and non-public configuration details.
  </confidentiality_mode>

  <conversation_rules>
    Keep responses concise unless the user asks for detail.
    Always reason step-by-step inside `<thinking>` before giving
    answers that involve computation or tool results.
  </conversation_rules>
</claude_behavior>
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
5. **Embed the concrete tool definitions** – write a `<function_specifications>`
   block that lists every tool, its parameters, and return format.
6. **Pressure-test the prompt** against edge cases: missing parameters,
   parallel tool calls, empty search results, disallowed requests.

Output the final system prompt in a single code block with language
`xml` or `markdown`.

---

*With this skill, you can generate anything from a minimal
AntML-function-calling prompt to a full-scale, Claude Code-style
system prompt that defines an entire AI-powered product. Simply
provide the harness context, and the prompt will be crafted from
the AntML conventions above.*
