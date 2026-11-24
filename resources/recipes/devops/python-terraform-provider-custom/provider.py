"""Terraform provider skeleton — ApiClient + ItemResource CRUD with a mock API.

Mirrors the resource lifecycle Terraform calls over gRPC: create, read,
update, delete, with empty-state-on-404 semantics. __main__ spins up a mock
items API and runs the full CRUD cycle as a smoke test.
"""

import json
import threading
import uuid
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any

import requests


class ApiClient:
    """Wrapper for the external API that Terraform would manage."""

    def __init__(self, base_url: str, api_token: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
        })

    def create_item(self, data: dict) -> dict:
        resp = self.session.post(f"{self.base_url}/items", json=data)
        resp.raise_for_status()
        return resp.json()

    def get_item(self, item_id: str) -> dict:
        resp = self.session.get(f"{self.base_url}/items/{item_id}")
        resp.raise_for_status()
        return resp.json()

    def update_item(self, item_id: str, data: dict) -> dict:
        resp = self.session.put(f"{self.base_url}/items/{item_id}", json=data)
        resp.raise_for_status()
        return resp.json()

    def delete_item(self, item_id: str) -> None:
        resp = self.session.delete(f"{self.base_url}/items/{item_id}")
        resp.raise_for_status()


class ItemResource:
    """CRUD for the custom_item resource — same contract Terraform expects."""

    def __init__(self, client: ApiClient):
        self.client = client

    def create(self, plan: dict) -> dict:
        result = self.client.create_item({
            "name": plan["name"],
            "description": plan.get("description", ""),
            "tags": plan.get("tags", ""),
        })
        return self._state(result)

    def read(self, state: dict) -> dict:
        try:
            return self._state(self.client.get_item(state["id"]))
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return {}  # empty state: resource is gone
            raise

    def update(self, state: dict, plan: dict) -> dict:
        result = self.client.update_item(state["id"], {
            "name": plan["name"],
            "description": plan.get("description", ""),
            "tags": plan.get("tags", ""),
        })
        return self._state(result)

    def delete(self, state: dict) -> None:
        self.client.delete_item(state["id"])

    @staticmethod
    def _state(result: dict) -> dict:
        return {
            "id": result["id"],
            "name": result["name"],
            "description": result.get("description", ""),
            "tags": result.get("tags", ""),
        }


class _ItemsHandler(BaseHTTPRequestHandler):
    """In-memory mock of the upstream items API for the smoke test."""

    store: dict[str, dict] = {}

    def _send(self, code: int, body: Any = None):
        payload = json.dumps(body).encode() if body is not None else b""
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_POST(self):
        data = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        item = {"id": str(uuid.uuid4())[:8], **data}
        self.store[item["id"]] = item
        self._send(201, item)

    def do_GET(self):
        item = self.store.get(self.path.rsplit("/", 1)[-1])
        self._send(200, item) if item else self._send(404, {"error": "not found"})

    def do_PUT(self):
        item_id = self.path.rsplit("/", 1)[-1]
        if item_id not in self.store:
            self._send(404, {"error": "not found"})
            return
        data = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        self.store[item_id].update(data)
        self._send(200, self.store[item_id])

    def do_DELETE(self):
        self.store.pop(self.path.rsplit("/", 1)[-1], None)
        self._send(204)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 0), _ItemsHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()

    client = ApiClient(f"http://127.0.0.1:{server.server_port}", api_token="test")
    resource = ItemResource(client)

    state = resource.create({"name": "prod-config", "tags": "prod,critical"})
    print("create:", state)

    state = resource.update(state, {"name": "prod-config", "description": "v2"})
    print("update:", state)

    print("read:", resource.read(state))

    resource.delete(state)
    print("read after delete:", resource.read(state))

    server.shutdown()
