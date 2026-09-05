"""Lightweight feature flag service with boolean, percentage, user, and group rollouts."""

from __future__ import annotations

import hashlib
from typing import Any


class FeatureFlags:
    def __init__(self, config: dict[str, Any]):
        self.config = config

    def is_enabled(self, flag: str, user_id: str | None = None) -> bool:
        rule = self.config.get(flag, False)

        if isinstance(rule, bool):
            return rule

        if isinstance(rule, dict):
            if "percentage" in rule and user_id:
                return self._hash_bucket(user_id, flag) < rule["percentage"]
            if "users" in rule and user_id:
                return user_id in rule["users"]
            if "groups" in rule:
                return self._check_groups(rule["groups"])

        return False

    def _hash_bucket(self, user_id: str, flag: str) -> int:
        digest = hashlib.md5(f"{flag}:{user_id}".encode()).hexdigest()
        return int(digest, 16) % 100

    def _check_groups(self, groups: list[str]) -> bool:
        # Hook for group membership lookup
        return False


if __name__ == "__main__":
    flags = FeatureFlags({
        "new_dashboard": True,
        "beta_search": {"percentage": 10},
        "vip_feature": {"users": ["user_123"]},
        "admin_tools": {"groups": ["admins"]},
    })

    print(f"new_dashboard: {flags.is_enabled('new_dashboard')}")
    print(f"beta_search (user_456): {flags.is_enabled('beta_search', user_id='user_456')}")
    print(f"vip_feature (user_123): {flags.is_enabled('vip_feature', user_id='user_123')}")
    print(f"missing_flag: {flags.is_enabled('missing_flag')}")
