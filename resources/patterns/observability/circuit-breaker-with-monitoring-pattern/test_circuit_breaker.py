"""Tests for MonitoredCircuitBreaker."""
import time
import pytest
from prometheus_client import CollectorRegistry
from python_circuit_breaker import (
    MonitoredCircuitBreaker,
    CircuitState,
    CircuitBreakerOpenError,
)


@pytest.fixture
def registry():
    return CollectorRegistry()


@pytest.fixture
def breaker(registry):
    return MonitoredCircuitBreaker(
        "test-service",
        "/api/test",
        failure_threshold=3,
        recovery_timeout=60,
        half_open_max_calls=2,
        registry=registry,
    )


@pytest.fixture
def fast_breaker(registry):
    """Breaker with recovery_timeout=0 for half-open transition tests."""
    return MonitoredCircuitBreaker(
        "test-service",
        "/api/test",
        failure_threshold=3,
        recovery_timeout=0,
        half_open_max_calls=2,
        registry=registry,
    )


def _fail():
    raise ValueError("boom")


def _ok():
    return "ok"


class TestStateTransitions:
    def test_starts_closed(self, breaker):
        assert breaker.state == CircuitState.CLOSED

    def test_closed_to_open_on_threshold(self, breaker):
        for _ in range(3):
            with pytest.raises(ValueError):
                breaker.call(_fail)
        assert breaker.state == CircuitState.OPEN

    def test_open_rejects_calls(self, breaker):
        for _ in range(3):
            with pytest.raises(ValueError):
                breaker.call(_fail)
        with pytest.raises(CircuitBreakerOpenError):
            breaker.call(_ok)

    def test_open_to_half_open_after_timeout(self, fast_breaker):
        for _ in range(3):
            with pytest.raises(ValueError):
                fast_breaker.call(_fail)
        assert fast_breaker.state == CircuitState.OPEN
        time.sleep(0.01)
        fast_breaker.call(_ok)
        assert fast_breaker.state in (CircuitState.HALF_OPEN, CircuitState.CLOSED)

    def test_half_open_to_closed_on_successes(self, fast_breaker):
        for _ in range(3):
            with pytest.raises(ValueError):
                fast_breaker.call(_fail)
        time.sleep(0.01)
        fast_breaker.call(_ok)
        fast_breaker.call(_ok)
        assert fast_breaker.state == CircuitState.CLOSED

    def test_half_open_to_open_on_failure(self, fast_breaker):
        for _ in range(3):
            with pytest.raises(ValueError):
                fast_breaker.call(_fail)
        time.sleep(0.01)
        fast_breaker.call(_ok)
        with pytest.raises(ValueError):
            fast_breaker.call(_fail)
        assert fast_breaker.state == CircuitState.OPEN


class TestMetricEmission:
    def test_state_metric_set_on_init(self, breaker, registry):
        samples = list(registry.collect())
        state_metric = [s for s in samples if s.name == "circuit_breaker_state"]
        assert len(state_metric) > 0

    def test_failures_increment_on_failure(self, breaker, registry):
        with pytest.raises(ValueError):
            breaker.call(_fail)
        samples = list(registry.collect())
        failures = [s for s in samples if s.name == "circuit_breaker_failures"]
        assert len(failures) > 0
        assert failures[0].samples[0].value == 1.0

    def test_successes_increment_on_success(self, breaker, registry):
        breaker.call(_ok)
        samples = list(registry.collect())
        successes = [s for s in samples if s.name == "circuit_breaker_successes"]
        assert len(successes) > 0
        assert successes[0].samples[0].value == 1.0

    def test_rejected_increment_when_open(self, breaker, registry):
        for _ in range(3):
            with pytest.raises(ValueError):
                breaker.call(_fail)
        with pytest.raises(CircuitBreakerOpenError):
            breaker.call(_ok)
        samples = list(registry.collect())
        rejected = [s for s in samples if s.name == "circuit_breaker_rejected"]
        assert len(rejected) > 0
        assert rejected[0].samples[0].value >= 1.0

    def test_transitions_increment_on_state_change(self, breaker, registry):
        for _ in range(3):
            with pytest.raises(ValueError):
                breaker.call(_fail)
        samples = list(registry.collect())
        transitions = [
            s for s in samples
            if s.name == "circuit_breaker_state_transitions"
        ]
        assert len(transitions) > 0
        total = sum(sample.value for sample in transitions[0].samples)
        assert total >= 1.0
