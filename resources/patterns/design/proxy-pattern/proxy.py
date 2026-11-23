"""Proxy pattern — lazy loading, access control and caching in Python.

Same composition as the JavaScript version: three single-purpose
proxies in front of one real subject.

Run the demo:   python proxy.py
Run the tests:  python -m pytest test_proxy.py -v
"""


class ReportService:
    """Real subject: an 'expensive' report generator."""

    def __init__(self):
        self.build_count = 0

    def generate(self, month: str) -> dict:
        self.build_count += 1
        return {"month": month, "rows": 42, "built_at": self.build_count}


class LazyReportService:
    """Virtual proxy: defer construction until the first real call."""

    def __init__(self):
        self._service = None

    @property
    def service(self) -> ReportService:
        if self._service is None:
            self._service = ReportService()
        return self._service

    @property
    def is_initialized(self) -> bool:
        return self._service is not None

    def generate(self, month: str) -> dict:
        return self.service.generate(month)


class CachedReportService:
    """Caching proxy: memoize generate() per month."""

    def __init__(self, real):
        self.real = real
        self.cache: dict[str, dict] = {}
        self.hits = 0
        self.misses = 0

    def generate(self, month: str) -> dict:
        if month in self.cache:
            self.hits += 1
            return self.cache[month]
        self.misses += 1
        report = self.real.generate(month)
        self.cache[month] = report
        return report

    def invalidate(self, month: str) -> None:
        self.cache.pop(month, None)


ROLES = {"admin": {"read", "write"}, "reader": {"read"}}


class ProtectedReportService:
    """Protection proxy: enforce role-based access before delegating."""

    def __init__(self, real, role: str):
        self.real = real
        self.role = role

    def generate(self, month: str) -> dict:
        if "read" not in ROLES.get(self.role, set()):
            raise PermissionError(f'Access denied: role "{self.role}" cannot read reports')
        return self.real.generate(month)


if __name__ == "__main__":
    lazy = LazyReportService()
    print("Before first call — initialized?", lazy.is_initialized)  # False
    lazy.generate("2026-11")
    print("After first call — initialized?", lazy.is_initialized)   # True

    cached = CachedReportService(lazy)
    cached.generate("2026-11")  # miss
    cached.generate("2026-11")  # hit
    print("Cache stats:", {"hits": cached.hits, "misses": cached.misses})
    print("Real builds:", lazy.service.build_count)  # 1

    guest = ProtectedReportService(cached, "guest")
    try:
        guest.generate("2026-11")
    except PermissionError as err:
        print(err)
