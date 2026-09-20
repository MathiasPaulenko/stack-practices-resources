"""Ambassador pattern — a local proxy that owns remote-call resilience.

The ambassador wraps a remote service behind the same interface the
client expects. Retries, timeouts, circuit breaking, and metrics live
here; the client just calls `get_user()`.

Run: python ambassador.py
"""

import random
import time
from typing import Callable, Literal, Optional

CircuitState = Literal["closed", "open", "half-open"]


class RemoteError(Exception):
    """The remote service failed in a retryable way."""


class CircuitOpenError(Exception):
    """The ambassador refused the call; the circuit is open."""


class ServiceAmbassador:
    """Wraps a remote callable with retry + timeout + circuit breaker.

    Order of operations: circuit check -> retry loop -> per-attempt
    timeout. The timeout bounds each attempt; the circuit bounds the
    whole disaster.
    """

    def __init__(
        self,
        remote: Callable[[], dict],
        *,
        retry_count: int = 3,
        timeout_s: float = 2.0,
        failure_threshold: int = 5,
        reset_after_s: float = 30.0,
        base_delay_s: float = 1.0,
        jitter_s: float = 0.5,
        sleep: Callable[[float], None] = time.sleep,
        clock: Callable[[], float] = time.monotonic,
    ):
        self.remote = remote
        self.retry_count = retry_count
        self.timeout_s = timeout_s
        self.failure_threshold = failure_threshold
        self.reset_after_s = reset_after_s
        self.base_delay_s = base_delay_s
        self.jitter_s = jitter_s
        self.sleep = sleep
        self.clock = clock
        self.state: CircuitState = "closed"
        self.failure_count = 0
        self.opened_at = 0.0

    def call(self) -> dict:
        if self.state == "open":
            # After the cool-down, let exactly one trial call through
            if self.clock() - self.opened_at >= self.reset_after_s:
                self.state = "half-open"
            else:
                raise CircuitOpenError("circuit breaker is open")

        for attempt in range(self.retry_count):
            try:
                result = self._call_with_timeout()
            except Exception:
                self._on_failure()
                if attempt == self.retry_count - 1:
                    raise
                # Real exponential backoff plus jitter, so clients
                # don't retry in lockstep after an outage
                self.sleep(self.base_delay_s * 2**attempt + random.random() * self.jitter_s)
            else:
                self._on_success()
                return result
        raise RemoteError("unreachable")

    def _call_with_timeout(self) -> dict:
        # Thread-based timeout keeps the demo dependency-free; real
        # deployments bound the socket/HTTP call instead.
        import concurrent.futures

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            return pool.submit(self.remote).result(timeout=self.timeout_s)

    def _on_success(self) -> None:
        self.failure_count = 0
        self.state = "closed"

    def _on_failure(self) -> None:
        self.failure_count += 1
        if self.state == "half-open" or self.failure_count >= self.failure_threshold:
            self.state = "open"
            self.opened_at = self.clock()


class MonitoringAmbassador:
    """Wraps any ambassador (or the raw remote) and counts outcomes.

    Composes cleanly: MonitoringAmbassador(ServiceAmbassador(remote))
    sees final results, not per-attempt noise.
    """

    def __init__(self, inner):
        self.inner = inner
        self.requests = 0
        self.errors = 0
        self.total_latency_s = 0.0

    def call(self) -> dict:
        start = time.monotonic()
        self.requests += 1
        try:
            result = self.inner.call() if hasattr(self.inner, "call") else self.inner()
        except Exception:
            self.errors += 1
            raise
        else:
            self.total_latency_s += time.monotonic() - start
            return result

    def metrics(self) -> dict:
        return {
            "requests": self.requests,
            "errors": self.errors,
            "avg_latency_s": (
                self.total_latency_s / self.requests if self.requests else 0.0
            ),
        }


def _demo() -> None:
    attempts = {"n": 0}

    def flaky_remote() -> dict:
        attempts["n"] += 1
        if attempts["n"] < 3:
            raise RemoteError("HTTP 503")
        return {"id": "user-123", "name": "Ana"}

    ambassador = ServiceAmbassador(
        flaky_remote, base_delay_s=0.05, jitter_s=0.0
    )
    monitored = MonitoringAmbassador(ambassador)

    print("result:", monitored.call())
    print("metrics:", monitored.metrics())


if __name__ == "__main__":
    _demo()
