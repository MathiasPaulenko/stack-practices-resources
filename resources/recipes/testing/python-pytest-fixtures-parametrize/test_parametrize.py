"""Runnable tests for the python-pytest-fixtures-parametrize companion.

Run with:  pytest -v
"""

import json
import os
import tempfile

import pytest


def is_palindrome(s: str) -> bool:
    cleaned = "".join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]


@pytest.fixture
def temp_config_file():
    """Create a temporary config file; teardown removes it."""
    config = {"api_key": "test-key", "timeout": 30}
    fd, path = tempfile.mkstemp(suffix=".json")
    with open(path, "w") as f:
        json.dump(config, f)
    yield path
    os.close(fd)
    os.unlink(path)


def test_config_loading(temp_config_file):
    with open(temp_config_file) as f:
        loaded = json.load(f)
    assert loaded["api_key"] == "test-key"
    assert loaded["timeout"] == 30


@pytest.mark.parametrize(
    "input,expected",
    [
        pytest.param("racecar", True, id="simple_palindrome"),
        pytest.param("A man a plan a canal Panama", True, id="phrase"),
        pytest.param("hello", False, id="non_palindrome"),
        pytest.param("", True, id="empty"),
        pytest.param("ab", False, id="two_chars"),
    ],
)
def test_is_palindrome(input, expected):
    assert is_palindrome(input) == expected


@pytest.mark.parametrize("user", ["admin", "editor", "viewer"], indirect=True)
def test_user_roles(user):
    """Indirect parametrize: the fixture turns the string into a user dict."""
    assert user["role"] in {"admin", "editor", "viewer"}
    assert user["id"] == 1


def test_parametrized_fixture(db_engine):
    """Runs once per ``params`` entry on the fixture (sqlite, postgres)."""
    assert db_engine["connected"]
    assert db_engine["engine"] in {"sqlite", "postgres"}


@pytest.mark.parametrize(
    "input,expected",
    [
        pytest.param("case1", True, id="normal"),
        pytest.param(
            "case2",
            False,
            marks=pytest.mark.skip(reason="Demonstrates skipping a case"),
            id="skipped_case",
        ),
    ],
)
def test_with_skipped_case(input, expected):
    assert (input == "case1") == expected
