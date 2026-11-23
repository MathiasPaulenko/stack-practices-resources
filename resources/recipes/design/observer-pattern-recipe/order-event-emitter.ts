interface OrderEvent {
  type: 'created' | 'updated' | 'shipped';
  orderId: string;
  payload: Record<string, unknown>;
}

type OrderListener = (event: OrderEvent) => void | Promise<void>;

export class OrderEventEmitter {
  private listeners: Map<string, OrderListener[]> = new Map();

  on(eventType: OrderEvent['type'], listener: OrderListener): () => void {
    if (!this.listeners.has(eventType)) {
      this.listeners.set(eventType, []);
    }
    this.listeners.get(eventType)!.push(listener);
    return () => this.off(eventType, listener);
  }

  off(eventType: OrderEvent['type'], listener: OrderListener): void {
    const list = this.listeners.get(eventType);
    if (list) {
      const index = list.indexOf(listener);
      if (index > -1) list.splice(index, 1);
    }
  }

  async emit(event: OrderEvent): Promise<void> {
    const list = this.listeners.get(event.type) || [];
    await Promise.all(list.map((listener) => listener(event)));
  }
}
