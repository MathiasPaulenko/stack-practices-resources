"""Tests for pg_pool.py using mocked psycopg2 pool."""

import sys
import pytest
from unittest.mock import MagicMock, patch
from types import ModuleType


@pytest.fixture(autouse=True)
def mock_psycopg2():
    """Inject a fake psycopg2 module before importing pg_pool."""
    fake_psycopg2 = ModuleType("psycopg2")
    fake_pool_mod = ModuleType("psycopg2.pool")

    class FakeThreadedConnectionPool:
        def __init__(self, minconn, maxconn, **kwargs):
            self.minconn = minconn
            self.maxconn = maxconn
            self._closed = False
            self._borrowed = []

        def getconn(self):
            conn = MagicMock()
            self._borrowed.append(conn)
            return conn

        def putconn(self, conn):
            if conn in self._borrowed:
                self._borrowed.remove(conn)

    fake_pool_mod.ThreadedConnectionPool = FakeThreadedConnectionPool
    fake_psycopg2.pool = fake_pool_mod

    with patch.dict(sys.modules, {
        "psycopg2": fake_psycopg2,
        "psycopg2.pool": fake_pool_mod,
    }):
        sys.modules.pop("pg_pool", None)
        yield


def test_get_conn_returns_connection():
    import pg_pool
    with pg_pool.get_conn() as conn:
        assert conn is not None
    # Connection was borrowed and returned
    assert len(pg_pool.pg_pool._borrowed) == 0


def test_get_conn_rollback_on_exception():
    import pg_pool
    with pytest.raises(ValueError):
        with pg_pool.get_conn() as conn:
            raise ValueError("boom")
    conn.rollback.assert_called_once()
    assert len(pg_pool.pg_pool._borrowed) == 0


def test_get_conn_commit_on_success():
    import pg_pool
    with pg_pool.get_conn() as conn:
        pass
    conn.commit.assert_called_once()
    assert len(pg_pool.pg_pool._borrowed) == 0


def test_get_user_returns_row():
    import pg_pool
    with patch.object(pg_pool, "pg_pool") as mock_pool:
        fake_conn = MagicMock()
        mock_pool.getconn.return_value = fake_conn
        fake_cursor = MagicMock()
        fake_conn.cursor.return_value.__enter__ = MagicMock(return_value=fake_cursor)
        fake_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
        fake_cursor.fetchone.return_value = (1, "Alice")

        result = pg_pool.get_user(1)
        assert result == (1, "Alice")
        fake_cursor.execute.assert_called_once_with(
            "SELECT * FROM users WHERE id = %s", (1,)
        )


def test_pool_status_returns_metrics():
    import pg_pool
    status = pg_pool.pool_status()
    assert status["minconn"] == 5
    assert status["maxconn"] == 20
    assert status["closed"] is False


def test_get_conn_always_returns_to_pool():
    import pg_pool
    with pg_pool.get_conn() as conn:
        pass
    assert len(pg_pool.pg_pool._borrowed) == 0


def test_get_conn_nested_context():
    import pg_pool
    with pg_pool.get_conn() as c1:
        assert c1 is not None
    with pg_pool.get_conn() as c2:
        assert c2 is not None
    assert len(pg_pool.pg_pool._borrowed) == 0