import DataLoader from 'dataloader';

// One instance per request — created inside the context function.
// Sharing a loader across requests leaks cached data between users.
export function createUserLoader(db: any) {
  return new DataLoader<string, any>(async (userIds: readonly string[]) => {
    const users = await db.users.findMany({
      where: { id: { in: [...userIds] } },
    });
    const userMap = new Map(users.map((u: any) => [u.id, u]));
    return userIds.map((id) => userMap.get(id) ?? null);
  });
}
