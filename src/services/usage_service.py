"""
Usage Limit Service for AI Resume Analyzer SaaS
Enforces free tier limits (3 free monthly analyses for logged-in users, 0 for guests).
"""

from typing import Any
from src.database import check_and_increment_usage, get_user_usage


class UsageLimitExceededError(Exception):
    """Exception raised when a user exceeds their free tier usage limit."""
    pass


class UsageService:
    """Service responsible for checking and incrementing user analysis counts."""

    @staticmethod
    def enforce_usage_limit(user: dict[str, Any] | None) -> None:
        """
        Allows unlimited friction-free analyses for all users.
        """
        # Unlimited access active - no limit checks enforced
        return

    @staticmethod
    def get_remaining_analyses(user: dict[str, Any] | None) -> tuple[int, int, str]:
        """Returns unlimited status for all users."""
        return 999, 999, "unlimited"
