export class DebouncedEventEmitter {
  private listeners: Map<string, Array<(payload: unknown) => void>> = new Map();
  private timers: Map<string, ReturnType<typeof setTimeout>> = new Map();
  private pendingPayloads: Map<string, unknown> = new Map();

  on(event: string, listener: (payload: unknown) => void): () => void {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event)!.push(listener);
    return () => this.off(event, listener);
  }

  off(event: string, listener: (payload: unknown) => void): void {
    const list = this.listeners.get(event);
    if (list) {
      const index = list.indexOf(listener);
      if (index > -1) list.splice(index, 1);
    }
  }

  emitDebounced(event: string, payload: unknown, delayMs: number = 100): void {
    this.pendingPayloads.set(event, payload);
    const existing = this.timers.get(event);
    if (existing) clearTimeout(existing);
    this.timers.set(
      event,
      setTimeout(() => {
        const finalPayload = this.pendingPayloads.get(event);
        this.timers.delete(event);
        this.pendingPayloads.delete(event);
        const list = [...(this.listeners.get(event) || [])];
        for (const listener of list) {
          try {
            listener(finalPayload);
          } catch (err) {
            console.error('Observer error:', err);
          }
        }
      }, delayMs),
    );
  }
}
