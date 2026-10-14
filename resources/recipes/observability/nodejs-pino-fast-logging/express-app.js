const express = require("express");
const pinoHttp = require("pino-http");
const { randomUUID } = require("crypto");
const logger = require("./logger");

const app = express();

// Automatic request/response logging. pino-http attaches req.log
// (a child logger with the request id) to every request.
app.use(
  pinoHttp({
    logger,
    genReqId: (req) => req.headers["x-request-id"] || randomUUID(),
  })
);

app.get("/api/users/:id", (req, res) => {
  // Correct signature: logger.info(mergingObject, message)
  req.log.info({ user_id: req.params.id }, "fetching_user");
  res.json({ id: req.params.id, name: "Alice" });
});

app.get("/api/users", (req, res) => {
  // This object gets REDACTED by the redact paths in logger.js
  logger.info({ user: { email: "alice@example.com", password: "secret123" } }, "user_lookup");
  res.json([]);
});

app.use((err, req, res, next) => {
  req.log.error({ err }, "unhandled_error");
  res.status(500).json({ error: "internal" });
});

app.listen(3000, () => logger.info({ port: 3000 }, "server_started"));
