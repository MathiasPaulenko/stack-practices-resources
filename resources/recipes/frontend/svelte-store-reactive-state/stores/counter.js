// stores/counter.js — custom store with a contract-based API
// Components can call increment/decrement/reset but never raw set/update
import { writable } from "svelte/store";

function createCounter(step = 1) {
  const { subscribe, update, set } = writable(0);

  return {
    subscribe,
    increment: () => update((n) => n + step),
    decrement: () => update((n) => n - step),
    reset: () => set(0),
  };
}

export const counter = createCounter(5);
