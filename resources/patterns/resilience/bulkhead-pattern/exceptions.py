# exceptions.py — Shared exceptions for the bulkhead examples.


class BulkheadFullError(Exception):
    """Raised when a bulkhead's pool and queue are exhausted."""
    pass


class CircuitBreakerOpenError(Exception):
    """Raised when a circuit breaker is open and calls are blocked."""
    pass
