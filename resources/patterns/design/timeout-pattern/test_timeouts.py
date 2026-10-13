"""Tests for the timeout wrappers."""

import time

import pytest

from with_timeout import with_timeout
from deadline_budget import DeadlineBudget, BudgetExceeded, api_handler, db_query


def test_with_timeout_passes_fast_calls():
    @with_timeout(seconds=2.0)
    def quick():
        return "ok"

    assert quick() == "ok"


def test_with_timeout_raises_on_slow_calls():
    @with_timeout(seconds=0.2)
    def slow():
        time.sleep(5)

    with pytest.raises(TimeoutError):
        slow()


def test_budget_shrinks_down_the_chain():
    budget = DeadlineBudget(5.0)
    time.sleep(0.05)
    assert budget.remaining() < 5.0
    assert api_handler(budget) == "rows"


def test_expired_budget_fails_fast():
    budget = DeadlineBudget(0.001)
    time.sleep(0.01)
    with pytest.raises(BudgetExceeded):
        api_handler(budget)


def test_db_query_respects_inner_timeout():
    with pytest.raises(BudgetExceeded):
        db_query(0.0)
