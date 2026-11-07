// Command handler with event publishing (TypeScript)
// Source: https://stackpractices.com/recipes/cqrs-pattern-recipe/

export interface Event {
  type: string;
  aggregateId: string;
  payload: unknown;
  occurredAt: Date;
}

export interface EventStore {
  append(events: Event[]): Promise<void>;
  getEvents(aggregateId: string): Promise<Event[]>;
  getEventsAfter?(aggregateId: string, fromVersion: number): Promise<Event[]>;
}

export class OrderWriteModel {
  constructor(
    public id: string,
    public customerId: string,
    public items: Array<{ productId: string; quantity: number; price: number }>,
    public status: 'pending' | 'paid' | 'shipped' = 'pending'
  ) {}

  pay(paymentMethod: string): Event[] {
    if (this.status !== 'pending') throw new Error('Order already paid');
    return [{
      type: 'OrderPaid',
      aggregateId: this.id,
      payload: { paymentMethod, total: this.total() },
      occurredAt: new Date(),
    }];
  }

  total(): number {
    return this.items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  }
}

export class PayOrderCommand {
  constructor(
    public orderId: string,
    public paymentMethod: string
  ) {}
}

export class PayOrderHandler {
  constructor(private eventStore: EventStore) {}

  async handle(command: PayOrderCommand): Promise<void> {
    const events = await this.eventStore.getEvents(command.orderId);
    const order = this.rehydrate(events);

    const newEvents = order.pay(command.paymentMethod);
    await this.eventStore.append(newEvents);
  }

  private rehydrate(events: Event[]): OrderWriteModel {
    if (events.length === 0) throw new Error(`No events found for order`);
    const order = new OrderWriteModel(events[0].aggregateId, '', []);
    for (const event of events) {
      if (event.type === 'OrderCreated') {
        const p = event.payload as {
          customerId: string;
          items: OrderWriteModel['items'];
        };
        order.customerId = p.customerId;
        order.items = p.items;
      } else if (event.type === 'OrderPaid') {
        order.status = 'paid';
      }
    }
    return order;
  }
}
