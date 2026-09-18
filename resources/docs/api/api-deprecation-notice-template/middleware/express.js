// express.js — Express middleware that emits Deprecation / Sunset /
// Link headers on responses from deprecated endpoints.
// Usage: app.use(deprecationMiddleware);

const DEPRECATED_PATHS = {
  "/v1/orders": { sunset: "2026-10-01", replacement: "/v2/orders" },
  "/v1/products": { sunset: "2026-10-01", replacement: "/v2/products" },
};

function deprecationMiddleware(req, res, next) {
  const match = Object.keys(DEPRECATED_PATHS).find((path) =>
    req.path.startsWith(path)
  );

  if (match) {
    const info = DEPRECATED_PATHS[match];
    res.setHeader("Deprecation", "true");
    res.setHeader("Sunset", new Date(info.sunset).toUTCString());
    res.setHeader(
      "Link",
      `<https://docs.example.com/api-migration>; rel="deprecation"`
    );
  }

  next();
}

module.exports = { deprecationMiddleware };
