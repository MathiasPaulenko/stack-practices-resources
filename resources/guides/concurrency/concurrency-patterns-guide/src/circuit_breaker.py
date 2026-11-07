"""Async circuit breaker: CLOSED -> OPEN -> HALF_OPEN.

Key details: rejections while OPEN do not count as dependency failures,
and timeouts use time.monotonic() so a clock adjustment can't wedge the
circuit open.

Run: python circuit_breaker.py
"""

import asyncio
import time
from enum import Enum


class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreakerOpen(Exception):
    """Raised when the circuit is OPEN and the call is rejected fast."""


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_timeout: float = 1.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.state = CircuitState.CLOSED
        self.last_failure_time = 0.0
        self._lock = asyncio.Lock()

    async def call(self, func, *args, **kwargs):
        async with self._lock:
            if self.state is CircuitState.OPEN:
                if time.monotonic() - self.last_failure_time > self.recovery_timeout:
                    self.state = CircuitState.HALF_OPEN
                else:
                    raise CircuitBreakerOpen("circuit breaker is OPEN")
        try:
            result = await func(*args, **kwargs)
        except Exception:
            async with self._lock:
                self.failure_count += 1
                self.last_failure_time = time.monotonic()
                if self.failure_count >= self.failure_threshold:
                    self.state = CircuitState.OPEN
            raise
        async with self._lock:
            self.failure_count = 0
            self.state = CircuitState.CLOSED
        return result


async def flaky_service(succeed: bool) -> str:
    await asyncio.sleep(0.01)
    if not succeed:
        raise ConnectionError("service unavailable")
    return "ok"


async def main() -> None:
    breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=0.5)

    for i in range(3):
        try:
            await breaker.call(flaky_service, succeed=False)
        except ConnectionError:
            print(f"call {i + 1}: real failure ({breaker.failure_count})")

    try:
        await breaker.call(flaky_service, succeed=True)
    except CircuitBreakerOpen:
        print("call rejected fast — circuit OPEN, failure_count still",
              breaker.failure_count)

    await asyncio.sleep(0.6)  # let the recovery timeout elapse
    result = await breaker.call(flaky_service, succeed=True)
    print(f"probe succeeded: {result} — circuit back to {breaker.state.value}")


if __name__ == "__main__":
    asyncio.run(main())
