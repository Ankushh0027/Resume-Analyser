"""
Unit Tests for ResumeAnalyzer Orchestrator
"""

import unittest
from unittest.mock import MagicMock
from src.analyzer import ResumeAnalyzer, AnalysisError
from src.parser import ParsingError
from src.llm import LLMError


class TestResumeAnalyzer(unittest.TestCase):
    """Test suite for ResumeAnalyzer facade class."""

    def setUp(self):
        self.mock_parser = MagicMock()
        self.mock_llm = MagicMock()
        self.analyzer = ResumeAnalyzer(
            parser=self.mock_parser,
            llm_client=self.mock_llm,
        )

    def test_successful_analysis_workflow(self):
        """Verify successful orchestration flow from text parsing to LLM result enrichment."""
        self.mock_parser.parse_file.return_value = "John Doe Python Developer text"
        self.mock_llm.analyze_resume.return_value = {
            "ats_score": 90,
            "summary": "Great candidate",
            "technical_skills": ["Python"],
            "soft_skills": ["Communication"],
            "missing_skills": [],
            "strengths": ["Strong coding"],
            "weaknesses": [],
            "improvement_suggestions": [],
        }

        result = self.analyzer.analyze(b"fake data", "resume.pdf", "Python Engineer")

        self.assertEqual(result["ats_score"], 90)
        self.assertEqual(result["meta"]["filename"], "resume.pdf")
        self.assertEqual(result["meta"]["target_role"], "Python Engineer")
        self.assertEqual(result["meta"]["char_count"], 30)

    def test_parser_failure_raises_analysis_error(self):
        """Verify that ParsingError is wrapped in AnalysisError."""
        self.mock_parser.parse_file.side_effect = ParsingError("Corrupted file")
        with self.assertRaises(AnalysisError):
            self.analyzer.analyze(b"corrupted", "bad.pdf")

    def test_llm_failure_raises_analysis_error(self):
        """Verify that LLMError is wrapped in AnalysisError."""
        self.mock_parser.parse_file.return_value = "Valid text"
        self.mock_llm.analyze_resume.side_effect = LLMError("API rate limit")
        with self.assertRaises(AnalysisError):
            self.analyzer.analyze(b"valid", "good.pdf")


if __name__ == "__main__":
    unittest.main()
