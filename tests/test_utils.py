"""
Unit Tests for Utility Functions Module
"""

import unittest
import json
from src.utils import generate_text_report, generate_json_report, clean_text


class TestUtils(unittest.TestCase):
    """Test suite for utility helper functions."""

    def setUp(self):
        self.sample_analysis = {
            "ats_score": 85,
            "summary": "Experienced Python Engineer",
            "technical_skills": ["Python", "Streamlit"],
            "soft_skills": ["Leadership"],
            "missing_skills": ["Docker"],
            "strengths": ["Strong coding experience"],
            "weaknesses": ["Lack of cloud certs"],
            "improvement_suggestions": ["Add AWS cert"],
            "meta": {
                "filename": "john_doe_resume.pdf",
                "char_count": 1500,
                "target_role": "Python Developer",
                "has_jd": True,
            },
            "jd_match_score": 90,
            "matching_keywords": ["Python"],
            "missing_jd_keywords": ["FastAPI"],
            "jd_tailored_suggestions": ["Highlight API projects"],
        }

    def test_clean_text_sanitizes_non_breaking_spaces(self):
        """Verify non-breaking space replacement."""
        raw = "Hello\xa0World\n\n\nTest"
        cleaned = clean_text(raw)
        self.assertEqual(cleaned, "Hello World\n\nTest")

    def test_clean_text_strips_dividers_and_page_headers(self):
        """Verify clean_text strips decorative dividers, page number artifacts, and standardizes bullets."""
        raw = """
========================================
ALEXANDER PIERCE
Page 1 of 3
----------------------------------------
• Developed microservices using Python
► Optimized SQL queries
Page 2
****************************************
"""
        cleaned = clean_text(raw)
        self.assertNotIn("========================================", cleaned)
        self.assertNotIn("----------------------------------------", cleaned)
        self.assertNotIn("Page 1 of 3", cleaned)
        self.assertNotIn("Page 2", cleaned)
        self.assertIn("- Developed microservices using Python", cleaned)
        self.assertIn("- Optimized SQL queries", cleaned)

    def test_clean_text_truncates_long_input(self):
        """Verify clean_text caps character length when exceeding max_chars."""
        raw = "Word " * 2000
        cleaned = clean_text(raw, max_chars=100)
        self.assertLessEqual(len(cleaned), 160)
        self.assertIn("[...Text Truncated for Token Efficiency...]", cleaned)

    def test_generate_json_report_returns_valid_json(self):
        """Verify json report generator returns parseable JSON."""
        output_json = generate_json_report(self.sample_analysis)
        parsed = json.loads(output_json)
        self.assertEqual(parsed["ats_score"], 85)
        self.assertEqual(parsed["meta"]["filename"], "john_doe_resume.pdf")

    def test_generate_text_report_includes_key_sections(self):
        """Verify text report contains all summary sections."""
        report = generate_text_report(self.sample_analysis)
        self.assertIn("AI RESUME EVALUATION REPORT", report)
        self.assertIn("john_doe_resume.pdf", report)
        self.assertIn("ATS Score     : 85/100", report)
        self.assertIn("Experienced Python Engineer", report)
        self.assertIn("JD Match Score        : 90%", report)


if __name__ == "__main__":
    unittest.main()
