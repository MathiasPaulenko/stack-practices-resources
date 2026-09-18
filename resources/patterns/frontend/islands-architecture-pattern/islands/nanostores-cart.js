// nanostores-cart.js — shared cart state across islands using the real
// nanostores library (Astro's recommended approach).
//
// npm install nanostores @nanostores/react
//
// Any island — React, Svelte, Vue — can read the same map() store
// through its framework's nanostores adapter, so the cart badge in the
// header and the cart list in the sidebar stay in sync without
// a shared framework root.

import { map } from 'nanostores';

export const cart = map({ items: [] });

export function addItem(product) {
  const items = cart.get().items;
  const existing = items.find((i) => i.id === product.id);
  cart.setKey('items', existing
    ? items.map((i) => i.id === product.id ? { ...i, qty: i.qty + 1 } : i)
    : [...items, { ...product, qty: 1 }]);
}

export function removeItem(id) {
  cart.setKey('items', cart.get().items.filter((i) => i.id !== id));
}

export function cartCount() {
  return cart.get().items.reduce((n, i) => n + i.qty, 0);
}

// In an .astro file, seed the store with server data so islands start
// from the same state the server rendered:
//
//   <script define:vars={{ initialCart }}>
//     window.__cart = initialCart;
//   </script>
//
// and at the top of this module:
//   if (typeof window !== 'undefined' && window.__cart) cart.set(window.__cart);
