// DataLoader with Redis fallback for cross-request caching.
import DataLoader from "dataloader";

/**
 * Creates a DataLoader that checks Redis first, then falls back to the database.
 * Use this pattern when the same entities are loaded across multiple requests.
 *
 * @param {object} db - Database client (e.g., Prisma, Drizzle).
 * @param {object} redis - Redis client.
 * @returns {DataLoader<number, object>} DataLoader for categories.
 */
export function createCategoryLoader(db, redis) {
  return new DataLoader(async (categoryIds) => {
    const keys = categoryIds.map((id) => `category:${id}`);
    const cached = await redis.mget(keys);
    const missing = categoryIds.filter((_, i) => !cached[i]);

    let fromDb = [];
    if (missing.length > 0) {
      fromDb = await db.categories.findMany({
        where: { id: { in: missing } },
      });
      await Promise.all(
        fromDb.map((c) =>
          redis.set(`category:${c.id}`, JSON.stringify(c), "EX", 3600)
        )
      );
    }

    return categoryIds.map((id, i) => {
      if (cached[i]) return JSON.parse(cached[i]);
      return fromDb.find((c) => c.id === id) ?? null;
    });
  });
}
