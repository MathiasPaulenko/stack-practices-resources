import requests
import hashlib
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor

class CDNManager:
    """Manages CDN interactions for cache warmup, purging, and health checks"""
    def __init__(self, base_url: str, api_key: str = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.edge_locations = [
            "us-east", "us-west", "eu-west", "eu-central",
            "ap-southeast", "ap-northeast", "sa-east"
        ]

    def generate_cache_key(self, path: str, params: Dict = None) -> str:
        """Generate a deterministic cache key for a URL"""
        content = f"{path}:{sorted(params.items()) if params else ''}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def warmup_cache(self, paths: List[str]) -> Dict[str, bool]:
        """Pre-populate CDN edge caches by requesting through each location"""
        results = {}

        def fetch(path):
            try:
                response = requests.get(
                    f"{self.base_url}{path}",
                    headers={"X-Cache-Warmup": "true"},
                    timeout=30
                )
                return path, response.status_code == 200
            except Exception:
                return path, False

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(fetch, p) for p in paths]
            for future in futures:
                path, success = future.result()
                results[path] = success

        return results

    def purge_cache(self, path: str) -> bool:
        """Purge a specific path from the CDN cache"""
        # Implementation varies by CDN provider (Fastly, Cloudflare, etc.)
        # This example uses a generic purge endpoint
        try:
            response = requests.post(
                f"{self.base_url}/__purge",
                json={"path": path},
                headers={"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Purge failed for {path}: {e}")
            return False

    def get_cache_status(self, path: str) -> Dict:
        """Check cache HIT/MISS status for a path"""
        response = requests.get(f"{self.base_url}{path}")
        return {
            "path": path,
            "cache_status": response.headers.get("X-Cache", "unknown"),
            "age": response.headers.get("Age", "0"),
            "ttl_remaining": response.headers.get("Cache-Control", "")
        }


if __name__ == "__main__":
    cdn = CDNManager("https://cdn.example.com", api_key="secret-key")

    # Warmup critical paths after deployment
    warmup_results = cdn.warmup_cache([
        "/assets/main.css",
        "/assets/app.js",
        "/api/config"
    ])
    print(f"Cache warmup: {sum(warmup_results.values())}/{len(warmup_results)} successful")

    # Check cache status
    status = cdn.get_cache_status("/assets/main.css")
    print(f"Cache: {status['cache_status']}, Age: {status['age']}s")
