"""
Centralized Configuration Module
Handles environment variables and application constants.
"""

import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def _get_secret(key: str, default: str = "") -> str:
    """Helper to resolve secret from environment or Streamlit secrets."""
    val = os.getenv(key, "")
    if val:
        return val
    try:
        import streamlit as st
        if hasattr(st, "secrets") and key in st.secrets:
            return str(st.secrets[key])
    except Exception:
        pass
    return default


@dataclass(frozen=True)
class Config:
    """Application configuration settings."""

    GEMINI_API_KEY: str = _get_secret("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = _get_secret("GEMINI_MODEL", "gemini-1.5-flash")
    OPENROUTER_API_KEY: str = _get_secret("OPENROUTER_API_KEY", "")
    OPENROUTER_MODEL: str = _get_secret("OPENROUTER_MODEL", "google/gemini-2.0-flash-lite-001:free")
    OPENAI_API_KEY: str = _get_secret("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = _get_secret("OPENAI_MODEL", "gpt-4o-mini")
    MAX_RETRIES: int = int(_get_secret("MAX_RETRIES", "3"))
    RATE_LIMIT_RPM: int = int(_get_secret("RATE_LIMIT_RPM", "15"))
    LOG_LEVEL: str = _get_secret("LOG_LEVEL", "INFO").upper()
    MAX_FILE_SIZE_MB: int = int(_get_secret("MAX_FILE_SIZE_MB", "5"))
    ALLOWED_EXTENSIONS: tuple[str, ...] = (".pdf", ".docx")
    UPLOADS_DIR: str = "uploads"

    def validate(self) -> None:
        """Validate critical configuration settings."""
        if not any([self.GEMINI_API_KEY, self.OPENROUTER_API_KEY, self.OPENAI_API_KEY]):
            raise ValueError(
                "At least one API key (GEMINI_API_KEY, OPENROUTER_API_KEY, or OPENAI_API_KEY) must be provided."
            )


config = Config()
