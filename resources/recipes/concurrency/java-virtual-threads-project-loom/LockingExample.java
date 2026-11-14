import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.ReentrantLock;

// JDK 24+ (JEP 491): synchronized no longer pins virtual threads.
// ReentrantLock is still useful for tryLock, fairness, conditions.
// On JDK 21–23 synchronized DID pin — the old advice lives there.
public class LockingExample {
    private static final ReentrantLock lock = new ReentrantLock();
    private static int counter = 0;

    public static void main(String[] args) throws InterruptedException {
        try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {
            for (int i = 0; i < 1000; i++) {
                executor.submit(() -> {
                    lock.lock();
                    try {
                        counter++;
                    } finally {
                        lock.unlock();
                    }
                });
            }

            executor.shutdown();
            executor.awaitTermination(5, TimeUnit.SECONDS);
        }

        System.out.println("Counter: " + counter);
    }
}
