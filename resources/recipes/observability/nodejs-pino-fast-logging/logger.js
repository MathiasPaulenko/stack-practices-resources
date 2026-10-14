const pino = require("pino");

// Shared logger configuration. LOG_LEVEL controls verbosity (default: info).
// In development, output is piped through pino-pretty in a worker thread.
const logger = pino({
  level: process.env.LOG_LEVEL || "info",
  base: { service: "user-api", version: "1.0.0" },
  redact: {
    paths: ["password", "api_key", "token", "headers.authorization", "*.credit_card"],
    censor: "[REDACTED]",
  },
  transport:
    process.env.NODE_ENV === "development"
      ? { target: "pino-pretty", options: { colorize: true, ignore: "pid,hostname" } }
      : undefined,
});

module.exports = logger;
