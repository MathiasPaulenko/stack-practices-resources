"""Three-state circuit breaker — runnable companion code.

Companion to https://stackpractices.com/patterns/circuit-breaker-half-open-pattern/

Implements closed / open / half-open transitions with thread-safe state
checks and a unittest suite that exercises every transition.

Run the tests:

    python -m unittest circuit_breaker -v
"""

from __future__ import annotations

import threading
import time
import unittest
from enum import Enum


class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreakerOpenError(Exception):
    """Raised when the circuit is open and requests are rejected."""


class CircuitBreaker:
    """Circuit breaker with closed, open, and half-open states."""

    def __init__(self, failure_threshold=5, recovery_timeout=30,
                 half_open_max_calls=3, success_threshold=2):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_calls = half_open_max_calls
        self.success_threshold = success_threshold

        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._success_count = 0
        self._half_open_calls = 0
        self._last_failure_time = 0.0
        self._lock = threading.Lock()

    @property
    def state(self):
        with self._lock:
            self._check_state_transition()
            return self._state

    def _check_state_transition(self):
        if self._state == CircuitState.OPEN:
            if time.time() - self._last_failure_time >= self.recovery_timeout:
                self._state = CircuitState.HALF_OPEN
                self._half_open_calls = 0
                self._success_count = 0

    def call(self, fn, *args, **kwargs):
        with self._lock:
            self._check_state_transition()

            if self._state == CircuitState.OPEN:
                raise CircuitBreakerOpenError(
                    "Circuit is open: service unavailable"
                )

            if self._state == CircuitState.HALF_OPEN:
                if self._half_open_calls >= self.half_open_max_calls:
                    raise CircuitBreakerOpenError(
                        "Circuit is half-open: trial request limit reached"
                    )
                self._half_open_calls += 1

        try:
            result = fn(*args, **kwargs)
            self._on_success()
            return result
        except Exception:
            self._on_failure()
            raise

    def _on_success(self):
        with self._lock:
            if self._state == CircuitState.HALF_OPEN:
                self._success_count += 1
                if self._success_count >= self.success_threshold:
                    self._state = CircuitState.CLOSED
                    self._failure_count = 0
            elif self._state == CircuitState.CLOSED:
                self._failure_count = 0

    def _on_failure(self):
        with self._lock:
            self._last_failure_time = time.time()

            if self._state == CircuitState.HALF_OPEN:
                self._state = CircuitState.OPEN
                self._failure_count = 0
            elif self._state == CircuitState.CLOSED:
                self._failure_count += 1
                if self._failure_count >= self.failure_threshold:
                    self._state = CircuitState.OPEN

    def get_state(self):
        with self._lock:
            self._check_state_transition()
            return {
                "state": self._state.value,
                "failure_count": self._failure_count,
                "success_count": self._success_count,
                "half_open_calls": self._half_open_calls,
            }

    def reset(self):
        with self._lock:
            self._state = CircuitState.CLOSED
            self._failure_count = 0
            self._success_count = 0
            self._half_open_calls = 0


class TestCircuitBreaker(unittest.TestCase):
    def setUp(self):
        # Short timeouts so tests run fast
        self.b = CircuitBreaker(
            failure_threshold=2, recovery_timeout=0.05,
            half_open_max_calls=2, success_threshold=2,
        )

    @staticmethod
    def fail():
        raise RuntimeError("downstream error")

    @staticmethod
    def ok():
        return "ok"

    def test_closed_passes_calls(self):
        self.assertEqual(self.b.call(self.ok), "ok")

    def _open_breaker(self):
        for _ in range(2):
            with self.assertRaises(RuntimeError):
                self.b.call(self.fail)
        self.assertEqual(self.b.state, CircuitState.OPEN)

    def test_opens_after_threshold(self):
        self._open_breaker()
        with self.assertRaises(CircuitBreakerOpenError):
            self.b.call(self.ok)

    def test_open_transitions_to_half_open_after_timeout(self):
        self._open_breaker()
        time.sleep(0.06)
        self.assertEqual(self.b.state, CircuitState.HALF_OPEN)

    def test_half_open_closes_on_enough_successes(self):
        self._open_breaker()
        time.sleep(0.06)
        self.b.call(self.ok)
        self.assertEqual(self.b.state, CircuitState.HALF_OPEN)
        self.b.call(self.ok)
        self.assertEqual(self.b.state, CircuitState.CLOSED)

    def test_half_open_reopens_on_failure(self):
        self._open_breaker()
        time.sleep(0.06)
        with self.assertRaises(RuntimeError):
            self.b.call(self.fail)
        self.assertEqual(self.b.state, CircuitState.OPEN)

    def test_half_open_trial_limit(self):
        self._open_breaker()
        time.sleep(0.06)
        self.b.state  # property triggers transition to half-open
        # burn the trial budget
        self.b._half_open_calls = self.b.half_open_max_calls
        with self.assertRaises(CircuitBreakerOpenError):
            self.b.call(self.ok)

    def test_success_resets_failure_count(self):
        with self.assertRaises(RuntimeError):
            self.b.call(self.fail)  # count = 1
        self.b.call(self.ok)      # count resets to 0
        with self.assertRaises(RuntimeError):
            self.b.call(self.fail)  # count = 1 again, not 2
        self.assertEqual(self.b.state, CircuitState.CLOSED)


if __name__ == "__main__":
    unittest.main()
