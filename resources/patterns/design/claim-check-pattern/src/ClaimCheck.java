import java.util.*;
import java.util.concurrent.*;

/**
 * Claim Check Pattern demo — JDK only.
 * Simulates: large payload -> object storage -> claim token -> broker -> consumer.
 * Run: javac ClaimCheck.java && java ClaimCheck
 */
public class ClaimCheck {

    interface BlobStorage {
        String upload(byte[] data, String contentType);
        byte[] download(String token);
        void delete(String token);
    }

    static class InMemoryBlobStorage implements BlobStorage {
        private final Map<String, byte[]> store = new ConcurrentHashMap<>();

        public String upload(byte[] data, String contentType) {
            String token = UUID.randomUUID().toString();
            store.put(token, data);
            return token;
        }

        public byte[] download(String token) {
            return store.get(token);
        }

        public void delete(String token) {
            store.remove(token);
        }
    }

    static class MessageBroker {
        private final Map<String, Queue<Map<String, Object>>> queues = new ConcurrentHashMap<>();

        public void publish(String queue, Map<String, Object> message) {
            queues.computeIfAbsent(queue, k -> new ConcurrentLinkedQueue<>()).offer(message);
        }

        public Map<String, Object> consume(String queue) {
            Queue<Map<String, Object>> q = queues.get(queue);
            return q != null ? q.poll() : null;
        }
    }

    static class ClaimCheckProducer {
        private final MessageBroker broker;
        private final BlobStorage storage;

        ClaimCheckProducer(MessageBroker broker, BlobStorage storage) {
            this.broker = broker;
            this.storage = storage;
        }

        String publishLargeMessage(String queue, String payloadJson, Map<String, Object> metadata) {
            byte[] data = payloadJson.getBytes();
            String token = storage.upload(data, "application/json");

            Map<String, Object> message = new HashMap<>();
            message.put("claimCheck", token);
            message.put("metadata", metadata);
            message.put("payloadSize", data.length);
            message.put("timestamp", new Date().toInstant().toString());

            broker.publish(queue, message);
            System.out.println("Published claim check: " + token);
            System.out.printf("  payload size in storage: %,d bytes%n", data.length);
            System.out.printf("  message size on broker:  ~%d bytes%n", message.toString().length());
            return token;
        }
    }

    static class ClaimCheckConsumer {
        private final MessageBroker broker;
        private final BlobStorage storage;

        ClaimCheckConsumer(MessageBroker broker, BlobStorage storage) {
            this.broker = broker;
            this.storage = storage;
        }

        String processNext(String queue) {
            Map<String, Object> message = broker.consume(queue);
            if (message == null) return null;

            String token = (String) message.get("claimCheck");
            byte[] data = storage.download(token);

            if (data == null) {
                System.err.println("ERROR: claim check not found: " + token);
                return null;
            }

            String payload = new String(data);
            System.out.printf("Retrieved payload (%,d bytes)%n", message.get("payloadSize"));
            storage.delete(token);
            System.out.println("Deleted claim check: " + token);
            return payload;
        }
    }

    public static void main(String[] args) {
        BlobStorage storage = new InMemoryBlobStorage();
        MessageBroker broker = new MessageBroker();
        ClaimCheckProducer producer = new ClaimCheckProducer(broker, storage);
        ClaimCheckConsumer consumer = new ClaimCheckConsumer(broker, storage);

        String largePayload = "{\"report_id\":\"RPT-2024-Q1\",\"data\":\"" + "x".repeat(1000000) + "\"}";
        producer.publishLargeMessage("reports.queue", largePayload, Map.of("priority", "high"));
        consumer.processNext("reports.queue");
    }
}
