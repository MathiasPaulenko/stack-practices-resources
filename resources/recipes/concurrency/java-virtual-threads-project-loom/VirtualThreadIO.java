import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.List;
import java.util.ArrayList;

public class VirtualThreadIO {
    private static final HttpClient client = HttpClient.newHttpClient();

    public static String fetch(String url) throws Exception {
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(url))
            .GET()
            .build();

        return client.send(request, HttpResponse.BodyHandlers.ofString()).body();
    }

    public static void main(String[] args) throws Exception {
        List<String> urls = List.of(
            "https://httpbin.org/delay/1",
            "https://httpbin.org/delay/2",
            "https://httpbin.org/delay/1",
            "https://httpbin.org/delay/3",
            "https://httpbin.org/delay/1"
        );

        try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {
            List<java.util.concurrent.Future<String>> futures = new ArrayList<>();

            for (String url : urls) {
                futures.add(executor.submit(() -> fetch(url)));
            }

            // Each fetch runs on its own virtual thread
            // Total ~3s (max delay), not 8s (sum of delays)
            long start = System.currentTimeMillis();
            for (java.util.concurrent.Future<String> f : futures) {
                System.out.println("Fetched " + f.get().length() + " bytes");
            }
            System.out.println("Total time: " + (System.currentTimeMillis() - start) + "ms");
        }
    }
}
