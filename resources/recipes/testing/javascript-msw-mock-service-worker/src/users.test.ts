import { afterAll, afterEach, beforeAll, describe, expect, it } from "vitest";
import { http, HttpResponse } from "msw";
import { server } from "./mocks/server";

const API = "https://api.example.com";

beforeAll(() => server.listen({ onUnhandledRequest: "error" }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe("User API", () => {
  it("fetches a user by ID", async () => {
    const response = await fetch(`${API}/users/1`);
    const user = await response.json();

    expect(user.id).toBe(1);
    expect(user.name).toBe("Alice");
  });

  it("creates a user", async () => {
    const response = await fetch(`${API}/users`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: "Charlie", email: "charlie@example.com" }),
    });

    expect(response.status).toBe(201);
    const user = await response.json();
    expect(user.id).toBe(42);
  });

  it("handles a 500 error with a per-test override", async () => {
    server.use(
      http.get(`${API}/users/1`, () => {
        return HttpResponse.json({ error: "Server error" }, { status: 500 });
      }),
    );

    const response = await fetch(`${API}/users/1`);
    expect(response.status).toBe(500);
  });

  it("paginates the users collection", async () => {
    const response = await fetch(`${API}/users?page=3`);
    const body = await response.json();

    expect(body.data).toHaveLength(10);
    expect(body.page).toBe(3);
    expect(body.total).toBe(50);
  });
});
