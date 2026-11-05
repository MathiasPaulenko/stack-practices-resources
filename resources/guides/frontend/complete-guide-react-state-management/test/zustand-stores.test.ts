import { beforeEach, describe, expect, it } from "vitest";
import { useCartStore } from "../src/stores/useCartStore";
import { useThemeStore } from "../src/stores/useThemeStore";

const keyboard = { id: "prod-1", name: "Aurora Keyboard", price: 129.99 };
const lamp = { id: "prod-4", name: "Lumen Lamp", price: 59.99 };

describe("useCartStore", () => {
  beforeEach(() => {
    useCartStore.setState({ items: [], total: 0 });
  });

  it("adds items and recalculates the total", () => {
    const { addItem } = useCartStore.getState();
    addItem(keyboard);
    addItem(keyboard);
    addItem(lamp);

    const state = useCartStore.getState();
    expect(state.items).toHaveLength(2);
    expect(state.items[0].quantity).toBe(2);
    expect(state.total).toBeCloseTo(129.99 * 2 + 59.99);
  });

  it("updates quantities and drops items that reach zero", () => {
    const { addItem, updateQuantity } = useCartStore.getState();
    addItem(keyboard);
    updateQuantity("prod-1", 3);
    expect(useCartStore.getState().items[0].quantity).toBe(3);

    updateQuantity("prod-1", 0);
    expect(useCartStore.getState().items).toHaveLength(0);
    expect(useCartStore.getState().total).toBe(0);
  });

  it("removes and clears items", () => {
    const { addItem, removeItem, clear } = useCartStore.getState();
    addItem(keyboard);
    addItem(lamp);
    removeItem("prod-1");
    expect(useCartStore.getState().items).toHaveLength(1);

    clear();
    expect(useCartStore.getState()).toMatchObject({ items: [], total: 0 });
  });
});

describe("useThemeStore", () => {
  beforeEach(() => {
    useThemeStore.setState({ theme: "light" });
  });

  it("toggles between light and dark", () => {
    useThemeStore.getState().toggleTheme();
    expect(useThemeStore.getState().theme).toBe("dark");
    useThemeStore.getState().toggleTheme();
    expect(useThemeStore.getState().theme).toBe("light");
  });

  it("sets an explicit theme", () => {
    useThemeStore.getState().setTheme("dark");
    expect(useThemeStore.getState().theme).toBe("dark");
  });
});
