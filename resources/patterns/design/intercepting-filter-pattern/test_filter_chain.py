"""Tests for the Intercepting Filter chain.

Run:  pytest test_filter_chain.py -v
"""
from filter_chain import (
    AuthenticationFilter,
    CompressionFilter,
    FilterChain,
    HttpRequest,
    LoggingFilter,
)


def build_chain():
    return (
        FilterChain()
        .add_filter(AuthenticationFilter)
        .add_filter(LoggingFilter)
        .add_filter(CompressionFilter)
    )


def authenticated(headers=None):
    base = {"Authorization": "Bearer token123"}
    return HttpRequest(path="/api/hello", headers={**base, **(headers or {})})


def test_authenticated_request_reaches_target():
    res = build_chain().execute(authenticated())
    assert res.status == 200
    assert res.body == {"message": "Hello, authenticated_user!"}


def test_missing_token_short_circuits_with_401():
    res = build_chain().execute(HttpRequest(path="/api/hello", headers={}))
    assert res.status == 401
    assert res.body == {"error": "Unauthorized"}


def test_gzip_accept_gets_content_encoding():
    res = build_chain().execute(authenticated({"Accept-Encoding": "gzip"}))
    assert res.headers["Content-Encoding"] == "gzip"


def test_no_gzip_no_encoding_header():
    res = build_chain().execute(authenticated())
    assert "Content-Encoding" not in res.headers


def test_401_responses_are_not_compressed():
    # Short-circuit: compression filter never ran, so no encoding header.
    res = build_chain().execute(HttpRequest(path="/api/hello", headers={"Accept-Encoding": "gzip"}))
    assert res.status == 401
    assert "Content-Encoding" not in res.headers


def test_chain_is_reusable_across_requests():
    chain = build_chain()
    first = chain.execute(authenticated())
    second = chain.execute(authenticated())
    assert first.status == second.status == 200
