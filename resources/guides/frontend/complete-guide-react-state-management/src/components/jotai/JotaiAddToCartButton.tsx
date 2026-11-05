import { useSetAtom } from "jotai";
import { addToCartAtom } from "../../atoms/cartAtoms";
import type { Product } from "../../types";

export function JotaiAddToCartButton({ product }: { product: Product }) {
  const addToCart = useSetAtom(addToCartAtom);
  return (
    <button type="button" onClick={() => addToCart(product)}>
      Add to cart
    </button>
  );
}
