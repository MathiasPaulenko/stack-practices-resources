"""cursor_pagination.py

Python async implementation of cursor-based (keyset) pagination with PostgreSQL.
Uses asyncpg and base64url cursor encoding.
"""

from __future__ import annotations

import base64
import json
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

import asyncpg

T = TypeVar("T")


@dataclass
class CursorData:
    created_at: str
    id: str


@dataclass
class PageResult(Generic[T]):
    data: list[T]
    next_cursor: str | None
    prev_cursor: str | None
    has_more: bool


def encode_cursor(data: CursorData) -> str:
    payload = json.dumps({"createdAt": data.created_at, "id": data.id}).encode()
    return base64.urlsafe_b64encode(payload).decode().rstrip("=")


def decode_cursor(cursor: str) -> CursorData:
    padding = "=" * (-len(cursor) % 4)
    payload = base64.urlsafe_b64decode(cursor + padding).decode()
    parsed = json.loads(payload)
    return CursorData(created_at=parsed["createdAt"], id=parsed["id"])


class PostRepository:
    def __init__(self, pool: asyncpg.Pool) -> None:
        self._pool = pool

    async def find_page(
        self,
        limit: int = 20,
        after_cursor: str | None = None,
        before_cursor: str | None = None,
    ) -> PageResult[dict[str, Any]]:
        async with self._pool.acquire() as conn:
            if after_cursor:
                cursor = decode_cursor(after_cursor)
                rows = await conn.fetch(
                    """
                    SELECT * FROM posts
                    WHERE (created_at, id) < ($1, $2)
                    ORDER BY created_at DESC, id DESC
                    LIMIT $3
                    """,
                    cursor.created_at,
                    cursor.id,
                    limit + 1,
                )
            elif before_cursor:
                cursor = decode_cursor(before_cursor)
                rows = await conn.fetch(
                    """
                    SELECT * FROM (
                      SELECT * FROM posts
                      WHERE (created_at, id) > ($1, $2)
                      ORDER BY created_at ASC, id ASC
                      LIMIT $3
                    ) sub
                    ORDER BY created_at DESC, id DESC
                    """,
                    cursor.created_at,
                    cursor.id,
                    limit + 1,
                )
            else:
                rows = await conn.fetch(
                    """
                    SELECT * FROM posts
                    ORDER BY created_at DESC, id DESC
                    LIMIT $1
                    """,
                    limit + 1,
                )

            has_more = len(rows) > limit
            data = [dict(row) for row in (rows[:limit] if has_more else rows)]

            next_cursor = None
            if has_more and data:
                last = data[-1]
                next_cursor = encode_cursor(
                    CursorData(created_at=str(last["created_at"]), id=str(last["id"]))
                )

            prev_cursor = None
            if data:
                first = data[0]
                prev_cursor = encode_cursor(
                    CursorData(created_at=str(first["created_at"]), id=str(first["id"]))
                )

            return PageResult(
                data=data,
                next_cursor=next_cursor,
                prev_cursor=prev_cursor,
                has_more=has_more,
            )
