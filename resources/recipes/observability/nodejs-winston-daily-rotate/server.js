import express from "express";
import morgan from "morgan";
import logger from "./logger.js";

const app = express();

// Pipe morgan access logs into Winston so they rotate with the rest.
const stream = { write: (msg) => logger.info(msg.trim()) };
app.use(morgan("combined", { stream }));

app.get("/api/users/:id", (req, res) => {
  logger.info("user_fetched", { user_id: req.params.id });
  res.json({ id: req.params.id, name: "Alice" });
});

app.get("/api/error", (req, res) => {
  logger.error("forced_error", { route: "/api/error" });
  res.status(500).json({ error: "boom" });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => logger.info("server_started", { port: PORT }));
