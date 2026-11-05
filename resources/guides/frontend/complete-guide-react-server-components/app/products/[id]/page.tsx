import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { auth } from "@/lib/auth";
import {
  getProductById,
  getProductReviews,
  getRelatedProducts,
  getViewerLike,
} from "@/lib/queries";
import { toClientProduct } from "@/lib/serialize";
import { AddToCartButton } from "../AddToCartButton";
import { DeleteProductButton } from "../DeleteProductButton";
import { LikeButton } from "../LikeButton";
import { ProductCard } from "../ProductCard";

// Viewer-specific content (like state, reviews freshness) must not be
// prerendered — force dynamic rendering for this segment.
export const dynamic = "force-dynamic";

type ProductPageProps = {
  // Next.js 15+: params is a Promise — always await it.
  params: Promise<{ id: string }>;
};

export async function generateMetadata({
  params,
}: ProductPageProps): Promise<Metadata> {
  const { id } = await params;
  // Same cached query the page uses — React's cache() dedupes it, so this
  // metadata fetch does not hit the database twice per request.
  const product = await getProductById(id);
  return {
    title: product?.name ?? "Product not found",
    description: product?.description,
  };
}

export default async function ProductPage({ params }: ProductPageProps) {
  const { id } = await params;

  // `product` and the session are independent — fetch them together instead
  // of paying two sequential round trips.
  const [product, session] = await Promise.all([
    getProductById(id),
    auth(),
  ]);

  if (!product) notFound();

  // reviews, related products, and the viewer's like all depend on `product`
  // but not on each other — Promise.all keeps them parallel. Awaiting them
  // one after another would serialize round trips that could run together.
  const [reviews, related, viewerLike] = await Promise.all([
    getProductReviews(product.id),
    getRelatedProducts(product.id),
    getViewerLike(product.id, session?.user.id),
  ]);

  return (
    <article className="mx-auto max-w-4xl space-y-8 p-6">
      <Link href="/products" className="text-sm text-blue-600 hover:underline">
        ← Back to products
      </Link>

      <header className="space-y-3">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={product.image}
          alt={product.name}
          className="h-72 w-full rounded-lg object-cover"
        />
        <h1 className="text-3xl font-bold">{product.name}</h1>
        <p className="text-2xl font-semibold">
          ${product.price.toFixed(2)}
        </p>
        <p className="max-w-2xl text-zinc-600">{product.description}</p>
        <div className="flex items-center gap-3 pt-1">
          <LikeButton
            productId={product.id}
            initialLikes={product.likeCount}
            initiallyLiked={viewerLike !== null}
          />
          <AddToCartButton productId={product.id} />
          <DeleteProductButton productId={product.id} />
        </div>
      </header>

      <section>
        <h2 className="text-xl font-semibold">
          Reviews ({reviews.length})
        </h2>
        {reviews.length === 0 ? (
          <p className="mt-2 text-sm text-zinc-500">No reviews yet.</p>
        ) : (
          <ul className="mt-4 space-y-3">
            {reviews.map((review) => (
              <li
                key={review.id}
                className="rounded-lg border border-zinc-200 bg-white p-4"
              >
                <div className="flex items-center justify-between">
                  <strong className="text-sm">{review.authorName}</strong>
                  <span
                    className="text-sm text-amber-500"
                    aria-label={`${review.rating} out of 5 stars`}
                  >
                    {"★".repeat(review.rating)}
                    {"☆".repeat(5 - review.rating)}
                  </span>
                </div>
                <p className="mt-1 text-sm text-zinc-600">{review.text}</p>
              </li>
            ))}
          </ul>
        )}
      </section>

      {related.length > 0 && (
        <section>
          <h2 className="text-xl font-semibold">You may also like</h2>
          <div className="mt-4 grid grid-cols-1 gap-6 sm:grid-cols-3">
            {related.map((relatedProduct) => (
              <ProductCard
                key={relatedProduct.id}
                product={toClientProduct(relatedProduct)}
              />
            ))}
          </div>
        </section>
      )}
    </article>
  );
}
