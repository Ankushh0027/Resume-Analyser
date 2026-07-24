"""
Gemini LLM Provider Implementation
Handles server-side execution for Google Gemini Generative API.
"""

import google.generativeai as genai
from src.config import config
from src.logger import logger
from src.providers.base import BaseLLMProvider


class GeminiProvider(BaseLLMProvider):
    """Google Gemini AI Provider."""

    def __init__(self, api_key: str | None = None) -> None:
        super().__init__(name="Google Gemini", default_model=config.GEMINI_MODEL)
        self.api_key = api_key or config.GEMINI_API_KEY
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
            except Exception as e:
                logger.warning(f"GeminiProvider configuration warning: {str(e)}")

    def generate(self, prompt: str, system_prompt: str, model_name: str | None = None) -> str:
        """Executes prompt via Google Gemini API."""
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not configured on the server.")

        target_model = model_name or self.default_model
        model_inst = genai.GenerativeModel(
            model_name=target_model,
            system_instruction=system_prompt,
            generation_config={"temperature": 0.2, "top_p": 0.95},
        )
        response = model_inst.generate_content(prompt)
        return response.text
