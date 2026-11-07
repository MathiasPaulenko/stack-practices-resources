// Type-safe API client.
// The fixed version: conditional lookups yield `never` for absent keys
// (direct indexing `ApiRoutes[K]["query"]` does not compile on a union),
// and each option slot becomes required or forbidden per route.

export interface User {
  id: string;
  name: string;
  email: string;
}

export type ApiRoutes = {
  "GET /users": { query: { page?: number }; response: User[] };
  "GET /users/:id": { params: { id: string }; response: User };
  "POST /users": { body: { name: string; email: string }; response: User };
  "DELETE /users/:id": { params: { id: string }; response: void };
};

export type ApiKey = keyof ApiRoutes;

export type Params<K extends ApiKey> = ApiRoutes[K] extends { params: infer P } ? P : never;
export type Query<K extends ApiKey> = ApiRoutes[K] extends { query: infer Q } ? Q : never;
export type BodyOf<K extends ApiKey> = ApiRoutes[K] extends { body: infer B } ? B : never;
export type ResponseOf<K extends ApiKey> = ApiRoutes[K]["response"];

// [X] in tuples tests without distributing over the union.
export type Options<K extends ApiKey> =
  ([Params<K>] extends [never] ? { params?: never } : { params: Params<K> }) &
  ([Query<K>] extends [never] ? { query?: never } : { query: Query<K> }) &
  ([BodyOf<K>] extends [never] ? { body?: never } : { body: BodyOf<K> });

export type HasOptions<K extends ApiKey> =
  [Params<K> | Query<K> | BodyOf<K>] extends [never] ? false : true;

export async function api<K extends ApiKey>(
  key: K,
  ...args: HasOptions<K> extends true ? [options: Options<K>] : []
): Promise<ResponseOf<K>> {
  const options = (args[0] ?? {}) as Options<K>;
  const [method, rawPath] = key.split(" ") as [string, string];
  let path = rawPath;

  const params = (options as { params?: Record<string, string> }).params;
  if (params) {
    for (const [name, value] of Object.entries(params)) {
      path = path.replace(`:${name}`, String(value));
    }
  }

  const res = await fetch(path, { method });
  return res.json() as Promise<ResponseOf<K>>;
}
