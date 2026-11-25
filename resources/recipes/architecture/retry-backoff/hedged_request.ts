/**
 * Hedged requests: fire a duplicate request after `hedgedDelay` ms
 * if the first one hasn't answered yet. First to finish wins;
 * the loser gets cancelled via AbortController.
 */

async function hedgedRequest(
  url: string,
  options: RequestInit,
  hedgedDelay: number = 200
): Promise<Response> {
  const controller = new AbortController();

  const firstPromise = fetch(url, { ...options, signal: controller.signal });

  const hedgedPromise = new Promise<Response>((resolve, reject) => {
    setTimeout(() => {
      if (!controller.signal.aborted) {
        fetch(url, { ...options, signal: controller.signal }).then(resolve, reject);
      }
    }, hedgedDelay);
    // If the first request settles or is cancelled before the delay,
    // reject so the race never hangs on a promise that can't settle.
    controller.signal.addEventListener("abort", () =>
      reject(new DOMException("Hedged request cancelled", "AbortError"))
    );
  });

  try {
    return await Promise.race([firstPromise, hedgedPromise]);
  } finally {
    controller.abort();
  }
}

// Usage:
// const res = await hedgedRequest("https://api.example.com/data", {
//   method: "GET",
//   headers: { Accept: "application/json" },
// }, 150);
export { hedgedRequest };
