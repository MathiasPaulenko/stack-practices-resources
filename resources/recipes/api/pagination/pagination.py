"""Offset and cursor pagination — runnable example over an in-memory dataset.

Mirrors the SQL from the recipe: offset pages skip N rows, cursor pages
resume after a stored position with a page_size + 1 probe for has_more.
"""

USERS = [{"id": i, "name": f"user-{i}"} for i in range(1, 101)]


def get_users_offset(page: int = 1, page_size: int = 20):
    """Offset pagination: `LIMIT page_size OFFSET (page-1)*page_size`."""
    if page < 1 or page_size < 1:
        raise ValueError("page and page_size must be positive")
    start = (page - 1) * page_size
    return USERS[start:start + page_size]


def get_users_cursor(cursor: int = None, page_size: int = 20):
    """Cursor pagination: `WHERE id > cursor ORDER BY id LIMIT page_size + 1`.

    The extra row is a probe: it answers has_more without a COUNT(*).
    next_cursor always comes from the last *returned* item, never the probe.
    """
    rows = [u for u in USERS if cursor is None or u["id"] > cursor]
    probe = rows[:page_size + 1]
    has_more = len(probe) > page_size
    items = probe[:page_size]
    next_cursor = items[-1]["id"] if items and has_more else None
    return {"items": items, "next_cursor": next_cursor, "has_more": has_more}


def walk_all_pages(page_size: int = 20):
    """Iterate the whole dataset through the cursor — the consumer pattern."""
    cursor = None
    seen = []
    while True:
        page = get_users_cursor(cursor, page_size)
        seen.extend(page["items"])
        if not page["has_more"]:
            return seen
        cursor = page["next_cursor"]


if __name__ == "__main__":
    print(get_users_offset(page=2, page_size=5))
    print(get_users_cursor(cursor=95, page_size=20))
