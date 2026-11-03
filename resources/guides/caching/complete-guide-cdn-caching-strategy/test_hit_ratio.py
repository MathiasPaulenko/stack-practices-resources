"""Smoke tests for the hit-ratio helpers."""
from hit_ratio import below_target, hit_ratio


def test_hit_ratio_basic():
    assert hit_ratio(95, 5) == 0.95


def test_hit_ratio_empty():
    assert hit_ratio(0, 0) == 0.0


def test_below_target_static():
    assert below_target(90, 10, "static_assets")   # 90% < 99%
    assert not below_target(995, 5, "static_assets")
