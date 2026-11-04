"""In-memory LLM metrics: requests, tokens, latency, cache hit rate."""
from collections import defaultdict


class LLMMetrics:
    def __init__(self):
        self.request_count = 0
        self.token_count = 0
        self.error_count = 0
        self.latencies: list[float] = []
        self.model_usage: dict[str, int] = defaultdict(int)
        self.cache_hits = 0
        self.cache_misses = 0

    def record_request(self, model: str, latency_ms: float, tokens: int,
                       cached: bool = False, error: bool = False):
        self.request_count += 1
        if error:
            self.error_count += 1
        else:
            self.latencies.append(latency_ms)
            self.token_count += tokens
            self.model_usage[model] += 1
        if cached:
            self.cache_hits += 1
        else:
            self.cache_misses += 1

    def summary(self) -> dict:
        latencies = self.latencies[-1000:]
        return {
            "total_requests": self.request_count,
            "total_tokens": self.token_count,
            "error_rate": self.error_count / max(self.request_count, 1),
            "avg_latency_ms": sum(latencies) / max(len(latencies), 1),
            "p95_latency_ms": sorted(latencies)[int(len(latencies) * 0.95)] if latencies else 0,
            "cache_hit_rate": self.cache_hits / max(self.cache_hits + self.cache_misses, 1),
            "model_usage": dict(self.model_usage),
        }
