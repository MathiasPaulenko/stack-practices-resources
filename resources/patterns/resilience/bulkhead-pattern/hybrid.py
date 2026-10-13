# hybrid.py — Bulkhead combined with a circuit breaker.
import time
import threading

from exceptions import BulkheadFullError, CircuitBreakerOpenError


class BulkheadWithCircuitBreaker:
    """Combines bulkhead (concurrency limit) with circuit breaker (failure limit).
    The bulkhead prevents resource exhaustion; the circuit breaker prevents
    calling a failing service."""

    def __init__(self, max_concurrent, failure_threshold=5, recovery_timeout=30):
        self._semaphore = threading.Semaphore(max_concurrent)
        self._failure_count = 0
        self._failure_threshold = failure_threshold
        self._recovery_timeout = recovery_timeout
        self._circuit_open = False
        self._last_failure = 0
        self._lock = threading.Lock()

    def call(self, fn, *args, **kwargs):
        with self._lock:
            if self._circuit_open:
                if time.time() - self._last_failure > self._recovery_timeout:
                    self._circuit_open = False
                    self._failure_count = 0
                else:
                    raise CircuitBreakerOpenError("Circuit is open")

        if not self._semaphore.acquire(timeout=10):
            raise BulkheadFullError("Bulkhead is full")

        try:
            result = fn(*args, **kwargs)
            with self._lock:
                self._failure_count = 0
                self._circuit_open = False
            return result
        except Exception:
            with self._lock:
                self._failure_count += 1
                self._last_failure = time.time()
                if self._failure_count >= self._failure_threshold:
                    self._circuit_open = True
            raise
        finally:
            self._semaphore.release()


if __name__ == "__main__":
    protected = BulkheadWithCircuitBreaker(max_concurrent=5)

    def flaky_api():
        return {"ok": True}

    print(protected.call(flaky_api))
