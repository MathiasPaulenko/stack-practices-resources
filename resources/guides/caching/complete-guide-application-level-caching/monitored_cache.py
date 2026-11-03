def get_user_resilient(user_id: int) -> dict | None:
    try:
        cached = cache.get(f"user:{user_id}")
        if cached:
            return cached
    except Exception:
        pass  # Cache unavailable, fall back to DB
    
    return db.users.find_by_id(user_id)
