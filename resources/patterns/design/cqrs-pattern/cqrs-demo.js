// CQRS Pattern — JavaScript demo
// Command side writes through the command handler; query side serves
// denormalized summaries from the store.
// Run: node cqrs-demo.js

// Write Model (Command Side)
class OrderCommandHandler {
  constructor() {
    this.orders = new Map();
  }

  createOrder(orderId, customerId) {
    this.orders.set(orderId, {
      orderId, customerId, items: [], status: "pending",
      createdAt: new Date().toISOString()
    });
  }

  addItem(orderId, product, qty, price) {
    this.orders.get(orderId).items.push({ product, qty, price });
  }

  confirm(orderId) {
    const order = this.orders.get(orderId);
    if (order.items.length === 0) throw new Error("Cannot confirm empty order");
    order.status = "confirmed";
  }
}

// Read Model (Query Side)
class OrderQueryHandler {
  constructor(commandStore) {
    this.store = commandStore;
  }

  getSummary(orderId) {
    const order = this.store.get(orderId);
    const total = order.items.reduce((sum, i) => sum + i.qty * i.price, 0);
    return {
      orderId: order.orderId,
      customerId: order.customerId,
      total,
      itemCount: order.items.length,
      status: order.status
    };
  }

  listByCustomer(customerId) {
    return Array.from(this.store.values())
      .filter(o => o.customerId === customerId)
      .map(o => this.getSummary(o.orderId));
  }
}

const commands = new OrderCommandHandler();
commands.createOrder("ORD-1", "CUST-1");
commands.addItem("ORD-1", "Laptop", 1, 999.99);
commands.confirm("ORD-1");

const queries = new OrderQueryHandler(commands.orders);
console.log(queries.getSummary("ORD-1"));
