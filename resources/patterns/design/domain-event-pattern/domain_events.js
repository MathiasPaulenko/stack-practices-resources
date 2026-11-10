// Domain Event pattern: immutable event + aggregate + in-memory publisher.
// Run: node domain_events.js

class DomainEvent {
  constructor(aggregateId, eventType, payload = {}) {
    this.eventId = crypto.randomUUID();
    this.occurredAt = new Date().toISOString();
    this.aggregateId = aggregateId;
    this.eventType = eventType;
    this.payload = payload;
  }
}

class EventPublisher {
  static handlers = [];

  static subscribe(handler) {
    this.handlers.push(handler);
  }

  static publish(event) {
    this.handlers.forEach((h) => h(event));
  }
}

class Order {
  constructor(customerId) {
    this.id = crypto.randomUUID();
    this.customerId = customerId;
    this.lines = [];
    this.status = "pending";
    this._events = [];
  }

  addLine(productId, quantity, price) {
    this.lines.push({ productId, quantity, price });
  }

  submit() {
    if (this.lines.length === 0) throw new Error("Cannot submit empty order");
    this.status = "submitted";
    this._events.push(
      new DomainEvent(this.id, "OrderSubmitted", {
        customer_id: this.customerId,
        line_count: this.lines.length,
      })
    );
  }

  clearEvents() {
    const events = [...this._events];
    this._events = [];
    return events;
  }
}

EventPublisher.subscribe((e) =>
  console.log(`  [email] order ${e.aggregateId.slice(0, 8)} confirmed`)
);
EventPublisher.subscribe((e) =>
  console.log(`  [analytics] tracked ${e.eventType}`, e.payload)
);

const order = new Order("cust-123");
order.addLine("prod-1", 2, 9.99);
order.submit();
order.clearEvents().forEach((e) => EventPublisher.publish(e));
