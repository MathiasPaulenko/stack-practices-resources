// Circuit breaker — minimal runnable implementation with fallback support.
// Usage: node circuitBreaker.mjs

export class CircuitBreakerOpen extends Error {}

export class CircuitBreaker {
  /**
   * @param {number} failureThreshold consecutive failures that trip the breaker
   * @param {number} recoveryTimeout ms the breaker stays open before probing
   * @param {(err) => boolean} isFailure return true if the error counts as a failure
   */
  constructor(failureThreshold = 3, recoveryTimeout = 5000, isFailure = () => true) {
    this.failureThreshold = failureThreshold;
    this.recoveryTimeout = recoveryTimeout;
    this.isFailure = isFailure;
    this.state = 'CLOSED';
    this.failures = 0;
    this.lastFailureTime = 0;
  }

  async call(fn, fallback = null) {
    if (this.state === 'OPEN') {
      if (Date.now() - this.lastFailureTime >= this.recoveryTimeout) {
        this.state = 'HALF_OPEN';
      } else {
        if (fallback) return fallback();
        throw new CircuitBreakerOpen('Circuit breaker is OPEN');
      }
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (err) {
      if (!this.isFailure(err)) throw err; // business errors don't count
      this.onFailure();
      if (fallback) return fallback();
      throw err;
    }
  }

  onSuccess() {
    this.failures = 0;
    this.state = 'CLOSED';
  }

  onFailure() {
    this.failures++;
    this.lastFailureTime = Date.now();
    if (this.failures >= this.failureThreshold) {
      this.state = 'OPEN';
    }
  }
}

// Demo
const breaker = new CircuitBreaker(2, 1000);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function flakyService() {
  if (Math.random() < 0.7) throw new Error('Service error');
  return 'Data';
}

for (let i = 0; i < 8; i++) {
  try {
    const result = await breaker.call(flakyService, () => 'cached value');
    console.log(`Call ${i + 1}:`, result);
  } catch (e) {
    console.log(`Call ${i + 1}: ${e.message} (state=${breaker.state})`);
  }
  await sleep(300);
}
