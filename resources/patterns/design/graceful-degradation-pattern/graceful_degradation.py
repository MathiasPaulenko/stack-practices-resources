from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Any
from enum import Enum
import time
import json

class ServiceStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    DOWN = "down"

@dataclass
class ServiceResult:
    data: Any
    status: ServiceStatus
    source: str
    degraded: bool = False
    error: Optional[str] = None

class GracefulDegradation:
    def __init__(self):
        self._cache: Dict[str, tuple] = {}

    def _cache_get(self, key: str) -> Optional[Any]:
        if key in self._cache:
            data, timestamp = self._cache[key]
            if time.time() - timestamp < 300:
                return data
        return None

    def _cache_set(self, key: str, data: Any) -> None:
        self._cache[key] = (data, time.time())

    def call_with_fallback(
        self,
        service_name: str,
        primary_fn: Callable,
        fallback_fn: Optional[Callable] = None,
        default: Any = None,
        cache_key: Optional[str] = None,
    ) -> ServiceResult:
        try:
            result = primary_fn()
            if cache_key:
                self._cache_set(cache_key, result)
            return ServiceResult(data=result, status=ServiceStatus.HEALTHY, source=service_name)

        except Exception as e:
            if cache_key:
                cached = self._cache_get(cache_key)
                if cached is not None:
                    return ServiceResult(
                        data=cached, status=ServiceStatus.DEGRADED,
                        source=f"{service_name}:cache", degraded=True, error=str(e),
                    )

            if fallback_fn:
                try:
                    result = fallback_fn()
                    return ServiceResult(
                        data=result, status=ServiceStatus.DEGRADED,
                        source=f"{service_name}:fallback", degraded=True, error=str(e),
                    )
                except Exception as fe:
                    pass

            return ServiceResult(
                data=default, status=ServiceStatus.DOWN,
                source=f"{service_name}:default", degraded=True, error=str(e),
            )

    def aggregate(
        self,
        calls: Dict[str, Callable],
        defaults: Dict[str, Any] = None,
    ) -> Dict[str, ServiceResult]:
        defaults = defaults or {}
        results = {}
        for name, fn in calls.items():
            results[name] = self.call_with_fallback(
                service_name=name,
                primary_fn=fn,
                default=defaults.get(name),
                cache_key=name,
            )
        return results

# Usage
deg = GracefulDegradation()

def fetch_recommendations():
    raise ConnectionError("Recommendation service down")

def fetch_reviews():
    return [{"user": "alice", "rating": 5, "text": "Great product"}]

def fetch_inventory():
    raise TimeoutError("Inventory API timed out")

def fetch_product_details():
    return {"id": "P100", "name": "Wireless Headphones", "price": 99.99}

results = deg.aggregate(
    calls={
        "product_details": fetch_product_details,
        "recommendations": fetch_recommendations,
        "reviews": fetch_reviews,
        "inventory": fetch_inventory,
    },
    defaults={
        "recommendations": [],
        "inventory": {"in_stock": None, "message": "Check back later"},
    },
)

print("=== Page Assembly ===")
for name, result in results.items():
    status_icon = "OK" if not result.degraded else "DEGRADED"
    print(f"  [{status_icon}] {name}: source={result.source}")
    if result.error:
        print(f"         error: {result.error}")
    print(f"         data: {result.data}")
