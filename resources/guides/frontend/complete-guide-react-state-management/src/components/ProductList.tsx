import type { ComponentType } from "react";
import { useProducts } from "../query/productsQuery";
import type { Product } from "../types";

interface ProductListProps {
  AddToCart: ComponentType<{ product: Product }>;
}

// Products are server state, so they always come from the TanStack Query
// cache no matter which client-state tool the active tab is demoing.
export function ProductList({ AddToCart }: ProductListProps) {
  const { data: products, isPending, isFetching, error, refetch } =
    useProducts();

  if (isPending) {
    return <p className="status">Loading products…</p>;
  }

  if (error) {
    return (
      <p className="status error">
        Error: {error.message}{" "}
        <button type="button" className="link" onClick={() => refetch()}>
          Retry
        </button>
      </p>
    );
  }

  return (
    <section className="product-list">
      <div className="section-head">
        <h2>Products</h2>
        {isFetching && <span className="badge">refetching…</span>}
      </div>
      <ul>
        {products?.map((product) => (
          <li key={product.id} className="product-card">
            <div className="product-info">
              <h3>{product.name}</h3>
              <p className="muted">{product.description}</p>
              <p className="price">${product.price.toFixed(2)}</p>
            </div>
            <AddToCart product={product} />
          </li>
        ))}
      </ul>
    </section>
  );
}
