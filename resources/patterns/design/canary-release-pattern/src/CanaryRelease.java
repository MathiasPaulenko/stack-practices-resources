import java.util.*;

public class CanaryRelease {

    record HealthMetrics(double errorRate, double p95LatencyMs, double successRate) {
        boolean isHealthy(double maxError, double maxP95) {
            return errorRate <= maxError && p95LatencyMs <= maxP95;
        }
    }

    record Stage(double percentage, long bakeTimeMs) {}

    private final String version, stableVersion;
    private final java.util.function.Supplier<HealthMetrics> healthCheckFn;
    private final double maxErrorRate, maxP95;
    private String status = "pending";
    private int currentStageIdx = -1;
    private final List<Stage> stages;

    public CanaryRelease(String version, String stableVersion,
                         java.util.function.Supplier<HealthMetrics> healthCheckFn,
                         double maxErrorRate, double maxP95) {
        this.version = version; this.stableVersion = stableVersion;
        this.healthCheckFn = healthCheckFn; this.maxErrorRate = maxErrorRate; this.maxP95 = maxP95;
        // Demo bake times; real stages run for minutes, not milliseconds.
        this.stages = List.of(
            new Stage(1.0, 100), new Stage(5.0, 100), new Stage(25.0, 100),
            new Stage(50.0, 100), new Stage(100.0, 100)
        );
    }

    private boolean runStage(Stage stage) {
        currentStageIdx++;
        status = "running";
        System.out.printf("  Canary at %.0f%% -> stable=%.0f%%%n", stage.percentage(), 100 - stage.percentage());
        try { Thread.sleep(stage.bakeTimeMs()); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
        HealthMetrics m = healthCheckFn.get();
        boolean healthy = m.isHealthy(maxErrorRate, maxP95);
        System.out.printf("    error_rate=%.2f%%, p95=%.0fms%n", m.errorRate() * 100, m.p95LatencyMs());
        if (healthy) { System.out.println("    PASS - advancing"); return true; }
        System.out.println("    FAIL - rolling back");
        status = "rolled_back";
        return false;
    }

    public Map<String, Object> execute() {
        System.out.printf("%n=== Canary Release: v%s (stable: v%s) ===%n", version, stableVersion);
        for (int i = 0; i < stages.size(); i++) {
            if (!runStage(stages.get(i))) {
                return Map.of("version", version, "status", status, "rolledBack", true,
                    "stagesPassed", currentStageIdx, "failedStage", i,
                    "maxPercentage", stages.get(currentStageIdx).percentage());
            }
        }
        status = "promoted";
        System.out.printf("%nCanary promoted. v%s is now at 100%%.%n", version);
        return Map.of("version", version, "status", status, "rolledBack", false,
            "stagesPassed", stages.size(), "maxPercentage", 100.0);
    }

    public static void main(String[] args) {
        int[] callCount = {0};
        var healthCheck = (java.util.function.Supplier<HealthMetrics>) () -> {
            callCount[0]++;
            if (callCount[0] == 3) return new HealthMetrics(0.05, 400, 0.95);
            return new HealthMetrics(0.005, 80, 0.995);
        };
        System.out.println("\nResult: " + new CanaryRelease("3.0.0", "2.9.0", healthCheck, 0.02, 300).execute());
    }
}
