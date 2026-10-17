// CQRS + Event-Driven Projection — JavaScript demo
// Shows the async variant: write events, then rebuild the read model
// with a projection consumer. Includes a naive projection-lag simulation.
// Run: node projection-demo.js

const events = []; // the event log — source of truth
const readStore = { orders: new Map() };

// Command side: emits events, never touches the read store directly
function createOrder(orderId, customerId) {
  events.push({
    type: "OrderCreated", orderId, customerId,
    timestamp: new Date().toISOString()
  });
}

function confirmOrder(orderId) {
  events.push({
    type: "OrderConfirmed", orderId,
    timestamp: new Date().toISOString()
  });
}

// Projection consumer: rebuilds the read model from events
function projectEvent(event) {
  switch (event.type) {
    case "OrderCreated":
      readStore.orders.set(event.orderId, {
        orderId: event.orderId,
        customerId: event.customerId,
        status: "pending",
        createdAt: event.timestamp
      });
      break;
    case "OrderConfirmed":
      const o = readStore.orders.get(event.orderId);
      if (o) { o.status = "confirmed"; o.confirmedAt = event.timestamp; }
      break;
  }
}

// Simulate lag: writes happen first, projection catches up after
createOrder("ORD-1", "CUST-1");
confirmOrder("ORD-1");
confirmOrder("ORD-1"); // duplicate — projections must be idempotent

console.log("Before projection:", readStore.orders.size, "read records");
events.forEach(projectEvent);
console.log("After projection:", readStore.orders.get("ORD-1"));

// Replay = full rebuild — truncate and reproject
readStore.orders.clear();
events.forEach(projectEvent);
console.log("After replay:", readStore.orders.get("ORD-1").status);
