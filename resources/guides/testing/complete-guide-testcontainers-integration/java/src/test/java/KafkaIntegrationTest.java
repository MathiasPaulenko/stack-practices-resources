// KafkaIntegrationTest.java — Kafka integration test
import org.junit.jupiter.api.*;
import org.testcontainers.containers.KafkaContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;
import org.apache.kafka.clients.consumer.*;
import org.apache.kafka.clients.producer.*;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.kafka.common.serialization.StringSerializer;
import static org.junit.jupiter.api.Assertions.*;
import java.time.Duration;
import java.util.*;

@Testcontainers
class KafkaIntegrationTest {

    @Container
    static KafkaContainer kafka = new KafkaContainer("confluentinc/cp-kafka:7.6.0");

    private Properties producerProps;
    private Properties consumerProps;

    @BeforeEach
    void setUp() {
        producerProps = new Properties();
        producerProps.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, kafka.getBootstrapServers());
        producerProps.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        producerProps.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class);

        consumerProps = new Properties();
        consumerProps.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, kafka.getBootstrapServers());
        consumerProps.put(ConsumerConfig.GROUP_ID_CONFIG, "test-group");
        consumerProps.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        consumerProps.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
        consumerProps.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
    }

    @Test
    void testProduceAndConsume() {
        String topic = "test-topic";

        // Produce
        try (KafkaProducer<String, String> producer = new KafkaProducer<>(producerProps)) {
            ProducerRecord<String, String> record = new ProducerRecord<>(topic, "key1", "value1");
            producer.send(record);
            producer.flush();
        }

        // Consume
        try (KafkaConsumer<String, String> consumer = new KafkaConsumer<>(consumerProps)) {
            consumer.subscribe(List.of(topic));
            ConsumerRecords<String, String> records = consumer.poll(Duration.ofSeconds(10));
            assertEquals(1, records.count());
            ConsumerRecord<String, String> record = records.iterator().next();
            assertEquals("key1", record.key());
            assertEquals("value1", record.value());
        }
    }
}
