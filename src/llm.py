"""
LLM Client Module
Handles authentication, prompt payload transmission, model fallbacks, and response parsing for the Google Gemini API.
"""

import json
import re
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted, GoogleAPICallError
from src.config import config
from src.logger import logger
from src.prompts import SYSTEM_INSTRUCTION, build_resume_analysis_prompt


class LLMError(Exception):
    """Base exception raised for LLM API integration errors."""
    pass


class LLMAuthenticationError(LLMError):
    """Raised when Gemini API authentication fails."""
    pass


class LLMQuotaExhaustedError(LLMError):
    """Raised when Gemini API daily or minute quota limit is reached."""
    pass


class LLMResponseParsingError(LLMError):
    """Raised when Gemini API response cannot be parsed into valid JSON."""
    pass


class GeminiClient:
    """Interface wrapper around Google Gemini Generative API with model fallback support."""

    FALLBACK_MODELS = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash-latest"]

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
            self._create_model_instance(self.model_name)
            logger.info(f"Initialized GeminiClient with model: '{self.model_name}'")
        except Exception as e:
            logger.error(f"Failed to configure Gemini API client: {str(e)}", exc_info=True)
            raise LLMAuthenticationError(f"Gemini API configuration failure: {str(e)}") from e

    def _create_model_instance(self, model_name: str) -> None:
        """Creates a GenerativeModel instance for the specified model name."""
        self.model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=SYSTEM_INSTRUCTION,
            generation_config={
                "temperature": 0.0,
                "response_mime_type": "application/json",
            },
        )
        self.active_model_name = model_name

    def analyze_resume(
        self,
        resume_text: str,
        target_role: str = "",
        job_description: str = "",
    ) -> dict:
        """
        Transmits extracted resume text and optional JD to Gemini API and returns structured JSON analysis.
        Implements automatic fallback across available Gemini models if quota limits are encountered.

        Args:
            resume_text: Sanitized text content from resume.
            target_role: Optional target job title.
            job_description: Optional target job description text.

        Returns:
            dict: Structured resume analysis containing scores, skills, strengths, suggestions, and JD match metrics.

        Raises:
            LLMQuotaExhaustedError: If all candidate models exhaust quota.
            LLMError: If network or generation fails.
            LLMResponseParsingError: If response JSON is invalid.
        """
        if not resume_text or not resume_text.strip():
            raise LLMError("Cannot analyze empty resume text.")

        prompt = build_resume_analysis_prompt(resume_text, target_role, job_description)
        logger.info("Sending resume analysis request to Gemini API...")

        # Model Fallback Loop with auto-retry on 429
        candidate_models = [self.model_name] + [m for m in self.FALLBACK_MODELS if m != self.model_name]

        for model_candidate in candidate_models:
            for attempt in range(2):  # Try twice per model with 3s backoff delay
                try:
                    if self.active_model_name != model_candidate:
                        logger.info(f"Attempting model fallback to: '{model_candidate}'")
                        self._create_model_instance(model_candidate)

                    response = self.model.generate_content(prompt)
                    raw_text = response.text
                    logger.debug(f"Raw response from Gemini ({model_candidate}): {raw_text[:200]}...")

                    parsed_json = self._parse_json_response(raw_text)
                    self._validate_schema(parsed_json)
                    logger.info(f"Successfully received and validated structured analysis from '{model_candidate}'.")
                    return parsed_json

                except (ResourceExhausted, GoogleAPICallError, Exception) as e:
                    err_str = str(e).upper()
                    if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str or "QUOTA" in err_str or "RATE" in err_str:
                        if attempt == 0:
                            logger.warning(f"Rate limit hit on '{model_candidate}'. Waiting 3 seconds before auto-retry...")
                            import time
                            time.sleep(3)
                            continue
                    elif "404" in err_str or "NOT_FOUND" in err_str:
                        logger.warning(f"Model '{model_candidate}' not found (404). Skipping to next candidate...")
                        break
                    else:
                        logger.error(f"Gemini API execution error on '{model_candidate}': {str(e)}")
                        break

        # If loop finishes without returning, all models & retries failed
        raise LLMQuotaExhaustedError(
            "Gemini API minute/daily quota limit reached. "
            "Please wait 30 seconds and try again, or paste your custom free API key from Google AI Studio in the sidebar to bypass immediately."
        )

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
            "score_breakdown",
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
                if key == "score_breakdown":
                    data[key] = {
                        "structure_formatting": 0,
                        "technical_skills": 0,
                        "quantifiable_results": 0,
                        "experience_fit": 0,
                    }
                elif key in ("ats_score", "jd_match_score"):
                    data[key] = 0
                elif key == "summary":
                    data[key] = "N/A"
                else:
                    data[key] = []

        # Enforce exact mathematical sum if breakdown exists
        if isinstance(data.get("score_breakdown"), dict):
            breakdown = data["score_breakdown"]
            calculated_sum = sum(int(v) for v in breakdown.values() if isinstance(v, (int, float)))
            if calculated_sum > 0:
                data["ats_score"] = calculated_sum

    def generate_cover_letter(
        self,
        resume_text: str,
        target_role: str = "",
        job_description: str = "",
    ) -> dict:
        """Generates a customized, professional 3-paragraph Cover Letter."""
        from src.prompts import build_cover_letter_prompt
        prompt = build_cover_letter_prompt(resume_text, target_role, job_description)
        logger.info("Generating Cover Letter with Gemini API...")
        try:
            response = self.model.generate_content(prompt)
            return self._parse_json_response(response.text)
        except Exception as e:
            logger.error(f"Cover Letter generation error: {str(e)}")
            raise LLMError(f"Cover Letter generation failed: {str(e)}") from e

    def enhance_bullet_point(self, bullet_text: str, target_role: str = "") -> dict:
        """Rewrites a weak bullet point into 3 high-impact quantified achievements."""
        from src.prompts import build_bullet_enhancer_prompt
        prompt = build_bullet_enhancer_prompt(bullet_text, target_role)
        logger.info("Enhancing bullet point with Gemini API...")
        try:
            response = self.model.generate_content(prompt)
            return self._parse_json_response(response.text)
        except Exception as e:
            logger.error(f"Bullet point enhancement error: {str(e)}")
            raise LLMError(f"Bullet enhancement failed: {str(e)}") from e

    def predict_interview_questions(
        self,
        resume_text: str,
        target_role: str = "",
        job_description: str = "",
    ) -> dict:
        """Predicts targeted technical & STAR behavioral interview questions."""
        from src.prompts import build_interview_predictor_prompt
        prompt = build_interview_predictor_prompt(resume_text, target_role, job_description)
        logger.info("Predicting interview questions with Gemini API...")
        try:
            response = self.model.generate_content(prompt)
            return self._parse_json_response(response.text)
        except Exception as e:
            logger.error(f"Interview prediction error: {str(e)}")
            raise LLMError(f"Interview prediction failed: {str(e)}") from e
