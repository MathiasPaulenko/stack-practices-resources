interface EventMap {
  orderCreated: { orderId: string; items: string[] };
  orderShipped: { orderId: string; trackingNumber: string };
  orderCancelled: { orderId: string; reason: string };
}

export class TypedEventEmitter<T extends Record<string, Record<string, unknown>>> {
  private listeners: Map<keyof T, Array<(payload: T[keyof T]) => void>> = new Map();

  on<K extends keyof T>(event: K, listener: (payload: T[K]) => void): () => void {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event)!.push(listener as (payload: T[keyof T]) => void);
    return () => this.off(event, listener);
  }

  off<K extends keyof T>(event: K, listener: (payload: T[K]) => void): void {
    const list = this.listeners.get(event);
    if (list) {
      const index = list.indexOf(listener as (payload: T[keyof T]) => void);
      if (index > -1) list.splice(index, 1);
    }
  }

  emit<K extends keyof T>(event: K, payload: T[K]): void {
    const list = [...(this.listeners.get(event) || [])];
    for (const listener of list) {
      try {
        listener(payload);
      } catch (err) {
        console.error(`Observer error for event "${String(event)}":`, err);
      }
    }
  }
}
