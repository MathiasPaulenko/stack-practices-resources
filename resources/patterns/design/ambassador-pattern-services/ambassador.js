/**
 * Ambassador pattern — a local proxy that owns remote-call resilience.
 *
 * The ambassador wraps a remote service behind the same interface the
 * client expects. Retries, timeouts, circuit breaking, and metrics
 * live here; the client just calls `call()`.
 *
 * Run the demo:   node ambassador.js
 * Run the tests:  node --test ambassador.test.js
 */

class RemoteError extends Error {}

class CircuitOpenError extends Error {}

// Order of operations: circuit check -> retry loop -> per-attempt
// timeout. The timeout bounds each attempt; the circuit bounds the
// whole disaster.
class ServiceAmbassador {
  constructor(remote, {
    retryCount = 3,
    timeoutMs = 2000,
    failureThreshold = 5,
    resetAfterMs = 30000,
    baseDelayMs = 1000,
    jitterMs = 500,
    sleep = (ms) => new Promise((r) => setTimeout(r, ms)),
    clock = () => Date.now(),
  } = {}) {
    this.remote = remote;
    this.retryCount = retryCount;
    this.timeoutMs = timeoutMs;
    this.failureThreshold = failureThreshold;
    this.resetAfterMs = resetAfterMs;
    this.baseDelayMs = baseDelayMs;
    this.jitterMs = jitterMs;
    this.sleep = sleep;
    this.clock = clock;
    this.state = "closed";
    this.failureCount = 0;
    this.openedAt = 0;
  }

  async call() {
    if (this.state === "open") {
      // After the cool-down, let exactly one trial call through
      if (this.clock() - this.openedAt >= this.resetAfterMs) {
        this.state = "half-open";
      } else {
        throw new CircuitOpenError("circuit breaker is open");
      }
    }

    for (let attempt = 0; attempt < this.retryCount; attempt++) {
      try {
        const result = await this.callWithTimeout();
        this.onSuccess();
        return result;
      } catch (err) {
        this.onFailure();
        if (attempt === this.retryCount - 1) throw err;
        // Real exponential backoff plus jitter, so clients don't
        // retry in lockstep after an outage
        await this.sleep(this.baseDelayMs * 2 ** attempt + Math.random() * this.jitterMs);
      }
    }
    throw new RemoteError("unreachable");
  }

  callWithTimeout() {
    return Promise.race([
      this.remote(),
      new Promise((_, reject) =>
        setTimeout(() => reject(new RemoteError("timeout")), this.timeoutMs)
      ),
    ]);
  }

  onSuccess() {
    this.failureCount = 0;
    this.state = "closed";
  }

  onFailure() {
    this.failureCount++;
    if (this.state === "half-open" || this.failureCount >= this.failureThreshold) {
      this.state = "open";
      this.openedAt = this.clock();
    }
  }
}

// Wraps any ambassador (or the raw remote) and counts outcomes.
// Composes cleanly: MonitoringAmbassador(ServiceAmbassador(remote))
// sees final results, not per-attempt noise.
class MonitoringAmbassador {
  constructor(inner) {
    this.inner = inner;
    this.requests = 0;
    this.errors = 0;
    this.totalLatencyMs = 0;
  }

  async call() {
    const start = Date.now();
    this.requests++;
    try {
      return await (typeof this.inner === "function"
        ? this.inner()
        : this.inner.call());
    } catch (err) {
      this.errors++;
      throw err;
    } finally {
      this.totalLatencyMs += Date.now() - start;
    }
  }

  metrics() {
    return {
      requests: this.requests,
      errors: this.errors,
      avgLatencyMs: this.requests ? this.totalLatencyMs / this.requests : 0,
    };
  }
}

function demo() {
  let attempts = 0;
  const flakyRemote = async () => {
    attempts++;
    if (attempts < 3) throw new RemoteError("HTTP 503");
    return { id: "user-123", name: "Ana" };
  };

  const ambassador = new ServiceAmbassador(flakyRemote, {
    baseDelayMs: 50,
    jitterMs: 0,
  });
  const monitored = new MonitoringAmbassador(ambassador);

  monitored.call().then((result) => {
    console.log("result:", result);
    console.log("metrics:", monitored.metrics());
  });
}

if (require.main === module) {
  demo();
}

module.exports = {
  ServiceAmbassador,
  MonitoringAmbassador,
  RemoteError,
  CircuitOpenError,
};
