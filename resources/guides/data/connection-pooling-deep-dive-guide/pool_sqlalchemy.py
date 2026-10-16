"""SQLAlchemy pool configuration with safe connection usage.

See https://stackpractices.com/guides/connection-pooling-deep-dive-guide/
"""
import os

from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql://app:secret@localhost/app",
    pool_size=10,           # minimum connections maintained
    max_overflow=5,         # extra connections beyond pool_size
    pool_timeout=30,        # seconds waiting for an available connection
    pool_recycle=1800,      # recycle connections after 30 minutes
    pool_pre_ping=True,     # verify the connection is alive before handing it out
    echo=False,
)


def get_user(user_id: int):
    """Connections return to the pool automatically via the context manager."""
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM users WHERE id = :id"), {"id": user_id}
        )
        return result.fetchone()


def leak_example():
    """Anti-pattern: the connection is never returned if this raises."""
    conn = engine.connect()
    result = conn.execute(text("SELECT * FROM users"))
    return result.fetchall()  # conn.close() missing — pool leaks one slot per call


if __name__ == "__main__":
    url = os.environ.get("DATABASE_URL")
    if url:
        engine = create_engine(url, pool_size=10, max_overflow=5,
                               pool_timeout=30, pool_recycle=1800,
                               pool_pre_ping=True)
    print(get_user(1))
