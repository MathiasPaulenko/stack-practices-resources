import java.util.concurrent.*;
import java.util.concurrent.locks.ReentrantReadWriteLock;

/**
 * Bounded thread pool with backpressure + a read-write locked cache.
 * Compile: javac ConcurrencyBasics.java
 * Run:     java ConcurrencyBasics
 */
public class ConcurrencyBasics {

    /** Read-heavy cache: many concurrent readers, exclusive writers. */
    static class CachedData {
        private String data = "initial";
        private final ReentrantReadWriteLock rwl = new ReentrantReadWriteLock();

        String read() {
            rwl.readLock().lock();
            try { return data; }
            finally { rwl.readLock().unlock(); }
        }

        void write(String newData) {
            rwl.writeLock().lock();
            try { this.data = newData; }
            finally { rwl.writeLock().unlock(); }
        }
    }

    public static void main(String[] args) throws InterruptedException {
        // Bounded pool + bounded queue + CallerRunsPolicy: producers slow
        // down instead of queueing unbounded work until OOM.
        ExecutorService executor = new ThreadPoolExecutor(
            4, 4, 0L, TimeUnit.MILLISECONDS,
            new ArrayBlockingQueue<>(100),
            new ThreadPoolExecutor.CallerRunsPolicy()
        );

        CachedData cache = new CachedData();
        for (int i = 0; i < 10; i++) {
            final int n = i;
            executor.submit(() -> {
                if (n % 5 == 0) cache.write("value-" + n);
                System.out.println("task " + n + " read: " + cache.read());
            });
        }

        executor.shutdown();
        if (!executor.awaitTermination(30, TimeUnit.SECONDS)) {
            executor.shutdownNow();
        }
        System.out.println("pool shut down cleanly");
    }
}
