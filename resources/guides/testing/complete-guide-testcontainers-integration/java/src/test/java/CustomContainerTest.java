// CustomContainerTest.java — Custom container for any Docker image
import org.junit.jupiter.api.*;
import org.testcontainers.containers.GenericContainer;
import org.testcontainers.containers.BindMode;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;
import static org.junit.jupiter.api.Assertions.*;
import java.net.http.*;
import java.net.URI;

@Testcontainers
class CustomContainerTest {

    @Container
    static GenericContainer<?> mockServer = new GenericContainer<>("mockserver/mockserver:5.15.0")
        .withExposedPorts(1080)
        .withEnv("MOCKSERVER_INITIALIZATION_JSON_PATH", "/config/expectations.json")
        .withClasspathResourceMapping("config/expectations.json",
            "/config/expectations.json",
            BindMode.READ_ONLY);

    @Test
    void testMockServerResponse() throws Exception {
        String baseUrl = String.format("http://%s:%d",
            mockServer.getHost(),
            mockServer.getMappedPort(1080));

        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(baseUrl + "/api/users"))
            .GET()
            .build();

        HttpResponse<String> response = client.send(request,
            HttpResponse.BodyHandlers.ofString());

        assertEquals(200, response.statusCode());
        assertTrue(response.body().contains("users"));
    }
}
