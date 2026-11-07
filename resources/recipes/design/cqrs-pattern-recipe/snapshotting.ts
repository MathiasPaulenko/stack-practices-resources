// Snapshotting for large event streams (TypeScript)
// Source: https://stackpractices.com/recipes/cqrs-pattern-recipe/

import type { Event, EventStore, OrderWriteModel, PayOrderCommand } from './command-handler';

export interface Snapshot {
  aggregateId: string;
  version: number;
  state: unknown;
}

export class SnapshotStore {
  async save(snapshot: Snapshot): Promise<void> {
    // Persist snapshot to database
  }

  async load(aggregateId: string): Promise<Snapshot | null> {
    // Load latest snapshot
    return null;
  }
}

export class PayOrderHandlerWithSnapshots {
  constructor(
    private eventStore: EventStore,
    private snapshots: SnapshotStore
  ) {}

  async handle(command: PayOrderCommand): Promise<void> {
    const snapshot = await this.snapshots.load(command.orderId);
    let order: OrderWriteModel;
    let fromVersion = 0;

    if (snapshot) {
      order = snapshot.state as OrderWriteModel;
      fromVersion = snapshot.version;
    } else {
      const events = await this.eventStore.getEvents(command.orderId);
      order = this.rehydrate(events);
      fromVersion = events.length;
    }

    // Apply only events after snapshot
    const recentEvents = await this.eventStore.getEventsAfter!(
      command.orderId, fromVersion
    );
    for (const event of recentEvents) {
      this.apply(order, event);
    }

    const newEvents = order.pay(command.paymentMethod);
    await this.eventStore.append(newEvents);

    // Save snapshot every 100 events
    if (fromVersion + recentEvents.length + newEvents.length >= 100) {
      await this.snapshots.save({
        aggregateId: command.orderId,
        version: fromVersion + recentEvents.length + newEvents.length,
        state: order,
      });
    }
  }

  private apply(order: OrderWriteModel, event: Event): void {
    // Apply event to order
  }

  private rehydrate(events: Event[]): OrderWriteModel {
    if (events.length === 0) throw new Error('No events found for order');
    return new OrderWriteModel(events[0].aggregateId, '', []);
  }
}
