// Runnable CORS middleware example for the "Handle CORS" recipe.
// Usage: npm install && node cors-server.mjs   (Express API on :5000)
// Then verify with: bash verify-cors.sh http://localhost:5000

import express from "express";

const app = express();

const ALLOWED_ORIGINS = new Set([
  "https://app.example.com",
  "https://admin.example.com",
  "http://localhost:3000",
]);

function corsMiddleware(req, res, next) {
  const origin = req.headers.origin;

  if (origin && ALLOWED_ORIGINS.has(origin)) {
    res.header("Access-Control-Allow-Origin", origin);
    res.header("Vary", "Origin");
  }

  res.header("Access-Control-Allow-Credentials", "true");

  // Preflight request
  if (req.method === "OPTIONS") {
    if (origin && !ALLOWED_ORIGINS.has(origin)) {
      return res.sendStatus(204);
    }
    res.header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, PATCH");
    res.header(
      "Access-Control-Allow-Headers",
      "Content-Type, Authorization, X-Request-ID",
    );
    res.header("Access-Control-Max-Age", "86400");
    return res.sendStatus(204);
  }

  next();
}

app.use(corsMiddleware);
app.use(express.json());

app.get("/api/users", (_req, res) => {
  res.json({ users: [{ id: 1, name: "Alice" }] });
});

app.put("/api/users", (_req, res) => {
  res.json({ updated: true });
});

app.listen(5000, () => console.log("API listening on :5000"));
