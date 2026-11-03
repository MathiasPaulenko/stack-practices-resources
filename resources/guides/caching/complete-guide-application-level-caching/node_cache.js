const cache = new Map();

function getUser(userId) {
  if (cache.has(userId)) return cache.get(userId);
  const user = db.users.findById(userId);
  if (user) cache.set(userId, user);
  return user;
}
