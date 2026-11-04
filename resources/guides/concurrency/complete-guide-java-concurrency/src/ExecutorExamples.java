import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

/** Thread-pool and backpressure examples for the concurrency guide. */
public class ExecutorExamples {

    /** Bounded queue + CallerRunsPolicy = natural backpressure. */
    public static ThreadPoolExecutor boundedPool() {
        return new ThreadPoolExecutor(
            4, 16, 60L, TimeUnit.SECONDS,
            new LinkedBlockingQueue<>(100),
            r -> {
                Thread t = new Thread(r);
                t.setDaemon(true);
                return t;
            },
            new ThreadPoolExecutor.CallerRunsPolicy());
    }

    /** Graceful shutdown pattern. */
    public static void shutdown(ExecutorService executor) throws InterruptedException {
        executor.shutdown();
        if (!executor.awaitTermination(60, TimeUnit.SECONDS)) {
            executor.shutdownNow();
            if (!executor.awaitTermination(10, TimeUnit.SECONDS)) {
                System.err.println("Pool did not terminate");
            }
        }
    }

    /** Virtual-thread-per-task executor: do NOT pool these. */
    public static void ioBoundWork() throws InterruptedException {
        AtomicInteger done = new AtomicInteger(0);
        try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
            for (int i = 0; i < 10_000; i++) {
                executor.submit(() -> {
                    try {
                        Thread.sleep(100);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                    done.incrementAndGet();
                });
            }
        }
        System.out.println("Completed: " + done.get());
    }
}
