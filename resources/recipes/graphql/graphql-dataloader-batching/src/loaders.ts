// loaders.ts — DataLoader batch functions. The returned array must align
// with the input keys: same length, same order, one slot per key.
import DataLoader from 'dataloader';
import type { Db, User, Post } from './mock-db.js';

export function createUserLoader(db: Db) {
  return new DataLoader<string, User>(async (userIds: readonly string[]) => {
    const users = await db.users.findMany({ where: { id: { in: [...userIds] } } });
    const userMap = new Map(users.map((u) => [u.id, u]));
    // One slot per input key; Error marks a missing key without sinking the batch.
    return userIds.map((id) => userMap.get(id) ?? new Error(`User ${id} not found`));
  });
}

export function createPostsByAuthorLoader(db: Db) {
  return new DataLoader<string, Post[]>(async (authorIds: readonly string[]) => {
    const posts = await db.posts.findMany({ where: { authorId: { in: [...authorIds] } } });
    return authorIds.map((authorId) => posts.filter((p) => p.authorId === authorId));
  });
}
