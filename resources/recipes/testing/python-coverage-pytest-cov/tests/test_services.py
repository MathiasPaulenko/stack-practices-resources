import pytest

from sample_app.models import User
from sample_app.services import UserService


@pytest.fixture
def service():
    return UserService(
        users=[
            User(id=1, email="alice@example.com", is_active=True),
            User(id=2, email="bob@example.com", is_active=False),
        ]
    )


def test_get_active_users(service):
    result = service.get_active_users()
    assert len(result) == 1
    assert result[0].email == "alice@example.com"


def test_get_user_by_email(service):
    user = service.get_user_by_email("bob@example.com")
    assert user is not None
    assert user.id == 2


def test_toggle_user_status(service):
    assert service.toggle_user_status(1) is True
    assert service.get_user_by_email("alice@example.com").is_active is False


def test_toggle_user_status_not_found(service):
    assert service.toggle_user_status(99) is False
