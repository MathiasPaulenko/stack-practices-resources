import org.springframework.boot.actuate.health.Health;
import org.springframework.boot.actuate.health.HealthIndicator;
import org.springframework.data.redis.connection.RedisConnection;
import org.springframework.data.redis.connection.RedisConnectionFactory;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Component;

@Component
public class RedisHealthIndicator implements HealthIndicator {

    private final RedisConnectionFactory connectionFactory;
    private final RedisTemplate<String, String> redisTemplate;

    public RedisHealthIndicator(RedisConnectionFactory connectionFactory,
                                RedisTemplate<String, String> redisTemplate) {
        this.connectionFactory = connectionFactory;
        this.redisTemplate = redisTemplate;
    }

    @Override
    public Health health() {
        try (RedisConnection connection = connectionFactory.getConnection()) {
            String pong = connection.ping();
            long latency = measureLatency();

            return Health.up()
                .withDetail("redis", "connected")
                .withDetail("ping", pong)
                .withDetail("latency_ms", latency)
                .build();
        } catch (Exception e) {
            return Health.down(e)
                .withDetail("redis", "disconnected")
                .build();
        }
    }

    private long measureLatency() {
        long start = System.currentTimeMillis();
        redisTemplate.opsForValue().get("health-check-key");
        return System.currentTimeMillis() - start;
    }
}
