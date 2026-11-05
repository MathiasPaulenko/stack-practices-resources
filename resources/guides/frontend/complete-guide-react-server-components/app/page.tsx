import Link from "next/link";
import { Suspense } from "react";
import { toClientProduct } from "@/lib/serialize";
import { getPublishedProducts } from "@/lib/queries";
import { ProductCard } from "./products/ProductCard";

// Async Server Component: fetches its own data and suspends while it does.
// The Suspense boundary below decides when its fallback gets replaced.
async function FeaturedProducts() {
  const products = (await getPublishedProducts()).slice(0, 3);
  return (
    <div className="grid grid-cols-1 gap-6 sm:grid-cols-3">
      {products.map((product) => (
        <ProductCard key={product.id} product={toClientProduct(product)} />
      ))}
    </div>
  );
}

export default function HomePage() {
  return (
    <div className="mx-auto max-w-6xl space-y-10 p-6">
      <section className="space-y-4">
        <h1 className="text-3xl font-bold">
          React Server Components playground
        </h1>
        <p className="max-w-2xl text-zinc-600">
          Executable companion to the{" "}
          <Link href="/products" className="text-blue-600 hover:underline">
            complete guide to React Server Components
          </Link>
          . Every component on this site is a Server Component unless it starts
          with <code className="rounded bg-zinc-200 px-1">"use client"</code>.
        </p>
      </section>

      <section className="space-y-4">
        <h2 className="text-xl font-semibold">Latest products</h2>
        <Suspense
          fallback={
            <div className="grid grid-cols-1 gap-6 sm:grid-cols-3">
              {[0, 1, 2].map((i) => (
                <div
                  key={i}
                  className="h-72 animate-pulse rounded-lg bg-zinc-200"
                />
              ))}
            </div>
          }
        >
          <FeaturedProducts />
        </Suspense>
      </section>
    </div>
  );
}
