"""Tests for soft deletes with SQLAlchemy.

Run: pytest test_soft_deletes.py -v
"""
import datetime
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from python_soft_deletes import Base, User, Post, restore_user, purge_old_soft_deletes


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    s = SessionLocal()
    yield s
    s.close()


def test_soft_deleted_user_excluded_from_visible(session):
    user = User(email="test@example.com", name="Test")
    session.add(user)
    session.commit()

    user.soft_delete(deleted_by="admin")
    session.commit()

    visible = User.query_visible(session).all()
    assert user not in visible
    assert len(visible) == 0


def test_restore_user(session):
    user = User(email="test@example.com", name="Test")
    session.add(user)
    session.commit()

    user.soft_delete()
    session.commit()

    restored = restore_user(session, user.id)
    assert restored is not None
    assert restored.deleted_at is None
    assert User.query_visible(session).filter_by(id=user.id).one()


def test_purge_only_old_records(session):
    old_user = User(email="old@example.com")
    old_user.deleted_at = datetime.datetime.utcnow() - datetime.timedelta(days=31)
    recent_user = User(email="recent@example.com")
    recent_user.deleted_at = datetime.datetime.utcnow() - datetime.timedelta(days=5)
    session.add_all([old_user, recent_user])
    session.commit()

    purged = purge_old_soft_deletes(session, days=30)

    assert purged == 1
    assert session.query(User).filter_by(email="old@example.com").first() is None
    assert session.query(User).filter_by(email="recent@example.com").first() is not None


def test_deleted_by_tracked(session):
    user = User(email="test@example.com")
    session.add(user)
    session.commit()

    user.soft_delete(deleted_by="admin@example.com")
    session.commit()

    assert user.deleted_by == "admin@example.com"
    assert user.deleted_at is not None


def test_cascade_restore_posts(session):
    user = User(email="test@example.com")
    session.add(user)
    session.commit()

    post = Post(user_id=user.id, title="My Post", body="Content")
    session.add(post)
    session.commit()

    user.soft_delete()
    post.soft_delete()
    session.commit()

    restore_user(session, user.id)

    restored_post = session.query(Post).filter_by(id=post.id).first()
    assert restored_post.deleted_at is None
