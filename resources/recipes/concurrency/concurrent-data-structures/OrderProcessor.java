import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;

record Order(int id) {}

public class OrderProcessor {
    private final BlockingQueue<Order> queue = new ArrayBlockingQueue<>(100);

    public void submit(Order order) throws InterruptedException {
        queue.put(order); // blocks if full
    }

    public Order take() throws InterruptedException {
        return queue.take(); // blocks if empty
    }

    public void process(Order order) {
        System.out.println("Processing " + order.id());
    }

    public void start() {
        Thread producer = new Thread(() -> {
            try {
                for (int i = 0; i < 1000; i++) {
                    submit(new Order(i));
                }
                for (int i = 0; i < 4; i++) {
                    submit(new Order(-1)); // sentinel to stop each consumer
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });

        for (int i = 0; i < 4; i++) {
            new Thread(() -> {
                while (!Thread.currentThread().isInterrupted()) {
                    try {
                        Order order = take();
                        if (order.id() == -1) break;
                        process(order);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        break;
                    }
                }
            }).start();
        }

        producer.start();
    }

    public static void main(String[] args) {
        new OrderProcessor().start();
    }
}
