"""Tests for the feature flag service."""

import pytest
from feature_flags import FeatureFlags


def test_boolean_flag():
    flags = FeatureFlags({"new_ui": True})
    assert flags.is_enabled("new_ui") is True


def test_boolean_flag_off():
    flags = FeatureFlags({"new_ui": False})
    assert flags.is_enabled("new_ui") is False


def test_percentage_flag_consistency():
    flags = FeatureFlags({"beta": {"percentage": 50}})
    result1 = flags.is_enabled("beta", user_id="user_123")
    result2 = flags.is_enabled("beta", user_id="user_123")
    assert result1 == result2


def test_percentage_flag_distribution():
    flags = FeatureFlags({"beta": {"percentage": 50}})
    enabled = sum(
        1 for i in range(1000)
        if flags.is_enabled("beta", user_id=f"user_{i}")
    )
    assert 400 <= enabled <= 600


def test_user_targeting():
    flags = FeatureFlags({"vip": {"users": ["user_123"]}})
    assert flags.is_enabled("vip", user_id="user_123") is True
    assert flags.is_enabled("vip", user_id="user_999") is False


def test_missing_flag_defaults_off():
    flags = FeatureFlags({})
    assert flags.is_enabled("nonexistent") is False


def test_missing_user_id_with_percentage():
    flags = FeatureFlags({"beta": {"percentage": 50}})
    assert flags.is_enabled("beta") is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
