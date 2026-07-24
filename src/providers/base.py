"""
Base LLM Provider Interface for AI Resume Analyzer SaaS
Defines standard provider interface for plug-and-play AI backends (Gemini, OpenRouter, OpenAI, etc.).
"""

from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):
    """Abstract base class for all LLM providers."""

    def __init__(self, name: str, default_model: str) -> None:
        self.name = name
        self.default_model = default_model

    @abstractmethod
    def generate(self, prompt: str, system_prompt: str, model_name: str | None = None) -> str:
        """
        Executes a prompt completion call to the provider.

        Args:
            prompt: User prompt string.
            system_prompt: System instruction string.
            model_name: Optional custom model override.

        Returns:
            str: Raw LLM response string.
        """
        pass
