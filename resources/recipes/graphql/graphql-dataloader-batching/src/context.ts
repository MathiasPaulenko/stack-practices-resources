// context.ts — per-request context factory. A new DataLoader instance per
// request keeps the cache scoped to that request and prevents data leaks.
import DataLoader from 'dataloader';
import type { Db, User, Post } from './mock-db.js';
import { createUserLoader, createPostsByAuthorLoader } from './loaders.js';

export type Context = {
  db: Db;
  user: User | null;
  loaders: {
    user: DataLoader<string, User>;
    postsByAuthor: DataLoader<string, Post[]>;
  };
};

export function createContext(db: Db): Context {
  return {
    db,
    user: null,
    loaders: {
      user: createUserLoader(db),
      postsByAuthor: createPostsByAuthorLoader(db),
    },
  };
}
