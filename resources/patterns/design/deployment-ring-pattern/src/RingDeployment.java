import java.util.*;

/**
 * Deployment Ring Pattern — runnable Java implementation.
 *
 * Simulates a progressive rollout through rings of increasing size. A mock
 * health check fails on the third call (ring 2), which forces a rollback
 * of the rings that already passed.
 *
 * Run: javac RingDeployment.java && java RingDeployment
 */
public class RingDeployment {

    record Ring(int ringId, String name, double percentage, String status, boolean healthCheckPassed) {
        Ring withStatus(String s) { return new Ring(ringId, name, percentage, s, healthCheckPassed); }
        Ring withHealth(boolean h) { return new Ring(ringId, name, percentage, status, h); }
    }

    record HealthMetrics(double errorRate, double p95LatencyMs, double successRate) {
        boolean isHealthy(double maxError, double maxP95) {
            return errorRate < maxError && p95LatencyMs < maxP95;
        }
    }

    private final String version;
    private final List<Ring> rings;
    private final java.util.function.Supplier<HealthMetrics> healthCheckFn;
    private final double maxErrorRate;
    private final double maxP95;

    public RingDeployment(String version, List<Ring> rings,
                          java.util.function.Supplier<HealthMetrics> healthCheckFn,
                          double maxErrorRate, double maxP95) {
        this.version = version; this.rings = rings;
        this.healthCheckFn = healthCheckFn; this.maxErrorRate = maxErrorRate; this.maxP95 = maxP95;
    }

    private boolean deployToRing(Ring ring) {
        System.out.printf("  Deploying v%s to %s (%.1f%%)%n", version, ring.name(), ring.percentage());
        try { Thread.sleep(100); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }

        HealthMetrics m = healthCheckFn.get();
        boolean healthy = m.isHealthy(maxErrorRate, maxP95);
        System.out.printf("    Health: error_rate=%.2f%%, p95=%.0fms%n", m.errorRate() * 100, m.p95LatencyMs());

        if (healthy) { System.out.printf("    PASS - Ring %d completed%n", ring.ringId()); return true; }
        System.out.printf("    FAIL - Ring %d failed, rolling back%n", ring.ringId());
        return false;
    }

    public Map<String, Object> execute() {
        System.out.printf("%n=== Ring Deployment: v%s ===%n", version);
        for (int i = 0; i < rings.size(); i++) {
            if (!deployToRing(rings.get(i))) {
                rollback();
                return Map.of("version", version, "status", "rolled_back", "failedRing", rings.get(i).ringId(), "ringsCompleted", i);
            }
        }
        System.out.printf("%nAll rings completed. v%s is live for 100%%.%n", version);
        return Map.of("version", version, "status", "completed", "ringsCompleted", rings.size());
    }

    private void rollback() {
        for (Ring r : rings) {
            if (r.status().equals("completed"))
                System.out.printf("  Rolling back ring %d (%s)%n", r.ringId(), r.name());
        }
    }

    public static void main(String[] args) {
        int[] callCount = {0};
        var healthCheck = (java.util.function.Supplier<HealthMetrics>) () -> {
            callCount[0]++;
            if (callCount[0] == 3) return new HealthMetrics(0.08, 600, 0.92);
            return new HealthMetrics(0.01, 120, 0.99);
        };

        var rings = List.of(
            new Ring(0, "internal", 1.0, "pending", false),
            new Ring(1, "early-adopters", 5.0, "pending", false),
            new Ring(2, "canary", 25.0, "pending", false),
            new Ring(3, "general", 100.0, "pending", false)
        );

        var deployment = new RingDeployment("2.1.0", rings, healthCheck, 0.05, 500);
        System.out.println("\nResult: " + deployment.execute());
    }
}
