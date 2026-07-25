"""
LLM Client Adapter Module
Provides backward compatible client wrappers using the server-side AIService provider engine.
"""

from typing import Any
from src.services.ai_service import AIService, AIServiceError
from src.logger import logger


class LLMError(Exception):
    """Base exception raised for LLM API integration errors."""
    pass


class LLMAuthenticationError(LLMError):
    """Raised when server-side LLM authentication is missing."""
    pass


class LLMQuotaExhaustedError(LLMError):
    """Raised when API daily or minute quota limit is reached across all providers."""
    pass


class LLMResponseParsingError(LLMError):
    """Raised when LLM API response cannot be parsed into valid JSON."""
    pass


class MultiProviderLLMClient:
    """
    SaaS Adapter wrapping server-side AIService.
    Does NOT require frontend or user API keys.
    """

    def __init__(
        self,
        api_key: str | None = None,
        model_name: str | None = None,
        openrouter_api_key: str | None = None,
        openai_api_key: str | None = None,
    ) -> None:
        self.ai_service = AIService()
        self.model_name = model_name

    def analyze(self, resume_text: str, target_role: str = "", job_description: str = "", *args: Any, **kwargs: Any) -> dict:
        """Analyzes resume text using server-side AIService."""
        from src.prompts import build_resume_analysis_prompt
        prompt = build_resume_analysis_prompt(resume_text, target_role, job_description)
        pref_model = kwargs.get("preferred_model", self.model_name)
        try:
            result, _, _, _, _ = self.ai_service.execute_ai_completion(prompt, preferred_model=pref_model)
            return result
        except AIServiceError as e:
            raise LLMError(str(e)) from e

    def analyze_resume(self, resume_text: str, target_role: str = "", job_description: str = "", *args: Any, **kwargs: Any) -> dict:
        return self.analyze(resume_text, target_role, job_description, *args, **kwargs)

    def generate_cover_letter(self, resume_text: str, target_role: str = "", job_description: str = "", *args: Any, **kwargs: Any) -> dict:
        from src.prompts import build_cover_letter_prompt
        prompt = build_cover_letter_prompt(resume_text, target_role, job_description)
        pref_model = kwargs.get("preferred_model", self.model_name)
        result, _, _, _, _ = self.ai_service.execute_ai_completion(prompt, preferred_model=pref_model)
        return result

    def enhance_bullet_point(self, bullet_text: str, target_role: str = "", *args: Any, **kwargs: Any) -> dict:
        from src.prompts import build_bullet_enhancer_prompt
        prompt = build_bullet_enhancer_prompt(bullet_text, target_role)
        pref_model = kwargs.get("preferred_model", self.model_name)
        result, _, _, _, _ = self.ai_service.execute_ai_completion(prompt, preferred_model=pref_model)
        return result

    def predict_interview_questions(self, resume_text: str, target_role: str = "", job_description: str = "", *args: Any, **kwargs: Any) -> dict:
        from src.prompts import build_interview_predictor_prompt
        prompt = build_interview_predictor_prompt(resume_text, target_role, job_description)
        pref_model = kwargs.get("preferred_model", self.model_name)
        result, _, _, _, _ = self.ai_service.execute_ai_completion(prompt, preferred_model=pref_model)
        return result

    def generate_outreach(self, resume_text: str, target_role: str = "", company_name: str = "", job_description: str = "", *args: Any, **kwargs: Any) -> dict:
        from src.prompts import build_outreach_prompt
        prompt = build_outreach_prompt(resume_text, target_role, company_name, job_description)
        pref_model = kwargs.get("preferred_model", self.model_name)
        result, _, _, _, _ = self.ai_service.execute_ai_completion(prompt, preferred_model=pref_model)
        return result

    def estimate_salary(self, resume_text: str, target_role: str = "", *args: Any, **kwargs: Any) -> dict:
        from src.prompts import build_salary_estimation_prompt
        prompt = build_salary_estimation_prompt(resume_text, target_role)
        pref_model = kwargs.get("preferred_model", self.model_name)
        result, _, _, _, _ = self.ai_service.execute_ai_completion(prompt, preferred_model=pref_model)
        return result


class GeminiClient(MultiProviderLLMClient):
    """Backward compatible subclass wrapper for GeminiClient."""
    pass
