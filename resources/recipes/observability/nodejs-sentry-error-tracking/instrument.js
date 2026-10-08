// Sentry v8+ initialization — must be loaded before the rest of the app.
// For ESM projects, convert to instrument.mjs and run:
//   node --import ./instrument.mjs app.js
const Sentry = require("@sentry/node");

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV || "development",
  release: process.env.SENTRY_RELEASE || "1.0.0",
  tracesSampleRate: 0.1,
});
