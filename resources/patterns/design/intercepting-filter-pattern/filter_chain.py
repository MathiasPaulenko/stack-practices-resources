"""Intercepting Filter pattern — runnable Python example.

A filter chain intercepts the request on the way in and the response on
the way back. Each filter can preprocess, short-circuit, or postprocess.

Run:  python filter_chain.py
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class HttpRequest:
    path: str
    headers: dict
    body: Any = None
    user: Any = None
    authenticated: bool = False


@dataclass
class HttpResponse:
    status: int = 200
    headers: dict = field(default_factory=dict)
    body: Any = None


class Filter(ABC):
    """Base filter that can delegate to the next filter."""

    def __init__(self, next_filter: "Filter" = None):
        self.next_filter = next_filter

    @abstractmethod
    def do_filter(self, request: HttpRequest, response: HttpResponse):
        pass

    def _invoke_next(self, request: HttpRequest, response: HttpResponse):
        if self.next_filter:
            self.next_filter.do_filter(request, response)


class AuthenticationFilter(Filter):
    """Short-circuits with 401 unless a Bearer token is present."""

    def do_filter(self, request: HttpRequest, response: HttpResponse):
        token = request.headers.get("Authorization")
        if token and token.startswith("Bearer "):
            request.user = "authenticated_user"
            request.authenticated = True
            self._invoke_next(request, response)
        else:
            response.status = 401
            response.body = {"error": "Unauthorized"}


class LoggingFilter(Filter):
    """Logs on both legs: request in, response out."""

    def do_filter(self, request: HttpRequest, response: HttpResponse):
        print(f"[LOG] -> {request.path}")
        self._invoke_next(request, response)
        print(f"[LOG] <- status {response.status}")


class CompressionFilter(Filter):
    """Postprocesses: marks the response as gzip-encoded if accepted."""

    def do_filter(self, request: HttpRequest, response: HttpResponse):
        self._invoke_next(request, response)
        if "gzip" in request.headers.get("Accept-Encoding", ""):
            response.headers["Content-Encoding"] = "gzip"
            print("[COMPRESS] response compressed")


class TargetHandler(Filter):
    """The final target: the actual business logic."""

    def __init__(self):
        super().__init__(None)

    def do_filter(self, request: HttpRequest, response: HttpResponse):
        if response.status == 200:
            response.body = {"message": f"Hello, {request.user or 'guest'}!"}


class FilterChain:
    """Builds the chain tail-to-head and executes it per request."""

    def __init__(self):
        self.filters: list[type[Filter]] = []

    def add_filter(self, filter_cls):
        self.filters.append(filter_cls)
        return self

    def execute(self, request: HttpRequest) -> HttpResponse:
        current = TargetHandler()
        for filter_cls in reversed(self.filters):
            f = filter_cls()
            f.next_filter = current
            current = f
        response = HttpResponse()
        current.do_filter(request, response)
        return response


if __name__ == "__main__":
    chain = FilterChain()
    chain.add_filter(AuthenticationFilter) \
         .add_filter(LoggingFilter) \
         .add_filter(CompressionFilter)

    ok = HttpRequest(
        path="/api/hello",
        headers={"Authorization": "Bearer abc123", "Accept-Encoding": "gzip"},
    )
    denied = HttpRequest(path="/api/hello", headers={})

    for req in (ok, denied):
        res = chain.execute(req)
        print(f"{req.path} auth={req.authenticated} -> {res.status} {res.body}\n")
