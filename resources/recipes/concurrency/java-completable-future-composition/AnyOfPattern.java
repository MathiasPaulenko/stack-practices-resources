import java.util.List;
import java.util.concurrent.CompletableFuture;

/**
 * Racing: anyOf resolves on the FIRST completion — success or failure.
 * fetchFirstAvailable adds an exceptionally filter so a fast error from one
 * replica doesn't beat a slow success from another.
 */
public class AnyOfPattern {

    // First completed response — raw anyOf semantics
    public static CompletableFuture<String> fetchFirstCompleted(List<String> urls) {
        CompletableFuture<?>[] futures = urls.stream()
            .map(AsyncApiClient::fetchAsync)
            .toArray(CompletableFuture[]::new);

        return CompletableFuture.anyOf(futures)
            .thenApply(obj -> (String) obj);
    }

    // First SUCCESSFUL response — failures collapse to null and keep racing
    public static CompletableFuture<String> fetchFirstAvailable(List<String> urls) {
        CompletableFuture<?>[] futures = urls.stream()
            .map(url -> AsyncApiClient.fetchAsync(url).exceptionally(ex -> null))
            .toArray(CompletableFuture[]::new);

        return CompletableFuture.anyOf(futures)
            .thenApply(obj -> (String) obj);
    }

    public static void main(String[] args) {
        List<String> replicaUrls = List.of(
            "https://replica1.example.com/data",
            "https://replica2.example.com/data",
            "https://replica3.example.com/data"
        );

        String result = fetchFirstAvailable(replicaUrls).join();
        System.out.println("First response: " + result);
    }
}
