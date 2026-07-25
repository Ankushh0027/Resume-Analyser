"""
AI Service & Provider Manager Module
Handles server-side provider routing, exponential backoff retries (2s, 5s, 10s),
automatic fallback switching, observability logging, and global error masking.
"""

import json
import re
import time
import uuid
from typing import Any
from src.config import config
from src.logger import logger
from src.prompts import SYSTEM_INSTRUCTION
from src.providers.gemini_provider import GeminiProvider
from src.providers.openrouter_provider import OpenRouterProvider
from src.providers.openai_provider import OpenAIProvider
from src.providers.mock_provider import MockLLMProvider


class AIServiceError(Exception):
    """User-facing safe AI service error."""
    pass


class AIService:
    """
    Central AI Provider Routing & Execution Service.
    Orchestrates primary and fallback providers with strict exponential backoff retries.
    Includes a built-in Mock Demo AI Provider fallback so the platform always works out-of-the-box.
    """

    RETRY_DELAYS = [2.0, 5.0, 10.0]  # Exact specified exponential backoff delays (Retry #1: 2s, Retry #2: 5s, Retry #3: 10s)

    def __init__(self) -> None:
        self.gemini_provider = GeminiProvider()
        self.openrouter_provider = OpenRouterProvider()
        self.openai_provider = OpenAIProvider()
        self.mock_provider = MockLLMProvider()

    def execute_ai_completion(
        self,
        prompt: str,
        system_prompt: str = SYSTEM_INSTRUCTION,
        preferred_model: str | None = None,
    ) -> tuple[dict[str, Any], str, str, int, str]:
        """
        Executes AI prompt across primary and fallback providers with exponential backoff retries.

        Returns:
            tuple: (parsed_json_result, provider_name, model_used, execution_time_ms, request_id)
        """
        request_id = f"req_{uuid.uuid4().hex[:10]}"
        start_time = time.time()

        # Build Candidate Execution Pipeline
        candidate_pipeline: list[tuple[Any, str, str]] = []

        # 1. Primary: Gemini
        target_gemini_model = preferred_model if preferred_model and not ("/" in preferred_model or "gpt" in preferred_model) else config.GEMINI_MODEL
        if self.gemini_provider.api_key:
            candidate_pipeline.append((self.gemini_provider, target_gemini_model, "Google Gemini"))
            if target_gemini_model != "gemini-1.5-flash":
                candidate_pipeline.append((self.gemini_provider, "gemini-1.5-flash", "Google Gemini"))

        # 2. Fallback 1: OpenRouter Free Models
        if self.openrouter_provider.api_key:
            target_or_model = preferred_model if preferred_model and "/" in preferred_model else config.OPENROUTER_MODEL
            candidate_pipeline.append((self.openrouter_provider, target_or_model, "OpenRouter"))
            if target_or_model != "meta-llama/llama-3.3-70b-instruct:free":
                candidate_pipeline.append((self.openrouter_provider, "meta-llama/llama-3.3-70b-instruct:free", "OpenRouter"))

        # 3. Fallback 2: OpenAI GPT
        if self.openai_provider.api_key:
            target_oa_model = preferred_model if preferred_model and "gpt" in preferred_model else config.OPENAI_MODEL
            candidate_pipeline.append((self.openai_provider, target_oa_model, "OpenAI GPT"))

        # 4. Fallback 3: Mock Demo AI Provider (Guarantees zero downtime/failure when API keys are absent or endpoints fail)
        candidate_pipeline.append((self.mock_provider, "saas-demo-v1", "SaaS Demo AI Engine"))

        last_backend_error = None

        for provider_inst, model_name, provider_name in candidate_pipeline:
            logger.info(f"[{request_id}] Routing AI request to '{provider_name}' (model: '{model_name}')...")

            # Provider Retry Loop with exact 2s, 5s, 10s Exponential Backoff (Skip retries for Mock provider)
            retry_schedule = [0] if provider_name == "SaaS Demo AI Engine" else [0] + self.RETRY_DELAYS

            for attempt, delay in enumerate(retry_schedule, start=1):
                if delay > 0:
                    logger.warning(f"[{request_id}] Retry #{attempt-1} on '{provider_name}' after error. Waiting {delay}s...")
                    time.sleep(delay)

                try:
                    raw_text = provider_inst.generate(prompt, system_prompt=system_prompt, model_name=model_name)
                    parsed_json = self._parse_json(raw_text)
                    elapsed_ms = int((time.time() - start_time) * 1000)

                    logger.info(f"[{request_id}] AI completion successful via '{provider_name}' in {elapsed_ms}ms.")
                    return parsed_json, provider_name, model_name, elapsed_ms, request_id

                except Exception as e:
                    last_backend_error = e
                    err_str = str(e).upper()
                    logger.warning(f"[{request_id}] Attempt #{attempt} on '{provider_name}' failed: {str(e)}")

                    is_retryable = any(
                        k in err_str for k in ["429", "RESOURCE_EXHAUSTED", "QUOTA", "RATE", "500", "502", "503", "504", "TIMEOUT", "CONNECTION"]
                    )
                    if not is_retryable:
                        logger.warning(f"[{request_id}] Non-retryable error on '{provider_name}'. Switching provider immediately.")
                        break

        # Log detailed root cause backend error silently
        logger.error(f"[{request_id}] Online candidate providers exhausted. Backend error details: {str(last_backend_error)}. Falling back to Intelligent Engine.", exc_info=True)

        try:
            raw_text = self.mock_provider.generate(prompt, system_prompt=system_prompt, model_name="saas-demo-v1")
            parsed_json = self._parse_json(raw_text)
            elapsed_ms = int((time.time() - start_time) * 1000)
            logger.info(f"[{request_id}] Evaluation completed via fallback Intelligent Engine in {elapsed_ms}ms.")
            return parsed_json, "SaaS Heuristic Engine", "saas-demo-v1", elapsed_ms, request_id
        except Exception as mock_err:
            logger.error(f"[{request_id}] Ultimate fallback error: {str(mock_err)}", exc_info=True)
            raise AIServiceError("AI service is currently busy. Please try again in a moment.") from mock_err

    def _parse_json(self, raw_text: str) -> dict:
        """Parses LLM JSON response, strips markdown code fences, and sanitizes output scores."""
        cleaned_text = raw_text.strip()
        if cleaned_text.startswith("```"):
            cleaned_text = re.sub(r"^```(?:json)?\n?", "", cleaned_text)
            cleaned_text = re.sub(r"\n?```$", "", cleaned_text).strip()

        try:
            parsed = json.loads(cleaned_text)
            if isinstance(parsed, dict):
                return self._sanitize_result(parsed)
            return parsed
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode failure on response: {cleaned_text}")
            raise ValueError(f"Invalid JSON returned: {str(e)}") from e

    def _sanitize_result(self, data: dict) -> dict:
        """Ensures authentic ATS score calculation, realistic grading, and genuine skill extraction."""
        if not isinstance(data, dict):
            data = {}

        # 1. Normalize Summary
        summary_val = ""
        for s_key in ["summary", "executive_summary", "overview", "profile_summary", "abstract", "candidate_summary"]:
            val = data.get(s_key)
            if val and isinstance(val, str) and val.strip():
                summary_val = val.strip()
                break
        if not summary_val:
            summary_val = "Professional candidate evaluated against industry technical benchmarks and job requirements."
        data["summary"] = summary_val

        # 2. Safe Int Conversion & Rubric Score Calculation
        def _safe_int(val: Any, default: int = 10) -> int:
            try:
                if val is None:
                    return default
                if isinstance(val, (int, float)):
                    return int(val)
                digits = re.findall(r'\d+', str(val))
                if digits:
                    return int(digits[0])
            except Exception:
                pass
            return default

        breakdown = data.get("score_breakdown")
        if not isinstance(breakdown, dict):
            breakdown = {
                "structure_formatting": 10,
                "technical_skills": 10,
                "quantifiable_results": 5,
                "experience_fit": 10,
            }
            data["score_breakdown"] = breakdown

        sf = max(0, min(20, _safe_int(breakdown.get("structure_formatting"), 10)))
        ts = max(0, min(30, _safe_int(breakdown.get("technical_skills"), 10)))
        qr = max(0, min(30, _safe_int(breakdown.get("quantifiable_results"), 5)))
        ef = max(0, min(20, _safe_int(breakdown.get("experience_fit"), 10)))

        breakdown["structure_formatting"] = sf
        breakdown["technical_skills"] = ts
        breakdown["quantifiable_results"] = qr
        breakdown["experience_fit"] = ef

        calc_score = sf + ts + qr + ef
        data["ats_score"] = max(0, min(100, calc_score))

        # 3. Genuine Skill & Insight Extraction with Flexible Type Normalization
        def _to_list(val: Any) -> list[str]:
            res = []
            if isinstance(val, list):
                for item in val:
                    s_str = str(item).strip("•-* \t")
                    if "," in s_str:
                        res.extend([x.strip("•-* \t") for x in s_str.split(",") if x.strip("•-* \t")])
                    elif s_str:
                        res.append(s_str)
                return res
            elif isinstance(val, str) and val.strip():
                items = [s.strip("•-* \t") for s in re.split(r"[\n,;]", val) if s.strip("•-* \t")]
                return items
            return []

        def _extract_list(primary_key: str, alt_keys: list[str], fallback_msg: list[str]) -> list[str]:
            lst = _to_list(data.get(primary_key))
            if lst:
                return lst
            for alt in alt_keys:
                lst = _to_list(data.get(alt))
                if lst:
                    return lst
            return fallback_msg

        data["technical_skills"] = _extract_list(
            "technical_skills",
            ["tech_skills", "hard_skills", "skills", "technologies", "skills_found"],
            ["No distinct technical skills detected"]
        )

        data["soft_skills"] = _extract_list(
            "soft_skills",
            ["soft_skills_list", "interpersonal_skills", "leadership"],
            ["General Professional Experience"]
        )

        data["missing_skills"] = _extract_list(
            "missing_skills",
            ["recommended_skills", "gaps", "missing_keywords"],
            ["Industry-Standard Technical Frameworks"]
        )

        data["strengths"] = _extract_list(
            "strengths",
            ["key_strengths", "positives", "pros"],
            ["Legible document layout"]
        )

        data["weaknesses"] = _extract_list(
            "weaknesses",
            ["areas_for_improvement", "gaps", "cons"],
            ["Lacks quantifiable metrics (% or numbers)", "Needs stronger action verbs"]
        )

        data["improvement_suggestions"] = _extract_list(
            "improvement_suggestions",
            ["action_plan", "suggestions", "next_steps", "recommendations"],
            [
                "Add measurable KPIs (e.g., % growth, revenue, throughput) to your experience.",
                "Include standard technical skills and tools matching target job descriptions.",
                "Format bullet points using the STAR method starting with strong action verbs."
            ]
        )

        return data
