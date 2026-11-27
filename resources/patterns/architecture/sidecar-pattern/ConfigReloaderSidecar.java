// ConfigReloaderSidecar.java — watch config dir, ping app on change
import java.nio.file.*;
import java.net.http.*;
import java.net.URI;
import java.nio.charset.StandardCharsets;

public class ConfigReloaderSidecar {
    private static final String CONFIG_PATH = "/etc/app/config";
    private static final String RELOAD_URL =
        "http://localhost:8080/admin/reload";

    public void watchAndReload() throws Exception {
        var watchService =
            FileSystems.getDefault().newWatchService();
        Paths.get(CONFIG_PATH).register(
            watchService, StandardWatchEventKinds.ENTRY_MODIFY);

        System.out.println("Watching " + CONFIG_PATH);
        while (true) {
            var key = watchService.take();
            for (var event : key.pollEvents()) {
                var file = (Path) event.context();
                System.out.println("Config changed: " + file);
                signalReload();
            }
            key.reset();
        }
    }

    private void signalReload() {
        try {
            var client = HttpClient.newHttpClient();
            var request = HttpRequest.newBuilder()
                .uri(URI.create(RELOAD_URL))
                .POST(HttpRequest.BodyPublishers.noBody())
                .build();
            var response = client.send(request,
                HttpResponse.BodyHandlers.ofString(
                    StandardCharsets.UTF_8));
            if (response.statusCode() == 200) {
                System.out.println("App reloaded config");
            } else {
                System.err.println(
                    "Reload failed: " + response.statusCode());
            }
        } catch (Exception e) {
            System.err.println("Reload failed: " + e.getMessage());
        }
    }

    public static void main(String[] args) throws Exception {
        new ConfigReloaderSidecar().watchAndReload();
    }
}
