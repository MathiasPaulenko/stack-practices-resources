// Composition root: five patterns wired together in a small order pipeline.
// Run with: npx tsx order-system/index.ts

import { shippingCost } from "./shipping";
import { NotificationFactory } from "./notifications";
import {
  EventBus,
  updateInventory,
  sendConfirmation,
  trackAnalytics,
} from "./events";
import { fetchProduct, withCache, withLogging } from "./products";
import { CancelOrderCommand, Order, Inventory } from "./commands";

const order = {
  id: "ORD-1042",
  shippingMethod: "express",
  weightKg: 2.4,
  channel: "email",
};

// Strategy: pick the shipping algorithm at runtime.
const total = shippingCost(order.shippingMethod, order.weightKg);
console.log(`Shipping (${order.shippingMethod}): $${total.toFixed(2)}`);

// Factory: get the right notifier for the order's channel.
const notifier = NotificationFactory.create(order.channel);
notifier.send("customer@example.com", "Your order shipped");

// Observer: three independent reactions to one event.
const bus = new EventBus();
bus.on("order.created", updateInventory);
bus.on("order.created", sendConfirmation);
bus.on("order.created", trackAnalytics);
bus.emit("order.created", {
  orderId: order.id,
  total,
  weightKg: order.weightKg,
  channel: order.channel,
});

// Decorator: cached + logged product fetch, same signature.
const fetchProductFast = withCache(withLogging(fetchProduct), 60_000);
fetchProductFast("p-1");
fetchProductFast("p-1"); // served from cache

// Command: cancellation as an undoable, auditable object.
const inventory: Inventory = {
  async reserve(items) {
    console.log(`[inventory] reserved ${items.join(", ")}`);
  },
  async release(items) {
    console.log(`[inventory] released ${items.join(", ")}`);
  },
};

const cancelable: Order = {
  id: order.id,
  status: "active",
  items: ["p-1"],
  async update(patch) {
    Object.assign(this, patch);
    console.log(`[order] ${this.id} -> ${this.status}`);
  },
};

const cmd = new CancelOrderCommand(cancelable, inventory);
await cmd.execute();
await cmd.undo();
