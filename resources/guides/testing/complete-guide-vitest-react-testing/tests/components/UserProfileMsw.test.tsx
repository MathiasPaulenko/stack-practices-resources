// tests/components/UserProfileMsw.test.tsx — Testing with MSW
import { describe, it, expect, beforeAll, afterEach, afterAll } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import { http, HttpResponse } from "msw";
import { server } from "@/mocks/server";
import { UserProfile } from "@/components/UserProfile";

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe("UserProfile with MSW", () => {
  it("renders user data from the intercepted request", async () => {
    render(<UserProfile userId={1} />);

    await waitFor(() => {
      expect(screen.getByText("Alice")).toBeInTheDocument();
    });
  });

  it("shows the error state on a 500", async () => {
    server.use(
      http.get("*/api/users/:id", () => {
        return new HttpResponse(null, { status: 500 });
      })
    );

    render(<UserProfile userId={1} />);

    await waitFor(() => {
      expect(screen.getByText(/failed to load/i)).toBeInTheDocument();
    });
  });
});
