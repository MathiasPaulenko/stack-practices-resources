// Client-side retry with exponential backoff + jitter for 429 responses
async function fetchWithRetry(url, options, maxRetries = 3) {
  let attempt = 0;
  while (attempt < maxRetries) {
    const response = await fetch(url, options);
    if (response.status !== 429) {
      return response;
    }
    const retryAfter = parseInt(response.headers.get("Retry-After") || "1");
    const jitter = Math.random() * 0.5;
    const delay = (retryAfter + jitter) * 1000;
    console.warn(`Rate limited. Retrying in ${delay}ms (attempt ${attempt + 1})`);
    await new Promise((resolve) => setTimeout(resolve, delay));
    attempt++;
  }
  throw new Error(`Max retries (${maxRetries}) exceeded`);
}
