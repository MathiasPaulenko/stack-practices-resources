"use client";

import { useTransition } from "react";
import { useRouter } from "next/navigation";
import { deleteProduct } from "./actions";

// Server Action invoked from an event handler (not a form). The action
// revalidates "/products"; we then navigate away from the now-deleted page.
export function DeleteProductButton({ productId }: { productId: string }) {
  const [isPending, startTransition] = useTransition();
  const router = useRouter();

  function handleClick() {
    startTransition(async () => {
      await deleteProduct(productId);
      router.push("/products");
    });
  }

  return (
    <button
      onClick={handleClick}
      disabled={isPending}
      className="rounded border border-red-300 px-3 py-1 text-sm text-red-700 disabled:opacity-50"
    >
      {isPending ? "Deleting…" : "Delete"}
    </button>
  );
}
