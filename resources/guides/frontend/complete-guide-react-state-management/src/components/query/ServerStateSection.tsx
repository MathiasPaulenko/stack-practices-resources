import { CreateProductForm } from "./CreateProductForm";
import { PaginatedProducts } from "./PaginatedProducts";

// The "server state" playground shown on the TanStack Query tab: pagination
// with keepPreviousData and a mutation with an optimistic update.
export function ServerStateSection() {
  return (
    <section className="server-state">
      <h2>Server state — TanStack Query</h2>
      <p className="muted">
        The product list above is cached, deduplicated, and invalidated by the
        query client in every mode. This section exercises the rest of the
        query lifecycle: page-based pagination and an optimistic mutation.
      </p>
      <div className="server-state-grid">
        <PaginatedProducts />
        <CreateProductForm />
      </div>
    </section>
  );
}
