"""SQL injection prevention with SQLAlchemy — runnable examples.

Demonstrates the vulnerable pattern and the safe alternatives side by side
against an in-memory SQLite database: text() with bound params, ORM select,
dynamic filters, ORDER BY whitelists, and LIKE wildcard escaping.
"""

from sqlalchemy import String, create_engine, select, text
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(20))


def get_user_vulnerable(engine, username: str):
    """VULNERABLE — string concatenation. Do not use."""
    with engine.connect() as conn:
        query = f"SELECT * FROM users WHERE username = '{username}'"
        return conn.execute(text(query)).fetchall()


def get_user_safe(engine, username: str):
    """Safe — bound parameter via text()."""
    with engine.connect() as conn:
        return conn.execute(
            text("SELECT * FROM users WHERE username = :username"),
            {"username": username},
        ).fetchone()


def get_user_orm(session: Session, username: str) -> "User | None":
    """Safe — ORM queries are parameterized automatically."""
    return session.execute(
        select(User).where(User.username == username)
    ).scalar_one_or_none()


def search_users(session: Session, role: str, order_by: str = "username"):
    """Safe dynamic query — conditions parameterized, column name whitelisted."""
    allowed_order = {"username", "email", "id", "role"}
    column = getattr(User, order_by if order_by in allowed_order else "username")
    stmt = select(User).where(User.role == role).order_by(column)
    return list(session.execute(stmt).scalars())


def search_by_pattern(session: Session, pattern: str):
    """Safe LIKE — value is bound, wildcards in input are escaped."""
    safe = pattern.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    stmt = select(User).where(User.username.ilike(f"%{safe}%"))
    return list(session.execute(stmt).scalars())


if __name__ == "__main__":
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with Session(engine) as s:
        s.add_all([
            User(username="alice", email="alice@example.com", role="admin"),
            User(username="bob", email="bob@example.com", role="user"),
        ])
        s.commit()

        attack = "' OR '1'='1' --"
        print("vulnerable:", len(get_user_vulnerable(engine, attack)), "rows leaked")
        print("safe text():", get_user_safe(engine, attack))
        print("safe ORM:", get_user_orm(s, attack))
        print("admins:", [u.username for u in search_users(s, "admin", "username")])
        print("injection via ORDER BY:", [u.username for u in search_users(s, "user", "1; DROP TABLE users")])
        print("LIKE escape:", [u.username for u in search_by_pattern(s, "100%")])
