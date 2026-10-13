import DataLoader from 'dataloader';
import { db, verifyToken, type User } from './db.js';

// Runs once per HTTP request. DataLoader lives here on purpose: its
// cache is per-request state, and sharing it across requests can leak
// one user's data into another.
export const createContext = async (authHeader?: string) => {
  const token = authHeader?.replace('Bearer ', '');
  const user = token ? await verifyToken(token) : null;

  return {
    db,
    user,
    loaders: {
      users: new DataLoader<string, User | undefined>(async (ids) => {
        const rows = await db.users.findMany({ where: { id: { in: [...ids] } } });
        return ids.map((id) => rows.find((u) => u.id === id));
      }),
    },
  };
};

export type GraphQLContext = Awaited<ReturnType<typeof createContext>>;
