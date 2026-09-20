"""Tests for the Pydantic v2 input validation example.

Run:  pytest test_validate_user.py -v
"""
import pytest
from pydantic import ValidationError

from validate_user import UserCreate, format_errors


def test_valid_input_passes():
    user = UserCreate(name="Ada Lovelace", email="ada@example.com", age=36)
    assert user.name == "Ada Lovelace"
    assert user.bio is None


def test_blank_name_is_rejected():
    with pytest.raises(ValidationError):
        UserCreate(name="   ", email="ada@example.com", age=36)


def test_name_is_trimmed():
    user = UserCreate(name="  Ada  ", email="ada@example.com", age=36)
    assert user.name == "Ada"


def test_invalid_email_is_rejected():
    with pytest.raises(ValidationError):
        UserCreate(name="Ada", email="not-an-email", age=36)


def test_age_bounds_are_enforced():
    with pytest.raises(ValidationError):
        UserCreate(name="Ada", email="ada@example.com", age=-1)
    with pytest.raises(ValidationError):
        UserCreate(name="Ada", email="ada@example.com", age=151)


def test_all_violations_are_aggregated():
    try:
        UserCreate(name="", email="bad", age=999)
    except ValidationError as e:
        fields = {err["field"] for err in format_errors(e)}
        assert {"name", "email", "age"} <= fields
    else:
        pytest.fail("expected ValidationError")


def test_format_errors_shape():
    try:
        UserCreate(name="Ada", email="bad", age=36)
    except ValidationError as e:
        errs = format_errors(e)
        assert errs[0]["field"] == "email"
        assert "message" in errs[0] and "type" in errs[0]
