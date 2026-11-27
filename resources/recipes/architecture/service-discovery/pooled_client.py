"""Connection pooling for discovered endpoints.

Creating a new HTTP connection per request to a discovered instance
wastes the TCP handshake (and TLS, if you encrypt) on every call. Pool
one session per instance URL and recycle it.
"""
import requests
from requests.adapters import HTTPAdapter


class PooledServiceClient:
    def __init__(self):
        self.sessions: dict[str, requests.Session] = {}

    def get_session(self, instance_url: str) -> requests.Session:
        if instance_url not in self.sessions:
            session = requests.Session()
            adapter = HTTPAdapter(pool_connections=10, pool_maxsize=100)
            session.mount("http://", adapter)
            self.sessions[instance_url] = session
        return self.sessions[instance_url]

    def get(self, instance_url: str, path: str) -> requests.Response:
        return self.get_session(instance_url).get(instance_url + path, timeout=5)


if __name__ == "__main__":
    client = PooledServiceClient()
    # Both calls reuse the same pooled session.
    client.get("http://10.0.3.7:8080", "/payments/123")
    client.get("http://10.0.3.7:8080", "/payments/456")
