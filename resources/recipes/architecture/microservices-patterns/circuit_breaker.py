"""Circuit breaker implemented from scratch (stdlib only).

Companion to https://stackpractices.com/recipes/microservices-patterns/
States: CLOSED -> OPEN (failure threshold) -> HALF_OPEN (recovery timeout)
-> CLOSED on successful probes.
"""

import time
from enum import Enum


class CircuitState(Enum):
    CLOSED = "closed"        # Normal operation
    OPEN = "open"            # Failing, reject fast
    HALF_OPEN = "half_open"  # Testing recovery


class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=30, half_open_max_calls=3):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_calls = half_open_max_calls
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None
        self.half_open_calls = 0

    def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
                self.half_open_calls = 0
            else:
                raise Exception("Circuit breaker is OPEN")

        if self.state == CircuitState.HALF_OPEN:
            if self.half_open_calls >= self.half_open_max_calls:
                raise Exception("Circuit breaker is HALF_OPEN (max calls reached)")
            self.half_open_calls += 1

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e

    def _on_success(self):
        self.failure_count = 0
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.CLOSED
            self.half_open_calls = 0

    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN


if __name__ == "__main__":
    breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=10)

    def get_user_profile(user_id):
        # HTTP call to user service
        raise ConnectionError("user-service unreachable")

    def get_cached_profile(user_id):
        return {"id": user_id, "name": "cached"}

    try:
        profile = breaker.call(get_user_profile, user_id=123)
    except Exception:
        profile = get_cached_profile(123)  # Fallback
    print(profile)
