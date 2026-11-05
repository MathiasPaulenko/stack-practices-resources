import type { Product } from "./db";

// Only plain, serializable values may cross the server/client boundary.
// This allowlist mapping is the habit to keep: never spread an ORM row into
// a Client Component — Decimals, class instances, and non-plain objects lose
// their prototype (or fail entirely) in the Flight serializer.
export type ClientProduct = {
  id: string;
  name: string;
  price: number;
  image: string;
  likeCount: number;
};

export function toClientProduct(product: Product): ClientProduct {
  return {
    id: product.id,
    name: product.name,
    price: product.price,
    image: product.image,
    likeCount: product.likeCount,
  };
}
