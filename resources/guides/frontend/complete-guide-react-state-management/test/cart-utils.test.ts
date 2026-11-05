import { describe, expect, it } from "vitest";
import {
  cartItemCount,
  parseCart,
  recalcTotal,
  removeCartItem,
  serializeCart,
  setCartItemQuantity,
  upsertCartItem,
} from "../src/lib/cart";
import type { CartItem } from "../src/types";

const keyboard = { id: "prod-1", name: "Aurora Keyboard", price: 129.99 };
const lamp = { id: "prod-4", name: "Lumen Lamp", price: 59.99 };

const sampleItems: CartItem[] = [
  { id: "prod-1", name: "Aurora Keyboard", price: 129.99, quantity: 2 },
  { id: "prod-4", name: "Lumen Lamp", price: 59.99, quantity: 1 },
];

describe("upsertCartItem", () => {
  it("adds a new item with quantity 1", () => {
    const result = upsertCartItem([], keyboard);
    expect(result).toEqual([{ ...keyboard, quantity: 1 }]);
  });

  it("increments the quantity when the item already exists", () => {
    const once = upsertCartItem([], keyboard);
    const twice = upsertCartItem(once, keyboard);
    expect(twice).toHaveLength(1);
    expect(twice[0].quantity).toBe(2);
  });

  it("only keeps cart fields — extra product fields do not leak in", () => {
    const product = { ...keyboard, description: "Hot-swap", category: "Peripherals" };
    const [item] = upsertCartItem([], product);
    expect(item).toEqual({ ...keyboard, quantity: 1 });
  });

  it("does not mutate the input array", () => {
    const items = upsertCartItem([], keyboard);
    upsertCartItem(items, lamp);
    expect(items).toHaveLength(1);
  });
});

describe("setCartItemQuantity", () => {
  it("updates the quantity of a matching item", () => {
    const result = setCartItemQuantity(sampleItems, "prod-1", 5);
    expect(result[0].quantity).toBe(5);
    expect(result[1].quantity).toBe(1);
  });

  it("clamps negative quantities and drops items that reach zero", () => {
    const result = setCartItemQuantity(sampleItems, "prod-1", 0);
    expect(result).toHaveLength(1);
    expect(result[0].id).toBe("prod-4");
  });
});

describe("removeCartItem", () => {
  it("filters out the item with the given id", () => {
    const result = removeCartItem(sampleItems, "prod-1");
    expect(result).toEqual([sampleItems[1]]);
  });
});

describe("totals", () => {
  it("recalcTotal sums price * quantity", () => {
    expect(recalcTotal(sampleItems)).toBeCloseTo(129.99 * 2 + 59.99);
  });

  it("cartItemCount sums quantities across items", () => {
    expect(cartItemCount(sampleItems)).toBe(3);
  });
});

describe("serializeCart / parseCart", () => {
  it("round-trips a cart through JSON", () => {
    expect(parseCart(serializeCart(sampleItems))).toEqual(sampleItems);
  });

  it("returns an empty cart for null, malformed JSON, and wrong shapes", () => {
    expect(parseCart(null)).toEqual([]);
    expect(parseCart("not json")).toEqual([]);
    expect(parseCart('{"items":"nope"}')).toEqual([]);
    expect(parseCart('{"items":[{"id":1}]}')).toEqual([]);
    expect(parseCart('{"items":[{"id":"a","name":"b","price":1,"quantity":0}]}')).toEqual([]);
  });
});
