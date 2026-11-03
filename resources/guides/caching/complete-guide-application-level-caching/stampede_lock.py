import time

def get_with_stampede_protection(key: str, loader: callable) -> object:
    # Check cache
    cached = cache.get(key)
    if cached is not None:
        return cached
    
    # Acquire lock — only one request regenerates
    lock_key = f"lock:{key}"
    acquired = r.set(lock_key, "1", nx=True, ex=10)
    
    if acquired:
        try:
            # Double-check after lock
            cached = cache.get(key)
            if cached is not None:
                return cached
            
            # Load from database
            value = loader()
            cache.set(key, value)
            return value
        finally:
            r.delete(lock_key)
    else:
        # Wait briefly and retry — bounded loop, not recursion
        for _ in range(20):
            time.sleep(0.05)
            cached = cache.get(key)
            if cached is not None:
                return cached
        # Last resort: load directly rather than crash
        return loader()
