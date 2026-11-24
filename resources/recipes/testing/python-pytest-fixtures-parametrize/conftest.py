"""Shared fixtures for the python-pytest-fixtures-parametrize companion.

Demonstrates: session-scope env setup, a parametrized fixture driven by
``request.param``, and an autouse cleanup fixture.
"""

import os

import pytest


@pytest.fixture(scope="session")
def test_env():
    """Set test environment variables once per session."""
    previous = {k: os.environ.get(k) for k in ("APP_ENV", "DATABASE_URL")}
    os.environ["APP_ENV"] = "test"
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    yield
    for key, value in previous.items():
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value


@pytest.fixture(autouse=True)
def reset_state(test_env):
    """Auto-applied to every test: runs after each test for cleanup."""
    yield


@pytest.fixture
def user(request):
    """Build a user dict from the indirect parameter value."""
    return {"id": 1, "name": "Test User", "role": request.param}


@pytest.fixture(params=["sqlite", "postgres"], ids=["sqlite", "postgres"])
def db_engine(request):
    """Parametrized fixture: each consumer test runs once per engine."""
    return {"engine": request.param, "connected": True}
