"""
Centralized Configuration Module
Handles environment variables and application constants.
"""

import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass(frozen=True)
class Config:
    """Application configuration settings."""

    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_MODEL: str = os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-lite-001:free")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    RATE_LIMIT_RPM: int = int(os.getenv("RATE_LIMIT_RPM", "15"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "5"))
    ALLOWED_EXTENSIONS: tuple[str, ...] = (".pdf", ".docx")
    UPLOADS_DIR: str = "uploads"

    def validate(self) -> None:
        """Validate critical configuration settings."""
        if not any([self.GEMINI_API_KEY, self.OPENROUTER_API_KEY, self.OPENAI_API_KEY]):
            raise ValueError(
                "At least one API key (GEMINI_API_KEY, OPENROUTER_API_KEY, or OPENAI_API_KEY) must be provided."
            )


config = Config()
