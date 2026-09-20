"""Tests for ambassador.py — companion to the Ambassador pattern."""

import pytest

from ambassador import (
    ServiceAmbassador,
    MonitoringAmbassador,
    RemoteError,
    CircuitOpenError,
)


class Fake:
    """Controllable remote + fake clock + recorded sleeps."""

    def __init__(self, outcomes):
        self.outcomes = list(outcomes)
        self.calls = 0
        self.sleeps = []
        self.now = [0.0]

    def remote(self):
        self.calls += 1
        outcome = self.outcomes.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome

    def sleep(self, s):
        self.sleeps.append(s)

    def clock(self):
        return self.now[0]

    def ambassador(self, **kw):
        kw.setdefault("sleep", self.sleep)
        kw.setdefault("clock", self.clock)
        kw.setdefault("jitter_s", 0.0)
        return ServiceAmbassador(self.remote, **kw)


def test_succeeds_after_retries():
    f = Fake([RemoteError("503"), RemoteError("503"), {"id": 1}])
    assert f.ambassador(base_delay_s=1.0).call() == {"id": 1}
    assert f.calls == 3


def test_exponential_backoff_delays():
    f = Fake([RemoteError("x")] * 4)
    with pytest.raises(RemoteError):
        f.ambassador(retry_count=4, base_delay_s=1.0).call()
    # 1s, 2s, 4s — doubling each attempt, not linear
    assert f.sleeps == [1.0, 2.0, 4.0]


def test_gives_up_after_max_retries():
    f = Fake([RemoteError("x")] * 5)
    with pytest.raises(RemoteError):
        f.ambassador(retry_count=3, base_delay_s=0.01).call()
    assert f.calls == 3  # never more than retry_count


def test_circuit_opens_and_fails_fast():
    f = Fake([RemoteError("x")] * 10)
    a = f.ambassador(retry_count=1, failure_threshold=3, base_delay_s=0)
    for _ in range(3):
        with pytest.raises(RemoteError):
            a.call()
    assert a.state == "open"
    calls_before = f.calls
    with pytest.raises(CircuitOpenError):
        a.call()
    assert f.calls == calls_before  # no remote hit — failed fast


def test_half_open_trial_then_closed():
    f = Fake([RemoteError("x")] * 3 + [{"ok": True}])
    a = f.ambassador(retry_count=1, failure_threshold=3, reset_after_s=30)
    for _ in range(3):
        with pytest.raises(RemoteError):
            a.call()
    assert a.state == "open"
    f.now[0] = 31.0  # cool-down elapsed
    assert a.call() == {"ok": True}
    assert a.state == "closed"


def test_failed_half_open_reopens_immediately():
    f = Fake([RemoteError("x")] * 4)
    a = f.ambassador(retry_count=1, failure_threshold=3, reset_after_s=30)
    for _ in range(3):
        with pytest.raises(RemoteError):
            a.call()
    f.now[0] = 31.0
    with pytest.raises(RemoteError):
        a.call()
    assert a.state == "open"  # trial failed -> re-opened, not retried freely


def test_monitoring_counts_outcomes():
    f = Fake([RemoteError("x"), {"ok": True}])
    monitored = MonitoringAmbassador(f.ambassador(base_delay_s=0))
    assert monitored.call() == {"ok": True}
    m = monitored.metrics()
    assert m["requests"] == 1 and m["errors"] == 0
    # The monitor sees the final result, not the per-attempt failure
    assert m["requests"] == 1


def test_monitoring_counts_errors():
    f = Fake([RemoteError("x")] * 3)
    monitored = MonitoringAmbassador(f.ambassador(retry_count=3, base_delay_s=0))
    with pytest.raises(RemoteError):
        monitored.call()
    assert monitored.metrics()["errors"] == 1
