import com.github.benmanes.caffeine.cache.Caffeine;
import com.github.benmanes.caffeine.cache.Cache;
import java.util.concurrent.TimeUnit;

Cache<String, User> userCache = Caffeine.newBuilder()
    .maximumSize(10_000)
    .expireAfterWrite(1, TimeUnit.HOURS)
    .recordStats()
    .build();

public User getUser(Long userId) {
    return userCache.get("user:" + userId, key -> {
        return db.users.findById(userId);
    });
}
