import pytest

from token_bucket import TokenBucket


class ManualClock:
    def __init__(self):
        self.t = 0.0

    def __call__(self):
        return self.t

    def advance(self, seconds):
        self.t += seconds


def make(capacity=5, refill_rate=1.0):
    clock = ManualClock()
    return TokenBucket(capacity, refill_rate, clock=clock), clock


def test_burst_up_to_capacity():
    b, _ = make(capacity=5)
    assert [b.consume() for _ in range(6)] == [True] * 5 + [False]


def test_refill_after_time_passes():
    b, clock = make(capacity=2, refill_rate=1.0)
    b.consume(); b.consume(); b.consume()  # empty
    clock.advance(1.5)
    assert b.consume() is True


def test_refill_capped_at_capacity():
    b, clock = make(capacity=3, refill_rate=10.0)
    b.consume()
    clock.advance(60)  # way past full
    assert sum(b.consume() for _ in range(4)) == 3


def test_rejects_when_empty_without_time():
    b, _ = make(capacity=1, refill_rate=0.1)
    assert b.consume() is True
    assert b.consume() is False


def test_retry_after_zero_when_tokens_available():
    b, _ = make(capacity=2, refill_rate=2.0)
    assert b.retry_after() == 0.0


def test_retry_after_positive_when_empty():
    b, _ = make(capacity=1, refill_rate=2.0)
    b.consume()
    assert b.retry_after() == pytest.approx(0.5)


def test_multi_token_consume():
    b, _ = make(capacity=4, refill_rate=1.0)
    assert b.consume(tokens=3) is True
    assert b.consume(tokens=2) is False
