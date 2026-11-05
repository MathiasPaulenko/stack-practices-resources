import {
  createContext,
  useContext,
  useMemo,
  useReducer,
  type Dispatch,
  type ReactNode,
} from "react";
import type { CartItem, CartItemInput } from "../types";
import {
  recalcTotal,
  removeCartItem,
  setCartItemQuantity,
  upsertCartItem,
} from "../lib/cart";

export type CartAction =
  | { type: "ADD_ITEM"; item: CartItemInput }
  | { type: "REMOVE_ITEM"; id: string }
  | { type: "UPDATE_QUANTITY"; id: string; quantity: number }
  | { type: "CLEAR" };

export interface CartState {
  items: CartItem[];
  total: number;
}

export const initialCartState: CartState = { items: [], total: 0 };

// The reducer is pure — every transition delegates to the shared helpers in
// lib/cart.ts, which keeps it trivially testable.
export function cartReducer(state: CartState, action: CartAction): CartState {
  switch (action.type) {
    case "ADD_ITEM": {
      const items = upsertCartItem(state.items, action.item);
      return { items, total: recalcTotal(items) };
    }
    case "REMOVE_ITEM": {
      const items = removeCartItem(state.items, action.id);
      return { items, total: recalcTotal(items) };
    }
    case "UPDATE_QUANTITY": {
      const items = setCartItemQuantity(
        state.items,
        action.id,
        action.quantity
      );
      return { items, total: recalcTotal(items) };
    }
    case "CLEAR":
      return initialCartState;
    default:
      return state;
  }
}

const CartContext = createContext<{
  state: CartState;
  dispatch: Dispatch<CartAction>;
} | null>(null);

export function CartProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(cartReducer, initialCartState);

  // dispatch is stable; state isn't. Memoize the wrapper so consumers only
  // re-render when the cart actually changes.
  const value = useMemo(() => ({ state, dispatch }), [state, dispatch]);

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>;
}

export function useCart() {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error("useCart must be used within a CartProvider");
  }
  return context;
}
