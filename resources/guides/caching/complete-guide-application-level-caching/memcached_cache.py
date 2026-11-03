import memcache
import json

mc = memcache.Client(["localhost:11211"], debug=0)

def get_user(user_id: int) -> dict | None:
    cached = mc.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)
    
    user = db.users.find_by_id(user_id)
    if user:
        mc.set(f"user:{user_id}", json.dumps(user), time=3600)
    return user
