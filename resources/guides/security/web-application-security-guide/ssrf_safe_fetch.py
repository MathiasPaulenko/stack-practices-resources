"""SSRF-safe fetch: scheme + host allowlist, internal IP ranges blocked.

    python ssrf_safe_fetch.py

Validates scheme, hostname allowlist, and the *resolved* IP before any
request leaves the process — so evil.com -> 169.254.169.254 fails too.
Stdlib only; no installs needed for the demo.
"""

import ipaddress
import socket
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ALLOWED_HOSTS = {"example.com", "api.github.com"}
ALLOWED_SCHEMES = {"https"}


def safe_fetch(user_url: str) -> bytes:
    parsed = urlparse(user_url)
    if parsed.scheme not in ALLOWED_SCHEMES:
        raise ValueError("Only https URLs allowed")
    if parsed.hostname not in ALLOWED_HOSTS:
        raise ValueError("URL not in allowlist")

    try:
        ip = ipaddress.ip_address(socket.gethostbyname(parsed.hostname))
    except socket.gaierror:
        raise ValueError("Cannot resolve host")
    if not ip.is_global:
        raise ValueError("Internal IP not allowed")

    req = Request(user_url, headers={"User-Agent": "ssrf-demo/1.0"})
    return urlopen(req, timeout=5).read(1024)


def check(label: str, url: str) -> None:
    try:
        safe_fetch(url)
        print(f"{label}: ALLOWED ({url})")
    except ValueError as e:
        print(f"{label}: BLOCKED — {e}")
    except Exception as e:
        # Network unavailable in the sandbox; validation still ran first.
        print(f"{label}: validated, fetch failed ({e.__class__.__name__})")


if __name__ == "__main__":
    check("ok        ", "https://api.github.com/")
    check("http      ", "http://api.github.com/")              # wrong scheme
    check("offlist   ", "https://evil.example.net/x")         # not in allowlist
    check("metadata  ", "https://169.254.169.254/latest")     # AWS metadata IP
    check("loopback  ", "https://127.0.0.1/admin")            # loopback
    check("file      ", "file:///etc/passwd")                 # local file read
