// Retry wrapper with a circuit breaker that only counts availability
// failures (5xx, 429, network/timeout) — definitive 4xx stay neutral.

export class CircuitBreaker {
    constructor(threshold = 5, resetTimeout = 60000) {
        this.threshold = threshold;
        this.resetTimeout = resetTimeout;
        this.failures = 0;
        this.lastFailureTime = null;
        this.state = "closed"; // closed | open | half-open
    }

    recordFailure() {
        this.failures++;
        this.lastFailureTime = Date.now();
        if (this.failures >= this.threshold) this.state = "open";
    }

    recordSuccess() {
        this.failures = 0;
        this.state = "closed";
    }

    canExecute() {
        if (this.state === "open") {
            if (Date.now() - this.lastFailureTime > this.resetTimeout) {
                this.state = "half-open";
                return true;
            }
            return false;
        }
        return true;
    }
}

export class FetchWithRetry {
    constructor(config = {}) {
        this.retries = config.retries ?? 3;
        this.baseDelay = config.baseDelay ?? 1000;
        this.maxDelay = config.maxDelay ?? 30000;
        this.timeoutMs = config.timeoutMs ?? 10000;
        this.breaker = new CircuitBreaker(
            config.breakerThreshold ?? 5,
            config.breakerResetTimeout ?? 60000
        );
    }

    isAvailabilityFailure(status) {
        return status >= 500 || status === 429;
    }

    async request(url, options = {}) {
        if (!this.breaker.canExecute()) {
            throw new Error("Circuit breaker is open — requests temporarily blocked");
        }

        for (let attempt = 0; attempt <= this.retries; attempt++) {
            const signal = options.signal
                ? AbortSignal.any([options.signal, AbortSignal.timeout(this.timeoutMs)])
                : AbortSignal.timeout(this.timeoutMs);

            try {
                const response = await fetch(url, { ...options, signal });

                if (response.ok) {
                    this.breaker.recordSuccess();
                    return response;
                }

                if (this.isAvailabilityFailure(response.status)) {
                    this.breaker.recordFailure();
                    if (attempt < this.retries) {
                        await this.waitFor(response, attempt);
                        continue;
                    }
                }

                return response;
            } catch (err) {
                if (options.signal?.aborted) throw err;
                this.breaker.recordFailure();
                if (attempt < this.retries) {
                    await this.sleep(this.jitter(attempt));
                    continue;
                }
                throw err;
            }
        }
    }

    waitFor(response, attempt) {
        if (response.status === 429) {
            const retryAfter = parseInt(response.headers.get("Retry-After") || "0", 10);
            if (retryAfter > 0) return this.sleep(retryAfter * 1000);
        }
        return this.sleep(this.jitter(attempt));
    }

    jitter(attempt) {
        const ceiling = Math.min(this.baseDelay * 2 ** attempt, this.maxDelay);
        return Math.floor(Math.random() * ceiling);
    }

    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}
