import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;

/**
 * GET request with Java 11+ HttpClient — timeout and status check.
 */
public class httpclient_get {

    public static void main(String[] args) {
        HttpClient client = HttpClient.newBuilder()
                .connectTimeout(Duration.ofSeconds(10))
                .build();

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("https://api.example.com/users/1"))
                .timeout(Duration.ofSeconds(10))
                .header("Accept", "application/json")
                .GET()
                .build();

        try {
            HttpResponse<String> response =
                    client.send(request, HttpResponse.BodyHandlers.ofString());

            if (response.statusCode() >= 400) {
                throw new RuntimeException("HTTP " + response.statusCode());
            }

            System.out.println(response.body());
        } catch (java.net.ConnectException e) {
            System.err.println("Connection failed: " + e.getMessage());
        } catch (java.net.http.HttpTimeoutException e) {
            System.err.println("Request timed out");
        } catch (Exception e) {
            System.err.println("Request failed: " + e.getMessage());
        }
    }
}
