"""Test doubles: all five Meszaros types in runnable pytest examples."""
import pytest
from unittest.mock import MagicMock


# --- Domain objects (minimal, for the examples to run) ---
class User:
    def __init__(self, id, name=None, email=None):
        self.id, self.name, self.email = id, name, email


class UserService:
    def __init__(self, repo):
        self.repo = repo

    def get_name(self, user_id):
        user = self.repo.find_by_id(user_id)
        if user is None:
            raise LookupError("not found")
        return user.name


# --- 1. Dummy: passed but never used ---
class DummyLogger:
    def info(self, msg): pass
    def error(self, msg): pass
    def warning(self, msg): pass


# --- 2. Stub: returns canned responses ---
class UserRepositoryStub:
    def __init__(self, user=None):
        self.user = user

    def find_by_id(self, user_id):
        return self.user

    def save(self, user):
        pass


# --- 3. Spy: MagicMock records calls (see tests below) ---

# --- 4. Fake: working, simplified implementation ---
class FakeUserRepository:
    def __init__(self):
        self._users = {}
        self._next_id = 1

    def create(self, name, email):
        user = User(id=self._next_id, name=name, email=email)
        self._users[self._next_id] = user
        self._next_id += 1
        return user

    def find_by_id(self, user_id):
        return self._users.get(user_id)

    def find_by_email(self, email):
        return next((u for u in self._users.values() if u.email == email), None)

    def delete(self, user_id):
        return self._users.pop(user_id, None) is not None

    def count(self):
        return len(self._users)


# --- Tests ---
def test_stub_returns_canned_user():
    repo = UserRepositoryStub(user=User(id=1, name="Alice"))
    assert UserService(repo).get_name(1) == "Alice"


def test_stub_missing_user_raises():
    with pytest.raises(LookupError):
        UserService(UserRepositoryStub(user=None)).get_name(999)


def test_spy_records_send_call():
    email_service = MagicMock()
    email_service.send(to="alice@x.com", subject="Order #42 completed")
    email_service.send.assert_called_once_with(
        to="alice@x.com", subject="Order #42 completed"
    )


def test_fake_create_and_find():
    repo = FakeUserRepository()
    user = repo.create("Alice", "alice@x.com")
    found = repo.find_by_id(user.id)
    assert found.name == "Alice"
    assert repo.count() == 1


def test_mock_expects_exact_call():
    repo = MagicMock()
    repo.find_by_id.return_value = User(id=1, name="Alice")
    assert UserService(repo).get_name(1) == "Alice"
    repo.find_by_id.assert_called_once_with(1)
