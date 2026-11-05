import { useCart } from "../../context/CartContext";
import type { Product } from "../../types";

export function ContextAddToCartButton({ product }: { product: Product }) {
  const { dispatch } = useCart();
  return (
    <button type="button" onClick={() => dispatch({ type: "ADD_ITEM", item: product })}>
      Add to cart
    </button>
  );
}
