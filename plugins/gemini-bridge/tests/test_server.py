"""
Tests for Gemini Bridge MCP Server
Run with: pytest tests/ -v
"""

import os
import pytest
from unittest.mock import patch, MagicMock

import gemini_bridge.server as server_module


@pytest.fixture(autouse=True)
def reset_configured():
    """Reset the global _configured flag between tests to prevent state leakage."""
    server_module._configured = False
    yield
    server_module._configured = False


# -- Unit Tests (no API key required) ----------------------------------------


class TestGeminiStatus:
    def test_status_no_api_key(self):
        """Should return error message when API key is missing."""
        with patch.dict(os.environ, {}, clear=True):
            result = server_module.gemini_status()
        assert "GEMINI_API_KEY not set" in result

    def test_status_with_mock(self):
        """Should return OK status with valid mock response."""
        mock_response = MagicMock()
        mock_response.text = "GEMINI_BRIDGE_OK"

        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}):
            with patch("google.generativeai.GenerativeModel.generate_content",
                       return_value=mock_response):
                result = server_module.gemini_status()
        assert "operational" in result.lower()

    def test_status_unexpected_response(self):
        """Should return warning when Gemini responds without expected token."""
        mock_response = MagicMock()
        mock_response.text = "Hello, how can I help?"

        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}):
            with patch("google.generativeai.GenerativeModel.generate_content",
                       return_value=mock_response):
                result = server_module.gemini_status()
        assert "Unexpected response" in result

    def test_status_connection_failure(self):
        """Should return error when API call fails."""
        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}):
            with patch("google.generativeai.GenerativeModel.generate_content",
                       side_effect=ConnectionError("Network unreachable")):
                result = server_module.gemini_status()
        assert "Connection failed" in result

    def test_status_shows_full_tool_names(self):
        """Tool names in status output must use the full gemini_ prefix."""
        mock_response = MagicMock()
        mock_response.text = "GEMINI_BRIDGE_OK"

        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}):
            with patch("google.generativeai.GenerativeModel.generate_content",
                       return_value=mock_response):
                result = server_module.gemini_status()
        assert "gemini_analyze_text" in result
        assert "gemini_analyze_codebase" in result
        assert "gemini_analyze_image" in result
        assert "gemini_compare_approaches" in result


class TestToolSignatures:
    """Verify tool functions exist and have correct signatures."""

    def test_analyze_text_exists(self):
        import inspect
        sig = inspect.signature(server_module.gemini_analyze_text)
        assert "prompt" in sig.parameters
        assert "context" in sig.parameters
        assert "temperature" in sig.parameters

    def test_analyze_codebase_exists(self):
        import inspect
        sig = inspect.signature(server_module.gemini_analyze_codebase)
        assert "code_content" in sig.parameters
        assert "task" in sig.parameters

    def test_analyze_image_exists(self):
        import inspect
        sig = inspect.signature(server_module.gemini_analyze_image)
        assert "image_path" in sig.parameters
        assert "question" in sig.parameters

    def test_compare_approaches_exists(self):
        import inspect
        sig = inspect.signature(server_module.gemini_compare_approaches)
        assert "problem" in sig.parameters
        assert "approach_a" in sig.parameters
        assert "approach_b" in sig.parameters


class TestGetClient:
    def test_missing_api_key_raises_valueerror(self):
        """Should raise ValueError when GEMINI_API_KEY is not set."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="GEMINI_API_KEY"):
                server_module._get_client()

    def test_configure_called_once(self):
        """genai.configure should be called only once across multiple invocations."""
        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}):
            with patch("google.generativeai.configure") as mock_configure:
                with patch("google.generativeai.GenerativeModel"):
                    server_module._get_client()
                    server_module._get_client()
                    assert mock_configure.call_count == 1


class TestAnalyzeText:
    def test_returns_response_text(self):
        """Should return Gemini's response text on success."""
        mock_response = MagicMock()
        mock_response.text = "Analysis result"

        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}):
            with patch("google.generativeai.GenerativeModel.generate_content",
                       return_value=mock_response):
                result = server_module.gemini_analyze_text("Analyze this")
        assert result == "Analysis result"

    def test_prepends_context(self):
        """Should prepend context to prompt when provided."""
        mock_response = MagicMock()
        mock_response.text = "ok"

        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}):
            with patch("google.generativeai.GenerativeModel.generate_content",
                       return_value=mock_response) as mock_gen:
                server_module.gemini_analyze_text("question", context="background")
                call_args = mock_gen.call_args[0][0]
                assert "background" in call_args
                assert "question" in call_args

    def test_api_error_propagates(self):
        """API errors should propagate as exceptions, not be swallowed."""
        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}):
            with patch("google.generativeai.GenerativeModel.generate_content",
                       side_effect=RuntimeError("Quota exceeded")):
                with pytest.raises(RuntimeError, match="Quota exceeded"):
                    server_module.gemini_analyze_text("test")

    def test_missing_api_key_raises(self):
        """Missing API key should raise ValueError, not return error string."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="GEMINI_API_KEY"):
                server_module.gemini_analyze_text("test")


class TestAnalyzeCodebase:
    def test_returns_response_text(self):
        """Should return Gemini's analysis on success."""
        mock_response = MagicMock()
        mock_response.text = "Codebase analysis result"

        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}):
            with patch("google.generativeai.GenerativeModel.generate_content",
                       return_value=mock_response):
                result = server_module.gemini_analyze_codebase("code", "review")
        assert result == "Codebase analysis result"

    def test_includes_language_hint(self):
        """Should include language hint in prompt when provided."""
        mock_response = MagicMock()
        mock_response.text = "ok"

        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}):
            with patch("google.generativeai.GenerativeModel.generate_content",
                       return_value=mock_response) as mock_gen:
                server_module.gemini_analyze_codebase("code", "review", language="Python")
                call_args = mock_gen.call_args[0][0]
                assert "Language: Python" in call_args

    def test_api_error_propagates(self):
        """API errors should propagate."""
        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}):
            with patch("google.generativeai.GenerativeModel.generate_content",
                       side_effect=RuntimeError("Server error")):
                with pytest.raises(RuntimeError):
                    server_module.gemini_analyze_codebase("code", "review")


