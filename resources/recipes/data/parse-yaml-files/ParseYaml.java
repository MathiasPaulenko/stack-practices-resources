// SnakeYAML: Maven dependency org.yaml:snakeyaml
import org.yaml.snakeyaml.Yaml;
import java.io.FileInputStream;
import java.util.Map;

public class ParseYaml {
    public static void main(String[] args) throws Exception {
        Yaml yaml = new Yaml();
        try (FileInputStream fis = new FileInputStream("config.yaml")) {
            Map<String, Object> config = yaml.load(fis);
            Map<String, Object> app = (Map<String, Object>) config.get("app");
            Map<String, Object> db = (Map<String, Object>) config.get("database");
            Map<String, Object> prod = (Map<String, Object>) config.get("production");
            System.out.println("app: " + app.get("name") + " " + app.get("version"));
            System.out.println("database host: " + db.get("host"));
            System.out.println("production: " + prod);
        }
    }
}
