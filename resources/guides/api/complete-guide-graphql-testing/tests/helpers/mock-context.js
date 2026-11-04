// Shared mock context factory — one shape, used by every test layer.
import { vi } from "vitest";
import DataLoader from "dataloader";

export function createMockContext() {
  return {
    db: {
      users: {
        findById: vi.fn().mockResolvedValue({ id: "1", name: "Alice", email: "alice@example.com" }),
        findMany: vi.fn().mockResolvedValue([
          { id: "1", name: "Alice", email: "alice@example.com" },
          { id: "2", name: "Bob", email: "bob@example.com" },
        ]),
        create: vi.fn().mockResolvedValue({ id: "3", name: "Charlie", email: "charlie@example.com" }),
      },
    },
    user: { id: "1", role: "ADMIN" },
    loaders: {
      postsLoader: new DataLoader(async (userIds) =>
        userIds.map(() => [{ id: "101", title: "First Post", authorId: "1" }])
      ),
    },
  };
}
