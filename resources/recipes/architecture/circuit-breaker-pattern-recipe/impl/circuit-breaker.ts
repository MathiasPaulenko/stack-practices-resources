type CircuitState = 'CLOSED' | 'OPEN' | 'HALF_OPEN';

interface CircuitBreakerConfig {
  failureThreshold: number;      // failures before opening
  recoveryTimeout: number;       // ms before half-open
  halfOpenMaxCalls: number;      // test calls in half-open
}

class CircuitBreaker<T extends (...args: any[]) => Promise<any>> {
  private state: CircuitState = 'CLOSED';
  private failures = 0;
  private successes = 0;
  private nextAttempt = Date.now();

  constructor(
    private fn: T,
    private config: CircuitBreakerConfig
  ) {}

  async execute(...args: Parameters<T>): Promise<ReturnType<T>> {
    if (this.state === 'OPEN') {
      if (Date.now() < this.nextAttempt) {
        throw new Error('Circuit breaker is OPEN');
      }
      this.state = 'HALF_OPEN';
      this.successes = 0;
    }

    try {
      const result = await this.fn(...args);
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  private onSuccess(): void {
    if (this.state === 'HALF_OPEN') {
      this.successes++;
      if (this.successes >= this.config.halfOpenMaxCalls) {
        this.state = 'CLOSED';
        this.failures = 0;
      }
    } else {
      this.failures = 0;
    }
  }

  private onFailure(): void {
    this.failures++;
    if (this.state === 'HALF_OPEN' || this.failures >= this.config.failureThreshold) {
      this.state = 'OPEN';
      this.nextAttempt = Date.now() + this.config.recoveryTimeout;
    }
  }

  getState(): CircuitState {
    return this.state;
  }
}

// Usage
const paymentBreaker = new CircuitBreaker(
  (amount: number) => paymentService.charge(amount),
  { failureThreshold: 5, recoveryTimeout: 30000, halfOpenMaxCalls: 3 }
);

try {
  await paymentBreaker.execute(100);
} catch (error) {
  await fallbackPaymentProcessor.charge(100);
}
