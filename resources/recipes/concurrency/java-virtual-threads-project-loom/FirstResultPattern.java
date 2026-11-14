import java.util.concurrent.StructuredTaskScope;
import java.util.concurrent.StructuredTaskScope.Joiner;

// JDK 25+ with --enable-preview (JEP 505).
// On JDK 21–24 use new StructuredTaskScope.ShutdownOnSuccess<String>() instead.
public class FirstResultPattern {
    static String fetchFromReplica(String replicaUrl) throws InterruptedException {
        Thread.sleep((long) (Math.random() * 500));
        return "Data from " + replicaUrl;
    }

    public static void main(String[] args) throws Exception {
        // anySuccessfulResultOrThrow: first success wins, the rest are cancelled
        var joiner = Joiner.<String>anySuccessfulResultOrThrow();

        try (var scope = StructuredTaskScope.open(joiner)) {
            scope.fork(() -> fetchFromReplica("replica-1"));
            scope.fork(() -> fetchFromReplica("replica-2"));
            scope.fork(() -> fetchFromReplica("replica-3"));

            // join() returns the first successful result directly
            String result = scope.join();
            System.out.println("First response: " + result);
        }
    }
}
