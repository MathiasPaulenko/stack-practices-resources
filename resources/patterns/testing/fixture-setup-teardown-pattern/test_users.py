"""Example tests consuming the fixtures defined in conftest.py."""

import pytest

from conftest import DuplicateEmailError


class TestUserService:
    def test_create_user(self, service):
        user = service.create_user("Bob", "bob@x.com")
        assert user["name"] == "Bob"

    def test_find_user(self, service_with_user):
        user = service_with_user.get_user_by_email("alice@x.com")
        assert user["name"] == "Alice"

    def test_duplicate_email(self, service_with_user):
        with pytest.raises(DuplicateEmailError):
            service_with_user.create_user("Bob", "alice@x.com")

    def test_fresh_state_each_test(self, repo):
        # Would fail if repo leaked state from another test
        assert repo.count("users") == 0


class TestTempDb:
    def test_insert_and_count(self, temp_db):
        temp_db.execute("INSERT INTO users VALUES ('Alice', 'a@x.com')")
        count = temp_db.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        assert count == 1


class TestEnvVars:
    def test_app_env(self, env_vars):
        assert env_vars["APP_ENV"] == "test"
        assert env_vars["DATABASE_URL"] == "sqlite:///:memory:"


class TestFixtureObject:
    def test_creation_notifies(self, test_context):
        test_context.create_user("Alice", "alice@x.com")
        test_context.assert_notified("alice@x.com")
