"""SSRF protection for user-supplied URLs (A01 — SSRF lives under access control in 2025)."""

import ipaddress
import socket
from urllib.parse import urlparse

BLOCKED_IP_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("169.254.0.0/16"),  # Link-local / cloud metadata
    ipaddress.ip_network("127.0.0.0/8"),     # Loopback
    ipaddress.ip_network("0.0.0.0/8"),
    ipaddress.ip_network("::1/128"),         # IPv6 loopback
    ipaddress.ip_network("fc00::/7"),        # IPv6 ULA
]

ALLOWED_SCHEMES = {"http", "https"}
ALLOWED_PORTS = {80, 443, 8080, 8443}


class SSRFProtector:
    """Validates URLs against scheme, port, and resolved-IP blocklists."""

    def validate_url(self, url: str) -> bool:
        """Return True if the URL resolves to a public, allowed destination."""
        parsed = urlparse(url)

        if parsed.scheme not in ALLOWED_SCHEMES:
            return False

        port = parsed.port or (443 if parsed.scheme == "https" else 80)
        if port not in ALLOWED_PORTS:
            return False

        if not parsed.hostname:
            return False

        try:
            ips = socket.getaddrinfo(parsed.hostname, port)
            for ip_info in ips:
                ip = ipaddress.ip_address(ip_info[4][0])
                for blocked in BLOCKED_IP_RANGES:
                    if ip in blocked:
                        return False
        except socket.gaierror:
            return False

        return True

    def safe_fetch(self, url: str, timeout: int = 10) -> str:
        """Fetch a URL after validation; redirects are re-validated manually."""
        import requests

        if not self.validate_url(url):
            raise ValueError("URL validation failed")

        response = requests.get(url, timeout=timeout, allow_redirects=False)

        if response.status_code in (301, 302, 307, 308):
            location = response.headers.get("Location", "")
            if not self.validate_url(location):
                raise ValueError("Redirect target validation failed")

        return response.text
