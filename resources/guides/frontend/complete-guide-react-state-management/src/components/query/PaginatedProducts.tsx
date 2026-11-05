import { useState } from "react";
import { usePaginatedProducts } from "../../query/productsQuery";

export function PaginatedProducts() {
  const [page, setPage] = useState(1);
  const { data, isPending, isPlaceholderData, isFetching } =
    usePaginatedProducts(page);

  return (
    <section className="paginated">
      <div className="section-head">
        <h3>Paginated products</h3>
        <span className="badge">
          page {data?.page ?? page} / {data?.totalPages ?? "…"}
        </span>
      </div>
      {isPending ? (
        <p className="status">Loading…</p>
      ) : (
        <>
          <ul>
            {data?.items.map((product) => (
              <li key={product.id}>
                {product.name} — ${product.price.toFixed(2)}
              </li>
            ))}
          </ul>
          {isPlaceholderData && (
            <p className="muted">
              Showing the previous page while the next one loads
              {isFetching ? "…" : ""}
            </p>
          )}
          <div className="pager">
            <button
              type="button"
              disabled={page <= 1 || isFetching}
              onClick={() => setPage((p) => p - 1)}
            >
              ← Prev
            </button>
            <button
              type="button"
              disabled={!data?.nextPage || isFetching}
              onClick={() => setPage((p) => p + 1)}
            >
              Next →
            </button>
          </div>
        </>
      )}
    </section>
  );
}
