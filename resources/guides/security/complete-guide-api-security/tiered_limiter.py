class TieredRateLimiter:
    TIERS = {
        "free": {"limit": 100, "window": 3600},       # 100/hour
        "pro": {"limit": 10000, "window": 3600},      # 10k/hour
        "enterprise": {"limit": 100000, "window": 3600}  # 100k/hour
    }
    
    def __init__(self, redis_limiter: RedisRateLimiter):
        self.limiter = redis_limiter
    
    def check(self, api_key: str, tier: str) -> dict:
        config = self.TIERS.get(tier, self.TIERS["free"])
        allowed = self.limiter.sliding_window(
            key=f"rate_limit:{tier}:{api_key}",
            limit=config["limit"],
            window=config["window"]
        )
        
        return {
            "allowed": allowed,
            "limit": config["limit"],
            "window": config["window"],
            "tier": tier
        }
