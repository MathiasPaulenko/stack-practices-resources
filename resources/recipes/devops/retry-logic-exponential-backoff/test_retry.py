"""Tests for the retry decorator — uses an injected fake sleep so runs are instant."""

import pytest
from retry import retry


def recorded_sleep(delays):
    return lambda d: delays.append(d)


def test_succeeds_first_try():
    delays = []

    @retry(max_retries=3, sleep=recorded_sleep(delays))
    def ok():
        return "done"

    assert ok() == "done"
    assert delays == []


def test_retries_until_success():
    delays = []
    calls = {"n": 0}

    @retry(max_retries=3, base_delay=1.0, jitter=False, sleep=recorded_sleep(delays))
    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise ConnectionError("transient")
        return "ok"

    assert flaky() == "ok"
    assert calls["n"] == 3
    # no jitter: exponential delays are exactly 1s and 2s
    assert delays == [1.0, 2.0]


def test_raises_after_max_retries():
    delays = []

    @retry(max_retries=2, jitter=False, sleep=recorded_sleep(delays))
    def always_fails():
        raise TimeoutError("boom")

    with pytest.raises(TimeoutError):
        always_fails()
    assert delays == [1.0, 2.0]


def test_jitter_stays_within_cap():
    delays = []

    @retry(max_retries=3, base_delay=1.0, max_delay=60.0, jitter=True,
           sleep=recorded_sleep(delays))
    def always_fails():
        raise ValueError("boom")

    with pytest.raises(ValueError):
        always_fails()
    for i, d in enumerate(delays):
        assert 0 <= d <= min(1.0 * (2 ** i), 60.0)


def test_exception_filtering_skips_retries():
    delays = []

    @retry(max_retries=3, exceptions=(ConnectionError,), jitter=False,
           sleep=recorded_sleep(delays))
    def validation_error():
        raise ValueError("client error — never retry")

    with pytest.raises(ValueError):
        validation_error()
    assert delays == []


def test_on_retry_callback_fires():
    events = []

    @retry(max_retries=2, jitter=False, sleep=lambda d: None,
           on_retry=lambda e, n, d: events.append((n, d)))
    def flaky():
        raise ConnectionError("x")

    with pytest.raises(ConnectionError):
        flaky()
    assert events == [(1, 1.0), (2, 2.0)]
