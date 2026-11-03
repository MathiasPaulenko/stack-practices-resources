# VULNERABLE: No limit on page size
@app.get("/api/users")
async def list_users(page: int = 1, size: int = 1000):
    # Attacker can request size=1000000 and overwhelm the server
    offset = (page - 1) * size
    return db.query(User).offset(offset).limit(size).all()

# SAFE: Enforce maximum page size
MAX_PAGE_SIZE = 100

@app.get("/api/users")
async def list_users(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=MAX_PAGE_SIZE)
):
    offset = (page - 1) * size
    users = db.query(User).offset(offset).limit(size).all()
    total = db.query(User).count()
    
    return {
        "data": [user_to_dict(u) for u in users],
        "pagination": {
            "page": page,
            "size": size,
            "total": total,
            "total_pages": (total + size - 1) // size
        }
    }

# SAFE: Cursor-based pagination (better for large datasets)
import base64
from fastapi import HTTPException

@app.get("/api/users/cursor")
async def list_users_cursor(
    cursor: str | None = Query(default=None),
    size: int = Query(20, ge=1, le=MAX_PAGE_SIZE)
):
    query = db.query(User).order_by(User.id.desc())
    
    if cursor:
        try:
            last_id = int(base64.b64decode(cursor).decode())
        except Exception:
            raise HTTPException(400, "Invalid cursor")
        query = query.filter(User.id < last_id)
    
    users = query.limit(size + 1).all()  # Fetch one extra to check has_more
    has_more = len(users) > size
    users = users[:size]
    
    next_cursor = None
    if has_more and users:
        next_cursor = base64.b64encode(str(users[-1].id).encode()).decode()
    
    return {
        "data": [user_to_dict(u) for u in users],
        "next_cursor": next_cursor,
        "has_more": has_more
    }
