import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

// ScopedValue lives in java.lang — no import needed.
// Final in JDK 25 (JEP 506); preview on JDK 21–24, needs --enable-preview there.
public class ScopedValueExample {
    static final ScopedValue<String> USER_ID = ScopedValue.newInstance();
    static final ScopedValue<String> REQUEST_ID = ScopedValue.newInstance();

    static void handleRequest() {
        System.out.println("User: " + USER_ID.get() + ", Request: " + REQUEST_ID.get());

        // Virtual threads inherit scoped value bindings
        try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {
            executor.submit(() -> {
                System.out.println("In child thread — User: " + USER_ID.get()
                    + ", Request: " + REQUEST_ID.get());
            }).get();
        } catch (Exception e) {
            Thread.currentThread().interrupt();
        }
    }

    public static void main(String[] args) {
        // Bind values for the duration of the call — they can't be reassigned
        ScopedValue.where(USER_ID, "user-42")
            .where(REQUEST_ID, "req-abc-123")
            .run(() -> handleRequest());
    }
}
