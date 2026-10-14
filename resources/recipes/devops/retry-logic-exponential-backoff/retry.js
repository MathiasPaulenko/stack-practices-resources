// Configurable retry helper with exponential backoff and jitter.
// Companion code for https://stackpractices.com/recipes/retry-logic-exponential-backoff/
//
// `sleep` is injectable so tests can record delays instead of waiting.

async function retry(fn, options = {}) {
  const {
    maxRetries = 3,
    baseDelay = 1000,
    maxDelay = 60000,
    jitter = true,
    retryableStatuses = [408, 429, 500, 502, 503, 504],
    onRetry = null,
    sleep = (ms) => new Promise((r) => setTimeout(r, ms)),
  } = options;

  let lastError;
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (err) {
      lastError = err;
      const isHttp = typeof err.status === "number";
      if (attempt === maxRetries || (isHttp && !retryableStatuses.includes(err.status))) {
        throw err;
      }
      let delay = Math.min(baseDelay * 2 ** attempt, maxDelay);
      if (jitter) delay = Math.random() * delay;
      if (onRetry) onRetry(err, attempt + 1, delay);
      await sleep(delay);
    }
  }
  throw lastError;
}

// Usage — generates one idempotency key per operation, reused on every retry.
async function createOrder(payload, idempotencyKey = crypto.randomUUID()) {
  return retry(async () => {
    const res = await fetch("https://api.example.com/orders", {
      method: "POST",
      headers: { "Content-Type": "application/json", "Idempotency-Key": idempotencyKey },
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      const err = new Error(`HTTP ${res.status}`);
      err.status = res.status;
      throw err;
    }
    return res.json();
  });
}

// Demo without network access: flaky fn fails twice, then succeeds.
if (process.argv[1].endsWith("retry.js")) {
  let n = 0;
  retry(async () => {
    n++;
    if (n < 3) throw new Error(`transient failure #${n}`);
    return "ok";
  }, { maxRetries: 5, baseDelay: 100 }).then((r) => console.log(r, `after ${n} attempts`));
}

module.exports = { retry, createOrder };
