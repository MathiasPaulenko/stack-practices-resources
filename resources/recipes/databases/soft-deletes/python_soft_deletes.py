"""Soft deletes implementation with SQLAlchemy.

Provides SoftDeleteMixin, User model, restore and purge functions.
Run: python python_soft_deletes.py
"""
from __future__ import annotations

import datetime
import os

from sqlalchemy import Column, DateTime, Integer, String, Text, create_engine, text
from sqlalchemy.orm import Session, declarative_base, sessionmaker

Base = declarative_base()


class SoftDeleteMixin:
    deleted_at = Column(DateTime, nullable=True)
    deleted_by = Column(String(100), nullable=True)

    @classmethod
    def query_visible(cls, session: Session):
        return session.query(cls).filter(cls.deleted_at.is_(None))

    def soft_delete(self, deleted_by: str = "system"):
        self.deleted_at = datetime.datetime.utcnow()
        self.deleted_by = deleted_by

    def restore(self):
        self.deleted_at = None
        self.deleted_by = None


class User(Base, SoftDeleteMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    name = Column(String, nullable=True)


class Post(Base, SoftDeleteMixin):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    body = Column(Text, nullable=True)


def restore_user(session: Session, user_id: int) -> User | None:
    user = session.query(User).filter_by(id=user_id).first()
    if user and user.deleted_at is not None:
        user.restore()
        session.query(Post).filter_by(user_id=user_id).update({"deleted_at": None, "deleted_by": None})
        session.commit()
    return user


def purge_old_soft_deletes(session: Session, days: int = 30) -> int:
    cutoff = datetime.datetime.utcnow() - datetime.timedelta(days=days)
    users_result = session.execute(
        text("DELETE FROM users WHERE deleted_at IS NOT NULL AND deleted_at < :cutoff"),
        {"cutoff": cutoff},
    )
    session.execute(
        text("DELETE FROM posts WHERE deleted_at IS NOT NULL AND deleted_at < :cutoff"),
        {"cutoff": cutoff},
    )
    session.commit()
    return users_result.rowcount


def main() -> None:
    engine = create_engine("sqlite:///soft_deletes.db", echo=False)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)

    with SessionLocal() as session:
        user = User(email="alice@example.com", name="Alice")
        session.add(user)
        session.commit()

        print(f"Created user: {user.email}")
        user.soft_delete(deleted_by="admin")
        session.commit()
        print(f"Soft-deleted user: {user.email} by {user.deleted_by}")

        visible = User.query_visible(session).all()
        print(f"Visible users: {len(visible)}")

        restored = restore_user(session, user.id)
        print(f"Restored: {restored.email if restored else 'not found'}")

        visible = User.query_visible(session).all()
        print(f"Visible users after restore: {len(visible)}")

        user.soft_delete()
        session.commit()
        user.deleted_at = datetime.datetime.utcnow() - datetime.timedelta(days=31)
        session.commit()

        purged = purge_old_soft_deletes(session, days=30)
        print(f"Purged {purged} old records")


if __name__ == "__main__":
    main()
