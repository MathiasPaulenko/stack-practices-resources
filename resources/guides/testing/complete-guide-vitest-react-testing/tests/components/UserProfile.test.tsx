// tests/components/UserProfile.test.tsx — Async component testing
import { describe, it, expect, vi } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import { UserProfile } from "@/components/UserProfile";

vi.mock("@/api/users", () => ({
  fetchUser: vi.fn(),
}));

import { fetchUser } from "@/api/users";

describe("UserProfile", () => {
  it("shows loading state then user data", async () => {
    vi.mocked(fetchUser).mockResolvedValue({
      id: 1,
      name: "Alice",
      email: "alice@example.com",
    });

    render(<UserProfile userId={1} />);

    // Loading state
    expect(screen.getByText(/loading/i)).toBeInTheDocument();

    // Data loaded
    await waitFor(() => {
      expect(screen.getByText("Alice")).toBeInTheDocument();
      expect(screen.getByText("alice@example.com")).toBeInTheDocument();
    });
  });

  it("shows error message on fetch failure", async () => {
    vi.mocked(fetchUser).mockRejectedValue(new Error("Network error"));

    render(<UserProfile userId={1} />);

    await waitFor(() => {
      expect(screen.getByText(/network error/i)).toBeInTheDocument();
    });
  });
});
