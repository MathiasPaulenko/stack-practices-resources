// express-cache-headers.js — Express app with HTTP Cache-Control patterns.
// Companion to https://stackpractices.com/recipes/http-cache-control-headers/
//
// Run: npm install express && node express-cache-headers.js
// Try: curl -I http://localhost:3000/api/products

import crypto from "node:crypto";
import express from "express";

const app = express();
const authMiddleware = (req, res, next) => next();

const products = [
  { id: 1, name: "Keyboard", price: 89 },
  { id: 2, name: "Mouse", price: 45 },
];

// Static assets with content hashes — one year, never revalidated.
app.use(express.static("public", {
  maxAge: "1y",
  setHeaders: (res, path) => {
    if (path.endsWith(".js") || path.endsWith(".css")) {
      res.setHeader("Cache-Control", "public, max-age=31536000, immutable");
    }
  },
}));

// Public API — 60s fresh, then stale up to 300s while a shared cache refetches.
app.get("/api/products", async (req, res) => {
  const etag = `"${crypto
    .createHash("sha256")
    .update(JSON.stringify(products))
    .digest("hex")
    .slice(0, 16)}"`;

  // Conditional request: the client sends If-None-Match and gets a 304.
  if (req.headers["if-none-match"] === etag) {
    return res.status(304).end();
  }

  res.setHeader("ETag", etag);
  res.setHeader("Cache-Control", "public, max-age=60, stale-while-revalidate=300");
  res.json(products);
});

// Last-Modified — note the date comparison, not an exact-string match.
app.get("/api/articles/:id", async (req, res) => {
  const article = { id: req.params.id, title: "Caching 101", updatedAt: "2026-10-01T12:00:00Z" };
  const lastModified = new Date(article.updatedAt);

  const ifModifiedSince = req.headers["if-modified-since"];
  if (ifModifiedSince && new Date(ifModifiedSince) >= lastModified) {
    return res.status(304).end();
  }

  res.setHeader("Last-Modified", lastModified.toUTCString());
  res.setHeader("Cache-Control", "public, max-age=300");
  res.json(article);
});

// SSR-style split TTL — CDN caches 1h, browser revalidates every 5 minutes.
app.get("/page", (req, res) => {
  res.setHeader("Cache-Control", "public, max-age=300, s-maxage=3600");
  res.send("<h1>Cached page</h1>");
});

// Authenticated data — browser only, always revalidated.
app.get("/api/users/me", authMiddleware, async (req, res) => {
  res.setHeader("Cache-Control", "private, no-cache");
  res.json({ id: 1, name: "Ada" });
});

// Sensitive data — nothing stored anywhere.
app.get("/api/user/billing", authMiddleware, async (req, res) => {
  res.setHeader("Cache-Control", "no-store");
  res.json({ balance: 120 });
});

// Content negotiation — keep variants separated in cache.
app.get("/api/offers", (req, res) => {
  res.setHeader("Vary", "Accept-Encoding, Accept-Language");
  res.setHeader("Cache-Control", "public, max-age=300");
  res.json([{ id: 1, name: "Bundle" }]);
});

app.listen(3000, () => console.log("http://localhost:3000"));
