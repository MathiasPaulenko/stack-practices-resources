// Observer pattern: one "order.created" event, several independent
// reactions. The publisher never knows who is listening.

export type OrderEvent = {
  orderId: string;
  total: number;
  weightKg: number;
  channel: string;
};

type Listener = (event: OrderEvent) => void;

export class EventBus {
  private listeners = new Map<string, Listener[]>();

  on(event: string, listener: Listener): void {
    const current = this.listeners.get(event) ?? [];
    current.push(listener);
    this.listeners.set(event, current);
  }

  emit(event: string, payload: OrderEvent): void {
    for (const listener of this.listeners.get(event) ?? []) {
      listener(payload);
    }
  }
}

// The three subscribers used in the guide's example.

export function updateInventory(event: OrderEvent): void {
  console.log(`[inventory] reserving stock for order ${event.orderId}`);
}

export function sendConfirmation(event: OrderEvent): void {
  console.log(`[confirmation] order ${event.orderId} total $${event.total.toFixed(2)}`);
}

export function trackAnalytics(event: OrderEvent): void {
  console.log(`[analytics] order.created weight=${event.weightKg}kg`);
}
