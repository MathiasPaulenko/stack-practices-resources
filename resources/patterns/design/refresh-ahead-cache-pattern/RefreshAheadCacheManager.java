// Refresh-ahead cache pattern implementation in Java.
// Requires: jedis@^5.0, jackson-databind@^2.15, Java 17+
// Compile: javac -cp jedis.jar:jackson.jar RefreshAheadCacheManager.java
// Usage: java -cp .:jedis.jar:jackson.jar RefreshAheadCacheManager

import redis.clients.jedis.Jedis;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.util.concurrent.*;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

public class RefreshAheadCacheManager {

    private final Jedis redis;
    private final ObjectMapper mapper = new ObjectMapper();
    private final ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(2);
    private final Map<String, RefreshConfig> refreshConfigs = new ConcurrentHashMap<>();
    private final double refreshThreshold;

    private record RefreshConfig(Callable<Object> loader, int ttl) {}

    public RefreshAheadCacheManager(Jedis jedis, double refreshThreshold) {
        this.redis = jedis;
        this.refreshThreshold = refreshThreshold;
        scheduler.scheduleAtFixedRate(this::checkAndRefresh, 10, 10, TimeUnit.SECONDS);
    }

    public void register(String key, Callable<Object> loader, int ttl) {
        refreshConfigs.put(key, new RefreshConfig(loader, ttl));
        refreshKey(key);
    }

    public <T> T get(String key, Class<T> type) {
        String cached = redis.get(key);
        if (cached != null) {
            try {
                return mapper.readValue(cached, type);
            } catch (Exception e) {
                // Fall through to refresh
            }
        }
        RefreshConfig config = refreshConfigs.get(key);
        if (config != null) {
            return refreshKey(key, type);
        }
        return null;
    }

    private void checkAndRefresh() {
        for (var entry : refreshConfigs.entrySet()) {
            String key = entry.getKey();
            RefreshConfig config = entry.getValue();
            long ttlRemaining = redis.ttl(key);
            if (ttlRemaining < 0 || ttlRemaining < config.ttl() * (1 - refreshThreshold)) {
                try {
                    refreshKey(key);
                } catch (Exception e) {
                    // Keep stale data, retry next cycle
                }
            }
        }
    }

    private void refreshKey(String key) {
        RefreshConfig config = refreshConfigs.get(key);
        if (config == null) return;
        try {
            Object value = config.loader().call();
            redis.setex(key, config.ttl(), mapper.writeValueAsString(value));
        } catch (Exception e) {
            throw new RuntimeException("Refresh failed for " + key, e);
        }
    }

    @SuppressWarnings("unchecked")
    private <T> T refreshKey(String key, Class<T> type) {
        refreshKey(key);
        String cached = redis.get(key);
        try {
            return mapper.readValue(cached, type);
        } catch (Exception e) {
            throw new RuntimeException("Deserialization failed for " + key, e);
        }
    }

    public void shutdown() {
        scheduler.shutdown();
    }
}
