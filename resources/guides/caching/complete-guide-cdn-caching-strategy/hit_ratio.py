"""Cache-hit-ratio helpers for CDN monitoring dashboards.

Source: https://stackpractices.com/guides/complete-guide-cdn-caching-strategy/
"""

TARGETS = {
    "static_assets": 0.99,
    "html_pages": 0.85,
    "public_api": 0.70,
    "private_api": 0.0,
}


def hit_ratio(hits: int, misses: int) -> float:
    total = hits + misses
    return hits / total if total else 0.0


def below_target(hits: int, misses: int, content_type: str) -> bool:
    return hit_ratio(hits, misses) < TARGETS.get(content_type, 0.5)
