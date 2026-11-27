import java.util.concurrent.*;
import java.util.concurrent.atomic.*;
import java.util.function.Function;

public class LoadShedder {

    private final int maxConcurrent;
    private final double cpuThreshold;
    private final double memoryThreshold;
    private final int queueThreshold;
    private final AtomicInteger active = new AtomicInteger();
    private final AtomicInteger shedCount = new AtomicInteger();
    private final AtomicInteger acceptCount = new AtomicInteger();

    public LoadShedder(int maxConcurrent, double cpuThreshold,
                       double memoryThreshold, int queueThreshold) {
        this.maxConcurrent = maxConcurrent;
        this.cpuThreshold = cpuThreshold;
        this.memoryThreshold = memoryThreshold;
        this.queueThreshold = queueThreshold;
    }

    private boolean shouldShed() {
        if (active.get() >= maxConcurrent) return true;
        double cpuLoad = (double) active.get() / maxConcurrent;
        if (cpuLoad >= cpuThreshold) return true;
        long freeMem = Runtime.getRuntime().freeMemory();
        long totalMem = Runtime.getRuntime().totalMemory();
        double memUsage = 1.0 - ((double) freeMem / totalMem);
        if (memUsage >= memoryThreshold) return true;
        return active.get() * 10 >= queueThreshold;
    }

    public String execute(String requestId,
                          Function<String, String> handler) {
        if (shouldShed()) {
            shedCount.incrementAndGet();
            return String.format(
                "{\"requestId\":\"%s\",\"status\":\"shed\",\"httpStatus\":503}",
                requestId);
        }
        active.incrementAndGet();
        acceptCount.incrementAndGet();
        try {
            String result = handler.apply(requestId);
            return String.format(
                "{\"requestId\":\"%s\",\"status\":\"accepted\"," +
                    "\"result\":\"%s\",\"httpStatus\":200}",
                requestId, result);
        } finally {
            active.decrementAndGet();
        }
    }

    public String stats() {
        int total = acceptCount.get() + shedCount.get();
        return String.format(
            "accepted=%d, shed=%d, active=%d, shedRate=%.2f",
            acceptCount.get(), shedCount.get(), active.get(),
            (double) shedCount.get() / Math.max(total, 1));
    }

    public static void main(String[] args) throws Exception {
        var shedder = new LoadShedder(3, 0.95, 0.95, 10000);
        var executor = Executors.newFixedThreadPool(10);
        var futures = new java.util.ArrayList<Future<String>>();

        for (int i = 0; i < 10; i++) {
            final int idx = i;
            futures.add(executor.submit(() -> shedder.execute(
                "req-" + idx,
                req -> {
                    try {
                        Thread.sleep(100);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                    return "processed-" + req;
                })));
        }

        for (Future<String> f : futures) {
            System.out.println("  " + f.get());
        }
        System.out.println("\nStats: " + shedder.stats());
        executor.shutdown();
    }
}
