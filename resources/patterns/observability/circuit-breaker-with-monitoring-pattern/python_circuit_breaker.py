"""Monitored Circuit Breaker with Prometheus metrics."""
import time
from enum import Enum
from prometheus_client import Gauge, Counter, Histogram, CollectorRegistry


class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreakerOpenError(Exception):
    pass


class MonitoredCircuitBreaker:
    def __init__(
        self,
        service_name,
        endpoint,
        failure_threshold=5,
        recovery_timeout=60,
        half_open_max_calls=3,
        registry=None,
    ):
        self.service = service_name
        self.endpoint = endpoint
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_calls = half_open_max_calls

        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._success_count = 0
        self._half_open_calls = 0
        self._last_failure_time = None
        self._opened_at = None

        reg = registry or _default_registry
        self._state_gauge = Gauge(
            "circuit_breaker_state",
            "Circuit breaker state (0=closed, 1=open, 2=half_open)",
            ["service", "endpoint"],
            registry=reg,
        )
        self._failures = Counter(
            "circuit_breaker_failures_total",
            "Total failures",
            ["service", "endpoint"],
            registry=reg,
        )
        self._successes = Counter(
            "circuit_breaker_successes_total",
            "Total successes",
            ["service", "endpoint"],
            registry=reg,
        )
        self._rejected = Counter(
            "circuit_breaker_rejected_total",
            "Total rejected calls",
            ["service", "endpoint"],
            registry=reg,
        )
        self._transitions = Counter(
            "circuit_breaker_state_transitions_total",
            "State transitions",
            ["service", "endpoint", "from_state", "to_state"],
            registry=reg,
        )
        self._open_duration = Histogram(
            "circuit_breaker_open_duration_seconds",
            "How long the breaker stayed open",
            ["service", "endpoint"],
            buckets=[1, 5, 10, 30, 60, 120, 300, 600],
            registry=reg,
        )

        self._update_state_metric()

    def _update_state_metric(self):
        state_map = {
            CircuitState.CLOSED: 0,
            CircuitState.OPEN: 1,
            CircuitState.HALF_OPEN: 2,
        }
        self._state_gauge.labels(
            service=self.service, endpoint=self.endpoint
        ).set(state_map[self._state])

    def _transition(self, new_state):
        old_state = self._state
        if old_state == new_state:
            return

        self._transitions.labels(
            service=self.service,
            endpoint=self.endpoint,
            from_state=old_state.value,
            to_state=new_state.value,
        ).inc()

        if old_state == CircuitState.OPEN and new_state == CircuitState.CLOSED:
            if self._opened_at:
                duration = time.time() - self._opened_at
                self._open_duration.labels(
                    service=self.service, endpoint=self.endpoint
                ).observe(duration)

        self._state = new_state
        self._update_state_metric()

        if new_state == CircuitState.OPEN:
            self._opened_at = time.time()
        elif new_state == CircuitState.CLOSED:
            self._opened_at = None
            self._failure_count = 0
            self._success_count = 0

    @property
    def state(self):
        return self._state

    def call(self, func, *args, **kwargs):
        if self._state == CircuitState.OPEN:
            if self._last_failure_time and time.time() - self._last_failure_time > self.recovery_timeout:
                self._transition(CircuitState.HALF_OPEN)
                self._half_open_calls = 0
            else:
                self._rejected.labels(
                    service=self.service, endpoint=self.endpoint
                ).inc()
                raise CircuitBreakerOpenError(
                    f"Circuit breaker open for {self.service}/{self.endpoint}"
                )

        if self._state == CircuitState.HALF_OPEN:
            if self._half_open_calls >= self.half_open_max_calls:
                self._rejected.labels(
                    service=self.service, endpoint=self.endpoint
                ).inc()
                raise CircuitBreakerOpenError("Half-open call limit reached")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception:
            self._on_failure()
            raise

    def _on_success(self):
        self._successes.labels(
            service=self.service, endpoint=self.endpoint
        ).inc()

        if self._state == CircuitState.HALF_OPEN:
            self._success_count += 1
            self._half_open_calls += 1
            if self._success_count >= self.half_open_max_calls:
                self._transition(CircuitState.CLOSED)
        elif self._state == CircuitState.CLOSED:
            self._failure_count = 0

    def _on_failure(self):
        self._failures.labels(
            service=self.service, endpoint=self.endpoint
        ).inc()
        self._last_failure_time = time.time()

        if self._state == CircuitState.HALF_OPEN:
            self._transition(CircuitState.OPEN)
        elif self._state == CircuitState.CLOSED:
            self._failure_count += 1
            if self._failure_count >= self.failure_threshold:
                self._transition(CircuitState.OPEN)


_default_registry = CollectorRegistry()
