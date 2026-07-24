"""
Unit Tests for ResumeAnalyzer SaaS Orchestrator
"""

import unittest
from unittest.mock import MagicMock
from src.analyzer import ResumeAnalyzer, AnalysisError
from src.parser import ParsingError
from src.services.ai_service import AIServiceError


class TestResumeAnalyzer(unittest.TestCase):
    """Test suite for ResumeAnalyzer SaaS facade class."""

    def setUp(self):
        self.mock_parser = MagicMock()
        self.mock_ai_service = MagicMock()
        self.analyzer = ResumeAnalyzer(
            parser=self.mock_parser,
            ai_service=self.mock_ai_service,
        )

    def test_successful_analysis_workflow(self):
        """Verify successful orchestration flow from text parsing to AI result enrichment."""
        self.mock_parser.parse_file.return_value = "John Doe Python Developer text"
        self.mock_ai_service.execute_ai_completion.return_value = (
            {
                "ats_score": 90,
                "summary": "Great candidate",
                "technical_skills": ["Python"],
                "soft_skills": ["Communication"],
                "missing_skills": [],
                "strengths": ["Strong coding"],
                "weaknesses": [],
                "improvement_suggestions": [],
            },
            "Google Gemini",
            "gemini-2.5-flash",
            120,
            "req_test123",
        )

        result = self.analyzer.analyze(b"fake data", "resume.pdf", "Python Engineer")

        self.assertEqual(result["ats_score"], 90)
        self.assertEqual(result["meta"]["filename"], "resume.pdf")
        self.assertEqual(result["meta"]["target_role"], "Python Engineer")
        self.assertEqual(result["meta"]["char_count"], 30)
        self.assertFalse(result["meta"]["has_jd"])
        self.assertEqual(result["meta"]["provider_used"], "Google Gemini")

    def test_job_description_analysis_workflow(self):
        """Verify orchestration flow when job_description is provided."""
        self.mock_parser.parse_file.return_value = "Python developer resume text"
        self.mock_ai_service.execute_ai_completion.return_value = (
            {
                "ats_score": 88,
                "summary": "Fit candidate",
                "technical_skills": ["Python"],
                "soft_skills": [],
                "missing_skills": [],
                "strengths": [],
                "weaknesses": [],
                "improvement_suggestions": [],
                "jd_match_score": 92,
                "matching_keywords": ["Python", "FastAPI"],
                "missing_jd_keywords": ["Docker"],
                "jd_tailored_suggestions": ["Mention Docker projects"],
            },
            "Google Gemini",
            "gemini-2.5-flash",
            150,
            "req_test456",
        )

        result = self.analyzer.analyze(
            b"fake data",
            "resume.pdf",
            "Python Dev",
            job_description="Seeking Python Developer with Docker",
        )

        self.assertTrue(result["meta"]["has_jd"])
        self.assertEqual(result["jd_match_score"], 92)

    def test_parser_failure_raises_analysis_error(self):
        """Verify that ParsingError is wrapped in AnalysisError."""
        self.mock_parser.parse_file.side_effect = ParsingError("Corrupted file")
        with self.assertRaises(AnalysisError):
            self.analyzer.analyze(b"corrupted", "bad.pdf")

    def test_ai_service_failure_raises_analysis_error(self):
        """Verify that AIServiceError is wrapped in AnalysisError."""
        self.mock_parser.parse_file.return_value = "Valid text"
        self.mock_ai_service.execute_ai_completion.side_effect = AIServiceError("AI service busy")
        with self.assertRaises(AnalysisError):
            self.analyzer.analyze(b"valid", "good.pdf")


if __name__ == "__main__":
    unittest.main()
