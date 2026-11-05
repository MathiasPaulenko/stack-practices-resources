import { describe, expect, it } from "vitest";
import type { Product } from "../lib/db";
import { toClientProduct } from "../lib/serialize";

// Mirrors what a Prisma row would look like: extra fields (description,
// published, createdAt) that must NOT cross into Client Components.
const dbRow: Product = {
  id: "prod-1",
  name: "Aurora Mechanical Keyboard",
  description: "Hot-swappable 75% board with tactile switches.",
  price: 129.99,
  image: "https://picsum.photos/seed/aurora-kb/600/400",
  published: true,
  likeCount: 24,
  createdAt: new Date("2026-01-15"),
};

describe("toClientProduct", () => {
  it("returns only the allowlisted card fields", () => {
    expect(toClientProduct(dbRow)).toEqual({
      id: "prod-1",
      name: "Aurora Mechanical Keyboard",
      price: 129.99,
      image: "https://picsum.photos/seed/aurora-kb/600/400",
      likeCount: 24,
    });
  });

  it("produces a value that survives a JSON round-trip unchanged", () => {
    const card = toClientProduct(dbRow);
    expect(JSON.parse(JSON.stringify(card))).toEqual(card);
  });
});
