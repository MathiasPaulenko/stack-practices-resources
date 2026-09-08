/**
 * Sentry SDK configuration for Node.js (Express).
 *
 * This module shows how to initialize the Sentry SDK with sensitive data
 * filtering, user context, breadcrumbs, and manual error capture.
 *
 * Usage:
 *   import { initSentry } from "./sentry_node";
 *   initSentry();
 */

import * as Sentry from "@sentry/node";
import { nodeProfilingIntegration } from "@sentry/profiling-node";

export function initSentry(): void {
  Sentry.init({
    dsn: "https://your-dsn@sentry.io/123",
    environment: process.env.NODE_ENV || "development",
    release: `api-gateway@${process.env.APP_VERSION || "1.0.0"}`,
    tracesSampleRate: 0.1,
    profilesSampleRate: 0.1,
    integrations: [
      nodeProfilingIntegration(),
      Sentry.httpIntegration(),
      Sentry.expressIntegration(),
    ],
    beforeSend(event) {
      if (event.request?.headers) {
        delete event.request.headers.authorization;
        delete event.request.headers.cookie;
      }
      if (event.request?.data && typeof event.request.data === "object") {
        delete event.request.data.password;
        delete event.request.data.creditCard;
      }
      return event;
    },
  });
}

interface OrderItem {
  price: number;
  quantity: number;
}

interface Order {
  userId: string;
  items: OrderItem[];
  status: string;
}

export class OrderService {
  async createOrder(userId: string, items: OrderItem[]): Promise<Order> {
    Sentry.setUser({ id: userId, email: "user@example.com" });
    Sentry.addBreadcrumb({
      category: "order",
      message: `Creating order for user ${userId} with ${items.length} items`,
      level: "info",
    });

    try {
      const order = await this.processOrder(userId, items);
      Sentry.addBreadcrumb({
        category: "order",
        message: "Order created successfully",
        level: "info",
      });
      return order;
    } catch (error) {
      Sentry.captureException(error, {
        extra: {
          userId,
          itemCount: items.length,
          totalAmount: items.reduce((sum, i) => sum + i.price * i.quantity, 0),
        },
        tags: { errorType: "order_creation", severity: "high" },
      });
      throw error;
    }
  }

  private async processOrder(userId: string, items: OrderItem[]): Promise<Order> {
    return { userId, items, status: "created" };
  }
}
