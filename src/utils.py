"""
Utility Functions Module
Helper utilities for text cleaning, file validation, and formatting.
"""

import os
import re
from src.config import config


def is_valid_file_extension(filename: str) -> bool:
    """
    Checks if the uploaded file has a supported extension (.pdf or .docx).

    Args:
        filename: Name of the file.

    Returns:
        bool: True if extension is valid, False otherwise.
    """
    ext = os.path.splitext(filename)[1].lower()
    return ext in config.ALLOWED_EXTENSIONS


def is_valid_file_size(file_bytes: bytes) -> bool:
    """
    Checks if the file size is within the allowed limit.

    Args:
        file_bytes: Raw bytes of the file.

    Returns:
        bool: True if size is valid, False otherwise.
    """
    max_bytes = config.MAX_FILE_SIZE_MB * 1024 * 1024
    return len(file_bytes) <= max_bytes


def clean_text(text: str) -> str:
    """
    Sanitizes and cleans extracted text from documents.

    Args:
        text: Raw text string.

    Returns:
        str: Cleaned and normalized text string.
    """
    if not text:
        return ""

    # Replace non-breaking spaces and normalize whitespace/newlines
    text = text.replace("\xa0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    return text.strip()
