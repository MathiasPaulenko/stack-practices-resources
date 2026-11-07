// tests/mocks/api.test.ts — Module mocking
import { describe, it, expect, vi, beforeEach } from "vitest";

vi.mock("@/api/client", () => ({
  apiClient: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
  },
}));

import { apiClient } from "@/api/client";
import { UserService } from "@/services/UserService";

describe("UserService", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("fetches users", async () => {
    vi.mocked(apiClient.get).mockResolvedValue({
      data: [{ id: 1, name: "Alice" }],
    });

    const users = await UserService.getAll();
    expect(users).toHaveLength(1);
    expect(apiClient.get).toHaveBeenCalledWith("/users");
  });

  it("creates user", async () => {
    vi.mocked(apiClient.post).mockResolvedValue({
      data: { id: 2, name: "Bob" },
    });

    const user = await UserService.create({ name: "Bob" });
    expect(user.id).toBe(2);
    expect(apiClient.post).toHaveBeenCalledWith("/users", { name: "Bob" });
  });
});
