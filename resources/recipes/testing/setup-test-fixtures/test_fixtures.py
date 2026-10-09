"""Example tests consuming fixtures from conftest.py."""

import pytest

from conftest import User


def test_admin_can_delete(admin_user):
    assert admin_user.can_delete() is True


def test_permissions_vary_by_role(user_factory):
    admin = user_factory(role="admin")
    viewer = user_factory(role="viewer")
    assert admin.can_edit()
    assert not viewer.can_edit()


def test_role_fixture_runs_per_value(role):
    # runs 3 times: admin, editor, viewer
    assert role in ("admin", "editor", "viewer")


def test_tmp_file_seeded(temp_file):
    assert temp_file.read_text() == "seed"


def test_session_config(app_config):
    assert app_config["env"] == "test"


@pytest.mark.parametrize("role,expected", [
    ("admin", True),
    ("editor", False),
    ("viewer", False),
])
def test_delete_permission(role, expected):
    assert User(id=1, name="x", email="x@x.com", role=role).can_delete() == expected
