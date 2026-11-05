"use client";

import Link from "next/link";

// Segment-level error boundary: an error thrown while rendering
// /products/[id] is caught here without taking down the rest of the app.
// Boundaries nest per segment — this one is more specific than the root
// app/error.tsx, so it wins for errors inside this route.
export default function ProductError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div className="mx-auto max-w-2xl p-6">
      <div className="rounded-lg border border-red-300 bg-red-50 p-6">
        <h2 className="text-lg font-semibold text-red-800">
          This product could not be loaded
        </h2>
        {/* In production, error.message is sanitized — correlate failures
            via error.digest in your server logs instead. */}
        <p className="mt-1 text-sm text-red-600">{error.message}</p>
        <div className="mt-4 flex gap-3">
          <button
            onClick={reset}
            className="rounded bg-red-600 px-4 py-2 text-white"
          >
            Try again
          </button>
          <Link
            href="/products"
            className="rounded border border-red-300 px-4 py-2 text-red-700"
          >
            Back to products
          </Link>
        </div>
      </div>
    </div>
  );
}
