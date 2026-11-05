import "server-only";

import { cache } from "react";
import { db } from "./db";
import type { Product, Review } from "./db";

// React's cache() memoizes these calls for the duration of a single request.
// If the page, a layout, and three nested components all ask for the same
// product, the database is still hit once — this is render-level dedup,
// different from Next.js's fetch cache (which is about caching across requests).

export const getPublishedProducts = cache(async (): Promise<Product[]> => {
  return db.product.findMany({
    where: { published: true },
    orderBy: { createdAt: "desc" },
    take: 50,
  });
});

export const getProductById = cache(
  async (id: string): Promise<Product | null> => {
    return db.product.findUnique({ where: { id } });
  }
);

export const getProductReviews = cache(
  async (productId: string, take = 10): Promise<Review[]> => {
    return db.review.findMany({
      where: { productId },
      orderBy: { createdAt: "desc" },
      take,
    });
  }
);

export const getRelatedProducts = cache(
  async (productId: string, take = 3): Promise<Product[]> => {
    const all = await getPublishedProducts();
    return all.filter((p) => p.id !== productId).slice(0, take);
  }
);

export const getCatalogStats = cache(() => db.stats.findFirst());

export const getViewerLike = cache(
  async (productId: string, viewerId?: string) => {
    if (!viewerId) return null;
    return db.like.findFirst({ where: { productId, userId: viewerId } });
  }
);
