const BASE = process.env.REST_BASE ?? 'http://localhost:4001';

export const api = {
  get: (path) => fetch(`${BASE}${path}`).then((r) => r.json()),
};
