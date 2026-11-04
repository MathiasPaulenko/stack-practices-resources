// OrderAggregate.ts — Aggregate root: raise events, rebuild state from history
abstract class AggregateRoot {
  protected id: string;
  protected version = 0;
  protected uncommittedEvents: DomainEvent[] = [];

  abstract apply(event: DomainEvent): void;

  protected raise(event: DomainEvent): void {
    this.apply(event);
    this.uncommittedEvents.push(event);
  }

  getUncommittedEvents(): DomainEvent[] { return this.uncommittedEvents; }
  markEventsAsCommitted(): void { this.uncommittedEvents = []; }
  getVersion(): number { return this.version; }

  loadFromHistory(events: DomainEvent[]): void {
    for (const event of events) {
      this.apply(event);
      this.version = event.version;
    }
  }
}

class OrderAggregate extends AggregateRoot {
  private customerId: string | null = null;
  private items: OrderItem[] = [];
  private status: string = 'non-existent';
  private totalAmount = 0;

  static place(orderId: string, customerId: string, items: OrderItemInput[]): OrderAggregate {
    const order = new OrderAggregate();
    order.id = orderId;
    if (items.length === 0) throw new Error('Cannot place an empty order');
    const total = items.reduce((s, i) => s + i.price * i.quantity, 0);
    order.raise({
      eventId: crypto.randomUUID(), eventType: 'OrderPlaced', aggregateId: orderId,
      aggregateType: 'Order', data: { customerId, items, totalAmount: total },
      metadata: { correlationId: crypto.randomUUID() }, version: 0, timestamp: new Date(),
    });
    return order;
  }

  cancel(reason: string): void {
    if (this.status !== 'pending' && this.status !== 'processing') {
      throw new Error(`Cannot cancel order in ${this.status} state`);
    }
    this.raise({
      eventId: crypto.randomUUID(), eventType: 'OrderCancelled', aggregateId: this.id,
      aggregateType: 'Order', data: { reason }, metadata: {}, version: this.version, timestamp: new Date(),
    });
  }

  apply(event: DomainEvent): void {
    switch (event.eventType) {
      case 'OrderPlaced':
        this.customerId = event.data.customerId;
        this.items = event.data.items;
        this.status = 'pending';
        this.totalAmount = event.data.totalAmount;
        break;
      case 'OrderCancelled': this.status = 'cancelled'; break;
      case 'OrderShipped': this.status = 'shipped'; break;
      case 'OrderCompleted': this.status = 'completed'; break;
    }
    this.version = event.version;
  }
}
