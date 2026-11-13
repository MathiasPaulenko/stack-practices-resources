class ServiceResult {
  constructor(data, status, source, degraded = false, error = null) {
    this.data = data;
    this.status = status;
    this.source = source;
    this.degraded = degraded;
    this.error = error;
  }
}

class GracefulDegradation {
  constructor() {
    this.cache = new Map();
  }

  _cacheGet(key) {
    if (this.cache.has(key)) {
      const { data, timestamp } = this.cache.get(key);
      if (Date.now() / 1000 - timestamp < 300) return data;
    }
    return null;
  }

  _cacheSet(key, data) {
    this.cache.set(key, { data, timestamp: Date.now() / 1000 });
  }

  callWithFallback(serviceName, primaryFn, fallbackFn = null, defaultVal = null, cacheKey = null) {
    try {
      const result = primaryFn();
      if (cacheKey) this._cacheSet(cacheKey, result);
      return new ServiceResult(result, "healthy", serviceName);
    } catch (e) {
      if (cacheKey) {
        const cached = this._cacheGet(cacheKey);
        if (cached !== null) {
          return new ServiceResult(cached, "degraded", `${serviceName}:cache`, true, e.message);
        }
      }
      if (fallbackFn) {
        try {
          const result = fallbackFn();
          return new ServiceResult(result, "degraded", `${serviceName}:fallback`, true, e.message);
        } catch (fe) {}
      }
      return new ServiceResult(defaultVal, "down", `${serviceName}:default`, true, e.message);
    }
  }

  aggregate(calls, defaults = {}) {
    const results = {};
    for (const [name, fn] of Object.entries(calls)) {
      results[name] = this.callWithFallback(name, fn, null, defaults[name] ?? null, name);
    }
    return results;
  }
}

// Usage
const deg = new GracefulDegradation();

const results = deg.aggregate(
  {
    product_details: () => ({ id: "P100", name: "Headphones", price: 99.99 }),
    recommendations: () => { throw new Error("Recommendation service down"); },
    reviews: () => [{ user: "alice", rating: 5, text: "Great" }],
    inventory: () => { throw new Error("Inventory API timed out"); },
  },
  {
    recommendations: [],
    inventory: { inStock: null, message: "Check back later" },
  }
);

console.log("=== Page Assembly ===");
for (const [name, result] of Object.entries(results)) {
  const icon = result.degraded ? "DEGRADED" : "OK";
  console.log(`  [${icon}] ${name}: source=${result.source}, data=${JSON.stringify(result.data)}`);
}
