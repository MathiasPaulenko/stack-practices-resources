// Fetch retry with exponential backoff, full jitter, AbortSignal timeouts
// and Retry-After handling. Works in browsers and Node.js 18+.

export function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Full jitter — random point inside the whole window, not noise on top
export function jitterDelay(attempt, baseDelay, maxDelay) {
    const ceiling = Math.min(baseDelay * 2 ** attempt, maxDelay);
    return Math.floor(Math.random() * ceiling);
}

export async function fetchWithRetry(url, options = {}, config = {}) {
    const {
        retries = 3,
        baseDelay = 1000,
        maxDelay = 30000,
        timeoutMs = 10000
    } = config;

    for (let attempt = 0; attempt <= retries; attempt++) {
        // Merge the per-attempt deadline with any signal the caller passed
        const signal = options.signal
            ? AbortSignal.any([options.signal, AbortSignal.timeout(timeoutMs)])
            : AbortSignal.timeout(timeoutMs);

        try {
            const response = await fetch(url, { ...options, signal });

            if (response.ok) return response;

            if (response.status === 429 && attempt < retries) {
                const retryAfter = parseInt(response.headers.get("Retry-After") || "0", 10);
                const wait = retryAfter > 0
                    ? retryAfter * 1000
                    : jitterDelay(attempt, baseDelay, maxDelay);
                await sleep(wait);
                continue;
            }

            if (response.status >= 500 && attempt < retries) {
                await sleep(jitterDelay(attempt, baseDelay, maxDelay));
                continue;
            }

            return response; // 4xx and other definitive statuses — no retry
        } catch (err) {
            // Caller aborts mean "cancel", not "retry"
            if (options.signal?.aborted) throw err;
            if (attempt < retries) {
                await sleep(jitterDelay(attempt, baseDelay, maxDelay));
                continue;
            }
            throw err;
        }
    }
}
