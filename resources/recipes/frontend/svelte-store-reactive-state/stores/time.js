// stores/time.js — readable store with internal updates
// The interval starts with the first subscriber and stops with the last
import { readable } from "svelte/store";

export const currentTime = readable(new Date(), (set) => {
  const interval = setInterval(() => {
    set(new Date());
  }, 1000);

  return () => clearInterval(interval);
});
