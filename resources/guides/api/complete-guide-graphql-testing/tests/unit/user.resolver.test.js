// Unit tests for resolvers — inputs in, outputs asserted, context injected.
import { describe, it, expect, vi } from "vitest";
import { resolvers } from "../../src/resolvers.js";

describe("Query.user", () => {
  it("returns user by id", async () => {
    const mockDb = {
      users: { findById: vi.fn().mockResolvedValue({ id: "1", firstName: "Alice", lastName: "Smith" }) },
    };
    const result = await resolvers.Query.user(null, { id: "1" }, { db: mockDb });
    expect(result).toEqual({ id: "1", firstName: "Alice", lastName: "Smith" });
    expect(mockDb.users.findById).toHaveBeenCalledWith("1");
  });

  it("returns null when user not found", async () => {
    const mockDb = { users: { findById: vi.fn().mockResolvedValue(null) } };
    const result = await resolvers.Query.user(null, { id: "999" }, { db: mockDb });
    expect(result).toBeNull();
  });
});

describe("User.fullName", () => {
  it("concatenates first and last name", () => {
    expect(resolvers.User.fullName({ firstName: "Alice", lastName: "Smith" })).toBe("Alice Smith");
  });
});
