import org.junit.jupiter.api.Test;
import org.testcontainers.containers.GenericContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;
import redis.clients.jedis.Jedis;

import static org.assertj.core.api.Assertions.assertThat;

@Testcontainers
class RedisIntegrationTest {

    @Container
    static GenericContainer<?> redis = new GenericContainer<>("redis:7-alpine")
        .withExposedPorts(6379);

    @Test
    void shouldSetAndGetValue() {
        String host = redis.getHost();
        Integer port = redis.getMappedPort(6379);

        try (Jedis jedis = new Jedis(host, port)) {
            jedis.set("test-key", "test-value");
            assertThat(jedis.get("test-key")).isEqualTo("test-value");
        }
    }
}
