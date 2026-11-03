import java.util.concurrent.ConcurrentHashMap;

ConcurrentHashMap<String, User> cache = new ConcurrentHashMap<>();

public User getUser(String key) {
    return cache.computeIfAbsent(key, k -> db.users.findById(k));
}
