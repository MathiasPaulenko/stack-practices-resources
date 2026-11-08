import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.ReentrantLock;

/**
 * Deadlock simulation: unordered vs ordered lock acquisition.
 * Two threads compete for two row locks; sorted ordering prevents
 * the circular wait. Run: javac DeadlockSimulation.java && java DeadlockSimulation
 */
public class DeadlockSimulation {

    private static final ReentrantLock LOCK_A = new ReentrantLock();
    private static final ReentrantLock LOCK_B = new ReentrantLock();

    static String transfer(String first, String second) throws InterruptedException {
        ReentrantLock l1 = first.equals("A") ? LOCK_A : LOCK_B;
        ReentrantLock l2 = first.equals("A") ? LOCK_B : LOCK_A;
        if (!l1.tryLock(500, TimeUnit.MILLISECONDS)) return "deadlock waiting " + first;
        try {
            Thread.sleep(50); // let the other txn grab its first lock
            if (!l2.tryLock(500, TimeUnit.MILLISECONDS)) return "deadlock waiting " + second;
            l2.unlock();
        } finally {
            l1.unlock();
        }
        return "ok: " + first + "->" + second;
    }

    static String transferOrdered(String first, String second) throws InterruptedException {
        String[] rows = {first, second};
        Arrays.sort(rows); // consistent order removes the circular wait
        return transfer(rows[0], rows[1]);
    }

    static String executeWithRetry(ThrowingSupplier op, int maxRetries) throws InterruptedException {
        for (int attempt = 1; attempt <= maxRetries; attempt++) {
            String result = op.get();
            if (!result.startsWith("deadlock")) return result;
            Thread.sleep((long) (Math.pow(2, attempt) * 10 + Math.random() * 10));
        }
        return "failed: max retries exceeded";
    }

    @FunctionalInterface
    interface ThrowingSupplier {
        String get() throws InterruptedException;
    }

    public static void main(String[] args) throws InterruptedException {
        List<String> results = new ArrayList<>();

        System.out.println("=== Unordered lock acquisition ===");
        Thread t1 = new Thread(() -> {
            try { results.add(transfer("A", "B")); } catch (InterruptedException ignored) {}
        });
        Thread t2 = new Thread(() -> {
            try { results.add(transfer("B", "A")); } catch (InterruptedException ignored) {}
        });
        t1.start(); t2.start(); t1.join(); t2.join();
        results.forEach(System.out::println);
        results.clear();

        System.out.println("\n=== Ordered lock acquisition ===");
        t1 = new Thread(() -> {
            try { results.add(transferOrdered("A", "B")); } catch (InterruptedException ignored) {}
        });
        t2 = new Thread(() -> {
            try { results.add(transferOrdered("B", "A")); } catch (InterruptedException ignored) {}
        });
        t1.start(); t2.start(); t1.join(); t2.join();
        results.forEach(System.out::println);

        System.out.println("\n=== Retry with jitter ===");
        System.out.println(executeWithRetry(() -> transferOrdered("A", "B"), 3));
    }
}
