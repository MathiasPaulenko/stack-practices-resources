"""Offline unit tests — no API calls needed. Run: pytest test_cost.py -v"""
from budget import BudgetController
from router import ModelRouter
from cache import LLMCache


def test_router_picks_mini_for_simple():
    r = ModelRouter()
    assert r.select_model("classify this as good or bad") == "gpt-4o-mini"
    assert r.select_model("hi") == "gpt-4o-mini"


def test_router_picks_flagship_for_complex():
    r = ModelRouter()
    assert r.select_model("write a full auth system with OAuth2") == "gpt-4o"


def test_budget_soft_then_hard():
    b = BudgetController(daily_budget=1.0, alert_at=0.5)
    assert b.check(0.3) == "ok"
    b.record("gpt-4o", 100_000, 0)  # $0.25
    assert b.check(0.4) == "alert"
    assert b.check(1.0) == "stop"


def test_exact_cache_roundtrip():
    c = LLMCache(ttl_hours=24)
    msgs = [{"role": "user", "content": "hi"}]
    c.set("gpt-4o", msgs, "hello")
    assert c.get("gpt-4o", msgs) == "hello"
    assert c.get
