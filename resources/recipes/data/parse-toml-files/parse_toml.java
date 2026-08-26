// Parse TOML files in Java.
// Maven dependency: org.tomlj:tomlj:1.1.0
import org.tomlj.Toml;
import org.tomlj.TomlTable;
import java.util.List;

public class parse_toml {
    public static void main(String[] args) throws Exception {
        TomlTable table = Toml.parse("config.toml");

        String appName = table.getString("app.name");
        String dbHost = table.getString("database.host");
        List<TomlTable> servers = table.getTables("servers");

        System.out.println("App: " + appName);
        System.out.println("DB Host: " + dbHost);
        System.out.println("Servers: " + servers.size());
    }
}
