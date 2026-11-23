import express from "express";
import jwt from "jsonwebtoken";

const SECRET = process.env.JWT_SECRET || "test-secret";

export function createApp() {
  const app = express();
  app.use(express.json());

  const users = Array.from({ length: 25 }, (_, i) => ({
    id: i + 1,
    name: `User ${i + 1}`,
  }));

  app.get("/api/health", (req, res) => {
    res.json({ status: "healthy", timestamp: Date.now() });
  });

  app.post("/api/users", (req, res) => {
    const { email, name } = req.body;
    if (!email || !name) {
      return res.status(400).json({ error: "email and name are required" });
    }
    res.status(201).json({ id: 26, email, name });
  });

  app.get("/api/users", (req, res) => {
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 10;
    const start = (page - 1) * limit;
    res.json({
      data: users.slice(start, start + limit),
      total: users.length,
      page,
      limit,
    });
  });

  app.get("/api/profile", (req, res) => {
    const auth = req.headers.authorization;
    if (!auth?.startsWith("Bearer ")) {
      return res.status(401).json({ error: "Unauthorized" });
    }
    try {
      const payload = jwt.verify(auth.slice(7), SECRET);
      res.json({ userId: payload.userId, email: payload.email });
    } catch {
      res.status(401).json({ error: "Invalid token" });
    }
  });

  app.post("/api/login", (req, res) => {
    res.cookie("session", "abc-123", { httpOnly: true });
    res.json({ authenticated: true });
  });

  app.get("/api/dashboard", (req, res) => {
    if (!req.headers.cookie?.includes("session=abc-123")) {
      return res.status(401).json({ error: "No session" });
    }
    res.json({ data: "secret dashboard data" });
  });

  app.get("/api/error", () => {
    throw new Error("Something went wrong");
  });

  app.use((err, req, res, next) => {
    res.status(500).json({
      error: err.message,
      stack: process.env.NODE_ENV === "production" ? undefined : err.stack,
    });
  });

  return app;
}
