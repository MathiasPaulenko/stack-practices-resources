import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

public class ConcurrentLinkedQueueDemo {

    public static void main(String[] args) throws InterruptedException {
        // Lock-free unbounded MPMC queue (Michael & Scott algorithm)
        ConcurrentLinkedQueue<Integer> queue = new ConcurrentLinkedQueue<>();
        AtomicInteger produced = new AtomicInteger();
        AtomicInteger consumed = new AtomicInteger();

        Runnable producer = () -> {
            for (int i = 0; i < 10000; i++) {
                queue.offer(i);
                produced.incrementAndGet();
            }
        };
        Runnable consumer = () -> {
            while (consumed.get() < 20000) {
                if (queue.poll() != null) consumed.incrementAndGet();
            }
        };

        ExecutorService pool = Executors.newFixedThreadPool(4);
        pool.submit(producer);
        pool.submit(producer); // 2 producers -> 20k items total
        pool.submit(consumer);
        pool.submit(consumer); // 2 consumers
        pool.shutdown();
        pool.awaitTermination(10, TimeUnit.SECONDS);
        System.out.println("Produced: " + produced + ", Consumed: " + consumed);
    }
}
