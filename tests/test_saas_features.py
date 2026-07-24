"""
Unit Tests for SaaS Features (Database, Authentication, Usage Limits)
"""

import unittest
import os
from src.database import register_user, authenticate_user, check_and_increment_usage, get_user_usage
from src.services.usage_service import UsageService, UsageLimitExceededError


class TestSaaSFeatures(unittest.TestCase):
    """Test suite for user registration, authentication, and usage limit enforcement."""

    def test_user_registration_and_authentication(self):
        """Verify user signup and login authentication."""
        email = f"test_{os.urandom(4).hex()}@example.com"
        user = register_user(email, "Test User", "password123")
        self.assertEqual(user["email"], email)

        auth_user = authenticate_user(email, "password123")
        self.assertIsNotNone(auth_user)
        self.assertEqual(auth_user["name"], "Test User")

        bad_auth = authenticate_user(email, "wrongpassword")
        self.assertIsNone(bad_auth)

    def test_free_tier_usage_limit_enforcement(self):
        """Verify 3 free monthly analyses limit enforcement."""
        email = f"usage_{os.urandom(4).hex()}@example.com"
        user = register_user(email, "Usage User", "password123")

        # 3 analyses allowed
        UsageService.enforce_usage_limit(user)
        UsageService.enforce_usage_limit(user)
        UsageService.enforce_usage_limit(user)

        # 4th analysis rejected
        with self.assertRaises(UsageLimitExceededError):
            UsageService.enforce_usage_limit(user)

    def test_guest_user_limit_rejection(self):
        """Verify guest users without account are rejected from running analyses."""
        with self.assertRaises(UsageLimitExceededError):
            UsageService.enforce_usage_limit(None)


if __name__ == "__main__":
    unittest.main()
