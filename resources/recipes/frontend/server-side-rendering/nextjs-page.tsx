// app/products/page.tsx — Next.js App Router
// Server component: fetches on the server, ships zero data-fetching code to the client.
// `next: { revalidate: 60 }` enables ISR — cached for 60s, revalidated in the background.

interface Product {
  id: string;
  name: string;
  price: number;
}

async function getProducts(): Promise<Product[]> {
  const res = await fetch('https://api.example.com/products', {
    next: { revalidate: 60 },
    // For pure SSR without caching: cache: 'no-store'
  });
  if (!res.ok) throw new Error(`Products API failed: ${res.status}`);
  return res.json();
}

export default async function ProductsPage() {
  const products = await getProducts();

  return (
    <main>
      <h1>Products</h1>
      <ul>
        {products.map((p) => (
          <li key={p.id}>
            {p.name} — ${p.price}
          </li>
        ))}
      </ul>
    </main>
  );
}

// Streaming variant: wrap slow sections in <Suspense> so the shell renders first:
//
// import { Suspense } from 'react';
// <Suspense fallback={<Skeleton />}>
//   <SlowReviews />   {/* fetches inside, streams when ready */}
// </Suspense>
