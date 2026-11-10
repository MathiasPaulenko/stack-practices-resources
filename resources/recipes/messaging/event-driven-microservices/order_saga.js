/**
 * Saga orchestration demo: multi-step order flow with compensation.
 *
 * Companion runnable for https://stackpractices.com/recipes/event-driven-microservices/
 * No dependencies — run `node order_saga.js`. Runs the happy path and a
 * failing payment to show the compensation chain.
 */

const log = [];

const inventoryService = {
  reserve: (items) => log.push(`inventory: reserved ${items.length} item(s)`),
  release: (items) => log.push(`inventory: released ${items.length} item(s)`),
};

const paymentService = {
  charge: (total) => log.push(`payment: charged ${total}`),
  refund: (total) => log.push(`payment: refunded ${total}`),
};

const shippingService = {
  createLabel: (order) => log.push(`shipping: label created for ${order.id}`),
  cancelLabel: (order) => log.push(`shipping: label cancelled for ${order.id}`),
};

class OrderSaga {
  constructor(order, { failAt } = {}) {
    this.order = order;
    this.steps = [
      {
        name: 'reserve_inventory',
        execute: async () => inventoryService.reserve(order.items),
        compensate: async () => inventoryService.release(order.items),
      },
      {
        name: 'process_payment',
        execute: async () => {
          if (failAt === 'process_payment') throw new Error('card declined');
          paymentService.charge(order.total);
        },
        compensate: async () => paymentService.refund(order.total),
      },
      {
        name: 'ship_order',
        execute: async () => shippingService.createLabel(order),
        compensate: async () => shippingService.cancelLabel(order),
      },
    ];
  }

  async execute() {
    const completed = [];
    try {
      for (const step of this.steps) {
        await step.execute();
        completed.push(step);
      }
      return 'completed';
    } catch (err) {
      for (const step of completed.reverse()) {
        await step.compensate();
      }
      return `failed at ${this.steps[completed.length].name}: ${err.message} — compensated ${completed.length} step(s)`;
    }
  }
}

const order = { id: 'order-42', items: [{ sku: 'KB-87', qty: 1 }], total: 89.99 };

// Happy path
log.length = 0;
console.log('--- happy path ---');
console.log(await new OrderSaga(order).execute());
log.forEach((l) => console.log(`  ${l}`));

// Payment fails: reserve compensated, payment+ship never ran
log.length = 0;
console.log('--- payment failure ---');
console.log(await new OrderSaga(order, { failAt: 'process_payment' }).execute());
log.forEach((l) => console.log(`  ${l}`));
