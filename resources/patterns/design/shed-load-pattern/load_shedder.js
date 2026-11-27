class LoadShedder {
  constructor(options = {}) {
    this.maxConcurrent = options.maxConcurrent ?? 100;
    this.cpuThreshold = options.cpuThreshold ?? 0.85;
    this.memoryThreshold = options.memoryThreshold ?? 0.90;
    this.queueThreshold = options.queueThreshold ?? 500;
    this.active = 0;
    this.shedCount = 0;
    this.acceptCount = 0;
  }

  _getMetrics() {
    const mem = process.memoryUsage();
    const memUsage = mem.rss / (mem.rss + 512 * 1024 * 1024);
    return {
      activeRequests: this.active,
      queueDepth: this.active * 10,
      cpuUsage: Math.min(this.active / this.maxConcurrent, 1.0),
      memoryUsage: memUsage,
    };
  }

  shouldShed() {
    const m = this._getMetrics();
    if (this.active >= this.maxConcurrent) return true;
    if (m.cpuUsage >= this.cpuThreshold) return true;
    if (m.memoryUsage >= this.memoryThreshold) return true;
    return m.queueDepth >= this.queueThreshold;
  }

  async execute(requestId, handler) {
    if (this.shouldShed()) {
      this.shedCount++;
      return {
        requestId,
        status: "shed",
        message: "Service overloaded, retry later",
        httpStatus: 503,
      };
    }
    this.active++;
    this.acceptCount++;
    try {
      const result = await handler(requestId);
      return { requestId, status: "accepted", result, httpStatus: 200 };
    } finally {
      this.active--;
    }
  }

  stats() {
    const total = this.acceptCount + this.shedCount;
    return {
      accepted: this.acceptCount,
      shed: this.shedCount,
      active: this.active,
      shedRate: this.shedCount / Math.max(total, 1),
    };
  }
}

// Usage
const shedder = new LoadShedder({
  maxConcurrent: 3, cpuThreshold: 0.95, memoryThreshold: 0.95,
});

async function mockHandler(reqId) {
  await new Promise(r => setTimeout(r, 100));
  return `processed-${reqId}`;
}

(async () => {
  const requests = Array.from({ length: 10 }, (_, i) =>
    shedder.execute(`req-${i}`, mockHandler));
  const results = await Promise.all(requests);
  for (const r of results) {
    console.log(`  ${r.requestId}: ${r.status} (HTTP ${r.httpStatus})`);
  }
  console.log(`\nStats:`, shedder.stats());
})();
