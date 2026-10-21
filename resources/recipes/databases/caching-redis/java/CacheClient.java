// Jedis cache client + Spring Cache example from the StackPractices Redis caching recipe.
// Requires redis.clients:jedis on the classpath (see README).

import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;

public class CacheClient {
    private final JedisPool pool = new JedisPool("localhost", 6379);

    public String get(String key) {
        try (Jedis jedis = pool.getResource()) {
            return jedis.get(key);
        }
    }

    public void setex(String key, int seconds, String value) {
        try (Jedis jedis = pool.getResource()) {
            jedis.setex(key, seconds, value);
        }
    }
}
