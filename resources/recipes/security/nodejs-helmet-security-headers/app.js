// Express app with Helmet 8 security headers.
// Exported (not listening) so supertest can drive it in headers.test.js.
const express = require("express");
const helmet = require("helmet");
const cors = require("cors");

const app = express();

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "https://cdn.jsdelivr.net"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", "data:", "https:"],
      frameAncestors: ["'none'"],
      objectSrc: ["'none'"],
      upgradeInsecureRequests: [],
    },
  },
  strictTransportSecurity: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true,
  },
  xFrameOptions: { action: "deny" },
  xDnsPrefetchControl: { allow: false },
  xDownloadOptions: true,
}));

app.use(cors({
  origin: ["https://example.com", "https://app.example.com"],
  methods: ["GET", "POST", "PUT", "DELETE"],
  allowedHeaders: ["Content-Type", "Authorization"],
  credentials: true,
}));

app.get("/", (req, res) => {
  res.json({ message: "Secure API" });
});

module.exports = app;
