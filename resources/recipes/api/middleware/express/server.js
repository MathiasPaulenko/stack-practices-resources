// Express middleware chain from the StackPractices middleware recipe.
// Run: node server.js  →  then curl http://localhost:3000/api/protected -H "Authorization: Bearer x"

const express = require("express");
const app = express();

// 1. Logging middleware — first, so everything downstream gets timed
app.use((req, res, next) => {
  const start = Date.now();
  res.on("finish", () => {
    const duration = Date.now() - start;
    console.log(`${req.method} ${req.path} - ${res.statusCode} (${duration}ms)`);
  });
  next();
});

// 2. Simple CORS for the demo (register BEFORE auth so preflights survive)
app.use((req, res, next) => {
  res.set("Access-Control-Allow-Origin", "https://example.com");
  res.set("Access-Control-Allow-Methods", "GET, POST");
  if (req.method === "OPTIONS") return res.sendStatus(204);
  next();
});

// 3. Auth middleware — scoped to /api
function authMiddleware(req, res, next) {
  const token = req.headers.authorization;
  if (!token || !token.startsWith("Bearer ")) {
    return res.status(401).json({ error: "Unauthorized" });
  }
  req.user = { token: token.slice(7) }; // your token verification here
  next();
}
app.use("/api", authMiddleware);

app.get("/api/protected", (req, res) => {
  res.json({ message: "Secret data", user: req.user });
});

app.get("/boom", () => {
  throw new Error("intentional failure");
});

// 4. Error handler — FOUR args, and always registered last
app.use((err, req, res, next) => {
  console.error(err);
  res.status(err.status || 500).json({ error: err.message || "Internal Server Error" });
});

app.listen(3000, () => console.log("Listening on http://localhost:3000"));
