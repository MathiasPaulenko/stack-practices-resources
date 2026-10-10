"""SQLAlchemy 2.x CRUD: User/Post model with relationships and eager loading.

Usage:
    pip install -r requirements.txt
    # Point DATABASE_URL at your Postgres instance, or use SQLite for a quick run:
    #   DATABASE_URL=sqlite:///orm_crud.db python python_sqlalchemy_crud.py
"""

import os

from sqlalchemy import ForeignKey, String, create_engine, select, update
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
    selectinload,
)

DATABASE_URL = os.getenv(
    "DATABASE_URL", "sqlite:///orm_crud.db"
)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    role: Mapped[str] = mapped_column(String, default="user")
    posts: Mapped[list["Post"]] = relationship(
        back_populates="author", cascade="all, delete-orphan"
    )


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped[User] = relationship(back_populates="posts")


def main() -> None:
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        # Create
        user = User(email="alice@example.com", role="admin")
        session.add(user)
        session.commit()

        # Read
        found = session.scalar(
            select(User).where(User.email == "alice@example.com")
        )
        print("read:", found.id, found.email)

        # Update — the session tracks the dirty attribute
        found.role = "superadmin"
        session.commit()

        # Eager loading with selectinload — avoids N+1
        stmt = select(User).options(selectinload(User.posts)).where(User.role == "superadmin")
        for u in session.execute(stmt).scalars():
            print("admin:", u.email, "posts:", len(u.posts))

        # Bulk update with Core
        session.execute(
            update(User).where(User.role == "user").values(role="member")
        )
        session.commit()

        # Delete
        session.delete(found)
        session.commit()

        print("remaining:", session.scalar(select(User).count()))


if __name__ == "__main__":
    main()
