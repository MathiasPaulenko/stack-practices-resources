// GET request with fetch and AbortController timeout (10 seconds).
async function fetchWithTimeout(url, timeoutMs = 10000) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(url, {
      signal: controller.signal,
      headers: { Accept: "application/json" },
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  } catch (err) {
    if (err.name === "AbortError") {
      console.error("Request timed out");
      return null;
    }
    throw err;
  } finally {
    clearTimeout(timeout);
  }
}

fetchWithTimeout("https://api.example.com/users/1")
  .then((data) => data && console.log(`User: ${data.name || "unknown"}`))
  .catch((err) => console.error("Request failed:", err.message));
