import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

/**
 * Sequential Convoy pattern — runnable simulation (no broker required).
 *
 * Events are routed to a partition by entity ID. Each partition is owned by a
 * single consumer that applies events in sequence-number order and buffers
 * out-of-order arrivals until the gap closes.
 *
 * Run: javac ConvoyProcessor.java && java ConvoyProcessor
 */
public class ConvoyProcessor {

    record Event(String entityId, int sequence, String type, String payload) {}

    static final class PartitionedBroker {
        private final List<Deque<Event>> partitions = new ArrayList<>();

        PartitionedBroker(int numPartitions) {
            for (int i = 0; i < numPartitions; i++) {
                partitions.add(new ArrayDeque<>());
            }
        }

        void publish(Event event) {
            int partition = Math.floorMod(event.entityId().hashCode(), partitions.size());
            partitions.get(partition).add(event);
        }

        List<Deque<Event>> partitions() {
            return partitions;
        }
    }

    static final class ConvoyProducer {
        private final PartitionedBroker broker;
        private final Map<String, Integer> sequences = new HashMap<>();

        ConvoyProducer(PartitionedBroker broker) {
            this.broker = broker;
        }

        void send(String entityId, String type, String payload) {
            int seq = sequences.merge(entityId, 1, Integer::sum);
            broker.publish(new Event(entityId, seq, type, payload));
        }
    }

    static final class ConvoyConsumer {
        private final Map<String, Integer> lastProcessed = new HashMap<>();
        private final Map<String, TreeMap<Integer, Event>> pending = new HashMap<>();
        final List<String> processedLog = new ArrayList<>();

        void consume(Event event) {
            String entity = event.entityId();
            int expected = lastProcessed.getOrDefault(entity, 0) + 1;

            if (event.sequence() == expected) {
                apply(event);
                drainPending(entity);
            } else if (event.sequence() > expected) {
                pending.computeIfAbsent(entity, k -> new TreeMap<>())
                        .put(event.sequence(), event);
            }
            // sequence < expected is a duplicate; skip it.
        }

        private void apply(Event event) {
            processedLog.add(event.entityId() + "#" + event.sequence());
            lastProcessed.put(event.entityId(), event.sequence());
        }

        private void drainPending(String entity) {
            TreeMap<Integer, Event> buffer = pending.get(entity);
            if (buffer == null) {
                return;
            }
            int expected = lastProcessed.getOrDefault(entity, 0) + 1;
            while (buffer.containsKey(expected)) {
                apply(buffer.remove(expected));
                expected++;
            }
        }
    }

    public static void main(String[] args) {
        PartitionedBroker broker = new PartitionedBroker(4);
        ConvoyProducer producer = new ConvoyProducer(broker);
        ConvoyConsumer consumer = new ConvoyConsumer();

        producer.send("user-123", "created", "{\"name\":\"Alice\"}");
        producer.send("user-123", "updated", "{\"name\":\"Alice Smith\"}");
        producer.send("user-456", "created", "{\"name\":\"Bob\"}");
        producer.send("user-123", "deleted", "{}");

        List<Event> events = new ArrayList<>();
        for (Deque<Event> partition : broker.partitions()) {
            events.addAll(partition);
        }

        // Simulate out-of-order delivery for user-123 (seq 3 before seq 2).
        List<Event> u123 = events.stream()
                .filter(e -> e.entityId().equals("user-123")).toList();
        List<Event> reordered = new ArrayList<>();
        reordered.add(u123.get(0));
        reordered.add(u123.get(2));
        reordered.add(u123.get(1));
        events.stream()
                .filter(e -> !e.entityId().equals("user-123"))
                .forEach(reordered::add);

        reordered.forEach(consumer::consume);

        System.out.println("Processed order: " + consumer.processedLog);
        List<String> expected = List.of("user-123#1", "user-123#2", "user-123#3");
        if (!consumer.processedLog.subList(0, 3).equals(expected)) {
            throw new AssertionError("convoy ordering broken");
        }
        System.out.println("user-123 processed strictly in order despite out-of-order delivery.");
    }
}
