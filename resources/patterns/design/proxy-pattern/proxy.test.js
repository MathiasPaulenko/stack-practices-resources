const { test } = require('node:test');
const assert = require('node:assert/strict');
const {
  ReportService,
  LazyReportService,
  CachedReportService,
  ProtectedReportService,
} = require('./proxy.js');

test('virtual proxy defers construction until first use', () => {
  const lazy = new LazyReportService();
  assert.equal(lazy.isInitialized, false);
  lazy.generate('2026-11');
  assert.equal(lazy.isInitialized, true);
});

test('virtual proxy forwards calls to the real subject', () => {
  const lazy = new LazyReportService();
  const report = lazy.generate('2026-11');
  assert.equal(report.month, '2026-11');
  assert.equal(report.rows, 42);
});

test('caching proxy calls the real subject only once per key', () => {
  const real = new ReportService();
  const cached = new CachedReportService(real);
  cached.generate('2026-11');
  cached.generate('2026-11');
  cached.generate('2026-11');
  assert.equal(real.buildCount, 1);
  assert.deepEqual({ hits: cached.hits, misses: cached.misses }, { hits: 2, misses: 1 });
});

test('caching proxy caches different keys independently', () => {
  const real = new ReportService();
  const cached = new CachedReportService(real);
  cached.generate('2026-10');
  cached.generate('2026-11');
  assert.equal(real.buildCount, 2);
});

test('caching proxy refetches after invalidation', () => {
  const real = new ReportService();
  const cached = new CachedReportService(real);
  cached.generate('2026-11');
  cached.invalidate('2026-11');
  cached.generate('2026-11');
  assert.equal(real.buildCount, 2);
});

test('protection proxy allows readers and admins to read', () => {
  const real = new ReportService();
  assert.doesNotThrow(() => new ProtectedReportService(real, 'reader').generate('m'));
  assert.doesNotThrow(() => new ProtectedReportService(real, 'admin').generate('m'));
});

test('protection proxy rejects unknown roles before delegating', () => {
  const real = new ReportService();
  const guest = new ProtectedReportService(real, 'guest');
  assert.throws(() => guest.generate('m'), /Access denied/);
  assert.equal(real.buildCount, 0); // never reached the real subject
});
