// Express.js health check endpoints: liveness, readiness and startup.
// Run: DATABASE_URL=postgres://user:pass@localhost/db node health_check.js

const express = require("express");
const { Pool } = require("pg");

const app = express();
const db = new Pool({ connectionString: process.env.DATABASE_URL });
let started = false;

async function checkDB() {
  await db.query("SELECT 1");
}

app.get("/health/live", (req, res) => {
  res.status(200).json({ status: "alive" });
});

app.get("/health/startup", (req, res) => {
  if (!started) {
    return res.status(503).json({ status: "starting" });
  }
  res.status(200).json({ status: "started" });
});

app.get("/health/ready", async (req, res) => {
  try {
    await checkDB();
    res.status(200).json({ status: "ready", checks: { db: true } });
  } catch {
    res.status(503).json({ status: "not ready", checks: { db: false } });
  }
});

// Flip the flag once the critical dependency answers for the first time.
// Until then /health/startup keeps returning 503 and Kubernetes holds off
// the other probes.
checkDB()
  .then(() => {
    started = true;
  })
  .catch(() => {});

const port = process.env.PORT || 8080;
app.listen(port, () => console.log(`health endpoints on :${port}`));
