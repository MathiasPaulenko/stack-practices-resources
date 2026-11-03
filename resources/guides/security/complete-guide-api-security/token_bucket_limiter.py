import time
from collections import defaultdict
from threading import Lock

class TokenBucketRateLimiter:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate  # tokens per second
        self.buckets: dict[str, dict] = defaultdict(lambda: {
            "tokens": capacity,
            "last_refill": time.time()
        })
        self.lock = Lock()
    
    def allow_request(self, key: str) -> bool:
        with self.lock:
            bucket = self.buckets[key]
            now = time.time()
            
            # Refill tokens
            elapsed = now - bucket["last_refill"]
            bucket["tokens"] = min(
                self.capacity,
                bucket["tokens"] + elapsed * self.refill_rate
            )
            bucket["last_refill"] = now
            
            if bucket["tokens"] >= 1:
                bucket["tokens"] -= 1
                return True
            return False

# Usage: 100 requests per minute per IP
rate_limiter = TokenBucketRateLimiter(capacity=100, refill_rate=100/60)

from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    if not rate_limiter.allow_request(client_ip):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded",
            headers={"Retry-After": "60"}
        )
    response = await call_next(request)
    response.headers["X-RateLimit-Limit"] = "100"
    response.headers["X-RateLimit-Remaining"] = str(int(rate_limiter.buckets[client_ip]["tokens"]))
    return response
