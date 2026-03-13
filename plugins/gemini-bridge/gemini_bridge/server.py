"""
Gemini Bridge MCP Server
========================
Exposes Google Gemini 2.5 Pro as MCP tools that Claude Code can call natively.
This enables model-agnostic multi-agent workflows where Claude orchestrates
and delegates specific tasks (long-context, vision, parallel reasoning) to Gemini.

Usage:
    Set GEMINI_API_KEY environment variable, then Claude Code will discover
    and call these tools automatically via the .mcp.json configuration.
"""

import os
import base64
import mimetypes
from pathlib import Path
from typing import Optional

try:
    import google.generativeai as genai
    from mcp.server.fastmcp import FastMCP
except ImportError as e:
    raise ImportError(
        f"Missing dependency: {e}\n"
        "Run: pip install google-generativeai fastmcp"
    ) from e

# ── Server Setup ─────────────────────────────────────────────────────────────

mcp = FastMCP(
    name="gemini-bridge",
    instructions="""
    Gemini Bridge exposes Google Gemini 2.5 Pro capabilities to Claude.
    Use these tools when:
    - Codebase analysis exceeds ~150K tokens (Gemini handles up to 1M)
    - Multimodal input is needed (screenshots, diagrams, PDFs)
    - A second model opinion adds value (model-agnostic validation)
    - Parallel reasoning with a different architecture is beneficial
    """,
)

GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-pro-preview-06-05")

_configured = False


def _get_client(temperature: float = 0.2) -> genai.GenerativeModel:
    """Initialize Gemini client from environment."""
    global _configured
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable not set.\n"
            "Get your key at: https://aistudio.google.com/app/apikey"
        )
    if not _configured:
        genai.configure(api_key=api_key)
        _configured = True
    return genai.GenerativeModel(
        model_name=GEMINI_MODEL,
        generation_config=genai.GenerationConfig(
            temperature=temperature,
            max_output_tokens=8192,
        ),
    )


# ── Tools ────────────────────────────────────────────────────────────────────

@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "openWorldHint": True,
    }
)
def gemini_analyze_text(
    prompt: str,
    context: Optional[str] = None,
    temperature: float = 0.2,
) -> str:
    """
    Send a text prompt to Gemini 2.5 Pro and return the response.

    Use this for:
    - Getting a second-model perspective on architecture decisions
    - Complex reasoning tasks where a different LLM approach adds value
    - Model-agnostic validation of Claude's output

    Args:
        prompt: The main question or instruction for Gemini
        context: Optional additional context (system prompt / background info)
        temperature: Creativity level 0.0–1.0 (default 0.2 for precise answers)

    Returns:
        Gemini's response as plain text
    """
    model = _get_client(temperature=temperature)

    full_prompt = f"{context}\n\n{prompt}" if context else prompt

    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"❌ Gemini analysis failed: {e}"


@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "openWorldHint": False,
    }
)
def gemini_analyze_codebase(
    code_content: str,
    task: str,
    language: Optional[str] = None,
) -> str:
    """
    Analyze a large codebase or file content with Gemini's 1M-token context window.

    Use this when:
    - Code content exceeds Claude's comfortable context (~150K tokens)
    - You need to analyze entire repositories at once
    - Deep cross-file dependency analysis is required

    Args:
        code_content: The full code content to analyze (paste entire files/codebase)
        task: What to analyze (e.g. "Find security vulnerabilities", "Explain architecture")
        language: Programming language hint (e.g. "Python", "TypeScript") — optional

    Returns:
        Gemini's analysis of the codebase
    """
    model = _get_client()

    lang_hint = f"Language: {language}\n" if language else ""
    prompt = f"""You are an expert software engineer performing codebase analysis.

{lang_hint}Task: {task}

Code to analyze:
```
{code_content}
```

Provide a detailed, structured analysis addressing the task above."""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Gemini codebase analysis failed: {e}"


@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "openWorldHint": False,
    }
)
def gemini_analyze_image(
    image_path: str,
    question: str,
) -> str:
    """
    Analyze an image or screenshot using Gemini's multimodal capabilities.

    Use this for:
    - Analyzing UI screenshots for code generation
    - Reading architecture diagrams and converting to code/docs
    - Extracting information from charts, mockups, or visual specs
    - OCR on complex documents (PDFs, whiteboard photos)

    Args:
        image_path: Absolute path to the image file (PNG, JPG, WEBP, PDF)
        question: What to extract or analyze from the image

    Returns:
        Gemini's description/analysis of the image content
    """
    model = _get_client()

    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    mime_type, _ = mimetypes.guess_type(str(path))
    if not mime_type:
        mime_type = "image/png"

    with open(path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode("utf-8")

    prompt_parts = [
        question,
        {
            "inline_data": {
                "mime_type": mime_type,
                "data": image_data,
            }
        },
    ]

    try:
        response = model.generate_content(prompt_parts)
        return response.text
    except Exception as e:
        return f"❌ Gemini image analysis failed: {e}"


@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "openWorldHint": False,
    }
)
def gemini_compare_approaches(
    problem: str,
    approach_a: str,
    approach_b: str,
    criteria: Optional[str] = None,
) -> str:
    """
    Use Gemini to compare two technical approaches or implementations objectively.

    Ideal for model-agnostic validation: Claude proposes, Gemini evaluates.
    Use this in multi-agent workflows where independent review adds value.

    Args:
        problem: The problem or context both approaches address
        approach_a: First approach / implementation (code, architecture, or description)
        approach_b: Second approach / implementation
        criteria: Optional evaluation criteria (e.g. "performance, maintainability, security")

    Returns:
        Structured comparison with recommendation
    """
    model = _get_client()

    criteria_text = f"\nEvaluate specifically on: {criteria}" if criteria else ""

    prompt = f"""You are a senior software architect conducting an objective technical review.

Problem/Context:
{problem}

Approach A:
{approach_a}

Approach B:
{approach_b}
{criteria_text}

Provide:
1. Strengths and weaknesses of each approach
2. Performance/scalability implications
3. Maintainability assessment
4. Clear recommendation with rationale
5. Any hybrid approach that could combine the best of both"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Gemini comparison failed: {e}"


@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "openWorldHint": True,
    }
)
def gemini_status() -> str:
    """
    Check Gemini Bridge connectivity and return model information.

    Use this to verify the bridge is working before starting a long task.

    Returns:
        Status information and available model details
    """
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        return "❌ GEMINI_API_KEY not set. Bridge is not operational."

    try:
        model = _get_client()
        response = model.generate_content("Reply with: GEMINI_BRIDGE_OK")
        if "GEMINI_BRIDGE_OK" in response.text:
            return (
                f"✅ Gemini Bridge operational\n"
                f"Model: {GEMINI_MODEL}\n"
                f"Context window: 1,000,000 tokens\n"
                f"Capabilities: text, code, vision (images/PDFs)\n"
                f"Tools available: analyze_text, analyze_codebase, analyze_image, compare_approaches"
            )
        return f"⚠️ Unexpected response: {response.text}"
    except Exception as e:
        return f"❌ Connection failed: {e}"


# ── Entry Point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run(transport="stdio")
