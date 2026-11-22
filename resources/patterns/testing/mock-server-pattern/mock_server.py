"""Mock Server Pattern — runnable Python companion (stdlib only).

A real HTTP mock server built on http.server: stubs are registered per-test,
requests are recorded for verification, and the whole thing runs on a free
port in a background thread — no network access, no dependencies.

Run: python mock_server.py
Tests: python -m unittest mock_server -v
"""

import json
import threading
import unittest
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class NotFoundError(Exception):
    pass


class MockServer:
    """Standalone HTTP server that returns canned responses.

    The four-step lifecycle mirrors every tool from the pattern page:
    configure stubs -> intercept real requests -> match and respond ->
    verify the request was made.
    """

    def __init__(self):
        self._stubs = []
        self.requests = []
        self._server = None
        self._thread = None

    def stub(self, method, path, status=200, body=None, headers=None):
        self._stubs.append({
            "method": method.upper(),
            "path": path,
            "status": status,
            "body": body,
            "headers": headers or {"Content-Type": "application/json"},
        })
        return self

    def reset(self):
        """Clear stubs and recorded requests — call between tests."""
        self._stubs.clear()
        self.requests.clear()

    def verify(self, method, path):
        return any(
            r["method"] == method.upper() and r["path"] == path
            for r in self.requests
        )

    @property
    def url(self):
        return f"http://127.0.0.1:{self._server.server_port}"

    def _match(self, method, path):
        for stub in self._stubs:
            if stub["method"] == method and stub["path"] == path:
                return stub
        return None

    def _handler(self):
        outer = self

        class Handler(BaseHTTPRequestHandler):
            def _dispatch(self, method):
                outer.requests.append({
                    "method": method,
                    "path": self.path,
                })
                stub = outer._match(method, self.path)
                if stub is None:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b'{"error": "no stub matched"}')
                    return
                self.send_response(stub["status"])
                for name, value in stub["headers"].items():
                    self.send_header(name, value)
                self.end_headers()
                if stub["body"] is not None:
                    payload = stub["body"]
                    if not isinstance(payload, (bytes, str)):
                        payload = json.dumps(payload)
                    self.wfile.write(payload.encode())

            def do_GET(self):
                self._dispatch("GET")

            def do_POST(self):
                length = int(self.headers.get("Content-Length", 0))
                outer.requests[-1]["body"] = self.rfile.read(length).decode() \
                    if outer.requests else None
                self._dispatch("POST")

            def log_message(self, *args):
                pass

        return Handler

    def start(self):
        self._server = ThreadingHTTPServer(("127.0.0.1", 0), self._handler())
        self._thread = threading.Thread(target=self._server.serve_forever)
        self._thread.start()
        return self

    def stop(self):
        if self._server:
            self._server.shutdown()
            self._server.server_close()
            self._thread.join()

    def __enter__(self):
        return self.start()

    def __exit__(self, *exc):
        self.stop()


class UserService:
    """Client under test — talks to whatever base URL it is given."""

    def __init__(self, base_url):
        self.base_url = base_url

    def get_user(self, user_id):
        try:
            with urllib.request.urlopen(
                f"{self.base_url}/users/{user_id}"
            ) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            code = e.code
            e.close()
            if code == 404:
                raise NotFoundError(f"user {user_id}") from e
            raise


class TestMockServer(unittest.TestCase):
    def setUp(self):
        self.mock = MockServer().start()
        self.client = UserService(self.mock.url)

    def tearDown(self):
        self.mock.stop()

    def test_stubbed_response(self):
        self.mock.stub("GET", "/users/1", body={
            "id": 1, "name": "Alice", "email": "alice@x.com",
        })
        user = self.client.get_user(1)
        self.assertEqual(user["name"], "Alice")

    def test_error_status_reaches_client(self):
        self.mock.stub("GET", "/users/999", status=404, body={
            "error": {"code": "NOT_FOUND"},
        })
        with self.assertRaises(NotFoundError):
            self.client.get_user(999)

    def test_unstubbed_path_404s(self):
        with self.assertRaises(NotFoundError):
            self.client.get_user(42)

    def test_verify_request_was_made(self):
        self.mock.stub("GET", "/users/1", body={"id": 1, "name": "Alice"})
        self.client.get_user(1)
        self.assertTrue(self.mock.verify("GET", "/users/1"))
        self.assertFalse(self.mock.verify("POST", "/users"))

    def test_reset_clears_state(self):
        self.mock.stub("GET", "/users/1", body={"id": 1})
        self.client.get_user(1)
        self.mock.reset()
        self.assertFalse(self.mock.verify("GET", "/users/1"))
        with self.assertRaises(NotFoundError):
            self.client.get_user(1)


if __name__ == "__main__":
    with MockServer() as mock:
        mock.stub("GET", "/users/1", body={
            "id": 1, "name": "Alice", "email": "alice@x.com",
        })
        user = UserService(mock.url).get_user(1)
        print(f"Mock server on {mock.url} answered: {user}")

    unittest.main(argv=[""], exit=False, verbosity=0)
