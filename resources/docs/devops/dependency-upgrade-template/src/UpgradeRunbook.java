// Simulation of the five-phase dependency upgrade runbook.
// Two upgrades run through the same checklist: one succeeds end to end,
// one fails validation and exercises the rollback path.

public class UpgradeRunbook {

    record Dep(String name, String current, String target, boolean breaksTests) { }

    static void runPhase(String label, String... steps) {
        System.out.println("\n== " + label + " ==");
        for (String step : steps) System.out.println("  [done] " + step);
    }

    static void upgrade(Dep dep) {
        System.out.println("\n########## upgrade " + dep.name() + " " + dep.current() + " -> " + dep.target() + " ##########");

        runPhase("1. Preparation",
            "changelog reviewed for breaking changes",
            "branch created: deps/upgrade-" + dep.name() + "-" + dep.target(),
            "CI green on main");

        runPhase("2. Upgrade",
            "version bumped in pom.xml",
            "mvn install completed, no conflicts",
            "tests run: " + (dep.breaksTests() ? "2 FAILING" : "all passing"));

        boolean stable = !dep.breaksTests();
        runPhase("3. Validation",
            "coverage report reviewed",
            "no new warnings in logs",
            "OWASP dependency check: 0 high/critical",
            "result: " + (stable ? "STABLE" : "UNSTABLE"));

        if (!stable) {
            runPhase("4. Rollback",
                "git checkout pre-upgrade-tag -- pom.xml",
                "mvn install restored last known good",
                "rollback executed in <15 min");
            System.out.println("  => " + dep.name() + " stays at " + dep.current() + "; upgrade rejected");
            return;
        }

        runPhase("5. Merge & Monitor",
            "PR opened with changelog summary",
            "staging soak: 24h clean",
            "production deploy in low-traffic window",
            "error rate flat after 48h");
        System.out.println("  => " + dep.name() + " is now " + dep.target());
    }

    public static void main(String[] args) {
        upgrade(new Dep("jackson-databind", "2.15.2", "2.17.0", false));
        upgrade(new Dep("left-pad-classic", "1.0.0", "2.0.0", true));
    }
}
