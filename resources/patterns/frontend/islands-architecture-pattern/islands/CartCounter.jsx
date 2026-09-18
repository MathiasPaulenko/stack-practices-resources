// CartCounter.jsx — second island on the same page, reading the
// shared store so it stays in sync with CartItems.
import { useSyncExternalStore } from 'react';
import { cartStore } from './store.js';

export default function CartCounter() {
  const items = useSyncExternalStore(
    cartStore.subscribe,
    () => cartStore.getSnapshot(),
    () => cartStore.getServerSnapshot()
  );
  const count = items.reduce((n, i) => n + i.qty, 0);
  return <a href="/cart" className="cart-counter">Cart ({count})</a>;
}
