import java.time.Instant;
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.HashMap;
import java.util.Map;
import java.util.TreeMap;

/**
 * In-memory simulation of the DLQ runbook workflow.
 *
 * Mirrors the procedures in the runbook: a poison message exhausts its
 * retries, lands in the DLQ with failure metadata, gets inspected and
 * categorized, then replays back to the source queue once the fix deploys.
 *
 * Compile and run:
 *   javac src/DlqRunbookSimulation.java -d out
 *   java -cp out DlqRunbookSimulation
 */
public class DlqRunbookSimulation {

    static final int MAX_RETRIES = 3;
    static boolean fixDeployed = false;

    static class Message {
        final Map<String, String> headers = new HashMap<>();
        final boolean poison;
        final int orderId;

        Message(int orderId, boolean poison) {
            this.orderId = orderId;
            this.poison = poison;
        }
    }

    /** Minimal message broker with a main queue and a DLQ. */
    static class Broker {
        final Deque<Message> main = new ArrayDeque<>();
        final Deque<Message> dlq = new ArrayDeque<>();

        void publish(Message msg) {
            main.addLast(msg);
        }
    }

    /** Business handler — fails on poison payloads until the fix deploys. */
    static void processMessage(Message msg) {
        if (msg.poison && !fixDeployed) {
            throw new IllegalArgumentException("ValidationError: poison payload");
        }
    }

    /** Consumer with retry-count headers and DLQ routing (runbook §1.3). */
    static void consume(Broker broker) {
        while (!broker.main.isEmpty()) {
            Message msg = broker.main.pollFirst();
            try {
                processMessage(msg);
            } catch (Exception e) {
                int retryCount = Integer.parseInt(
                        msg.headers.getOrDefault("retry-count", "0")) + 1;
                msg.headers.put("retry-count", String.valueOf(retryCount));
                if (retryCount <= MAX_RETRIES) {
                    broker.publish(msg); // requeue on the source queue
                } else {
                    msg.headers.put("error", e.getMessage());
                    msg.headers.put("failed-at", Instant.now().toString());
                    broker.dlq.addLast(msg);
                }
            }
        }
    }

    /** Aggregate inspection — runbook §2.3. */
    static Map<String, Integer> inspectDlq(Broker broker) {
        Map<String, Integer> categories = new TreeMap<>();
        for (Message msg : broker.dlq) {
            String error = msg.headers.getOrDefault("error", "unknown");
            String category = error.contains("ValidationError")
                    ? "schema_validation_error"
                    : "business_logic_error";
            categories.merge(category, 1, Integer::sum);
        }
        return categories;
    }

    /** Replay after the fix deploys — runbook §4. */
    static int replayDlq(Broker broker) {
        int replayed = 0;
        while (!broker.dlq.isEmpty()) {
            Message msg = broker.dlq.pollFirst();
            for (String h : new String[]{"retry-count", "error", "failed-at"}) {
                msg.headers.remove(h); // strip DLQ metadata
            }
            broker.publish(msg);
            replayed++;
        }
        return replayed;
    }

    public static void main(String[] args) {
        Broker broker = new Broker();
        broker.publish(new Message(1, true));
        broker.publish(new Message(2, false));

        System.out.println("== Phase 1: consume (poison message retries then dead-letters) ==");
        consume(broker);
        System.out.printf("  main queue: %d | dlq: %d%n",
                broker.main.size(), broker.dlq.size());

        System.out.println("== Phase 2: inspect DLQ (error categorization) ==");
        inspectDlq(broker).forEach((cat, n) -> System.out.printf("  %s: %d%n", cat, n));

        System.out.println("== Phase 3: fix deploys, replay DLQ ==");
        fixDeployed = true; // the consumer now handles the poison payload
        System.out.printf("  replayed: %d%n", replayDlq(broker));
        consume(broker);

        System.out.printf("== Phase 4: verified — dlq: %d, unprocessed: %d ==%n",
                broker.dlq.size(), broker.main.size());
    }
}
