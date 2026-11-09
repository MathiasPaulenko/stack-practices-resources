/**
 * Deployment Ring Pattern — runnable JavaScript implementation.
 *
 * Simulates a progressive rollout through rings of increasing size. A mock
 * health check fails on the third call (ring 2), which forces a rollback
 * of the rings that already passed.
 *
 * Run: node ring-deployment.js
 */

class RingDeployment {
  constructor(version, rings, healthCheckFn, options = {}) {
    this.version = version;
    this.rings = rings;
    this.healthCheckFn = healthCheckFn;
    this.maxErrorRate = options.maxErrorRate ?? 0.05;
    this.maxP95 = options.maxP95 ?? 500;
    this.bakeTimeMs = options.bakeTimeMs ?? 2000;
  }

  async _deployToRing(ring) {
    ring.status = "active";
    ring.startedAt = Date.now();
    console.log(`  Deploying v${this.version} to ${ring.name} (${ring.percentage}% of users)`);

    await new Promise(r => setTimeout(r, this.bakeTimeMs));

    const metrics = this.healthCheckFn();
    ring.healthCheckPassed = metrics.errorRate < this.maxErrorRate && metrics.p95LatencyMs < this.maxP95;

    console.log(`    Health: error_rate=${(metrics.errorRate * 100).toFixed(1)}%, p95=${metrics.p95LatencyMs}ms`);

    if (ring.healthCheckPassed) {
      ring.status = "completed";
      console.log(`    PASS - Ring ${ring.ringId} completed`);
      return true;
    }
    ring.status = "failed";
    console.log(`    FAIL - Ring ${ring.ringId} failed, rolling back`);
    return false;
  }

  async execute() {
    console.log(`\n=== Ring Deployment: v${this.version} ===`);
    for (let i = 0; i < this.rings.length; i++) {
      const success = await this._deployToRing(this.rings[i]);
      if (!success) {
        this._rollback();
        return { version: this.version, status: "rolled_back", failedRing: this.rings[i].ringId, ringsCompleted: i };
      }
    }
    console.log(`\nAll rings completed. v${this.version} is live for 100% of users.`);
    return { version: this.version, status: "completed", ringsCompleted: this.rings.length };
  }

  _rollback() {
    for (const ring of this.rings) {
      if (ring.status === "completed") {
        ring.status = "rolled_back";
        console.log(`  Rolling back ring ${ring.ringId} (${ring.name})`);
      }
    }
  }
}

// Usage
let callCount = 0;
const mockHealthCheck = () => {
  callCount++;
  if (callCount === 3) return { errorRate: 0.08, p95LatencyMs: 600, successRate: 0.92 };
  return { errorRate: 0.01, p95LatencyMs: 120, successRate: 0.99 };
};

const rings = [
  { ringId: 0, name: "internal", percentage: 1.0, status: "pending" },
  { ringId: 1, name: "early-adopters", percentage: 5.0, status: "pending" },
  { ringId: 2, name: "canary", percentage: 25.0, status: "pending" },
  { ringId: 3, name: "general", percentage: 100.0, status: "pending" },
];

(async () => {
  const deployment = new RingDeployment("2.1.0", rings, mockHealthCheck,
    { maxErrorRate: 0.05, maxP95: 500, bakeTimeMs: 100 });
  const result = await deployment.execute();
  console.log(`\nResult:`, result);
})();
