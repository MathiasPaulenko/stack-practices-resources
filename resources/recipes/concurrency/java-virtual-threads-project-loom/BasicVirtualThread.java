public class BasicVirtualThread {
    public static void main(String[] args) throws InterruptedException {
        // Create and start a virtual thread — no executor needed
        Thread vt = Thread.ofVirtual().name("my-virtual-thread").start(() -> {
            System.out.println("Running in: " + Thread.currentThread());
            System.out.println("Is virtual: " + Thread.currentThread().isVirtual());
        });

        vt.join();
        System.out.println("Virtual thread completed");
    }
}
