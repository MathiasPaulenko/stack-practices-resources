import type { CartItem, CartItemInput } from "../types";

// All cart mutations are pure functions so the exact same logic backs the
// Context reducer, the Zustand store, and the Jotai write atoms — and it
// stays unit testable without a React runtime.

export function recalcTotal(items: CartItem[]): number {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

export function cartItemCount(items: CartItem[]): number {
  return items.reduce((count, item) => count + item.quantity, 0);
}

export function upsertCartItem(
  items: CartItem[],
  input: CartItemInput
): CartItem[] {
  const existing = items.find((item) => item.id === input.id);
  if (!existing) {
    // Pick the cart fields explicitly — callers pass full Product objects.
    return [
      ...items,
      { id: input.id, name: input.name, price: input.price, quantity: 1 },
    ];
  }
  return items.map((item) =>
    item.id === input.id ? { ...item, quantity: item.quantity + 1 } : item
  );
}

export function setCartItemQuantity(
  items: CartItem[],
  id: string,
  quantity: number
): CartItem[] {
  return items
    .map((item) =>
      item.id === id ? { ...item, quantity: Math.max(0, quantity) } : item
    )
    .filter((item) => item.quantity > 0);
}

export function removeCartItem(items: CartItem[], id: string): CartItem[] {
  return items.filter((item) => item.id !== id);
}

export function sanitizeCartItems(value: unknown): CartItem[] {
  if (!Array.isArray(value)) return [];
  return value.filter(isCartItem);
}

// Cart (de)serialization helpers — the wire format is `{ "items": [...] }`,
// the same shape the Zustand `persist` middleware writes to storage.
export function serializeCart(items: CartItem[]): string {
  return JSON.stringify({ items });
}

export function parseCart(raw: string | null): CartItem[] {
  if (!raw) return [];
  try {
    const parsed: unknown = JSON.parse(raw);
    if (typeof parsed !== "object" || parsed === null) return [];
    return sanitizeCartItems((parsed as { items?: unknown }).items);
  } catch {
    return [];
  }
}

function isCartItem(value: unknown): value is CartItem {
  if (typeof value !== "object" || value === null) return false;
  const item = value as Record<string, unknown>;
  return (
    typeof item.id === "string" &&
    typeof item.name === "string" &&
    typeof item.price === "number" &&
    typeof item.quantity === "number" &&
    item.quantity > 0
  );
}
