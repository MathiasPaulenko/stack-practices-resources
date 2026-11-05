"use server";

import { revalidatePath } from "next/cache";
import { auth } from "@/lib/auth";
import { db } from "@/lib/db";
import {
  parseProductInput,
  productFormDataToInput,
} from "@/lib/product-schema";

export type ProductFormState = {
  success: boolean;
  error?: string;
} | null;

// Signature matches useActionState: (previousState, payload) => newState.
// Expected failures (validation, duplicates, permissions) return an error
// state — reserve throws for genuinely exceptional cases, which propagate
// to the nearest error boundary.
export async function createProduct(
  _prevState: ProductFormState,
  formData: FormData
): Promise<ProductFormState> {
  // A "use server" function is a public POST endpoint whether you meant it or
  // not — authenticate inside the action, every time.
  const session = await auth();
  if (!session?.user?.isAdmin) {
    return { success: false, error: "Unauthorized" };
  }

  const parsed = parseProductInput(productFormDataToInput(formData));
  if (!parsed.success) {
    return { success: false, error: parsed.error };
  }

  try {
    await db.product.create({ data: parsed.data });
  } catch {
    return { success: false, error: "Could not create product" };
  }

  // Invalidate the cached products page so the new item shows up.
  revalidatePath("/products");
  return { success: true };
}

export async function deleteProduct(productId: string): Promise<void> {
  const session = await auth();
  if (!session?.user?.isAdmin) {
    throw new Error("Unauthorized");
  }

  await db.product.delete({ where: { id: productId } });
  revalidatePath("/products");
}

export async function toggleLike(productId: string): Promise<void> {
  const session = await auth();
  if (!session) throw new Error("Login required");

  const existing = await db.like.findFirst({
    where: { productId, userId: session.user.id },
  });

  // A real app would wrap these two writes in a transaction.
  if (existing) {
    await db.like.delete({ where: { id: existing.id } });
    await db.product.update({
      where: { id: productId },
      data: { likeCount: { increment: -1 } },
    });
  } else {
    await db.like.create({
      data: { productId, userId: session.user.id },
    });
    await db.product.update({
      where: { id: productId },
      data: { likeCount: { increment: 1 } },
    });
  }

  revalidatePath("/products");
  revalidatePath(`/products/${productId}`);
}

export async function addToCart(
  productId: string,
  quantity: number
): Promise<{ ok: boolean }> {
  const session = await auth();
  if (!session) throw new Error("Login required");
  if (!Number.isInteger(quantity) || quantity < 1 || quantity > 99) {
    throw new Error("Invalid quantity");
  }

  // Stub: a real app would write to a cart table or call a commerce API.
  console.log(
    `[stub] addToCart product=${productId} qty=${quantity} user=${session.user.id}`
  );
  return { ok: true };
}
