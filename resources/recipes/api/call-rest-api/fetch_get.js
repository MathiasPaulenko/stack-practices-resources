// GET request with fetch — check response.ok and parse JSON.
async function fetchUser(userId, baseUrl = "https://api.example.com") {
  const response = await fetch(`${baseUrl}/users/${userId}`);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  return response.json();
}

fetchUser(1)
  .then((user) => console.log(`User: ${user.name || "unknown"}`))
  .catch((err) => console.error("Request failed:", err.message));
