// Safe POST retries with an Idempotency-Key shared across attempts.
// Only works against APIs that honor the header (Stripe-style).

import { randomUUID } from "node:crypto"; // in browsers: crypto.randomUUID()

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

export async function postWithRetry(url, body, config = {}) {
    const { retries = 3, baseDelay = 500, timeoutMs = 10000 } = config;
    const idempotencyKey = randomUUID();

    for (let attempt = 0; attempt <= retries; attempt++) {
        try {
            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Idempotency-Key": idempotencyKey
                },
                body: JSON.stringify(body),
                signal: AbortSignal.timeout(timeoutMs)
            });

            if (response.ok) return response;
            if (response.status >= 500 && attempt < retries) {
                await sleep(baseDelay * 2 ** attempt);
                continue;
            }
            return response;
        } catch (err) {
            if (attempt < retries) {
                await sleep(baseDelay * 2 ** attempt);
                continue;
            }
            throw err;
        }
    }
}
