"""
Resume Analyzer Module
High-level service orchestrator connecting document parsing and LLM evaluation with caching.
"""

import hashlib
from src.parser import ResumeParser, ParsingError
from src.llm import GeminiClient, LLMError, LLMQuotaExhaustedError
from src.logger import logger


class AnalysisError(Exception):
    """Custom exception raised when the overall analysis workflow fails."""
    pass


# Global in-memory cache to prevent duplicate API requests for identical resumes/inputs
_ANALYSIS_CACHE: dict[str, dict] = {}


class ResumeAnalyzer:
    """
    Facade orchestrator class that coordinates file parsing and Gemini AI evaluation.
    Follows Dependency Injection principles and implements content-hash caching.
    """

    def __init__(
        self,
        parser: ResumeParser | None = None,
        llm_client: GeminiClient | None = None,
    ) -> None:
        """
        Initializes ResumeAnalyzer with optional parser and LLM client dependencies.

        Args:
            parser: Optional ResumeParser instance.
            llm_client: Optional GeminiClient instance.
        """
        self.parser = parser or ResumeParser()
        self.llm_client = llm_client or GeminiClient()
        logger.info("ResumeAnalyzer service initialized successfully.")

    def analyze(
        self,
        file_source: str | bytes,
        filename: str,
        target_role: str = "",
        job_description: str = "",
    ) -> dict:
        """
        Orchestrates full resume parsing and Gemini AI analysis pipeline with caching.

        Args:
            file_source: File path or raw byte stream of the resume.
            filename: Original file name (used for extension detection).
            target_role: Optional target job role/title.
            job_description: Optional target job description text for match analysis.

        Returns:
            dict: Comprehensive analysis result containing metadata, scores, skills, suggestions, and JD metrics.

        Raises:
            AnalysisError: High-level error if parsing or LLM evaluation fails.
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

        # Step 2: LLM Inference & Structured Evaluation
        try:
            analysis_result = self.llm_client.analyze_resume(
                resume_text=extracted_text,
                target_role=target_role,
                job_description=job_description,
            )
        except LLMQuotaExhaustedError as e:
            logger.error(f"Analysis failed due to quota limit: {str(e)}")
            raise AnalysisError(f"API Quota Limit: {str(e)}") from e
        except LLMError as e:
            logger.error(f"Analysis failed at LLM evaluation phase: {str(e)}")
            raise AnalysisError(f"AI evaluation error: {str(e)}") from e

        # Step 3: Enrich Result with Document Metadata
        analysis_result["meta"] = {
            "filename": filename,
            "char_count": len(extracted_text),
            "target_role": target_role if target_role else "General Software / Tech",
            "has_jd": bool(job_description and job_description.strip()),
            "cached": False,
        }

        # Store in cache
        _ANALYSIS_CACHE[cache_key] = analysis_result

        logger.info(f"Analysis workflow completed successfully for '{filename}'.")
        return analysis_result
