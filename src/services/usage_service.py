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
        Validates user usage limit prior to running AI analysis.

        Raises:
            UsageLimitExceededError: If user is guest or has reached 3 free monthly analyses.
        """
        if not user:
            raise UsageLimitExceededError(
                "Please sign in or create a free account to run resume analyses (Includes 3 Free Monthly Analyses)."
            )

        user_id = user["id"]
        can_proceed, count, limit, message = check_and_increment_usage(user_id)

        if not can_proceed:
            raise UsageLimitExceededError(message)

    @staticmethod
    def get_remaining_analyses(user: dict[str, Any] | None) -> tuple[int, int]:
        """Returns (remaining, limit) tuple for current user."""
        if not user:
            return 0, 3
        usage = get_user_usage(user["id"])
        count = usage.get("analysis_count", 0)
        limit = usage.get("analysis_limit", 3)
        return max(0, limit - count), limit
