// failover/client.js — Client-side failover for API calls
class FailoverClient {
    constructor(endpoints, options = {}) {
        this.endpoints = endpoints;  // ["https://api1.com", "https://api2.com"]
        this.activeIndex = 0;
        this.healthPath = options.healthPath || "/health";
        this.checkInterval = options.checkInterval || 10000;
        this.failureThreshold = options.failureThreshold || 3;
        this.failures = 0;
        this.isChecking = false;
    }

    get activeEndpoint() {
        return this.endpoints[this.activeIndex];
    }

    async checkHealth() {
        try {
            const response = await fetch(
                `${this.activeEndpoint}${this.healthPath}`,
                { signal: AbortSignal.timeout(3000) }
            );
            if (response.ok) {
                this.failures = 0;
                return true;
            }
        } catch (error) {
            // Health check failed
        }

        this.failures++;
        if (this.failures >= this.failureThreshold) {
            this.failover();
        }
        return false;
    }

    failover() {
        const nextIndex = (this.activeIndex + 1) % this.endpoints.length;
        if (nextIndex !== this.activeIndex) {
            console.log(`Failing over from ${this.endpoints[this.activeIndex]} ` +
                        `to ${this.endpoints[nextIndex]}`);
            this.activeIndex = nextIndex;
            this.failures = 0;
        }
    }

    async request(method, path, options = {}) {
        const url = `${this.activeEndpoint}${path}`;
        try {
            const response = await fetch(url, {
                method,
                ...options,
                signal: AbortSignal.timeout(10000)
            });
            if (response.status >= 500) {
                this.failures++;
                if (this.failures >= this.failureThreshold) {
                    this.failover();
                    // Retry on the new endpoint
                    return this.request(method, path, options);
                }
                throw new Error(`HTTP ${response.status}`);
            }
            this.failures = 0;
            return response;
        } catch (error) {
            this.failures++;
            if (this.failures >= this.failureThreshold) {
                this.failover();
                return this.request(method, path, options);
            }
            throw error;
        }
    }

    startHealthChecks() {
        this.isChecking = true;
        const check = async () => {
            if (!this.isChecking) return;
            await this.checkHealth();
            setTimeout(check, this.checkInterval);
        };
        check();
    }

    stopHealthChecks() {
        this.isChecking = false;
    }
}

export default FailoverClient;

// Usage
// const client = new FailoverClient(
//     ["https://api-primary.example.com", "https://api-standby.example.com"],
//     { failureThreshold: 3, checkInterval: 10000 }
// );
// client.startHealthChecks();
// const response = await client.request("GET", "/api/products");
