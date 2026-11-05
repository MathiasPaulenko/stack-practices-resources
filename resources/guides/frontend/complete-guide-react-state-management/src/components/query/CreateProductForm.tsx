import { useState, type FormEvent } from "react";
import { useCreateProduct } from "../../query/productsQuery";

export function CreateProductForm() {
  const createProduct = useCreateProduct();
  const [simulateError, setSimulateError] = useState(false);

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = event.currentTarget;
    const formData = new FormData(form);
    createProduct.mutate(
      {
        product: {
          name: String(formData.get("name") ?? ""),
          description: String(formData.get("description") ?? ""),
          price: Number(formData.get("price")),
          category: String(formData.get("category") ?? "Misc"),
        },
        simulateError,
      },
      { onSuccess: () => form.reset() }
    );
  }

  return (
    <form className="create-form" onSubmit={handleSubmit}>
      <h3>Create product</h3>
      <input name="name" placeholder="Name" required />
      <input name="description" placeholder="Description" />
      <input
        name="price"
        type="number"
        step="0.01"
        min="0"
        placeholder="Price"
        required
      />
      <input name="category" placeholder="Category" />
      <label className="checkbox">
        <input
          type="checkbox"
          checked={simulateError}
          onChange={(event) => setSimulateError(event.target.checked)}
        />
        Simulate server error — watch the optimistic row roll back
      </label>
      <button type="submit" disabled={createProduct.isPending}>
        {createProduct.isPending ? "Creating…" : "Create"}
      </button>
      {createProduct.isError && (
        <p className="error">
          Mutation failed — the cache rolled back to the previous snapshot.
        </p>
      )}
      {createProduct.isSuccess && (
        <p className="ok">
          Product created — the ["products"] queries were invalidated and
          refetched.
        </p>
      )}
    </form>
  );
}
