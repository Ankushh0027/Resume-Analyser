"""
Unit Tests for Gemini Client Module
"""

import unittest
from unittest.mock import MagicMock, patch
from src.llm import GeminiClient, LLMAuthenticationError, LLMResponseParsingError


class TestGeminiClient(unittest.TestCase):
    """Test suite for GeminiClient."""

    def test_missing_api_key_raises_error(self):
        """Verify error when API key is missing."""
        with patch("src.llm.config.GEMINI_API_KEY", ""):
            with self.assertRaises(LLMAuthenticationError):
                GeminiClient(api_key="")

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


if __name__ == "__main__":
    unittest.main()
