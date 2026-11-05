"use client";

import { useEffect } from "react";

// error.tsx must be a Client Component — it needs onClick for reset().
// In production Next.js sanitizes the error: the client gets a generic
// message plus error.digest, the correlation id for your server logs.
export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <div className="mx-auto max-w-2xl p-6">
      <div className="rounded-lg border border-red-300 bg-red-50 p-6">
        <h2 className="text-lg font-semibold text-red-800">
          Something went wrong
        </h2>
        <p className="mt-1 text-sm text-red-600">{error.message}</p>
        {error.digest && (
          <p className="mt-1 text-xs text-red-400">Digest: {error.digest}</p>
        )}
        <button
          onClick={reset}
          className="mt-4 rounded bg-red-600 px-4 py-2 text-white"
        >
          Try again
        </button>
      </div>
    </div>
  );
}
