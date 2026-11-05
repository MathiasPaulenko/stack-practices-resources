"use client";

import { useState, useTransition } from "react";
import { addToCart } from "./actions";

// Minimal client leaf: a Server Component can render it and pass only
// serializable props — it never imports server code itself. The "use server"
// reference inside the action is the one kind of function allowed to cross
// the boundary.
export function AddToCartButton({ productId }: { productId: string }) {
  const [isPending, startTransition] = useTransition();
  const [added, setAdded] = useState(false);

  function handleClick() {
    startTransition(async () => {
      await addToCart(productId, 1);
      setAdded(true);
      window.setTimeout(() => setAdded(false), 2000);
    });
  }

  return (
    <button
      onClick={handleClick}
      disabled={isPending}
      className="rounded border border-zinc-300 px-3 py-1 text-sm disabled:opacity-50"
    >
      {isPending ? "Adding…" : added ? "Added ✓" : "Add to cart"}
    </button>
  );
}
