// Command pattern: cancellations become objects, so they can be queued,
// audited and undone.

export interface Order {
  id: string;
  status: string;
  items: string[];
  update(patch: Partial<Order>): Promise<void>;
}

export interface Inventory {
  reserve(items: string[]): Promise<void>;
  release(items: string[]): Promise<void>;
}

export interface Command {
  execute(): Promise<void>;
  undo(): Promise<void>;
}

export class CancelOrderCommand implements Command {
  constructor(
    private order: Order,
    private inventory: Inventory
  ) {}

  async execute(): Promise<void> {
    await this.inventory.release(this.order.items);
    await this.order.update({ status: "cancelled" });
  }

  async undo(): Promise<void> {
    await this.inventory.reserve(this.order.items);
    await this.order.update({ status: "active" });
  }
}
