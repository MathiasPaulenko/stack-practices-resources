"""Sliding-window limiter keyed on both requests AND tokens.

Token-based limiting stops wallet-DoS: a hundred 1-token calls and
ten 4k-token calls don't cost the same.
"""
import time
from collections import defaultdict
from dataclasses import dataclass


@dataclass
class RateLimitConfig:
    requests_per_minute: int = 30
    requests_per_hour: int = 500
    tokens_per_minute: int = 10000
    max_input_tokens: int = 4000
    max_output_tokens: int = 2000


class LLMRateLimiter:
    def __init__(self, config: RateLimitConfig):
        self.config = config
        self.requests: dict[str, list[float]] = defaultdict(list)
        self.tokens: dict[str, list[tuple[float, int]]] = defaultdict(list)

    def check(self, user_id: str, input_tokens: int) -> tuple[bool, str]:
        now = time.time()
        if input_tokens > self.config.max_input_tokens:
            return False, f"Input exceeds max tokens ({self.config.max_input_tokens})"

        self.requests[user_id] = [t for t in self.requests[user_id] if now - t < 3600]
        if len(self.requests[user_id]) >= self.config.requests_per_hour:
            return False, "Hourly request limit exceeded"

        minute_hits = [t for t in self.requests[user_id] if now - t < 60]
        if len(minute_hits) >= self.config.requests_per_minute:
            return False, "Per-minute request limit exceeded"

        recent = [(t, n) for t, n in self.tokens[user_id] if now - t < 60]
        if sum(n for _, n in recent) + input_tokens > self.config.tokens_per_minute:
            return False, "Token rate limit exceeded"

        self.requests[user_id].append(now)
     
