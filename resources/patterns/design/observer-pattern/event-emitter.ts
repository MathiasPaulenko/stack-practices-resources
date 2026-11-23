/**
 * Typed EventEmitter: Observer pattern with per-event channels,
 * duplicate-safe subscriptions, and error isolation per observer.
 */
interface Observer {
  update(event: string, data: unknown): void;
}

class EventEmitter {
  private observers = new Map<string, Set<Observer>>();

  subscribe(event: string, observer: Observer): () => void {
    if (!this.observers.has(event)) {
      this.observers.set(event, new Set());
    }
    this.observers.get(event)!.add(observer);
    return () => this.observers.get(event)?.delete(observer);
  }

  emit(event: string, data: unknown): void {
    this.observers.get(event)?.forEach((obs) => {
      try {
        obs.update(event, data);
      } catch (err) {
        // one bad observer must not break the event
        console.error(`Observer error: ${err}`);
      }
    });
  }
}

// Example: e-commerce order events. sendEmail / decrementStock / trackEvent
// would be your domain code.
declare function sendEmail(to: string, subject: string): void;
declare function decrementStock(items: string[]): void;
declare function trackEvent(event: string, data: unknown): void;
interface Order {
  id: string;
  userEmail: string;
  items: string[];
}

const emitter = new EventEmitter();

class EmailNotifier implements Observer {
  update(event: string, data: unknown): void {
    if (event === "order.created") sendEmail((data as Order).userEmail, "Order confirmed");
  }
}

class InventoryUpdater implements Observer {
  update(event: string, data: unknown): void {
    if (event === "order.created") decrementStock((data as Order).items);
  }
}

class AnalyticsTracker implements Observer {
  update(event: string, data: unknown): void {
    trackEvent(event, data);
  }
}

emitter.subscribe("order.created", new EmailNotifier());
emitter.subscribe("order.created", new InventoryUpdater());
emitter.subscribe("order.created", new AnalyticsTracker());

emitter.emit("order.created", { id: "123", userEmail: "user@example.com", items: [] });
