import { auth } from "@/lib/auth";
import { getViewerLike } from "@/lib/queries";
import type { ClientProduct } from "@/lib/serialize";
import { AddToCartButton } from "./AddToCartButton";
import { LikeButton } from "./LikeButton";

// Server Component — no "use client" directive. It can be async, fetch its
// own viewer-specific state, and compose Client Components as islands.
// The client leaves only ever receive plain serializable props.
export async function ProductCard({
  product,
}: {
  product: ClientProduct;
}) {
  const session = await auth();
  const viewerLike = await getViewerLike(product.id, session?.user.id);

  return (
    <article className="flex flex-col rounded-lg border border-zinc-200 bg-white p-4 shadow-sm">
      {/* eslint-disable-next-line @next/next/no-img-element -- stub image URLs,
          next/image would need remotePatterns config for zero benefit here */}
      <img
        src={product.image}
        alt={product.name}
        className="h-48 w-full rounded-md object-cover"
      />
      <h3 className="mt-3 text-lg font-semibold">{product.name}</h3>
      <p className="mt-1 text-xl font-bold">${product.price.toFixed(2)}</p>
      <div className="mt-4 flex items-center gap-2">
        <LikeButton
          productId={product.id}
          initialLikes={product.likeCount}
          initiallyLiked={viewerLike !== null}
        />
        <AddToCartButton productId={product.id} />
      </div>
    </article>
  );
}
