// Connect to Redis with Jedis: JedisPooled, strings, hashes, Lua rate limit.
// Needs jedis on the classpath.
import redis.clients.jedis.JedisPooled;
import java.util.Map;

public class RedisExample {
    // For TLS use a URI: new JedisPooled("rediss://default:pass@host:6379")
    private static final JedisPooled jedis = new JedisPooled("redis://localhost:6379");

    public static boolean rateLimit(String userId, int maxRequests, int windowSeconds) {
        String key = "rate:" + userId;
        String luaScript =
            "local current = redis.call('INCR', KEYS[1]) " +
            "if current == 1 then " +
            "  redis.call('EXPIRE', KEYS[1], ARGV[2]) " +
            "end " +
            "return tonumber(current) <= tonumber(ARGV[1])";
        Object allowed = jedis.eval(luaScript, 1, key,
            String.valueOf(maxRequests), String.valueOf(windowSeconds));
        return Boolean.TRUE.equals(allowed);
    }

    public static void main(String[] args) {
        jedis.setex("user:1:name", 3600, "Alice");
        System.out.println(jedis.get("user:1:name"));

        jedis.hset("user:1", Map.of("email", "alice@example.com", "role", "admin"));
        System.out.println(jedis.hgetAll("user:1"));

        for (int i = 0; i < 7; i++) {
            System.out.println("request " + i + ": " + (rateLimit("u42", 5, 60) ? "allowed" : "blocked"));
        }
    }
}
