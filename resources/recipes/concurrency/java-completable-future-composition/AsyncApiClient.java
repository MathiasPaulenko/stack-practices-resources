import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.concurrent.CompletableFuture;

/**
 * Base async HTTP client: every other example builds on fetchAsync(url).
 * sendAsync already returns a CompletableFuture — the pipeline starts there.
 */
public class AsyncApiClient {
    private static final HttpClient client = HttpClient.newHttpClient();

    public static CompletableFuture<String> fetchAsync(String url) {
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(url))
            .GET()
            .build();

        return client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
            .thenApply(HttpResponse::body);
    }

    public static void main(String[] args) {
        // Non-blocking — runs on the HttpClient's executor
        CompletableFuture<String> future = fetchAsync("https://api.example.com/users");

        // Do other work while the request is in flight...

        // Block only when you need the result
        String result = future.join();
        System.out.println(result);
    }
}
