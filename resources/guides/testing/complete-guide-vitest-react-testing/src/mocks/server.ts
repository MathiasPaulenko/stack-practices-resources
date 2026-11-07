// src/mocks/server.ts — MSW server for tests
import { setupServer } from "msw/node";
import { http, HttpResponse } from "msw";

export const server = setupServer(
  http.get("*/api/users/:id", ({ params }) => {
    return HttpResponse.json({
      id: Number(params.id),
      name: "Alice",
      email: "alice@example.com",
    });
  })
);
