# SpotBugs Static Analysis — Companion Resources

Runnable companion project for the [SpotBugs static analysis recipe](https://stackpractices.com/recipes/java-spotbugs-static-analysis/) on StackPractices.

## Contents

- `pom.xml` — Maven build with spotbugs-maven-plugin 4.9.3.0, `effort=Max`, `threshold=Medium`, and the Find Security Bugs plugin.
- `build.gradle` / `settings.gradle` — Gradle Groovy DSL equivalent of the Maven setup.
- `spotbugs-exclude.xml` — FindBugsFilter exclude file: test classes, generated code, per-class and per-pattern exclusions.
- `spotbugs-include-security.xml` — Include filter that runs only `SECURITY`, `CORRECTNESS`, and `MALICIOUS_CODE` categories, for a security-only gate.
- `github-actions/spotbugs.yml` — GitHub Actions workflow that runs `spotbugs:check` and uploads the XML report, with a commented SARIF/code-scanning variant.
- `src/main/java/com/example/spotbugsdemo/` — four classes with intentional bugs so the reports are not empty:
  - `NullPathBug.java` → `NP_NULL_ON_SOME_PATH`
  - `ExposedRep.java` → `EI_EXPOSE_REP` / `EI_EXPOSE_REP2`
  - `UnclosedResource.java` → `OBL_UNSATISFIED_OBLIGATION`
  - `SqlConcat.java` → `SQL_INJECTION_JDBC` (Find Security Bugs)

## Usage

Maven:

```bash
# Analysis + report (build does NOT fail on findings)
mvn spotbugs:spotbugs
# Report: target/spotbugsXml.xml — or run mvn spotbugs:gui for the triage viewer

# CI gate — fails the build on Medium+ findings (expected on this demo!)
mvn spotbugs:check
```

Gradle (needs `gradle` installed, or drop in a wrapper):

```bash
gradle spotbugsMain
# Reports: build/reports/spotbugs/main/spotbugs.html and .xml
```

Baseline adoption — silence existing findings and only gate on new ones:

```bash
mvn spotbugs:spotbugs
cp target/spotbugsXml.xml spotbugs-baseline.xml
mvn spotbugs:check -Dspotbugs.excludeBugsFile=spotbugs-baseline.xml
```

Security-only gate — point the include filter at `spotbugs-include-security.xml`:

```bash
mvn spotbugs:check -Dspotbugs.includeFilterFile=spotbugs-include-security.xml
```

Requires Java 17+ and Maven 3.6+ or Gradle 7+.
