"""
Unit Tests for Gemini Client Module
"""

import unittest
from unittest.mock import MagicMock, patch
from src.llm import GeminiClient, LLMAuthenticationError, LLMResponseParsingError


class TestGeminiClient(unittest.TestCase):
    """Test suite for GeminiClient."""

    def test_missing_api_key_raises_error(self):
        """Verify error when API key is missing across all providers."""
        with patch("src.llm.config.GEMINI_API_KEY", ""), \
             patch("src.llm.config.OPENROUTER_API_KEY", ""), \
             patch("src.llm.config.OPENAI_API_KEY", ""):
            with self.assertRaises(LLMAuthenticationError):
                GeminiClient(api_key="", openrouter_api_key="", openai_api_key="")

    def test_json_parsing_cleans_markdown_fences(self):
        """Verify _parse_json_response strips markdown code fences."""
        client = GeminiClient(api_key="fake_key")
        raw_markdown = """```json
{
  "ats_score": 85,
  "summary": "Experienced Developer",
  "technical_skills": ["Python"],
  "soft_skills": ["Leadership"],
  "missing_skills": ["Docker"],
  "strengths": ["Strong Python background"],
  "weaknesses": ["Lack of cloud certs"],
  "improvement_suggestions": ["Add AWS cert"]
}
```"""
        result = client._parse_json_response(raw_markdown)
        self.assertEqual(result["ats_score"], 85)
        self.assertEqual(result["technical_skills"], ["Python"])

    def test_provider_detection(self):
        """Verify model string provider detection."""
        client = GeminiClient(api_key="fake_key")
        self.assertEqual(client._detect_provider("gemini-1.5-flash"), "gemini")
        self.assertEqual(client._detect_provider("meta-llama/llama-3.3-70b-instruct:free"), "openrouter")
        self.assertEqual(client._detect_provider("gpt-4o-mini"), "openai")

    def test_rate_limiter_acquires_tokens(self):
        """Verify RateLimiter acquires tokens without error."""
        from src.llm import RateLimiter
        limiter = RateLimiter(requests_per_minute=60)
        limiter.acquire()
        self.assertEqual(len(limiter.timestamps), 1)

    def test_retry_with_backoff_retries_on_transient_error(self):
        """Verify call_with_retry retries on transient errors and succeeds."""
        from src.llm import call_with_retry
        mock_func = MagicMock(side_effect=[Exception("429 Rate limit"), "Success"])
        res = call_with_retry(mock_func, max_retries=2, initial_delay=0.01)
        self.assertEqual(res, "Success")
        self.assertEqual(mock_func.call_count, 2)


if __name__ == "__main__":
    unittest.main()
