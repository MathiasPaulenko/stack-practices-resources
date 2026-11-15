"""LLM Fallback Pattern — runnable demo.

A provider chain with per-provider retry budgets, a retryable/non-retryable
error taxonomy, an optional per-provider circuit breaker, and a static
last-resort response. Uses a mock provider call so it runs without API keys.

Run: python llm_fallback.py
"""

import random
import time
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Dict, List, Optional


class ErrorType(Enum):
    RATE_LIMIT = "rate_limit"      # retryable: quota exceeded, back off
    TIMEOUT = "timeout"            # retryable: no response in time
    SERVER_ERROR = "server_error"  # retryable: provider-side 5xx
    AUTH = "auth"                  # NOT retryable: bad key
    INVALID_REQUEST = "invalid_request"  # NOT retryable: malformed input
    UNKNOWN = "unknown"


@dataclass
class LLMError(Exception):
    error_type: ErrorType
    message: str
    provider: str


@dataclass
class ProviderConfig:
    name: str
    model: str
    max_retries: int = 3        # attempts within THIS provider
    base_delay: float = 1.0
    max_delay: float = 30.0
    timeout_s: float = 10.0     # per-attempt budget, not per-chain


@dataclass
class LLMResponse:
    provider: str
    model: str
    content: str
    latency_ms: float
    from_fallback: bool = False


RETRYABLE_ERRORS = {ErrorType.RATE_LIMIT, ErrorType.TIMEOUT, ErrorType.SERVER_ERROR}

ProviderCall = Callable[[str, str, str], str]


def exponential_backoff(attempt: int, base: float, max_delay: float) -> float:
    delay = min(base * (2 ** attempt), max_delay)
    return delay + random.uniform(0, 0.1 * delay)  # jitter avoids thundering herd


def mock_provider_call(provider: str, model: str, prompt: str) -> str:
    """Simulate provider calls with configurable failures."""
    if provider == "openai" and "rate limit" in prompt.lower():
        raise LLMError(ErrorType.RATE_LIMIT, "Rate limit exceeded", provider)
    if provider == "anthropic" and "timeout" in prompt.lower():
        raise LLMError(ErrorType.TIMEOUT, "Request timed out", provider)
    if provider == "local" and "auth" in prompt.lower():
        raise LLMError(ErrorType.AUTH, "Invalid API key", provider)
    return f"[{provider}/{model}] Response to: {prompt[:40]}..."


class LLMFallbackChain:
    def __init__(self, providers: List[ProviderConfig],
                 call: ProviderCall = mock_provider_call,
                 static_fallback: str = "I'm unable to respond right now. Please try again later."):
        self.providers = providers
        self.call = call
        self.static_fallback = static_fallback

    def _call_with_retry(self, provider: ProviderConfig, prompt: str) -> str:
        for attempt in range(provider.max_retries + 1):
            try:
                return self.call(provider.name, provider.model, prompt)
            except LLMError as e:
                if e.error_type not in RETRYABLE_ERRORS:
                    raise
                if attempt < provider.max_retries:
                    delay = exponential_backoff(attempt, provider.base_delay, provider.max_delay)
                    print(f"  [{provider.name}] {e.error_type.value}, retrying in {delay:.1f}s...")
                    time.sleep(min(delay, 0.5))  # capped for the demo
                else:
                    raise

    def complete(self, prompt: str) -> LLMResponse:
        for i, provider in enumerate(self.providers):
            try:
                start = time.time()
                content = self._call_with_retry(provider, prompt)
                latency = (time.time() - start) * 1000
                return LLMResponse(provider.name, provider.model, content,
                                   latency, from_fallback=i > 0)
            except LLMError as e:
                # Log every fallthrough — a silent chain hides provider outages
                print(f"  [{provider.name}] Failed: {e.error_type.value} - {e.message}")
                continue
            except Exception as e:
                print(f"  [{provider.name}] Unexpected error: {e}")
                continue

        return LLMResponse("static", "none", self.static_fallback, 0, True)


class CircuitBreaker:
    """Minimal per-provider breaker: OPEN after N consecutive failures,
    HALF-OPEN probe after cooldown_s."""

    def __init__(self, name: str, failure_threshold: int = 3, cooldown_s: float = 30.0):
        self.name = name
        self.failure_threshold = failure_threshold
        self.cooldown_s = cooldown_s
        self.consecutive_failures = 0
        self.opened_at: Optional[float] = None

    def allow_request(self) -> bool:
        if self.opened_at is None:
            return True
        return (time.time() - self.opened_at) >= self.cooldown_s  # half-open probe

    def record_success(self) -> None:
        self.consecutive_failures = 0
        self.opened_at = None

    def record_failure(self) -> None:
        self.consecutive_failures += 1
        if self.consecutive_failures >= self.failure_threshold and self.opened_at is None:
            self.opened_at = time.time()
            print(f"  [{self.name}] Circuit OPEN — skipping provider until cooldown")


class BreakerChain(LLMFallbackChain):
    """Chain that skips providers whose breaker is OPEN."""

    def __init__(self, providers: List[ProviderConfig],
                 breakers: Optional[Dict[str, CircuitBreaker]] = None, **kw):
        super().__init__(providers, **kw)
        self.breakers = breakers or {p.name: CircuitBreaker(p.name) for p in providers}

    def complete(self, prompt: str) -> LLMResponse:
        candidates = [p for p in self.providers if self.breakers[p.name].allow_request()]
        if not candidates:
            return LLMResponse("static", "none", self.static_fallback, 0, True)
        saved, self.providers = self.providers, candidates
        response: Optional[LLMResponse] = None
        try:
            response = super().complete(prompt)
            if response.provider != "static":
                self.breakers[response.provider].record_success()
            return response
        finally:
            for p in candidates:
                if p.name != (response.provider if response else None):
                    self.breakers[p.name].record_failure()
            self.providers = saved


def demo() -> None:
    chain = LLMFallbackChain([
        ProviderConfig("openai", "gpt-4o", max_retries=2, base_delay=1.0),
        ProviderConfig("anthropic", "claude-3.5-sonnet", max_retries=1, base_delay=2.0),
        ProviderConfig("local", "llama-3-70b", max_retries=1, base_delay=0.5),
    ])

    test_prompts = [
        "What is machine learning?",
        "This prompt will trigger rate limit on OpenAI",
        "This prompt will trigger timeout on Anthropic too",
        "This prompt will trigger auth error on local provider",
    ]

    for prompt in test_prompts:
        print(f"\nPrompt: {prompt}")
        response = chain.complete(prompt)
        print(f"  Provider: {response.provider}/{response.model}")
        print(f"  Fallback: {response.from_fallback}")
        print(f"  Content: {response.content[:60]}...")


if __name__ == "__main__":
    demo()
