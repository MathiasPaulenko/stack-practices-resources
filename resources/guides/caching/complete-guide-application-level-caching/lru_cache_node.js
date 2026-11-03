const { LRUCache } = require("lru-cache");

const cache = new LRUCache({
  max: 1024,
  ttl: 3600 * 1000, // 1 hour in ms
});

function getUser(userId) {
  const cached = cache.get(`user:${userId}`);
  if (cached) return cached;
  
  const user = db.users.findById(userId);
  if (user) cache.set(`user:${userId}`, user);
  return user;
}
