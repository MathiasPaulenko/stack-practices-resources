from functools import lru_cache

@lru_cache(maxsize=1024)
def get_user(user_id: int) -> dict:
    return db.users.find_by_id(user_id)
