"""Runnable examples for mocking HTTP calls with the responses library.

Requires responses >= 0.25 (matchers module, RequestsMock).
"""
import json
import re

import pytest
import requests
import responses
from responses import matchers

BASE = "https://api.example.com"


@responses.activate
def test_get_user():
    responses.add(
        method=responses.GET,
        url=f"{BASE}/users/1",
        json={"id": 1, "name": "Alice", "email": "alice@example.com"},
        status=200,
    )

    resp = requests.get(f"{BASE}/users/1")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Alice"


@responses.activate
def test_search_with_matchers():
    responses.add(
        method=responses.GET,
        url=f"{BASE}/search",
        json={"results": [{"title": "Python Guide"}]},
        status=200,
        headers={"X-RateLimit-Remaining": "99"},
        match=[matchers.query_param_matcher({"q": "python"})],
    )

    resp = requests.get(
        f"{BASE}/search",
        params={"q": "python", "page": 1},
        headers={"Authorization": "Bearer test-token"},
    )

    assert resp.headers["X-RateLimit-Remaining"] == "99"
    assert resp.json()["results"][0]["title"] == "Python Guide"
    assert len(responses.calls) == 1
    assert "q=python" in responses.calls[0].request.url


@responses.activate
def test_handle_server_error():
    responses.add(method=responses.GET, url=f"{BASE}/users/1", status=500)

    with pytest.raises(requests.HTTPError):
        resp = requests.get(f"{BASE}/users/1")
        resp.raise_for_status()


@responses.activate
def test_handle_timeout():
    responses.add(
        method=responses.GET,
        url=f"{BASE}/slow-endpoint",
        body=requests.exceptions.Timeout("Connection timed out"),
    )

    with pytest.raises(requests.exceptions.Timeout):
        requests.get(f"{BASE}/slow-endpoint")


@responses.activate
def test_retry_sequence():
    responses.add(method=responses.GET, url=f"{BASE}/data", status=503)
    responses.add(
        method=responses.GET, url=f"{BASE}/data", status=200, json={"data": "ok"}
    )

    assert requests.get(f"{BASE}/data").status_code == 503
    assert requests.get(f"{BASE}/data").status_code == 200


@responses.activate
def test_callback_dynamic_response():
    def request_callback(request):
        if b"premium" in request.body:
            return (200, {}, json.dumps({"tier": "premium", "quota": 10000}))
        return (200, {}, json.dumps({"tier": "free", "quota": 100}))

    responses.add_callback(
        method=responses.POST,
        url=f"{BASE}/subscribe",
        callback=request_callback,
        content_type="application/json",
    )

    resp = requests.post(f"{BASE}/subscribe", json={"plan": "premium"})
    assert resp.json()["quota"] == 10000


@responses.activate
def test_request_body_assertion():
    responses.add(
        method=responses.POST,
        url=f"{BASE}/orders",
        status=201,
        json={"id": 42, "status": "created"},
    )

    requests.post(f"{BASE}/orders", json={"product_id": 10, "quantity": 3})

    sent = json.loads(responses.calls[0].request.body)
    assert sent == {"product_id": 10, "quantity": 3}


@responses.activate
def test_regex_url_match():
    responses.add(
        method=responses.GET,
        url=re.compile(r"https://api\.example\.com/users/\d+"),
        json={"id": 1},
    )

    assert requests.get(f"{BASE}/users/7").json()["id"] == 1


@responses.activate
def test_streaming_response():
    def stream_generator():
        yield b"chunk1\n"
        yield b"chunk2\n"

    responses.add(
        method=responses.GET,
        url=f"{BASE}/stream",
        body=stream_generator(),
        content_type="text/event-stream",
    )

    assert requests.get(f"{BASE}/stream").content == b"chunk1\nchunk2\n"


def test_with_fixture(mock_api):
    mock_api.add(
        method=responses.GET,
        url=f"{BASE}/health",
        status=200,
        json={"status": "healthy"},
    )

    assert requests.get(f"{BASE}/health").json()["status"] == "healthy"
