import java.util.ArrayDeque;
import java.util.Deque;
import java.util.HashMap;
import java.util.Map;

/**
 * Dead Letter Channel pattern — in-memory simulation.
 *
 * A minimal broker with a main queue, a retry queue, and a dead letter
 * queue. The consumer processes orders; a poison message (missing
 * orderId) keeps failing, exhausts its retry budget, and lands in the
 * DLQ with failure metadata.
 *
 * Run: javac src/DeadLetterChannel.java && java -cp src DeadLetterChannel
 */
public class DeadLetterChannel {

    static final int MAX_RETRIES = 3;

    record Order(String orderId, int amount) {}

    static class Envelope {
        final Order body;
        int attempts;
        String failure;

        Envelope(Order body) {
            this.body = body;
        }
    }

    static class Broker {
        private final Map<String, Deque<Envelope>> queues = new HashMap<>();

        void declare(String name) {
            queues.putIfAbsent(name, new ArrayDeque<>());
        }

        void send(String name, Order body) {
            queues.get(name).add(new Envelope(body));
        }

        void sendEnvelope(String name, Envelope envelope) {
            queues.get(name).add(envelope);
        }

        Envelope receive(String name) {
            return queues.get(name).poll();
        }

        int depth(String name) {
            return queues.get(name).size();
        }
    }

    static String handleOrder(Order order) {
        if (order.orderId() == null) {
            throw new IllegalArgumentException("Missing orderId");
        }
        return order.orderId();
    }

    public static void main(String[] args) {
        Broker broker = new Broker();
        for (String queue : new String[] {"main", "retry", "dlq"}) {
            broker.declare(queue);
        }

        broker.send("main", new Order("A-1", 25));
        broker.send("main", new Order(null, 99)); // poison message
        broker.send("main", new Order("A-3", 40));

        int processed = 0;
        int retries = 0;

        while (true) {
            Envelope msg = broker.receive("main");
            if (msg == null) msg = broker.receive("retry");
            if (msg == null) break;

            try {
                String orderId = handleOrder(msg.body);
                processed++;
                System.out.println("[main] processed order " + orderId);
            } catch (Exception e) {
                msg.attempts++;
                if (msg.attempts >= MAX_RETRIES) {
                    msg.failure = e.getMessage();
                    broker.sendEnvelope("dlq", msg);
                    System.out.println("[dlq ] moved message after " + msg.attempts + " attempts: " + e.getMessage());
                } else {
                    retries++;
                    System.out.println("[main] attempt " + msg.attempts + " failed (" + e.getMessage() + "); retrying");
                    broker.sendEnvelope("retry", msg);
                }
            }
        }

        System.out.println();
        System.out.println("main=" + broker.depth("main") + " retry=" + broker.depth("retry") + " dlq=" + broker.depth("dlq"));
        System.out.println("processed=" + processed + " retried=" + retries);

        // Replay: fix the poisoned payload, then move it back to the main queue
        Envelope msg = broker.receive("dlq");
        if (msg != null) {
            System.out.println();
            System.out.println("[replay] fixing message and re-queuing (was: " + msg.failure + ")");
            broker.sendEnvelope("main", new Envelope(new Order("A-2-repaired", msg.body.amount())));
            Envelope fixed = broker.receive("main");
            System.out.println("[main] processed order " + handleOrder(fixed.body));
        }
    }
}
