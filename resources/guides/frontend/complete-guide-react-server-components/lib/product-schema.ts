import { z } from "zod";

// Shared by the Server Action and the unit tests — keeping the schema out of
// the "use server" module makes the pure validation logic testable without a
// Next.js runtime.
export const productFormSchema = z.object({
  name: z.string().min(1, "Name is required").max(100),
  price: z.number().positive("Price must be greater than 0"),
  description: z
    .string()
    .min(10, "Description must be at least 10 characters")
    .max(500),
  image: z.string().url("Image must be a valid URL"),
});

export type ProductInput = z.infer<typeof productFormSchema>;

export type ParseProductResult =
  | { success: true; data: ProductInput }
  | { success: false; error: string };

// FormData is untyped user input — coerce the numeric field and let zod do
// the rest. Returning the first issue message keeps the UX simple.
export function parseProductInput(raw: unknown): ParseProductResult {
  const parsed = productFormSchema.safeParse(raw);
  if (!parsed.success) {
    return {
      success: false,
      error: parsed.error.issues[0]?.message ?? "Invalid input",
    };
  }
  return { success: true, data: parsed.data };
}

export function productFormDataToInput(formData: FormData): unknown {
  return {
    name: formData.get("name"),
    price: Number(formData.get("price")),
    description: formData.get("description"),
    image: formData.get("image"),
  };
}
