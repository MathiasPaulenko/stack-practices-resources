export class WeakObserver<T> {
  private listeners: Map<string, WeakRef<{ notify: (payload: T) => void }[]>> = new Map();

  subscribe(event: string, target: { notify: (payload: T) => void }): () => void {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    const list = this.listeners.get(event)!;
    const ref = new WeakRef(target);
    list.push(ref);

    return () => {
      const refs = this.listeners.get(event);
      if (refs) {
        const index = refs.indexOf(ref);
        if (index > -1) refs.splice(index, 1);
      }
    };
  }

  emit(event: string, payload: T): void {
    const refs = this.listeners.get(event) || [];
    for (const ref of [...refs]) {
      const target = ref.deref();
      if (target) {
        try {
          target.notify(payload);
        } catch (err) {
          console.error('Weak observer error:', err);
        }
      } else {
        refs.splice(refs.indexOf(ref), 1);
      }
    }
  }
}
