// mediator/EventBus.ts
class EventBus {
  private listeners = new Map<string, Set<(data: unknown) => void>>();

  subscribe(event: string, callback: (data: unknown) => void): () => void {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event)!.add(callback);

    return () => this.listeners.get(event)?.delete(callback);
  }

  emit(event: string, data?: unknown): void {
    this.listeners.get(event)?.forEach(cb => cb(data));
  }
}

const bus = new EventBus();
bus.subscribe('user-login', user => console.log('Logged in:', user));
bus.emit('user-login', { id: 1 });
