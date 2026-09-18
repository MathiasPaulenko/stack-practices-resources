// store.js — a dependency-free shared store for islands that need
// common state. Mirrors the nanostores API shape so the mental model
// transfers if you adopt the real library.

export function createStore(initial = { items: [] }) {
  let state = initial;
  const listeners = new Set();

  return {
    subscribe(listener) {
      listeners.add(listener);
      return () => listeners.delete(listener);
    },
    getSnapshot() {
      return state;
    },
    // Server-rendered islands need a stable snapshot for SSR output.
    getServerSnapshot() {
      return state;
    },
    setState(next) {
      state = typeof next === 'function' ? next(state) : next;
      listeners.forEach((fn) => fn());
    },
  };
}

export const cartStore = createStore(
  typeof window !== 'undefined' && window.__cartStore
    ? window.__cartStore
    : { items: [] }
);
