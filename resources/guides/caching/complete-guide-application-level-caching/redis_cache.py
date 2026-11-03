import redis
import json

r = redis.Redis(host="localhost", port=6379, db=0)

def get_user(user_id: int) -> dict | None:
    cache_key = f"user:{user_id}"
    cached = r.get(cache_key)
    
    if cached:
        return json.loads(cached)
    
    user = db.users.find_by_id(user_id)
    if user:
        r.setex(cache_key, 3600, json.dumps(user))
    return user
