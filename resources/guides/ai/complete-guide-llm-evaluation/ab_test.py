"""A/B testing: deterministic assignment + z-test significance."""
import math
from dataclasses import dataclass


def ab_test_significance(conv_a: int, total_a: int, conv_b: int, total_b: int) -> dict:
    rate_a, rate_b = conv_a / total_a, conv_b / total_b
    pooled = (conv_a + conv_b) / (total_a + total_b)
    se = math.sqrt(pooled * (1 - pooled) * (1 / total_a + 1 / total_b))
    if se == 0:
        return {"z_score": 0, "significant": False}
    z = (rate_b - rate_a) / se
    return {"rate_a": rate_a, "rate_b": rate_b,
            "lift": (rate_b - rate_a) / rate_a if rate_a > 0 else 0,
            "z_score": z, "significant": abs(z) > 1.96}


@dataclass
class ABTestConfig:
    model_a: str
    model_b: str
    traffic_split: float
    min_samples: int = 100


class ABTestRunner:
    def __init__(self, config: ABTestConfig):
        self.config = config
        self.results_a: list[dict] = []
        self.results_b: list[dict] = []

    def assign(self, user_id: str) -> str:
        """Deterministic — same user always gets the same model."""
        if (hash(user_id) % 100 / 100) < self.config.traffic_split:
            return self.config.model_b
        return self.config.model_a

    def record(self, model: str, rating: int, latency_ms: float):
        if model == self.config.model_a:
            self.results_a.append({"rating": rating, "latency_ms": latency_ms})
        else:
            self.results_b.append({"rating": rating, "latency_ms": latency_ms})


def cohen_kappa(ratings_a: list[int], ratings_b: list[int]) -> float:
    """Inter-annotator agreement — validates rubric clarity, not label truth."""
    assert len(ratings_a) == len(ratings_b)
    n = len(ratings_a)
    cats = sorted(set(ratings_a + ratings_b))
    observed = sum(1 for a, b in zip(ratings_a, ratings_b) if a == b) / n
    expected = sum((ratings_a.count(c) / n) * (ratings_b.count(c) / n) for c in cats)
    return 1.0 if expected == 1 else (observed - expected) / (1 - expected)
