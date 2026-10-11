import type { DomainEvent } from './eventstore';

export interface OrderItem {
  sku: string;
  quantity: number;
  price: number;
}

export interface OrderSnapshot {
  status: string;
  items: OrderItem[];
  total: number;
}

/**
 * Order aggregate rebuilt by replaying its event history.
 * applyEvent is a pure state transition — the same event sequence
 * always produces the same state, which is what makes replay safe.
 */
export class OrderAggregate {
  private status: string = 'pending';
  private items: OrderItem[] = [];
  private total: number = 0;

  applyEvent(event: DomainEvent): void {
    switch (event.eventType) {
      case 'OrderCreated':
        this.status = 'created';
        this.total = event.payload.total as number;
        break;
      case 'ItemAdded':
        this.items.push(event.payload.item as OrderItem);
        this.total += (event.payload.item as OrderItem).price;
        break;
      case 'OrderShipped':
        this.status = 'shipped';
        break;
      case 'OrderCancelled':
        this.status = 'cancelled';
        break;
    }
  }

  static fromEvents(events: DomainEvent[]): OrderAggregate {
    const order = new OrderAggregate();
    for (const event of events) {
      order.applyEvent(event);
    }
    return order;
  }

  toSnapshot(): OrderSnapshot {
    return {
      status: this.status,
      items: this.items,
      total: this.total,
    };
  }
}
