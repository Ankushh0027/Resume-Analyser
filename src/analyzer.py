"""
Resume Analyzer Module
High-level service orchestrator connecting document parsing and LLM evaluation.
"""

from src.parser import ResumeParser, ParsingError
from src.llm import GeminiClient, LLMError
from src.logger import logger


class AnalysisError(Exception):
    """Custom exception raised when the overall analysis workflow fails."""
    pass


class ResumeAnalyzer:
    """
    Facade orchestrator class that coordinates file parsing and Gemini AI evaluation.
    Follows Dependency Injection principles for parser and LLM client.
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
    ) -> dict:
        """
        Orchestrates full resume parsing and Gemini AI analysis pipeline.

        Args:
            file_source: File path or raw byte stream of the resume.
            filename: Original file name (used for extension detection).
            target_role: Optional target job role/title.

        Returns:
            dict: Comprehensive analysis result containing metadata, scores, skills, and suggestions.

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

        # Step 2: LLM Inference & Structured Evaluation
        try:
            analysis_result = self.llm_client.analyze_resume(
                resume_text=extracted_text,
                target_role=target_role,
            )
        except LLMError as e:
            logger.error(f"Analysis failed at LLM evaluation phase: {str(e)}")
            raise AnalysisError(f"AI evaluation error: {str(e)}") from e

        # Step 3: Enrich Result with Document Metadata
        analysis_result["meta"] = {
            "filename": filename,
            "char_count": len(extracted_text),
            "target_role": target_role if target_role else "General Software / Tech",
        }

        logger.info(f"Analysis workflow completed successfully for '{filename}'.")
        return analysis_result
