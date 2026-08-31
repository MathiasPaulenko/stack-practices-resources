import java.time.Duration;
import java.util.List;
import java.util.Properties;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.serialization.StringDeserializer;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.params.SetParams;

public class KafkaConsumerDedup {
    public static void main(String[] args) {
        Properties props = new Properties();
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, System.getenv().getOrDefault("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"));
        props.put(ConsumerConfig.GROUP_ID_CONFIG, System.getenv().getOrDefault("KAFKA_GROUP_ID", "payment-workers"));
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
        props.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, false);

        KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props);
        consumer.subscribe(List.of(System.getenv().getOrDefault("KAFKA_TOPIC", "orders")));

        String redisHost = System.getenv().getOrDefault("REDIS_HOST", "localhost");
        int redisPort = Integer.parseInt(System.getenv().getOrDefault("REDIS_PORT", "6379"));

        try (Jedis jedis = new Jedis(redisHost, redisPort)) {
            while (true) {
                ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
                for (ConsumerRecord<String, String> record : records) {
                    String key = "idempotency:" + extractIdempotencyKey(record.value());

                    Boolean locked = jedis.set(key, "processing", SetParams.setParams().nx().ex(86400));
                    if (Boolean.TRUE.equals(locked)) {
                        try {
                            String result = chargeCustomer(record.value());
                            jedis.set(key, result, SetParams.setParams().ex(86400));
                            consumer.commitSync();
                        } catch (Exception e) {
                            jedis.del(key);
                            throw e;
                        }
                    } else {
                        consumer.commitSync();
                    }
                }
            }
        }
    }

    private static String extractIdempotencyKey(String json) {
        // Simplified parser for the example. Replace with a real JSON library.
        int idx = json.indexOf("\"orderId\"");
        if (idx < 0) return java.util.UUID.randomUUID().toString();
        int start = json.indexOf("\"", idx + 10) + 1;
        int end = json.indexOf("\"", start);
        return json.substring(start, end);
    }

    private static String chargeCustomer(String json) {
        // Replace with your real payment call.
        return "{\"status\":\"charged\"}";
    }
}
