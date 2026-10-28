import java.util.*;

public class BlueGreenDeployment {

    enum Color { BLUE, GREEN }

    static class Environment {
        Color color; String version = ""; String status = "inactive";
        boolean health = false; int instanceCount = 0;
        Environment(Color c) { this.color = c; }
    }

    private Environment active, inactive;
    private final List<Map<String, Object>> history = new ArrayList<>();

    public BlueGreenDeployment() {
        active = new Environment(Color.BLUE);
        active.version = "1.0.0"; active.status = "active"; active.health = true; active.instanceCount = 3;
        inactive = new Environment(Color.GREEN);
    }

    private void switchEnv() {
        Environment tmp = active; active = inactive; inactive = tmp;
        active.status = "active"; inactive.status = "inactive";
    }

    public Map<String, Object> deploy(String newVersion, List<java.util.function.Supplier<Boolean>> smokeTests) {
        System.out.printf("%n=== Blue-Green Deploy: v%s ===%n", newVersion);
        Environment target = inactive;
        System.out.printf("  Deploying to %s (inactive)%n", target.color);
        target.status = "deploying"; target.version = newVersion; target.instanceCount = 3;
        System.out.printf("  Deployed v%s to %s%n", newVersion, target.color);

        target.status = "testing";
        for (var test : smokeTests) {
            if (!test.get()) {
                target.health = false; target.status = "inactive";
                System.out.printf("  Smoke tests FAILED on %s%n", target.color);
                return Map.of("success", false, "activeColor", active.color, "version", active.version);
            }
        }
        target.health = true;
        System.out.printf("  Smoke tests passed on %s%n", target.color);
        switchEnv();
        System.out.printf("  Switched: %s (v%s) is now active%n", active.color, active.version);
        history.add(Map.of("version", newVersion, "active", active.color.toString()));
        return Map.of("success", true, "activeColor", active.color, "version", newVersion);
    }

    public Map<String, Object> rollback() {
        System.out.println("\n=== Rollback ===");
        if (inactive.health && !inactive.version.isEmpty()) {
            switchEnv();
            System.out.printf("  Rolled back to %s (v%s)%n", active.color, active.version);
            return Map.of("success", true, "activeColor", active.color, "version", active.version, "rollback", true);
        }
        return Map.of("success", false, "activeColor", active.color, "version", active.version);
    }

    public static void main(String[] args) {
        var bg = new BlueGreenDeployment();
        var result = bg.deploy("2.0.0", List.of(
            () -> { System.out.println("    Test: API response"); return true; },
            () -> { System.out.println("    Test: DB connection"); return true; }
        ));
        System.out.println("Result: " + result);
        System.out.println("\n=== Rolling back ===");
        System.out.println("Rollback: " + bg.rollback());
    }
}
