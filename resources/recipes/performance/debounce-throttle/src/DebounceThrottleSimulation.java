import java.util.ArrayList;
import java.util.List;

/**
 * Event burst simulation: debounce vs throttle over a synthetic stream.
 * Run: javac DebounceThrottleSimulation.java && java DebounceThrottleSimulation
 */
public class DebounceThrottleSimulation {

    private static final long DEBOUNCE_WAIT = 250;
    private static final long THROTTLE_LIMIT = 300;

    static void simulate(List<Long> events) {
        long throttleLast = -THROTTLE_LIMIT; // first event always fires
        int throttleFires = 0;
        long quietStart = -1;
        int debounceFires = 0;

        for (long t : events) {
            if (t - throttleLast >= THROTTLE_LIMIT) {
                throttleLast = t;
                throttleFires++;
            }
            if (quietStart >= 0 && t - quietStart >= DEBOUNCE_WAIT) {
                debounceFires++;
            }
            quietStart = t;
        }
        debounceFires++;

        System.out.printf(
            "events=%d  raw=%d  debounce=%d  throttle=%d%n",
            events.size(), events.size(), debounceFires, throttleFires);
    }

    public static void main(String[] args) {
        List<Long> events = new ArrayList<>();
        for (int i = 0; i < 12; i++) events.add(i * 25L);
        events.add(1000L);
        events.add(1050L);
        events.add(1100L);
        simulate(events);
    }
}
