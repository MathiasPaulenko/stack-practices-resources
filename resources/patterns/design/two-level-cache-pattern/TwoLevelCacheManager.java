import com.github.benmanes.caffeine.cache.Cache;
import com.github.benmanes.caffeine.cache.Caffeine;
import redis.clients.jedis.Jedis;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.util.concurrent.TimeUnit;

public class TwoLevelCacheManager {

    private final Cache<String, Object> l1;
    private final Jedis l2;
    private final ObjectMapper mapper = new ObjectMapper();
    private final int l2Ttl;

    public TwoLevelCacheManager(Jedis jedis, int l1MaxSize, int l1TtlMinutes, int l2TtlSeconds) {
        this.l2 = jedis;
        this.l2Ttl = l2TtlSeconds;
        this.l1 = Caffeine.newBuilder()
            .maximumSize(l1MaxSize)
            .expireAfterWrite(l1TtlMinutes, TimeUnit.MINUTES)
            .build();
    }

    @SuppressWarnings("unchecked")
    public <T> T getOrLoad(String key, java.util.function.Function<String, T> loader, Class<T> type) {
        T l1Value = (T) l1.getIfPresent(key);
        if (l1Value != null) {
            return l1Value;
        }

        String l2Cached = l2.get(key);
        if (l2Cached != null) {
            try {
                T value = mapper.readValue(l2Cached, type);
                l1.put(key, value);
                return value;
            } catch (Exception e) {
                // Deserialization failed, treat as miss
            }
        }

        T value = loader.apply(key);
        try {
            l2.setex(key, l2Ttl, mapper.writeValueAsString(value));
        } catch (Exception e) {
            // Serialization failed, skip L2
        }
        l1.put(key, value);
        return value;
    }

    public void invalidate(String key) {
        l1.invalidate(key);
        l2.del(key);
        l2.publish("cache:invalidate", key);
    }
}
