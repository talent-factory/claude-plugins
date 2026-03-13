"""
Tests for Gemini Bridge MCP Server
Run with: pytest tests/ -v
"""

import os
import pytest
from unittest.mock import patch, MagicMock


# ── Unit Tests (no API key required) ────────────────────────────────────────

class TestGeminiStatus:
    def test_status_no_api_key(self):
        """Should return error message when API key is missing."""
        from gemini_bridge.server import gemini_status
        with patch.dict(os.environ, {}, clear=True):
            if "GEMINI_API_KEY" in os.environ:
                del os.environ["GEMINI_API_KEY"]
            result = gemini_status()
        assert "not set" in result or "GEMINI_API_KEY" in result

    def test_status_with_mock(self):
        """Should return OK status with valid mock response."""
        from gemini_bridge.server import gemini_status
        mock_response = MagicMock()
        mock_response.text = "GEMINI_BRIDGE_OK"

        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}):
            with patch("google.generativeai.GenerativeModel.generate_content",
                       return_value=mock_response):
                result = gemini_status()
        assert "operational" in result.lower() or "OK" in result


class TestToolSignatures:
    """Verify tool functions exist and have correct signatures."""

    def test_analyze_text_exists(self):
        from gemini_bridge.server import gemini_analyze_text
        import inspect
        sig = inspect.signature(gemini_analyze_text)
        assert "prompt" in sig.parameters
        assert "context" in sig.parameters
        assert "temperature" in sig.parameters

    def test_analyze_codebase_exists(self):
        from gemini_bridge.server import gemini_analyze_codebase
        import inspect
        sig = inspect.signature(gemini_analyze_codebase)
        assert "code_content" in sig.parameters
        assert "task" in sig.parameters

    def test_analyze_image_exists(self):
        from gemini_bridge.server import gemini_analyze_image
        import inspect
        sig = inspect.signature(gemini_analyze_image)
        assert "image_path" in sig.parameters
        assert "question" in sig.parameters

    def test_compare_approaches_exists(self):
        from gemini_bridge.server import gemini_compare_approaches
        import inspect
        sig = inspect.signature(gemini_compare_approaches)
        assert "problem" in sig.parameters
        assert "approach_a" in sig.parameters
        assert "approach_b" in sig.parameters


class TestImageAnalysis:
    def test_missing_image_raises_error(self):
        """Should raise FileNotFoundError for non-existent image."""
        from gemini_bridge.server import gemini_analyze_image
        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}):
            with pytest.raises(FileNotFoundError):
                gemini_analyze_image("/nonexistent/path.png", "Describe this")


# ── Integration Tests (require GEMINI_API_KEY) ───────────────────────────────

@pytest.mark.skipif(
    not os.environ.get("GEMINI_API_KEY"),
    reason="GEMINI_API_KEY not set — skipping live API tests"
)
class TestLiveIntegration:
    def test_live_status(self):
        from gemini_bridge.server import gemini_status
        result = gemini_status()
        assert "operational" in result.lower()

    def test_live_analyze_text(self):
        from gemini_bridge.server import gemini_analyze_text
        result = gemini_analyze_text("Reply with exactly: BRIDGE_TEST_OK")
        assert "BRIDGE_TEST_OK" in result

    def test_live_analyze_codebase(self):
        from gemini_bridge.server import gemini_analyze_codebase
        sample_code = """
def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
"""
        result = gemini_analyze_codebase(
            code_content=sample_code,
            task="Identify performance issues and suggest improvements",
            language="Python"
        )
        assert len(result) > 50  # Non-trivial response
        assert "recursion" in result.lower() or "memoization" in result.lower()
