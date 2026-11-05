"use client";

import { useOptimistic, useTransition } from "react";
import { toggleLike } from "./actions";

// Optimistic UI: the count updates instantly and rolls back automatically if
// the Server Action throws. This is the pending-state counterpart to
// useActionState — reach for it when waiting for the server feels laggy
// (likes, toggles, reordering).
export function LikeButton({
  productId,
  initialLikes,
  initiallyLiked,
}: {
  productId: string;
  initialLikes: number;
  initiallyLiked: boolean;
}) {
  const [likes, addOptimisticDelta] = useOptimistic(
    initialLikes,
    (current: number, delta: number) => current + delta
  );
  const [isPending, startTransition] = useTransition();

  function handleClick() {
    const delta = initiallyLiked ? -1 : 1;
    startTransition(async () => {
      addOptimisticDelta(delta); // UI updates instantly
      await toggleLike(productId); // rolls back automatically on error
    });
  }

  return (
    <button
      onClick={handleClick}
      disabled={isPending}
      className="rounded border border-zinc-300 px-3 py-1 text-sm disabled:opacity-50"
      aria-label={initiallyLiked ? "Unlike product" : "Like product"}
    >
      {likes} {likes === 1 ? "like" : "likes"}
    </button>
  );
}
