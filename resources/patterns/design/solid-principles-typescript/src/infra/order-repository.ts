import type { Order } from '../domain/order';
import type { Readable, Writable } from './interfaces';

export class OrderRepository implements Readable, Writable {
  private store = new Map<string, Order>();

  async write(order: Order): Promise<void> {
    this.store.set(order.id, order);
  }

  async read(id: string): Promise<Order | null> {
    return this.store.get(id) ?? null;
  }
}
