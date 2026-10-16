# tests/integration/test_postgres.py — Testcontainers in Python
import pytest
from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine, text

@pytest.fixture(scope="module")
def postgres_container():
    with PostgresContainer("postgres:16") as postgres:
        yield postgres

@pytest.fixture(scope="module")
def db_engine(postgres_container):
    engine = create_engine(postgres_container.get_connection_url())
    return engine

@pytest.fixture(scope="function")
def db_session(db_engine):
    with db_engine.connect() as conn:
        # Setup
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                name VARCHAR(100) NOT NULL
            )
        """))
        conn.commit()
        yield conn
        # Cleanup
        conn.execute(text("DROP TABLE IF EXISTS users"))
        conn.commit()

def test_insert_user(db_session):
    result = db_session.execute(text(
        "INSERT INTO users (email, name) VALUES (:email, :name) RETURNING id"
    ), {"email": "alice@example.com", "name": "Alice"})
    db_session.commit()
    assert result.fetchone()[0] > 0

def test_unique_email_constraint(db_session):
    db_session.execute(text(
        "INSERT INTO users (email, name) VALUES ('bob@test.com', 'Bob')"
    ))
    db_session.commit()

    with pytest.raises(Exception) as exc_info:
        db_session.execute(text(
            "INSERT INTO users (email, name) VALUES ('bob@test.com', 'Bob2')"
        ))
        db_session.commit()
    assert "unique" in str(exc_info.value).lower()
