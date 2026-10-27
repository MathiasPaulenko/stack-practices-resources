import hashlib

def key_hash(api_key: str) -> str:
    return hashlib.sha256(api_key.encode()).hexdigest()

# On issue: store key_hash(api_key) in Redis/DB, never api_key itself
# On request: look up redis.get(f"apikey:{key_hash(incoming)}")
