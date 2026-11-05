import { Suspense } from "react";
import {
  getCatalogStats,
  getPublishedProducts,
} from "@/lib/queries";
import { toClientProduct } from "@/lib/serialize";
import { CreateProductForm } from "./CreateProductForm";
import { ProductCard } from "./ProductCard";

// ISR lever from the guide: the route is prerendered and regenerated at most
// once per hour. Server Actions call revalidatePath("/products") after
// mutations, which busts this cache on demand.
export const revalidate = 3600;

// Sibling async Server Components: each one suspends independently, so the
// stats widget and the product grid resolve in parallel and stream into the
// page as soon as their own data arrives — a single shared boundary would
// make the whole section wait for the slowest query.
async function CatalogStats() {
  const stats = await getCatalogStats();
  return (
    <dl className="grid grid-cols-3 gap-4 rounded-lg border border-zinc-200 bg-white p-4 text-center">
      <div>
        <dt className="text-xs font-medium uppercase tracking-wide text-zinc-500">
          Products
        </dt>
        <dd className="mt-1 text-2xl font-bold">{stats.totalProducts}</dd>
      </div>
      <div>
        <dt className="text-xs font-medium uppercase tracking-wide text-zinc-500">
          Reviews
        </dt>
        <dd className="mt-1 text-2xl font-bold">{stats.totalReviews}</dd>
      </div>
      <div>
        <dt className="text-xs font-medium uppercase tracking-wide text-zinc-500">
          Likes
        </dt>
        <dd className="mt-1 text-2xl font-bold">{stats.totalLikes}</dd>
      </div>
    </dl>
  );
}

async function ProductGrid() {
  const products = await getPublishedProducts();

  if (products.length === 0) {
    return <p className="text-zinc-500">No products published yet.</p>;
  }

  return (
    <div className="grid grid-cols-1 gap-6 sm:grid-cols-3">
      {products.map((product) => (
        <ProductCard
          key={product.id}
          // Explicit allowlist mapping: only serializable fields are passed
          // down, the same habit you need before crossing into Client
          // Components (see lib/serialize.ts).
          product={toClientProduct(product)}
        />
      ))}
    </div>
  );
}

function StatsSkeleton() {
  return <div className="h-20 animate-pulse rounded-lg bg-zinc-200" />;
}

function GridSkeleton() {
  return (
    <div className="grid grid-cols-1 gap-6 sm:grid-cols-3">
      {[0, 1, 2].map((i) => (
        <div key={i} className="h-72 animate-pulse rounded-lg bg-zinc-200" />
      ))}
    </div>
  );
}

export default function ProductsPage() {
  return (
    <div className="mx-auto max-w-6xl space-y-8 p-6">
      <header className="space-y-1">
        <h1 className="text-2xl font-bold">Products</h1>
        <p className="text-sm text-zinc-600">
          Server Components fetch during render; only the interactive leaves
          ship JavaScript to the browser.
        </p>
      </header>

      <CreateProductForm />

      <Suspense fallback={<StatsSkeleton />}>
        <CatalogStats />
      </Suspense>

      <Suspense fallback={<GridSkeleton />}>
        <ProductGrid />
      </Suspense>
    </div>
  );
}
