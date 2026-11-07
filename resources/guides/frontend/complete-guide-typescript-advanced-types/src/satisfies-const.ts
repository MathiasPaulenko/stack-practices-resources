// satisfies, as const, and const type parameters (TS 4.9 / 5.0).

export const routes = {
  home: "/",
  user: "/users/:id",
} satisfies Record<string, `/${string}`>;

export type Route = (typeof routes)[keyof typeof routes];
// "/" | "/users/:id" — a plain `Record` annotation would widen to string.

export function makeTable<const T extends { columns: readonly string[] }>(t: T): T {
  return t;
}

export const table = makeTable({ columns: ["id", "name"] });
// columns: readonly ["id", "name"]
export type Column = (typeof table.columns)[number]; // "id" | "name"
