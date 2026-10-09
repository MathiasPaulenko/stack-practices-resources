"""Shared pytest fixtures — auto-discovered by every test in this directory.

Usage:
    pytest -v
"""

from dataclasses import dataclass

import pytest


@dataclass
class User:
    id: int
    name: str
    email: str
    role: str = "user"

    def can_delete(self) -> bool:
        return self.role == "admin"

    def can_edit(self) -> bool:
        return self.role in ("admin", "editor")


@pytest.fixture
def admin_user() -> User:
    """Fresh object per test (default function scope)."""
    return User(id=1, name="Alice", email="alice@example.com", role="admin")


@pytest.fixture
def temp_file(tmp_path):
    """Fixture with teardown via yield."""
    path = tmp_path / "data.txt"
    path.write_text("seed")
    yield path
    # tmp_path is cleaned by pytest; add explicit cleanup for real resources


@pytest.fixture(params=["admin", "editor", "viewer"])
def role(request) -> str:
    """Parametrized fixture: each test runs once per value."""
    return request.param


@pytest.fixture
def user_factory():
    """Factory fixture: builds variants on demand with deterministic IDs."""
    _counter = 0

    def make(name=None, role="user"):
        nonlocal _counter
        _counter += 1
        return User(
            id=_counter,
            name=name or f"user_{_counter}",
            email=f"user_{_counter}@test.com",
            role=role,
        )

    return make


@pytest.fixture(scope="session")
def app_config():
    """Session scope: expensive setup computed once per run."""
    return {"env": "test", "debug": False}
