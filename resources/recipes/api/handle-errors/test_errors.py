"""Contract tests for RFC 7807 Problem Details error handling."""

import pytest
from fastapi.testclient import TestClient
from python_fastapi import app

client = TestClient(app)


def test_get_user_not_found():
    response = client.get("/users/-1")
    assert response.status_code == 404
    assert response.headers["content-type"] == "application/problem+json"
    body = response.json()
    assert body["type"] == "https://api.example.com/errors/not-found"
    assert body["title"] == "User Not Found"
    assert "detail" in body
    assert body["status"] == 404


def test_get_user_valid():
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Ada"


def test_invalid_input_returns_422():
    response = client.get("/users/abc")
    assert response.status_code == 422
    body = response.json()
    assert "errors" in body or "detail" in body


def test_crash_returns_500():
    response = client.get("/crash")
    assert response.status_code == 500
    assert response.headers["content-type"] == "application/problem+json"
    body = response.json()
    assert body["status"] == 500
    # Stack trace must not leak in production mode
    assert "traceback" not in response.text.lower()


def test_content_type_is_problem_json():
    response = client.get("/users/-1")
    assert "application/problem+json" in response.headers["content-type"]


def test_instance_field_present():
    response = client.get("/users/-1")
    body = response.json()
    assert "instance" in body
    assert "/users/-1" in body["instance"]
