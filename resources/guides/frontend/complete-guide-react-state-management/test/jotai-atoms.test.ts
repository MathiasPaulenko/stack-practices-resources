import { createStore } from "jotai/vanilla";
import { describe, expect, it } from "vitest";
import { themeAtom, toggleThemeAtom } from "../src/atoms/themeAtoms";
import {
  addToCartAtom,
  cartItemCountAtom,
  cartItemQuantityAtomFamily,
  cartItemsAtom,
  cartTotalAtom,
  clearCartAtom,
  removeFromCartAtom,
  updateCartQuantityAtom,
} from "../src/atoms/cartAtoms";

const keyboard = { id: "prod-1", name: "Aurora Keyboard", price: 129.99 };
const lamp = { id: "prod-4", name: "Lumen Lamp", price: 59.99 };

describe("theme atoms", () => {
  it("toggles through the write-only atom", () => {
    const store = createStore();
    expect(store.get(themeAtom)).toBe("light");

    store.set(toggleThemeAtom);
    expect(store.get(themeAtom)).toBe("dark");

    store.set(toggleThemeAtom);
    expect(store.get(themeAtom)).toBe("light");
  });
});

describe("cart atoms", () => {
  it("adds items and derives totals automatically", () => {
    const store = createStore();

    store.set(addToCartAtom, keyboard);
    store.set(addToCartAtom, keyboard);
    store.set(addToCartAtom, lamp);

    expect(store.get(cartItemsAtom)).toHaveLength(2);
    expect(store.get(cartItemQuantityAtomFamily("prod-1"))).toBe(2);
    expect(store.get(cartItemQuantityAtomFamily("prod-4"))).toBe(1);
    expect(store.get(cartItemQuantityAtomFamily("missing"))).toBe(0);
    expect(store.get(cartTotalAtom)).toBeCloseTo(129.99 * 2 + 59.99);
    expect(store.get(cartItemCountAtom)).toBe(3);
  });

  it("updates quantities through the write atom", () => {
    const store = createStore();
    store.set(addToCartAtom, keyboard);

    store.set(updateCartQuantityAtom, { id: "prod-1", quantity: 4 });
    expect(store.get(cartTotalAtom)).toBeCloseTo(129.99 * 4);

    store.set(updateCartQuantityAtom, { id: "prod-1", quantity: 0 });
    expect(store.get(cartItemsAtom)).toHaveLength(0);
  });

  it("removes items and clears the cart", () => {
    const store = createStore();
    store.set(addToCartAtom, keyboard);
    store.set(addToCartAtom, lamp);

    store.set(removeFromCartAtom, "prod-1");
    expect(store.get(cartItemsAtom)).toHaveLength(1);

    store.set(clearCartAtom);
    expect(store.get(cartItemsAtom)).toEqual([]);
    expect(store.get(cartTotalAtom)).toBe(0);
  });
});
