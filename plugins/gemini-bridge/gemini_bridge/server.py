"""
Gemini Bridge MCP Server
========================
Exposes Google Gemini models (default: 2.5 Pro) as MCP tools that Claude Code
can call natively. The model is configurable via the GEMINI_MODEL environment
variable.

This enables model-agnostic multi-agent workflows where Claude orchestrates
and delegates specific tasks (long-context, vision, parallel reasoning) to Gemini.

Usage:
    Set GEMINI_API_KEY environment variable, then Claude Code will discover
    and call these tools automatically via the .mcp.json configuration.
"""

import mimetypes
import os
from pathlib import Path

try:
    from google import genai
    from google.genai import types
    from mcp.server.fastmcp import FastMCP
except ImportError as e:
    raise ImportError(
        f"Missing dependency: {e}\n"
        "Run: pip install google-genai fastmcp"
    ) from e

GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-pro")
MAX_IMAGE_SIZE = 20 * 1024 * 1024  # 20 MB
SUPPORTED_MIME_TYPES = {"image/png", "image/jpeg", "image/webp", "image/gif", "application/pdf"}

mcp = FastMCP(
    name="gemini-bridge",
    instructions="""
    Gemini Bridge exposes Google Gemini capabilities to Claude.
    Use these tools when:
    - Codebase analysis exceeds ~150K tokens (Gemini handles up to 1M)
    - Multimodal input is needed (screenshots, diagrams, PDFs)
    - A second model opinion adds value (model-agnostic validation)
    - Parallel reasoning with a different architecture is beneficial
    """,
)

_client: genai.Client | None = None


def _get_client() -> genai.Client:
    """Return a cached Gemini Client, creating it on first call."""
    global _client
    if _client is not None:
        return _client
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable not set.\n"
            "Get your key at: https://aistudio.google.com/app/apikey"
        )
    _client = genai.Client(api_key=api_key)
    return _client


def _generate(contents, *, temperature: float = 0.2) -> str:
    """Send a prompt to Gemini and return the response text.

    Exceptions propagate to FastMCP, which converts them into proper
    MCP error responses with isError: true.
    """
    client = _get_client()
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=contents,
        config=types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=8192,
        ),
    )
    return response.text


@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "openWorldHint": True,
    }
)
def gemini_analyze_text(
    prompt: str,
    context: str | None = None,
    temperature: float = 0.2,
) -> str:
    """
    Send a text prompt to Gemini and return the response.

    Use this for:
    - Getting a second-model perspective on architecture decisions
    - Complex reasoning tasks where a different LLM approach adds value
    - Model-agnostic validation of Claude's output

    Args:
        prompt: The main question or instruction for Gemini
        context: Optional additional context (system prompt / background info)
        temperature: Creativity level 0.0-2.0 (default 0.2 for precise answers)

    Returns:
        Gemini's response as plain text
    """
    full_prompt = f"{context}\n\n{prompt}" if context else prompt
    return _generate(full_prompt, temperature=temperature)


@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "openWorldHint": False,
    }
)
def gemini_analyze_codebase(
    code_content: str,
    task: str,
    language: str | None = None,
) -> str:
    """
    Analyze a large codebase or file content with Gemini's extended context window.

    Use this when:
    - Code content exceeds Claude's comfortable context (~150K tokens)
    - You need to analyze entire repositories at once
    - Deep cross-file dependency analysis is required

    The context limit depends on the configured model (default: 1M tokens for
    gemini-2.5-pro). No client-side token validation is performed.

    Args:
        code_content: The full code content to analyze (paste entire files/codebase)
        task: What to analyze (e.g. "Find security vulnerabilities", "Explain architecture")
        language: Programming language hint (e.g. "Python", "TypeScript") -- optional

    Returns:
        Gemini's analysis of the codebase
    """
    lang_hint = f"Language: {language}\n" if language else ""
    prompt = f"""You are an expert software engineer performing codebase analysis.

{lang_hint}Task: {task}

Code to analyze:
```
{code_content}
```

Provide a detailed, structured analysis addressing the task above."""

    return _generate(prompt)


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
        image_path: Absolute path to the image file (PNG, JPG, WEBP, GIF, PDF)
        question: What to extract or analyze from the image

    Returns:
        Gemini's description/analysis of the image content
    """
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    file_size = path.stat().st_size
    if file_size > MAX_IMAGE_SIZE:
        raise ValueError(
            f"File too large ({file_size / 1024 / 1024:.1f} MB). "
            f"Maximum supported size is {MAX_IMAGE_SIZE / 1024 / 1024:.0f} MB."
        )

    mime_type, _ = mimetypes.guess_type(str(path))
    if not mime_type or mime_type not in SUPPORTED_MIME_TYPES:
        raise ValueError(
            f"Unsupported file type '{mime_type or 'unknown'}' for '{image_path}'. "
            f"Supported: {', '.join(sorted(SUPPORTED_MIME_TYPES))}"
        )

    with open(path, "rb") as f:
        image_bytes = f.read()

    contents = [
        types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
        question,
    ]

    return _generate(contents)


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
    criteria: str | None = None,
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

    return _generate(prompt)


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
        return "GEMINI_API_KEY not set. Bridge is not operational."

    try:
        client = _get_client()
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents="Reply with: GEMINI_BRIDGE_OK",
            config=types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=64,
            ),
        )
        if "GEMINI_BRIDGE_OK" in response.text:
            return (
                f"Gemini Bridge operational\n"
                f"Model: {GEMINI_MODEL}\n"
                f"Context window: 1,000,000 tokens (gemini-2.5-pro; varies by model)\n"
                f"Capabilities: text, code, vision (images/PDFs)\n"
                f"Tools: gemini_analyze_text, gemini_analyze_codebase, "
                f"gemini_analyze_image, gemini_compare_approaches"
            )
        return f"Unexpected response: {response.text}"
    except Exception as e:
        return f"Connection failed: {e}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
