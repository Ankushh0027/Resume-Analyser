"""
Logger Module
Provides a standardized logging setup for the application.
"""

import logging
import sys
from src.config import config


def setup_logger(name: str = "AI_Resume_Analyzer") -> logging.Logger:
    """
    Creates and configures a logger instance with stdout output.

    Args:
        name: Name of the logger instance.

    Returns:
        logging.Logger: Configured logger.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        log_level = getattr(logging, config.LOG_LEVEL, logging.INFO)
        logger.setLevel(log_level)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)

        # Formatter
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


logger = setup_logger()
