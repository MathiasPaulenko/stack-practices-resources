// stores/cart.js — writable cart with derived values
import { writable, derived } from "svelte/store";

export const cart = writable([]);

export const itemCount = derived(cart, ($cart) =>
  $cart.reduce((sum, item) => sum + item.quantity, 0)
);

export const totalPrice = derived(cart, ($cart) =>
  $cart.reduce((sum, item) => sum + item.price * item.quantity, 0)
);

export const formattedTotal = derived(
  totalPrice,
  ($total) => `$${$total.toFixed(2)}`
);
