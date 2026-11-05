"use client";

import { useActionState } from "react";
import { createProduct } from "./actions";

// Client Component wired to a Server Action. useActionState gives pending
// state and a result channel in one hook; the action signature is
// (previousState, formData) => newState.
export function CreateProductForm() {
  const [state, formAction, isPending] = useActionState(createProduct, null);

  return (
    <form
      action={formAction}
      className="space-y-4 rounded-lg border border-zinc-200 bg-white p-4"
    >
      <h2 className="text-lg font-semibold">Create product</h2>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <label className="block text-sm">
          <span className="font-medium">Name</span>
          <input
            name="name"
            type="text"
            required
            maxLength={100}
            className="mt-1 w-full rounded border border-zinc-300 px-3 py-2"
          />
        </label>
        <label className="block text-sm">
          <span className="font-medium">Price (USD)</span>
          <input
            name="price"
            type="number"
            min="0.01"
            step="0.01"
            required
            className="mt-1 w-full rounded border border-zinc-300 px-3 py-2"
          />
        </label>
      </div>

      <label className="block text-sm">
        <span className="font-medium">Description</span>
        <textarea
          name="description"
          required
          minLength={10}
          maxLength={500}
          rows={3}
          className="mt-1 w-full rounded border border-zinc-300 px-3 py-2"
        />
      </label>

      <label className="block text-sm">
        <span className="font-medium">Image URL</span>
        <input
          name="image"
          type="url"
          required
          placeholder="https://…"
          className="mt-1 w-full rounded border border-zinc-300 px-3 py-2"
        />
      </label>

      <button
        type="submit"
        disabled={isPending}
        className="rounded bg-blue-600 px-4 py-2 text-white disabled:opacity-50"
      >
        {isPending ? "Creating…" : "Create Product"}
      </button>

      {state?.success && (
        <p className="text-sm text-green-600" role="status">
          Product created!
        </p>
      )}
      {state && !state.success && state.error && (
        <p className="text-sm text-red-600" role="alert">
          {state.error}
        </p>
      )}
    </form>
  );
}
