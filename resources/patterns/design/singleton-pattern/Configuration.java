/**
 * Enum Singleton — the recommended Java form (Effective Java, item 3).
 *
 * Thread-safe by JVM guarantee, lazy at class init, and the only variant
 * immune to serialization and reflection attacks. A second instance is
 * impossible: the JVM creates each enum constant exactly once.
 */
public enum Configuration {
    INSTANCE;

    private final java.util.Map<String, String> properties = loadProperties();

    public String get(String key) {
        return properties.get(key);
    }

    private java.util.Map<String, String> loadProperties() {
        // load from file/env; static values here for the runnable demo
        return java.util.Map.of(
            "env", System.getenv().getOrDefault("APP_ENV", "dev"),
            "region", "us-east-1"
        );
    }

    public static void main(String[] args) {
        Configuration a = Configuration.INSTANCE;
        Configuration b = Configuration.INSTANCE;
        System.out.println("same instance: " + (a == b));
        System.out.println("env=" + a.get("env") + " region=" + a.get("region"));
    }
}
