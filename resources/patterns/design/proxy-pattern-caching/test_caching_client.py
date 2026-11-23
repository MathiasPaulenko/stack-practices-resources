import threading

from caching_client import WeatherClient, CachedWeatherClient


def test_repeat_calls_served_from_cache():
    real = WeatherClient()
    cached = CachedWeatherClient(real)
    cached.get_forecast("madrid")
    cached.get_forecast("MADRID")  # case-insensitive key -> hit
    assert real.calls == 1
    assert cached.hits == 1 and cached.misses == 1


def test_concurrent_misses_coalesced_to_one_call():
    real = WeatherClient()
    cached = CachedWeatherClient(real)
    results = []
    threads = [threading.Thread(target=lambda: results.append(cached.get_forecast("paris")))
               for _ in range(5)]
    for t in threads: t.start()
    for t in threads: t.join()
    assert real.calls == 1
    assert all(r["temp"] == results[0]["temp"] for r in results)


def test_refetches_after_invalidation():
    real = WeatherClient()
    cached = CachedWeatherClient(real)
    cached.get_forecast("rome")
    cached.invalidate("rome")
    cached.get_forecast("rome")
    assert real.calls == 2


def test_expired_entries_refetched():
    real = WeatherClient()
    cached = CachedWeatherClient(real, ttl_ms=-1)
    cached.get_forecast("oslo")
    cached.get_forecast("oslo")
    assert real.calls == 2


def test_lru_eviction_on_max_size():
    real = WeatherClient()
    cached = CachedWeatherClient(real, max_size=2)
    cached.get_forecast("a")
    cached.get_forecast("b")
    cached.get_forecast("c")  # evicts "a"
    cached.get_forecast("a")  # miss again
    assert real.calls == 4


def test_stats_hit_rate():
    cached = CachedWeatherClient(WeatherClient())
    cached.get_forecast("x")
    cached.get_forecast("x")
    cached.get_forecast("y")
    stats = cached.get_stats()
    assert stats["hits"] == 1 and stats["misses"] == 2
    assert abs(stats["hit_rate"] - 1 / 3) < 1e-9
