import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.stream.Collectors;

/**
 * Fan-out: start N fetches, wait for all with allOf, collect typed results.
 * allOf returns CompletableFuture<Void> — results are joined afterwards.
 * allOf fails fast on the first exception but does NOT cancel the others.
 */
public class AllOfPattern {

    public static CompletableFuture<List<String>> fetchAllUrls(List<String> urls) {
        // Start all fetches in parallel
        List<CompletableFuture<String>> futures = urls.stream()
            .map(AsyncApiClient::fetchAsync)
            .collect(Collectors.toList());

        // allOf returns a CompletableFuture<Void> — completes when all complete
        CompletableFuture<Void> allDone = CompletableFuture.allOf(
            futures.toArray(new CompletableFuture[0])
        );

        // After all complete, collect results
        return allDone.thenApply(v ->
            futures.stream()
                .map(CompletableFuture::join)  // Safe — all are complete
                .collect(Collectors.toList())
        );
    }

    // Same shape, typed results: one optional source degrades to EMPTY
    // instead of taking down the whole report.
    public static CompletableFuture<AggregatedReport> buildReport(
            String userId, String dateRange) {
        CompletableFuture<SalesData> sales = fetchSales(userId, dateRange)
            .exceptionally(ex -> SalesData.EMPTY);
        CompletableFuture<TrafficData> traffic = fetchTraffic(userId, dateRange);
        CompletableFuture<RevenueData> revenue = fetchRevenue(userId, dateRange);

        return CompletableFuture.allOf(sales, traffic, revenue)
            .thenApply(v -> new AggregatedReport(
                sales.join(),
                traffic.join(),
                revenue.join()
            ));
    }

    // Service stubs — same shape as UserService.fetchUser.
    static CompletableFuture<SalesData> fetchSales(String userId, String range) {
        return AsyncApiClient.fetchAsync("https://api.example.com/sales?u=" + userId)
            .thenApply(json -> new SalesData(userId, range, 0));
    }

    static CompletableFuture<TrafficData> fetchTraffic(String userId, String range) {
        return AsyncApiClient.fetchAsync("https://api.example.com/traffic?u=" + userId)
            .thenApply(json -> new TrafficData(userId, range, 0));
    }

    static CompletableFuture<RevenueData> fetchRevenue(String userId, String range) {
        return AsyncApiClient.fetchAsync("https://api.example.com/revenue?u=" + userId)
            .thenApply(json -> new RevenueData(userId, range, 0));
    }

    public static void main(String[] args) {
        List<String> urls = List.of(
            "https://api.example.com/data/1",
            "https://api.example.com/data/2",
            "https://api.example.com/data/3"
        );

        List<String> results = fetchAllUrls(urls).join();
        results.forEach(System.out::println);
    }
}
