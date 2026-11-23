import pytest

from proxy import (
    ReportService,
    LazyReportService,
    CachedReportService,
    ProtectedReportService,
)


def test_virtual_proxy_defers_construction():
    lazy = LazyReportService()
    assert lazy.is_initialized is False
    lazy.generate("2026-11")
    assert lazy.is_initialized is True


def test_virtual_proxy_forwards_calls():
    report = LazyReportService().generate("2026-11")
    assert report["month"] == "2026-11"
    assert report["rows"] == 42


def test_caching_proxy_calls_real_once_per_key():
    real = ReportService()
    cached = CachedReportService(real)
    for _ in range(3):
        cached.generate("2026-11")
    assert real.build_count == 1
    assert (cached.hits, cached.misses) == (2, 1)


def test_caching_proxy_caches_keys_independently():
    real = ReportService()
    cached = CachedReportService(real)
    cached.generate("2026-10")
    cached.generate("2026-11")
    assert real.build_count == 2


def test_caching_proxy_refetches_after_invalidation():
    real = ReportService()
    cached = CachedReportService(real)
    cached.generate("2026-11")
    cached.invalidate("2026-11")
    cached.generate("2026-11")
    assert real.build_count == 2


def test_protection_proxy_allows_reader_and_admin():
    real = ReportService()
    ProtectedReportService(real, "reader").generate("m")
    ProtectedReportService(real, "admin").generate("m")


def test_protection_proxy_rejects_unknown_role_before_delegating():
    real = ReportService()
    guest = ProtectedReportService(real, "guest")
    with pytest.raises(PermissionError, match="Access denied"):
        guest.generate("m")
    assert real.build_count == 0
