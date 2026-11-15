import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Smooth weighted round-robin: the algorithm Nginx runs when you write
 * {@code weight=}. Each pick adds every server's weight to its running
 * score, chooses the max, then subtracts the total from the winner —
 * producing interleaved sequences (ABACA…) instead of bursts (AAA…BC).
 *
 * Run: javac SmoothWeightedBalancer.java && java SmoothWeightedBalancer
 */
public class SmoothWeightedBalancer {

    private static class Server {
        final String name;
        final int weight;
        int current;

        Server(String name, int weight) {
            this.name = name;
            this.weight = weight;
        }
    }

    private final List<Server> servers = new ArrayList<>();
    private int total;

    public void addServer(String name, int weight) {
        servers.add(new Server(name, weight));
        total += weight;
    }

    public synchronized String next() {
        Server best = null;
        for (Server s : servers) {
            s.current += s.weight;
            if (best == null || s.current > best.current) {
                best = s;
            }
        }
        if (best == null) return null;
        best.current -= total;
        return best.name;
    }

    public static void main(String[] args) {
        SmoothWeightedBalancer lb = new SmoothWeightedBalancer();
        lb.addServer("api1", 5);
        lb.addServer("api2", 3);
        lb.addServer("api3", 1);

        System.out.println("== Smooth weighted RR (5:3:1), 18 picks ==");
        Map<String, Integer> counts = new LinkedHashMap<>();
        StringBuilder seq = new StringBuilder();
        for (int i = 0; i < 18; i++) {
            String pick = lb.next();
            seq.append(pick).append(' ');
            counts.merge(pick, 1, Integer::sum);
        }
        System.out.println("sequence: " + seq);
        System.out.println("shares:   " + counts + " (expected 10:6:2, interleaved)");

        // Compare with naive weighted selection: weights taken as a block
        System.out.println("\nnaive block order would be: " +
            "api1 api1 api1 api1 api1 api2 api2 api2 api3 (bursty)");
    }
}
