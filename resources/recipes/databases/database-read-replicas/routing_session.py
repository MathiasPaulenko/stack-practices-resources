"""SQLAlchemy read/write splitting session for PostgreSQL read replicas.

Usage:
    from routing_session import RoutingSession

    session = RoutingSession(
        primary_url="postgresql://user:pass@primary:5432/app",
        replica_urls=[
            "postgresql://user:pass@replica1:5432/app",
            "postgresql://user:pass@replica2:5432/app",
        ],
    )
    users = session.execute_read("SELECT * FROM users WHERE active = true")
    session.execute_write(
        "UPDATE users SET last_login = NOW() WHERE id = :id", {"id": 1}
    )
    session.commit()
"""

import random

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


class RoutingSession:
    """Route reads to replicas and writes to the primary."""

    def __init__(self, primary_url, replica_urls):
        self._primary_engine = create_engine(primary_url)
        self._replica_engines = [
            create_engine(url) for url in replica_urls
        ]
        self._write_session = sessionmaker(bind=self._primary_engine)()
        self._replica = random.choice(self._replica_engines)
        self._read_session = sessionmaker(bind=self._replica)()

    def execute_write(self, query, params=None):
        return self._write_session.execute(text(query), params or {})

    def execute_read(self, query, params=None):
        return self._read_session.execute(text(query), params or {})

    def commit(self):
        self._write_session.commit()

    def close(self):
        self._write_session.close()
        self._read_session.close()


if __name__ == "__main__":
    session = RoutingSession(
        primary_url="postgresql://user:pass@localhost:5432/app",
        replica_urls=[
            "postgresql://user:pass@localhost:5433/app",
        ],
    )
    result = session.execute_read("SELECT 1 AS test")
    print(f"Read test: {result.fetchone()}")
    session.close()