class TestImageAnalysis:
    def test_missing_image_raises_error(self):
        """Should raise FileNotFoundError for non-existent image."""
        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}):
            with pytest.raises(FileNotFoundError):
                server_module.gemini_analyze_image("/nonexistent/path.png", "Describe this")

    def test_unsupported_mime_type_raises(self):
        """Should raise ValueError for unsupported file types."""
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".xyz", delete=False) as f:
            f.write(b"dummy")
            tmp_path = f.name
        try:
            with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}):
                with pytest.raises(ValueError, match="Unsupported file type"):
                    server_module.gemini_analyze_image(tmp_path, "Describe this")
        finally:
            os.unlink(tmp_path)

    def test_oversized_file_raises(self):
        """Should raise ValueError for files exceeding MAX_IMAGE_SIZE."""
        mock_path = MagicMock()
        mock_path.exists.return_value = True
        mock_stat = MagicMock()
        mock_stat.st_size = 25 * 1024 * 1024  # 25 MB
        mock_path.stat.return_value = mock_stat

        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}):
            with patch("gemini_bridge.server.Path", return_value=mock_path):
                with pytest.raises(ValueError, match="File too large"):
                    server_module.gemini_analyze_image("/fake/large.png", "Describe")

    def test_successful_image_analysis(self):
        """Should return analysis for valid image files."""
        import tempfile
        mock_response = MagicMock()
        mock_response.text = "Image shows a dashboard"

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            f.write(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)
            tmp_path = f.name
        try:
            with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}):
                with patch("google.generativeai.GenerativeModel.generate_content",
                           return_value=mock_response):
                    result = server_module.gemini_analyze_image(tmp_path, "Describe")
            assert result == "Image shows a dashboard"
        finally:
            os.unlink(tmp_path)


class TestCompareApproaches:
    def test_returns_comparison(self):
        """Should return Gemini's comparison on success."""
        mock_response = MagicMock()
        mock_response.text = "Approach A is better"

        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}):
            with patch("google.generativeai.GenerativeModel.generate_content",
                       return_value=mock_response):
                result = server_module.gemini_compare_approaches(
                    "scaling", "Redis", "PostgreSQL"
                )
        assert result == "Approach A is better"

    def test_includes_criteria(self):
        """Should include criteria in prompt when provided."""
        mock_response = MagicMock()
        mock_response.text = "ok"

        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}):
            with patch("google.generativeai.GenerativeModel.generate_content",
                       return_value=mock_response) as mock_gen:
                server_module.gemini_compare_approaches(
                    "scaling", "A", "B", criteria="performance, cost"
                )
                call_args = mock_gen.call_args[0][0]
                assert "performance, cost" in call_args

    def test_api_error_propagates(self):
        """API errors should propagate."""
        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}):
            with patch("google.generativeai.GenerativeModel.generate_content",
                       side_effect=RuntimeError("Rate limited")):
                with pytest.raises(RuntimeError):
                    server_module.gemini_compare_approaches("p", "a", "b")


# -- Integration Tests (require GEMINI_API_KEY) -------------------------------

@pytest.mark.skipif(
    not os.environ.get("GEMINI_API_KEY"),
    reason="GEMINI_API_KEY not set -- skipping live API tests"
)
class TestLiveIntegration:
    def test_live_status(self):
        result = server_module.gemini_status()
        assert "operational" in result.lower()

    def test_live_analyze_text(self):
        result = server_module.gemini_analyze_text("Reply with exactly: BRIDGE_TEST_OK")
        assert "BRIDGE_TEST_OK" in result

    def test_live_analyze_codebase(self):
        sample_code = """
def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
"""
        result = server_module.gemini_analyze_codebase(
            code_content=sample_code,
            task="Identify performance issues and suggest improvements",
            language="Python"
        )
        assert len(result) > 50
        assert "recursion" in result.lower() or "memoization" in result.lower()
