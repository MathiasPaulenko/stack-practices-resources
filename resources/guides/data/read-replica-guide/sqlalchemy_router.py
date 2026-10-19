"""SQLAlchemy session that routes reads to a random replica, writes to the primary."""
import random

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

primary_engine = create_engine("postgresql://user:pass@primary:5432/app")
replica_engines = [
    create_engine("postgresql://user:pass@replica1:5432/app"),
    create_engine("postgresql://user:pass@replica2:5432/app"),
]


class RoutingSession:
    def __init__(self):
        self._write_session = sessionmaker(bind=primary_engine)()
        self._read_session = sessionmaker(bind=random.choice(replica_engines))()

    def execute_write(self, query, params=None):
        return self._write_session.execute(text(query), params or {})

    def execute_read(self, query, params=None):
        return self._read_session.execute(text(query), params or {})

    def commit(self):
        self._write_session.commit()


if __name__ == "__main__":
    session = RoutingSession()
    users = session.execute_read("SELECT * FROM users WHERE active = true")
    session.execute_write(
        "UPDATE users SET last_login = NOW() WHERE id = :id", {"id": 1}
    )
    session.commit()
