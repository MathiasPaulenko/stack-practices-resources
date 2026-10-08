require("./instrument"); // must be the first require
const Sentry = require("@sentry/node");
const express = require("express");

const app = express();
app.use(express.json());

// Attach user context to every request (simplified — use real auth in production)
app.use((req, res, next) => {
  Sentry.setUser({ id: 42, username: "alice" });
  next();
});

app.get("/api/users/:id", (req, res) => {
  if (req.params.id === "0") {
    throw new Error("Invalid user ID");
  }
  res.json({ id: req.params.id, name: "Alice" });
});

// Manual capture with breadcrumbs
app.post("/api/orders", async (req, res, next) => {
  try {
    Sentry.addBreadcrumb({
      category: "order",
      message: "Order submitted",
      level: "info",
      data: { items: req.body.items ?? 0 },
    });

    await Sentry.startSpan({ name: "process_order", op: "function" }, async (span) => {
      span.setAttribute("order_id", "ord-123");
      // ... validate payment, save order ...
    });

    res.status(201).json({ orderId: "ord-123" });
  } catch (err) {
    next(err); // forwards to the Sentry error handler below
  }
});

// Test route — hit it to verify Sentry receives the event
app.get("/debug-sentry", () => {
  throw new Error("Sentry test error");
});

// Register AFTER all routes — captures errors that reach the end of the chain
Sentry.setupExpressErrorHandler(app);

// Optional: your own error middleware still runs after Sentry's
app.use((err, req, res, next) => {
  res.status(err.status || 500).json({ error: err.message });
});

app.listen(3000, () => {
  console.log("Listening on http://localhost:3000");
});
