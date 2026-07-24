"""
LLM Client Module
Handles authentication, prompt payload transmission, and response parsing for the Google Gemini API.
"""

import json
import re
import google.generativeai as genai
from src.config import config
from src.logger import logger
from src.prompts import SYSTEM_INSTRUCTION, build_resume_analysis_prompt


class LLMError(Exception):
    """Base exception raised for LLM API integration errors."""
    pass


class LLMAuthenticationError(LLMError):
    """Raised when Gemini API authentication fails."""
    pass


class LLMResponseParsingError(LLMError):
    """Raised when Gemini API response cannot be parsed into valid JSON."""
    pass


class GeminiClient:
    """Interface wrapper around Google Gemini Generative API."""

    def __init__(self, api_key: str | None = None, model_name: str | None = None) -> None:
        """
        Initializes the Gemini API client.

        Args:
            api_key: Optional custom API key (defaults to config.GEMINI_API_KEY).
            model_name: Optional custom model identifier (defaults to config.GEMINI_MODEL).
        """
        self.api_key = api_key or config.GEMINI_API_KEY
        self.model_name = model_name or config.GEMINI_MODEL

        if not self.api_key:
            logger.error("GeminiClient initialization failed: GEMINI_API_KEY is missing")
            raise LLMAuthenticationError(
                "Gemini API Key missing. Please configure GEMINI_API_KEY in your .env file."
            )

        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=SYSTEM_INSTRUCTION,
                generation_config={
                    "temperature": 0.2,
                    "response_mime_type": "application/json",
                },
            )
            logger.info(f"Initialized GeminiClient with model: '{self.model_name}'")
        except Exception as e:
            logger.error(f"Failed to configure Gemini API client: {str(e)}", exc_info=True)
            raise LLMAuthenticationError(f"Gemini API configuration failure: {str(e)}") from e

    def analyze_resume(
        self,
        resume_text: str,
        target_role: str = "",
        job_description: str = "",
    ) -> dict:
        """
        Transmits extracted resume text and optional JD to Gemini API and returns structured JSON analysis.

        Args:
            resume_text: Sanitized text content from resume.
            target_role: Optional target job title.
            job_description: Optional target job description text.

        Returns:
            dict: Structured resume analysis containing scores, skills, strengths, suggestions, and JD match metrics.

        Raises:
            LLMError: If network or generation fails.
            LLMResponseParsingError: If response JSON is invalid.
        """
        if not resume_text or not resume_text.strip():
            raise LLMError("Cannot analyze empty resume text.")

        prompt = build_resume_analysis_prompt(resume_text, target_role, job_description)
        logger.info("Sending resume analysis request to Gemini API...")

        try:
            response = self.model.generate_content(prompt)
            raw_text = response.text
            logger.debug(f"Raw response from Gemini: {raw_text[:200]}...")

            parsed_json = self._parse_json_response(raw_text)
            self._validate_schema(parsed_json)
            logger.info("Successfully received and validated structured resume analysis from Gemini.")
            return parsed_json

        except LLMResponseParsingError:
            raise
        except Exception as e:
            logger.error(f"Gemini API execution error: {str(e)}", exc_info=True)
            raise LLMError(f"Gemini API execution failed: {str(e)}") from e

    def _parse_json_response(self, raw_text: str) -> dict:
        """Strips markdown code fences if present and parses text into a dictionary."""
        cleaned_text = raw_text.strip()

        # Remove markdown ```json or ``` code fences if model returned them
        if cleaned_text.startswith("```"):
            cleaned_text = re.sub(r"^```(?:json)?\n?", "", cleaned_text)
            cleaned_text = re.sub(r"\n?```$", "", cleaned_text).strip()

        try:
            return json.loads(cleaned_text)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON from LLM response: {cleaned_text}")
            raise LLMResponseParsingError(f"LLM returned invalid JSON output: {str(e)}") from e

    def _validate_schema(self, data: dict) -> None:
        """Verifies that all required top-level JSON keys exist in the response."""
        required_keys = [
            "ats_score",
            "summary",
            "technical_skills",
            "soft_skills",
            "missing_skills",
            "strengths",
            "weaknesses",
            "improvement_suggestions",
            "jd_match_score",
            "matching_keywords",
            "missing_jd_keywords",
            "jd_tailored_suggestions",
        ]
        missing = [k for k in required_keys if k not in data]
        if missing:
            logger.warning(f"Response missing required keys: {missing}")
            # Ensure defaults for missing keys to prevent UI breakage
            for key in missing:
                if key in ("ats_score", "jd_match_score"):
                    data[key] = 0
                elif key == "summary":
                    data[key] = "N/A"
                else:
                    data[key] = []
