"""
Resume Analyzer Module
High-level SaaS service orchestrator connecting document parsing, AI evaluation, usage limits, and database history.
"""

import hashlib
from typing import Any
from src.parser import ResumeParser, ParsingError
from src.services.ai_service import AIService, AIServiceError
from src.database import save_analysis_history
from src.logger import logger


class AnalysisError(Exception):
    """Custom exception raised when the overall analysis workflow fails."""
    pass


# Global in-memory cache to prevent duplicate API requests for identical resumes/inputs
_ANALYSIS_CACHE: dict[str, dict] = {}


class ResumeAnalyzer:
    """
    SaaS Facade orchestrator class coordinating file parsing, AI provider evaluation,
    and persistent database history logging.
    """

    def __init__(
        self,
        parser: ResumeParser | None = None,
        ai_service: AIService | None = None,
    ) -> None:
        self.parser = parser or ResumeParser()
        self.ai_service = ai_service or AIService()
        logger.info("ResumeAnalyzer SaaS service initialized successfully.")

    def analyze(
        self,
        file_source: str | bytes,
        filename: str,
        target_role: str = "",
        job_description: str = "",
        user: dict[str, Any] | None = None,
        preferred_model: str | None = None,
    ) -> dict:
        """
        Orchestrates full resume parsing, AI evaluation, and database history persistence.
        """
        logger.info(f"Starting analysis workflow for file: '{filename}'")

        # Step 1: Text Extraction & Sanitization
        try:
            extracted_text = self.parser.parse_file(file_source, filename)
        except ParsingError as e:
            logger.error(f"Analysis failed at document parsing phase: {str(e)}")
            raise AnalysisError(f"Document parsing error: {str(e)}") from e

        # Compute Content MD5 Hash for Caching
        cache_raw = f"{extracted_text}:{target_role.strip().lower()}:{job_description.strip().lower()}"
        cache_key = hashlib.md5(cache_raw.encode("utf-8")).hexdigest()

        if cache_key in _ANALYSIS_CACHE:
            logger.info(f"Serving cached analysis for key '{cache_key}' (0 API tokens consumed)")
            cached_result = dict(_ANALYSIS_CACHE[cache_key])
            cached_result["meta"]["cached"] = True
            cached_result["meta"]["filename"] = filename
            return cached_result

        # Step 2: AI Provider Routing & Evaluation
        from src.prompts import build_resume_analysis_prompt
        prompt = build_resume_analysis_prompt(extracted_text, target_role, job_description)

        try:
            analysis_result, provider_used, model_used, exec_time_ms, request_id = (
                self.ai_service.execute_ai_completion(prompt, preferred_model=preferred_model)
            )
        except AIServiceError as e:
            logger.error(f"Analysis failed at AI evaluation phase: {str(e)}")
            raise AnalysisError(str(e)) from e

        # Step 3: Enrich Result with Document Metadata
        has_jd = bool(job_description and job_description.strip())
        analysis_result["meta"] = {
            "filename": filename,
            "char_count": len(extracted_text),
            "target_role": target_role if target_role else "General Software / Tech",
            "has_jd": has_jd,
            "cached": False,
            "provider_used": provider_used,
            "model_used": model_used,
            "execution_time_ms": exec_time_ms,
            "request_id": request_id,
        }

        # Store in global in-memory cache for deterministic consistency
        _ANALYSIS_CACHE[cache_key] = analysis_result

        # Step 4: Persist in Database History if user logged in
        if user and "id" in user:
            try:
                save_analysis_history(
                    user_id=user["id"],
                    request_id=request_id,
                    filename=filename,
                    target_role=target_role,
                    has_jd=has_jd,
                    extracted_text=extracted_text,
                    result_dict=analysis_result,
                    provider_used=provider_used,
                    model_used=model_used,
                    execution_time_ms=exec_time_ms,
                )
            except Exception as e:
                logger.error(f"Failed to persist analysis history: {str(e)}")

        # Store in cache
        _ANALYSIS_CACHE[cache_key] = analysis_result

        logger.info(f"Analysis workflow completed successfully for '{filename}' via '{provider_used}'.")
        return analysis_result

    def generate_cover_letter(
        self,
        file_source: str | bytes,
        filename: str,
        target_role: str = "",
        job_description: str = "",
    ) -> dict:
        """Parses file and generates a tailored Cover Letter via AI Service."""
        from src.prompts import build_cover_letter_prompt
        extracted_text = self.parser.parse_file(file_source, filename)
        prompt = build_cover_letter_prompt(extracted_text, target_role, job_description)
        result, _, _, _, _ = self.ai_service.execute_ai_completion(prompt)
        return result

    def enhance_bullet_point(self, bullet_text: str, target_role: str = "") -> dict:
        """Enhances weak bullet point into 3 quantified action bullet points."""
        from src.prompts import build_bullet_enhancer_prompt
        prompt = build_bullet_enhancer_prompt(bullet_text, target_role)
        result, _, _, _, _ = self.ai_service.execute_ai_completion(prompt)
        return result

    def predict_interview_questions(
        self,
        file_source: str | bytes,
        filename: str,
        target_role: str = "",
        job_description: str = "",
    ) -> dict:
        """Parses file and predicts 10 targeted interview questions."""
        from src.prompts import build_interview_predictor_prompt
        extracted_text = self.parser.parse_file(file_source, filename)
        prompt = build_interview_predictor_prompt(extracted_text, target_role, job_description)
        result, _, _, _, _ = self.ai_service.execute_ai_completion(prompt)
        return result

    def compare_resumes(
        self,
        file_source_a: str | bytes,
        filename_a: str,
        file_source_b: str | bytes,
        filename_b: str,
        target_role: str = "",
        job_description: str = "",
        user: dict[str, Any] | None = None,
    ) -> dict:
        """Parses 2 resumes and compares ATS compatibility scores side-by-side."""
        res_a = self.analyze(file_source_a, filename_a, target_role, job_description, user=user)
        res_b = self.analyze(file_source_b, filename_b, target_role, job_description, user=user)
        return {
            "resume_a": res_a,
            "resume_b": res_b,
            "winner": "resume_a" if res_a.get("ats_score", 0) >= res_b.get("ats_score", 0) else "resume_b",
        }

    def generate_outreach(
        self,
        file_source: str | bytes,
        filename: str,
        target_role: str = "",
        company_name: str = "",
        job_description: str = "",
    ) -> dict:
        """Parses file and generates recruiter outreach emails."""
        from src.prompts import build_outreach_prompt
        extracted_text = self.parser.parse_file(file_source, filename)
        prompt = build_outreach_prompt(extracted_text, target_role, company_name, job_description)
        result, _, _, _, _ = self.ai_service.execute_ai_completion(prompt)
        return result

    def estimate_salary(
        self,
        file_source: str | bytes,
        filename: str,
        target_role: str = "",
        target_location: str = "United States (USD $)",
        company_tier: str = "Mid-Size IT Enterprise",
    ) -> dict:
        """Parses file and estimates compensation ranges adjusted for region and company tier."""
        from src.prompts import build_salary_estimation_prompt
        extracted_text = self.parser.parse_file(file_source, filename)
        prompt = build_salary_estimation_prompt(extracted_text, target_role, target_location, company_tier)
        result, _, _, _, _ = self.ai_service.execute_ai_completion(prompt)
        return result
