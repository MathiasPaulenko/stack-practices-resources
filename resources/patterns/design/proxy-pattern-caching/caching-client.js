/**
 * Caching proxy — wraps a "remote" client behind the same interface and
 * serves repeat calls from a TTL cache. Includes request coalescing,
 * hit/miss metrics, LRU bounds, and explicit invalidation.
 *
 * Run the demo:   node caching-client.js
 * Run the tests:  node --test caching-client.test.js
 */

// Real subject stand-in: counts calls like a metered API would bill them.
class WeatherClient {
  constructor() {
    this.calls = 0;
  }

  async getForecast(city) {
    this.calls += 1;
    return { city, temp: 12 + this.calls, calls: this.calls };
  }
}

// Caching proxy: same interface, TTL map, in-flight promise coalescing.
class CachedWeatherClient {
  constructor(client, { ttlMs = 300_000, maxSize = 1000 } = {}) {
    this.client = client;
    this.ttlMs = ttlMs;
    this.maxSize = maxSize;
    this.cache = new Map();   // key -> { data, expiry }
    this.inflight = new Map(); // key -> Promise  (miss coalescing)
    this.accessOrder = [];
    this.hits = 0;
    this.misses = 0;
  }

  #key(city) {
    return city.toLowerCase();
  }

  async getForecast(city) {
    const key = this.#key(city);
    const cached = this.cache.get(key);
    if (cached && cached.expiry > Date.now()) {
      this.hits += 1;
      this.#touch(key);
      return cached.data;
    }

    // Coalesce concurrent misses into one upstream call.
    if (this.inflight.has(key)) {
      return this.inflight.get(key);
    }

    this.misses += 1;
    const pending = this.client.getForecast(city).then((data) => {
      this.cache.set(key, { data, expiry: Date.now() + this.ttlMs });
      this.#touch(key);
      this.#evictIfNeeded();
      this.inflight.delete(key);
      return data;
    });
    this.inflight.set(key, pending);
    return pending;
  }

  invalidate(city) {
    this.cache.delete(this.#key(city));
  }

  getStats() {
    const total = this.hits + this.misses;
    return { hits: this.hits, misses: this.misses, hitRate: total ? this.hits / total : 0 };
  }

  #touch(key) {
    const i = this.accessOrder.indexOf(key);
    if (i > -1) this.accessOrder.splice(i, 1);
    this.accessOrder.push(key);
  }

  #evictIfNeeded() {
    while (this.cache.size > this.maxSize) {
      const oldest = this.accessOrder.shift();
      if (oldest) this.cache.delete(oldest);
    }
  }
}

if (require.main === module) {
  (async () => {
    const real = new WeatherClient();
    const cached = new CachedWeatherClient(real, { ttlMs: 60_000 });

    // Concurrent calls on a cold key: one upstream call, three answers.
    const [a, b, c] = await Promise.all([
      cached.getForecast('London'),
      cached.getForecast('London'),
      cached.getForecast('LONDON'),
    ]);
    console.log('Upstream calls after 3 concurrent requests:', real.calls); // 1
    console.log('All callers got the same data:', a.temp === b.temp && b.temp === c.temp);

    await cached.getForecast('London'); // hit
    console.log('Stats:', cached.getStats());

    cached.invalidate('london');
    await cached.getForecast('London'); // miss again
    console.log('Upstream calls after invalidation:', real.calls); // 2
  })();
}

module.exports = { WeatherClient, CachedWeatherClient };
