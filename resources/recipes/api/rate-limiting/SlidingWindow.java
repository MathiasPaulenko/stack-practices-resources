import java.util.concurrent.*;

/**
 * Sliding-window-log rate limiter — keeps one timestamp per request.
 * Accurate, no boundary bursts; O(requests-per-window) memory.
 */
public class SlidingWindow {
    private final int capacity;
    private final long windowMs;
    private final ConcurrentLinkedDeque<Long> timestamps = new ConcurrentLinkedDeque<>();

    public SlidingWindow(int capacity, long windowMs) {
        this.capacity = capacity;
        this.windowMs = windowMs;
    }

    public synchronized boolean allow() {
        long now = System.currentTimeMillis();
        while (!timestamps.isEmpty() && now - timestamps.peekFirst() > windowMs) {
            timestamps.pollFirst();
        }
        if (timestamps.size() < capacity) {
            timestamps.addLast(now);
            return true;
        }
        return false;
    }

    public static void main(String[] args) {
        SlidingWindow w = new SlidingWindow(100, 60_000); // 100 req/min
        System.out.println(w.allow()); // true
    }
}
