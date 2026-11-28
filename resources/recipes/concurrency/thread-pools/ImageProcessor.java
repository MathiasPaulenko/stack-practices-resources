import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Fixed thread pool for CPU-bound work plus a production-grade
 * ThreadPoolExecutor with bounded queue and rejection policy.
 */
public class ImageProcessor {
    private final ExecutorService executor;

    public ImageProcessor(int poolSize) {
        this.executor = Executors.newFixedThreadPool(poolSize);
    }

    public CompletableFuture<String> processAsync(String imageId) {
        return CompletableFuture.supplyAsync(() -> {
            // CPU-intensive image processing
            return processImage(imageId);
        }, executor);
    }

    private String processImage(String imageId) {
        // Simulate work
        return "processed-" + imageId;
    }

    public void shutdown() {
        executor.shutdown();
        try {
            if (!executor.awaitTermination(60, TimeUnit.SECONDS)) {
                executor.shutdownNow();
            }
        } catch (InterruptedException e) {
            executor.shutdownNow();
        }
    }

    /** Production pool: bounded queue, named threads, explicit rejection policy. */
    public static ExecutorService productionPool() {
        return new ThreadPoolExecutor(
            4,                                   // core pool size
            8,                                   // maximum pool size
            30L, TimeUnit.SECONDS,               // keep-alive for extra threads
            new LinkedBlockingQueue<>(100),      // bounded queue
            new ThreadFactory() {
                private final AtomicInteger counter = new AtomicInteger(0);
                public Thread newThread(Runnable r) {
                    return new Thread(r, "worker-" + counter.incrementAndGet());
                }
            },
            new ThreadPoolExecutor.CallerRunsPolicy()  // run in caller thread if full
        );
    }
}
