// RedisIntegrationTest.java — Redis integration test
import org.junit.jupiter.api.*;
import org.testcontainers.containers.GenericContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;
import redis.clients.jedis.Jedis;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

@Testcontainers
class RedisIntegrationTest {

    @Container
    static GenericContainer<?> redis = new GenericContainer<>("redis:7-alpine")
        .withExposedPorts(6379);

    private Jedis jedis;

    @BeforeEach
    void setUp() {
        jedis = new Jedis(redis.getHost(), redis.getMappedPort(6379));
    }

    @AfterEach
    void tearDown() {
        jedis.flushAll();
        jedis.close();
    }

    @Test
    void testSetAndGet() {
        jedis.set("key1", "value1");
        assertEquals("value1", jedis.get("key1"));
    }

    @Test
    void testHashOperations() {
        jedis.hset("user:1", "name", "Alice");
        jedis.hset("user:1", "email", "alice@example.com");

        Map<String, String> hash = jedis.hgetAll("user:1");
        assertEquals("Alice", hash.get("name"));
        assertEquals("alice@example.com", hash.get("email"));
    }

    @Test
    void testListOperations() {
        jedis.lpush("queue", "item1", "item2", "item3");
        assertEquals(3, jedis.llen("queue"));
        assertEquals("item3", jedis.rpop("queue"));
        assertEquals("item2", jedis.rpop("queue"));
    }
}
