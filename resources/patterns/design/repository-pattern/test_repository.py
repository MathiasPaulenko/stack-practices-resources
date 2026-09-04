"""Unit tests for the Repository Pattern Python implementation."""
import pytest
from user_repository import User, InMemoryUserRepository, UserService


class TestInMemoryUserRepository:
    def test_save_and_get_by_id(self):
        repo = InMemoryUserRepository()
        user = User(1, "Alice")

        repo.save(user)

        assert repo.get_by_id(1) == user

    def test_get_by_id_returns_none_for_missing(self):
        repo = InMemoryUserRepository()
        assert repo.get_by_id(999) is None

    def test_find_all_returns_all_users(self):
        repo = InMemoryUserRepository()
        repo.save(User(1, "Alice"))
        repo.save(User(2, "Bob"))

        all_users = repo.find_all()

        assert len(all_users) == 2

    def test_delete_existing_user(self):
        repo = InMemoryUserRepository()
        repo.save(User(1, "Alice"))

        assert repo.delete(1) is True
        assert repo.get_by_id(1) is None

    def test_delete_missing_user_returns_false(self):
        repo = InMemoryUserRepository()
        assert repo.delete(999) is False


class TestUserService:
    def test_promote_user(self):
        repo = InMemoryUserRepository()
        repo.save(User(1, "Alice", role="member"))
        service = UserService(repo)

        user = service.promote_user(1)

        assert user.role == "admin"

    def test_promote_missing_user_raises(self):
        repo = InMemoryUserRepository()
        service = UserService(repo)

        with pytest.raises(ValueError, match="User not found"):
            service.promote_user(999)

    def test_promote_persists_change(self):
        repo = InMemoryUserRepository()
        repo.save(User(1, "Alice", role="member"))
        service = UserService(repo)

        service.promote_user(1)

        assert repo.get_by_id(1).role == "admin"
