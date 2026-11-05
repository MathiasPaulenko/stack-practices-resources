import { useCartStore } from "../../stores/useCartStore";
import type { Product } from "../../types";

export function ZustandAddToCartButton({ product }: { product: Product }) {
  const addItem = useCartStore((s) => s.addItem);
  return (
    <button type="button" onClick={() => addItem(product)}>
      Add to cart
    </button>
  );
}
