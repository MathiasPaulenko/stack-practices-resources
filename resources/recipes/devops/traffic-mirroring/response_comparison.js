const express = require("express");

const app = express();
app.use(express.json());

/**
 * Middleware that mirrors production traffic to staging and compares responses.
 * The production response is always returned to the client.
 * The staging response is compared async and logged if different.
 */
app.use(async (req, res, next) => {
  const prodResponse = await fetch(`http://production:8080${req.url}`, {
    method: req.method,
    headers: req.headers,
    body: JSON.stringify(req.body),
  });

  const prodJson = await prodResponse.json();

  // Fire-and-forget: do not block production on staging
  fetch(`http://staging:8080${req.url}`, {
    method: req.method,
    headers: sanitizeHeaders(req.headers),
    body: JSON.stringify(req.body),
  })
    .then((stagingResponse) => stagingResponse.json())
    .then((stagingJson) => {
      const diff = deepDiff(prodJson, stagingJson);
      if (diff) {
        console.log(JSON.stringify({
          url: req.url,
          method: req.method,
          diff,
          timestamp: new Date().toISOString(),
        }));
      }
    })
    .catch((err) => {
      console.error("Mirror request failed:", err.message);
    });

  res.status(prodResponse.status).json(prodJson);
});

function sanitizeHeaders(headers) {
  const sanitized = { ...headers };
  delete sanitized.authorization;
  delete sanitized.cookie;
  delete sanitized["x-api-key"];
  return sanitized;
}

function deepDiff(obj1, obj2) {
  const diff = {};
  for (const key of Object.keys(obj1)) {
    if (JSON.stringify(obj1[key]) !== JSON.stringify(obj2[key])) {
      diff[key] = { prod: obj1[key], staging: obj2[key] };
    }
  }
  return Object.keys(diff).length > 0 ? diff : null;
}

app.listen(3000, () => {
  console.log("Mirror comparison proxy running on port 3000");
});
