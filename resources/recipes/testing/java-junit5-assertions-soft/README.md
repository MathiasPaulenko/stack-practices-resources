# AssertJ Soft Assertions in JUnit5

Companion code for [StackPractices: AssertJ Soft Assertions in JUnit5](https://stackpractices.com/recipes/java-junit5-assertions-soft/).

## Requirements

- Java 17+
- Maven 3.9+
- JUnit Jupiter 5.12.x
- AssertJ Core 3.27.7

## Files

| File | Description |
| ------ | ----------- |
| `pom.xml` | Maven project with JUnit5 + AssertJ test dependencies, plus the `assertj-assertions-generator-maven-plugin` wired to `generate-test-sources` |
| `src/main/java/domain/User.java` | Domain POJO that the assertion generator reads to emit `UserAssert`/`SoftAssertions` |
| `src/test/java/UserSoftAssertionsTest.java` | 7 runnable soft-assertion examples: basic `SoftAssertions`, `assertSoftly` lambda, collections, `.as()` custom messages, recursive comparison, `@RegisterExtension` injection, and JUnit5 `assertAll` for comparison |
| `src/test/java/GeneratedSoftAssertionsTest.java` | 2 tests using the plugin-generated `domain.SoftAssertions` entry point and typed `UserAssert` (`hasEmail()`, `hasRole()`, `isActive()`) |

The generator plugin (v2.2.0) emits `javax.annotation.Generated`, which the JDK removed in Java 11 — the `javax.annotation-api` test dependency in `pom.xml` covers it.

## Usage

The folder is a ready-made Maven project — just run:

```bash
mvn test
```

All tests pass out of the box — the service collaborators are stub records inside the test class so everything compiles standalone. To see the aggregated failure report, change an expected value (e.g., `isEqualTo(201)` → `isEqualTo(200)` in `should_validate_order_response`) and rerun: `assertAll()` throws a `SoftAssertionError` listing every failed check.

## What it demonstrates

- Why soft assertions matter: one run reports all failures instead of stopping at the first.
- The three entry points: `new SoftAssertions()`, `assertSoftly(lambda)`, and `SoftAssertionsExtension` via `@RegisterExtension`.
- `.as()` descriptions so a 10-failure report stays readable.
- `usingRecursiveComparison()` routed through the soft proxy for field-by-field object diffs.
