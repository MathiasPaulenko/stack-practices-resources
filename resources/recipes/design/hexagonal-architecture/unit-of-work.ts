// Unit of Work: a domain-defined port for coordinating a transaction across
// several secondary ports. The domain calls save(); the adapter owns BEGIN /
// COMMIT / ROLLBACK.

import type { Pool, PoolClient } from "pg";

export interface UnitOfWork {
  begin(): Promise<void>;
  commit(): Promise<void>;
  rollback(): Promise<void>;
}

// Placeholder domain types for the order example.
interface OrderItem {
  sku: string;
  quantity: number;
}
interface Order {
  id: string;
  items: OrderItem[];
}
interface OrderRepository {
  save(order: Order): Promise<void>;
}
interface InventoryRepository {
  decrement(sku: string, quantity: number): Promise<void>;
}

export class OrderService {
  constructor(
    private orders: OrderRepository,
    private inventory: InventoryRepository,
    private uow: UnitOfWork
  ) {}

  async placeOrder(items: OrderItem[]): Promise<Order> {
    await this.uow.begin();
    try {
      const order: Order = { id: crypto.randomUUID(), items };
      await this.orders.save(order);

      for (const item of items) {
        await this.inventory.decrement(item.sku, item.quantity);
      }

      await this.uow.commit();
      return order;
    } catch (err) {
      await this.uow.rollback();
      throw err;
    }
  }
}

export class PostgresUnitOfWork implements UnitOfWork {
  private client?: PoolClient;

  constructor(private pool: Pool) {}

  async begin(): Promise<void> {
    this.client = await this.pool.connect();
    await this.client.query("BEGIN");
  }

  async commit(): Promise<void> {
    if (!this.client) throw new Error("Transaction not started");
    await this.client.query("COMMIT");
    this.client.release();
  }

  async rollback(): Promise<void> {
    if (!this.client) throw new Error("Transaction not started");
    await this.client.query("ROLLBACK");
    this.client.release();
  }
}
