import { create } from "zustand";
import { createJSONStorage, devtools, persist } from "zustand/middleware";
import type { CartItem, CartItemInput } from "../types";
import {
  recalcTotal,
  removeCartItem,
  sanitizeCartItems,
  setCartItemQuantity,
  upsertCartItem,
} from "../lib/cart";

// `persist` needs synchronous Web Storage. Fall back to an in-memory map
// where localStorage doesn't exist (SSR, Node test runs) so the store keeps
// working everywhere.
const memoryStorage = (() => {
  const map = new Map<string, string>();
  return {
    getItem: (key: string) => map.get(key) ?? null,
    setItem: (key: string, value: string) => {
      map.set(key, value);
    },
    removeItem: (key: string) => {
      map.delete(key);
    },
  };
})();

const cartStorage =
  typeof window !== "undefined" ? window.localStorage : memoryStorage;

interface CartStore {
  items: CartItem[];
  total: number;
  addItem: (item: CartItemInput) => void;
  removeItem: (id: string) => void;
  updateQuantity: (id: string, quantity: number) => void;
  clear: () => void;
}

export const useCartStore = create<CartStore>()(
  devtools(
    persist(
      (set) => ({
        items: [],
        total: 0,
        addItem: (item) =>
          set((state) => {
            const items = upsertCartItem(state.items, item);
            return { items, total: recalcTotal(items) };
          }),
        removeItem: (id) =>
          set((state) => {
            const items = removeCartItem(state.items, id);
            return { items, total: recalcTotal(items) };
          }),
        updateQuantity: (id, quantity) =>
          set((state) => {
            const items = setCartItemQuantity(state.items, id, quantity);
            return { items, total: recalcTotal(items) };
          }),
        clear: () => set({ items: [], total: 0 }),
      }),
      {
        name: "sp-cart",
        storage: createJSONStorage(() => cartStorage),
        // Only the items are persisted — `total` is derived state, so it is
        // rebuilt from the items on rehydration instead of being trusted.
        partialize: (state) => ({ items: state.items }),
        merge: (persisted, current) => {
          const items = sanitizeCartItems(
            (persisted as { items?: unknown }).items
          );
          return { ...current, items, total: recalcTotal(items) };
        },
      }
    ),
    { name: "CartStore" }
  )
);
