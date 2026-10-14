"""Shared pytest fixtures: scopes, yield teardown, env vars, fixture object.

Run:  pytest -v
"""

import os
import sqlite3
import subprocess
import tempfile
import time

import pytest


class UserService:
    """Minimal service used by the example tests."""

    def __init__(self, repo):
        self.repo = repo
        self.notifier = None

    def set_notifier(self, notifier):
        self.notifier = notifier

    def create_user(self, name, email):
        if any(u["email"] == email for u in self.repo.find_all("users")):
            raise DuplicateEmailError(email)
        user = {"name": name, "email": email}
        self.repo.insert("users", user)
        if self.notifier:
            self.notifier.send(to=email, subject="Welcome")
        return user

    def get_user_by_email(self, email):
        for u in self.repo.find_all("users"):
            if u["email"] == email:
                return u
        return None


class DuplicateEmailError(Exception):
    pass


class FakeUserRepository:
    """In-memory stand-in for a real repository (a 'fake' test double)."""

    def __init__(self):
        self._tables = {"users": []}

    def insert(self, table, row):
        self._tables[table].append(row)

    def find_all(self, table):
        return list(self._tables[table])

    def find_one(self, table, where):
        for row in self._tables[table]:
            if all(row.get(k) == v for k, v in where.items()):
                return row
        return None

    def count(self, table):
        return len(self._tables[table])

    def clear(self):
        for t in self._tables.values():
            t.clear()


# --- function scope: fresh repo per test ---------------------------------

@pytest.fixture
def repo():
    return FakeUserRepository()


@pytest.fixture
def service(repo):
    return UserService(repo)


@pytest.fixture
def service_with_user(service):
    service.create_user("Alice", "alice@x.com")
    return service


# --- yield teardown: temp SQLite file cleaned up after each test ---------

@pytest.fixture
def temp_db():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    db = sqlite3.connect(path)
    db.execute("CREATE TABLE users (name TEXT, email TEXT)")

    yield db  # test runs here

    # teardown: runs even if the test fails
    db.close()
    os.unlink(path)


# --- module scope: shared read-only context -------------------------------

@pytest.fixture(scope="module")
def test_config():
    return {"app_env": "test", "retries": 3}


# --- env var fixture: sets and restores os.environ ------------------------

@pytest.fixture
def env_vars():
    original = dict(os.environ)
    os.environ["APP_ENV"] = "test"
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"

    yield os.environ

    os.environ.clear()
    os.environ.update(original)


# --- fixture object: bundle collaborators behind one handle --------------

@pytest.fixture
def test_context(service):
    from unittest.mock import MagicMock

    notifier = MagicMock()
    service.set_notifier(notifier)

    class TestContext:
        def __init__(self, repo, service, notifier):
            self.repo = repo
            self.service = service
            self.notifier = notifier

        def create_user(self, name, email):
            return self.service.create_user(name, email)

        def assert_notified(self, email):
            self.notifier.send.assert_called_once()
            assert self.notifier.send.call_args.kwargs["to"] == email

    return TestContext(service.repo, service, notifier)


# --- external resource: disposable postgres via Docker --------------------

@pytest.fixture(scope="session")
def postgres_container():
    """Disposable postgres container; requires docker on PATH."""
    container_id = subprocess.check_output([
        "docker", "run", "-d", "-p", "5432:5432",
        "-e", "POSTGRES_PASSWORD=test",
        "postgres:16-alpine",
    ]).decode().strip()

    # Poll readiness instead of sleeping a fixed amount
    for _ in range(30):
        ready = subprocess.run(
            ["docker", "exec", container_id, "pg_isready"],
            capture_output=True,
        )
        if ready.returncode == 0:
            break
        time.sleep(1)
    else:
        subprocess.run(["docker", "stop", container_id])
        raise RuntimeError("postgres container did not become ready")

    yield {"host": "localhost", "port": "5432", "password": "test"}

    subprocess.run(["docker", "stop", container_id])
    subprocess.run(["docker", "rm", container_id])
