import { atom } from "jotai";
// atomFamily is a util, not part of the core entry point — in Jotai v3 it
// moved to the separate `jotai-family` package.
import { atomFamily } from "jotai/utils";
import type { CartItem, CartItemInput } from "../types";
import {
  recalcTotal,
  removeCartItem,
  setCartItemQuantity,
  upsertCartItem,
} from "../lib/cart";

// Primitive atom holding the cart lines.
export const cartItemsAtom = atom<CartItem[]>([]);

// Derived (read-only) atoms — they recompute automatically when
// cartItemsAtom changes; no selector wiring required.
export const cartTotalAtom = atom((get) => recalcTotal(get(cartItemsAtom)));

export const cartItemCountAtom = atom((get) =>
  get(cartItemsAtom).reduce((count, item) => count + item.quantity, 0)
);

// atomFamily generates one atom per product id, so a component subscribed
// to a single item's quantity re-renders only when that item changes.
export const cartItemQuantityAtomFamily = atomFamily((id: string) =>
  atom((get) => get(cartItemsAtom).find((item) => item.id === id)?.quantity ?? 0)
);

// Write-only atoms are the "actions" — components grab them with useSetAtom.
export const addToCartAtom = atom(null, (_get, set, item: CartItemInput) => {
  set(cartItemsAtom, (items) => upsertCartItem(items, item));
});

export const removeFromCartAtom = atom(null, (_get, set, id: string) => {
  set(cartItemsAtom, (items) => removeCartItem(items, id));
});

export const updateCartQuantityAtom = atom(
  null,
  (_get, set, change: { id: string; quantity: number }) => {
    set(cartItemsAtom, (items) =>
      setCartItemQuantity(items, change.id, change.quantity)
    );
  }
);

export const clearCartAtom = atom(null, (_get, set) => {
  set(cartItemsAtom, []);
});
