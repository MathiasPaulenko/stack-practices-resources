// helmet-config-example.js
// Production-ready Helmet configuration for Express APIs.
// Companion to https://stackpractices.com/guides/api-security-checklist-guide/

const helmet = require("helmet");
const express = require("express");

const app = express();

app.use(
  helmet({
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        scriptSrc: ["'self'"],
        styleSrc: ["'self'", "'unsafe-inline'"],
        imgSrc: ["'self'", "data:"],
        connectSrc: ["'self'"],
        frameAncestors: ["'none'"],
      },
    },
    crossOriginEmbedderPolicy: false, // disable if you embed third-party resources
    crossOriginOpenerPolicy: true,
    crossOriginResourcePolicy: { policy: "same-origin" },
    hsts: {
      maxAge: 31536000, // 1 year
      includeSubDomains: true,
      preload: true,
    },
    referrerPolicy: { policy: "no-referrer" },
    xContentTypeOptions: true,
    xDnsPrefetchControl: { allow: false },
    xDownloadOptions: true,
    xFrameOptions: { action: "deny" },
    xPermittedCrossDomainPolicies: { permittedPolicies: "none" },
    xXssProtection: false, // deprecated in modern browsers; CSP covers it
  })
);

// Disable Express version header
app.disable("x-powered-by");

module.exports = app;
