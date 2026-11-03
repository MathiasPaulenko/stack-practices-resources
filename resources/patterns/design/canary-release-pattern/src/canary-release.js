class CanaryRelease {
  constructor(version, stableVersion, healthCheckFn, options = {}) {
    this.version = version;
    this.stableVersion = stableVersion;
    this.healthCheckFn = healthCheckFn;
    this.maxErrorRate = options.maxErrorRate ?? 0.02;
    this.maxP95 = options.maxP95 ?? 300;
    this.status = "pending";
    this.currentStageIdx = -1;
    // Demo bake times; real stages run for minutes, not milliseconds.
    this.stages = options.stages ?? [
      { percentage: 1.0, bakeTimeMs: 100 },
      { percentage: 5.0, bakeTimeMs: 100 },
      { percentage: 25.0, bakeTimeMs: 100 },
      { percentage: 50.0, bakeTimeMs: 100 },
      { percentage: 100.0, bakeTimeMs: 100 },
    ];
  }

  async _runStage(stage) {
    this.currentStageIdx++;
    this.status = "running";
    console.log(`  Canary at ${stage.percentage}% -> stable=${100 - stage.percentage}%`);
    await new Promise(r => setTimeout(r, stage.bakeTimeMs));
    const m = this.healthCheckFn();
    const healthy = m.errorRate <= this.maxErrorRate && m.p95LatencyMs <= this.maxP95;
    console.log(`    error_rate=${(m.errorRate * 100).toFixed(2)}%, p95=${m.p95LatencyMs}ms`);
    if (healthy) { console.log(`    PASS - advancing`); return true; }
    console.log(`    FAIL - rolling back`);
    this.status = "rolled_back";
    return false;
  }

  async execute() {
    console.log(`\n=== Canary Release: v${this.version} (stable: v${this.stableVersion}) ===`);
    for (let i = 0; i < this.stages.length; i++) {
      if (!await this._runStage(this.stages[i])) {
        return { version: this.version, status: this.status, rolledBack: true,
                 stagesPassed: this.currentStageIdx, failedStage: i,
                 maxPercentage: this.stages[this.currentStageIdx].percentage };
      }
    }
    this.status = "promoted";
    console.log(`\nCanary promoted. v${this.version} is now at 100%.`);
    return { version: this.version, status: this.status, rolledBack: false,
             stagesPassed: this.stages.length, maxPercentage: 100 };
  }
}

// Usage
let callCount = 0;
const mockHealthCheck = () => {
  callCount++;
  if (callCount === 3) return { errorRate: 0.05, p95LatencyMs: 400, successRate: 0.95 };
  return { errorRate: 0.005, p95LatencyMs: 80, successRate: 0.995 };
};

(async () => {
  const canary = new CanaryRelease("3.0.0", "2.9.0", mockHealthCheck, { maxErrorRate: 0.02, maxP95: 300 });
  console.log("\nResult:", await canary.execute());
})();
