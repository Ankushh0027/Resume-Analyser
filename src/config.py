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
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "5"))
    ALLOWED_EXTENSIONS: tuple[str, ...] = (".pdf", ".docx")
    UPLOADS_DIR: str = "uploads"

    def validate(self) -> None:
        """Validate critical configuration settings."""
        if not self.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is not set. Please add it to your .env file."
            )


config = Config()
