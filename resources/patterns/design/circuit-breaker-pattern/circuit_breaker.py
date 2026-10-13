"""Circuit breaker — minimal runnable implementation with fallback support."""

import time
from enum import Enum, auto


class CircuitState(Enum):
    CLOSED = auto()      # Normal operation
    OPEN = auto()        # Failing fast
    HALF_OPEN = auto()   # Testing recovery


class CircuitBreakerOpen(Exception):
    """Raised when a call is rejected because the circuit is open."""


class CircuitBreaker:
    """Count-based circuit breaker.

    Args:
        failure_threshold: consecutive failures that trip the breaker.
        recovery_timeout: seconds the breaker stays open before probing.
        expected_exceptions: exception types counted as failures. Any other
            exception propagates without incrementing the counter.
    """

    def __init__(self, failure_threshold=3, recovery_timeout=5.0,
                 expected_exceptions=(Exception,)):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exceptions = expected_exceptions
        self.state = CircuitState.CLOSED
        self.failures = 0
        self.last_failure_time = 0.0

    def call(self, func, *args, fallback=None, **kwargs):
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time >= self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                if fallback is not None:
                    return fallback()
                raise CircuitBreakerOpen("Circuit breaker is OPEN")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exceptions:
            self._on_failure()
            if fallback is not None:
                return fallback()
            raise

    def _on_success(self):
        self.failures = 0
        self.state = CircuitState.CLOSED

    def _on_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()
        if self.failures >= self.failure_threshold:
            self.state = CircuitState.OPEN


if __name__ == "__main__":
    import random

    def flaky_service():
        if random.random() < 0.7:
            raise ConnectionError("Service error")
        return "Data"

    breaker = CircuitBreaker(failure_threshold=2, recovery_timeout=1)

    for i in range(8):
        try:
            print(breaker.call(flaky_service,
                               fallback=lambda: "cached value"))
        except CircuitBreakerOpen:
            print(f"Call {i + 1}: rejected, state={breaker.state.name}")
        except Exception as e:
            print(f"Call {i + 1}: {type(e).__name__}: {e}")
        time.sleep(0.3)
