"""Cursor-based pagination for a collection endpoint.

Offsets go stale on hot tables; a cursor on the last seen id
stays stable while rows are inserted.
"""

import base64
import json

from fastapi import FastAPI

app = FastAPI()
USERS = [{"id": f"usr_{i:03d}", "email": f"user{i}@example.com"} for i in range(1, 51)]


def encode_cursor(last_id: str) -> str:
    return base64.urlsafe_b64encode(json.dumps({"last_id": last_id}).encode()).decode()


def decode_cursor(cursor: str) -> str | None:
    return json.loads(base64.urlsafe_b64decode(cursor)).get("last_id")


@app.get("/v1/users")
async def list_users(cursor: str | None = None, limit: int = 20):
    start = 0
    if cursor:
        last_id = decode_cursor(cursor)
        start = next((i + 1 for i, u in enumerate(USERS) if u["id"] == last_id), 0)
    page = USERS[start : start + limit]
    next_cursor = encode_cursor(page[-1]["id"]) if start + limit < len(USERS) and page else None
    return {"data": page, "next_cursor": next_cursor}
