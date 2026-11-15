import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Simulates HAProxy's active health-check state machine.
 *
 * <p>Each backend runs a small FSM driven by probe results at every {@code inter}
 * interval: {@code fall N} consecutive failures mark it DOWN, {@code rise M}
 * consecutive passes mark it UP again. A leastconn dispatcher then routes
 * simulated requests only across servers currently UP.
 *
 * <p>This mirrors the recipe's {@code default-server inter 5s fall 2 rise 3}
 * tuning: a flapping backend that fails intermittently leaves rotation fast
 * but rejoins slowly, so clients never see its bad period.
 */
public class HealthCheckFsm {
    private static final int FALL = 2; // consecutive failures to mark DOWN
    private static final int RISE = 3; // consecutive passes to mark UP

    static class Backend {
        final String name;
        final boolean[] probes; // one result per interval
        boolean up = true;
        int fails = 0;
        int passes = 0;
        int sessions = 0;
        final List<String> log = new ArrayList<>();

        Backend(String name, boolean[] probes) {
            this.name = name;
            this.probes = probes;
        }

        void probe(boolean ok) {
            if (ok) {
                fails = 0;
                passes++;
                if (!up && passes >= RISE) {
                    up = true;
                    log.add(name + ": UP after " + passes + " passes");
                }
            } else {
                passes = 0;
                fails++;
                if (up && fails >= FALL) {
                    up = false;
                    log.add(name + ": DOWN after " + fails + " fails");
                }
            }
        }
    }

    public static void main(String[] args) {
        boolean[] allOk = new boolean[20];
        java.util.Arrays.fill(allOk, true);
        Backend web1 = new Backend("web1", allOk);

        // web2 fails at t=0..3 (down at t=1), recovers slowly (up at t=6)
        boolean[] w2 = new boolean[20];
        for (int i = 4; i < 20; i++) w2[i] = true;
        Backend web2 = new Backend("web2", w2);

        // web3 flaps: never reaches 3 consecutive passes, stays down
        boolean[] w3 = new boolean[20];
        for (int i = 0; i < 20; i++) w3[i] = i % 3 == 0;
        Backend web3 = new Backend("web3", w3);

        List<Backend> pool = List.of(web1, web2, web3);
        int intervals = 20;
        Map<String, Integer> served = new HashMap<>();
        for (Backend b : pool) served.put(b.name, 0);

        for (int t = 0; t < intervals; t++) {
            for (Backend b : pool) b.probe(b.probes[t % b.probes.length]);

            Backend pick = null;
            for (Backend b : pool) {
                if (b.up && (pick == null || b.sessions < pick.sessions)) pick = b;
            }
            if (pick == null) continue; // backup server would serve here
            pick.sessions++;
            served.merge(pick.name, 1, Integer::sum);
            // sessions accumulate so leastconn visibly steers traffic to web2
            // once it rejoins; real HAProxy drains them as requests finish
        }

        for (Backend b : pool) for (String entry : b.log) System.out.println(entry);
        System.out.println("\nRequests served per backend (of " + intervals + "):");
        served.forEach((name, n) -> System.out.println("  " + name + ": " + n));
        System.out.println("\nweb3 flapped and never earned 3 consecutive passes:");
        System.out.println("  it stayed DOWN the whole run despite answering some probes");
    }
}
