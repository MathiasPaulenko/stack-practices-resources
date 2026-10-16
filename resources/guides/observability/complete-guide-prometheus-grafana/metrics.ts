// metrics.ts — Prometheus instrumentation for Node.js
import { Counter, Histogram, Gauge, register } from "prom-client";

// Define metrics
const ordersTotal = new Counter({
  name: "orders_total",
  help: "Total number of orders created",
  labelNames: ["status", "paymentMethod"] as const,
});

const orderDuration = new Histogram({
  name: "order_creation_duration_seconds",
  help: "Time spent creating orders",
  labelNames: ["endpoint"] as const,
  buckets: [0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
});

const activeUsers = new Gauge({
  name: "active_users",
  help: "Number of currently active users",
});

const queueDepth = new Gauge({
  name: "message_queue_depth",
  help: "Number of messages in the queue",
  labelNames: ["queueName"] as const,
});

// Usage in service code
class OrderService {
  async createOrder(userId: string, items: OrderItem[]): Promise<Order> {
    const start = Date.now();
    try {
      const order = await this.processOrder(userId, items);
      ordersTotal.inc({ status: "success", paymentMethod: order.paymentMethod });
      return order;
    } catch (error) {
      ordersTotal.inc({ status: "error", paymentMethod: "unknown" });
      throw error;
    } finally {
      orderDuration.observe({ endpoint: "/api/orders" }, (Date.now() - start) / 1000);
    }
  }
}

// Metrics endpoint (Express)
import express from "express";
const app = express();

app.get("/metrics", async (req, res) => {
  res.set("Content-Type", register.contentType);
  res.end(await register.metrics());
});
