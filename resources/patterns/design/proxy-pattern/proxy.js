/**
 * Proxy pattern — lazy loading, access control and caching in front of
 * a single real subject. Each proxy is small and single-purpose; the
 * composition does the work.
 *
 * Run the demo:   node proxy.js
 * Run the tests:  node --test proxy.test.js
 */

// Real subject: an "expensive" report generator. The counter makes the
// cost observable — a good proxy never builds this twice unnecessarily.
class ReportService {
  constructor() {
    this.buildCount = 0;
  }

  generate(month) {
    this.buildCount += 1;
    return { month, rows: 42, builtAt: this.buildCount };
  }
}

// Virtual proxy: defer construction until the first real call.
class LazyReportService {
  constructor() {
    this._service = null;
  }

  get service() {
    if (this._service === null) {
      this._service = new ReportService();
    }
    return this._service;
  }

  generate(month) {
    return this.service.generate(month);
  }

  get isInitialized() {
    return this._service !== null;
  }
}

// Caching proxy: memoize generate() per month; expose stats so tests
// and callers can verify hits vs. real calls.
class CachedReportService {
  constructor(real) {
    this.real = real;
    this.cache = new Map();
    this.hits = 0;
    this.misses = 0;
  }

  generate(month) {
    if (this.cache.has(month)) {
      this.hits += 1;
      return this.cache.get(month);
    }
    this.misses += 1;
    const report = this.real.generate(month);
    this.cache.set(month, report);
    return report;
  }

  invalidate(month) {
    this.cache.delete(month);
  }
}

// Protection proxy: enforce role-based access before delegating.
const ROLES = { admin: ["read", "write"], reader: ["read"] };

class ProtectedReportService {
  constructor(real, role) {
    this.real = real;
    this.role = role;
  }

  generate(month) {
    if (!ROLES[this.role]?.includes("read")) {
      throw new Error(`Access denied: role "${this.role}" cannot read reports`);
    }
    return this.real.generate(month);
  }
}

if (require.main === module) {
  const lazy = new LazyReportService();
  console.log("Before first call — initialized?", lazy.isInitialized); // false
  lazy.generate("2026-11");
  console.log("After first call — initialized?", lazy.isInitialized);  // true

  const cached = new CachedReportService(lazy);
  cached.generate("2026-11"); // miss (delegates to lazy -> real)
  cached.generate("2026-11"); // hit
  console.log("Cache stats:", { hits: cached.hits, misses: cached.misses });
  console.log("Real builds:", lazy.service.buildCount); // 1 — not per call

  const guest = new ProtectedReportService(cached, "guest");
  try {
    guest.generate("2026-11");
  } catch (err) {
    console.log(err.message);
  }
}

module.exports = {
  ReportService,
  LazyReportService,
  CachedReportService,
  ProtectedReportService,
};
