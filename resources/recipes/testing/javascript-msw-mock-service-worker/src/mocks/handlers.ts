import { http, graphql, HttpResponse } from "msw";

const API = "https://api.example.com";

export const handlers = [
  http.get(`${API}/users/:id`, ({ params }) => {
    return HttpResponse.json({
      id: Number(params.id),
      name: "Alice",
      email: "alice@example.com",
    });
  }),

  http.post(`${API}/users`, async ({ request }) => {
    const body = (await request.json()) as Record<string, unknown>;
    return HttpResponse.json({ id: 42, ...body }, { status: 201 });
  }),

  http.get(`${API}/users`, ({ request }) => {
    const url = new URL(request.url);
    const page = Number(url.searchParams.get("page") || "1");
    const allUsers = Array.from({ length: 50 }, (_, i) => ({ id: i + 1 }));
    const perPage = 10;

    return HttpResponse.json({
      data: allUsers.slice((page - 1) * perPage, page * perPage),
      page,
      total: allUsers.length,
    });
  }),

  graphql.query("GetUser", ({ variables }) => {
    return HttpResponse.json({
      data: {
        user: {
          id: variables.id,
          name: "Alice",
          email: "alice@example.com",
        },
      },
    });
  }),
];
