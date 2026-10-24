// Decorator pattern: logging and caching wrap the product fetch without
// changing its signature. Each layer adds one orthogonal concern.

export type Product = { id: string; name: string; price: number };

const catalog: Record<string, Product> = {
  "p-1": { id: "p-1", name: "Keyboard", price: 79.9 },
  "p-2": { id: "p-2", name: "Mouse", price: 39.5 },
};

export function fetchProduct(id: string): Product {
  const product = catalog[id];
  if (!product) throw new Error(`Product not found: ${id}`);
  return product;
}

export function withLogging<T extends (id: string) => Product>(fn: T): T {
  return ((id: string) => {
    const start = Date.now();
    const result = fn(id);
    console.log(`[fetchProduct] ${id} in ${Date.now() - start}ms`);
    return result;
  }) as T;
}

export function withCache<T extends (id: string) => Product>(
  fn: T,
  ttlMs: number
): T {
  const cache = new Map<string, { value: Product; expires: number }>();
  return ((id: string) => {
    const hit = cache.get(id);
    if (hit && hit.expires > Date.now()) return hit.value;
    const value = fn(id);
    cache.set(id, { value, expires: Date.now() + ttlMs });
    return value;
  }) as T;
}
