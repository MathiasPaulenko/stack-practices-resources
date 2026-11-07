// Type-safe event emitter: event names and payloads checked together.

export type Events = {
  "user:created": { id: string };
  "user:deleted": { id: string };
  "order:paid": { orderId: string; amount: number };
};

export class TypedEmitter<T extends Record<string, unknown>> {
  private handlers = new Map<keyof T, Set<(data: never) => void>>();

  on<K extends keyof T>(event: K, handler: (data: T[K]) => void): void {
    const set = this.handlers.get(event) ?? new Set();
    set.add(handler as (data: never) => void);
    this.handlers.set(event, set);
  }

  emit<K extends keyof T>(event: K, data: T[K]): void {
    this.handlers.get(event)?.forEach((h) => (h as (d: T[K]) => void)(data));
  }
}
