const { test } = require('node:test');
const assert = require('node:assert/strict');
const { WeatherClient, CachedWeatherClient } = require('./caching-client.js');

test('serves repeat calls from cache without hitting upstream', async () => {
  const real = new WeatherClient();
  const cached = new CachedWeatherClient(real);
  await cached.getForecast('madrid');
  await cached.getForecast('MADRID'); // case-insensitive key -> hit
  assert.equal(real.calls, 1);
  assert.equal(cached.hits, 1);
  assert.equal(cached.misses, 1);
});

test('coalesces concurrent misses into one upstream call', async () => {
  const real = new WeatherClient();
  const cached = new CachedWeatherClient(real);
  const [a, b, c] = await Promise.all([
    cached.getForecast('paris'),
    cached.getForecast('paris'),
    cached.getForecast('PARIS'),
  ]);
  assert.equal(real.calls, 1);
  assert.equal(a.temp, b.temp);
  assert.equal(b.temp, c.temp);
});

test('refetches after invalidation', async () => {
  const real = new WeatherClient();
  const cached = new CachedWeatherClient(real);
  await cached.getForecast('rome');
  cached.invalidate('rome');
  await cached.getForecast('rome');
  assert.equal(real.calls, 2);
});

test('expires entries past their TTL', async () => {
  const real = new WeatherClient();
  const cached = new CachedWeatherClient(real, { ttlMs: -1 }); // already expired
  await cached.getForecast('oslo');
  await cached.getForecast('oslo');
  assert.equal(real.calls, 2);
});

test('evicts least recently used when maxSize is exceeded', async () => {
  const real = new WeatherClient();
  const cached = new CachedWeatherClient(real, { maxSize: 2 });
  await cached.getForecast('a');
  await cached.getForecast('b');
  await cached.getForecast('c'); // evicts 'a'
  await cached.getForecast('a'); // miss again
  assert.equal(real.calls, 4);
});

test('getStats reports hit rate', async () => {
  const cached = new CachedWeatherClient(new WeatherClient());
  await cached.getForecast('x');
  await cached.getForecast('x');
  await cached.getForecast('y');
  const stats = cached.getStats();
  assert.equal(stats.hits, 1);
  assert.equal(stats.misses, 2);
  assert.ok(Math.abs(stats.hitRate - 1 / 3) < 1e-9);
});
