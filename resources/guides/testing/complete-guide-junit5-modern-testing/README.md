# JUnit 5: Extensions, Parameterized Tests, Dynamic Tests — Examples

Runnable companion for the StackPractices guide
[JUnit 5: Extensions, Parameterized Tests, Dynamic Tests](https://stackpractices.com/guides/complete-guide-junit5-modern-testing/).

Self-contained Maven project with working versions of the code shown in the guide:

- `LifecycleTest`, `TaggedOrderServiceTest` — lifecycle annotations, `@DisplayName`, `@Tag`
- `BasicAssertionsTest` — `assertAll`, lazy messages, `assertThrows`, timeouts
- `BasicParameterizedTest` — `@ValueSource`, `@CsvSource`, `@MethodSource`, `@NullAndEmptySource`, custom display names
- `RetryExtension` + `FlakyServiceTest` — a custom `InvocationInterceptor` that retries failed tests
- `DynamicTestsTest` — `@TestFactory` dynamic tests from maps and lists
- `ComparableContract` + `StringComparableTest` — contract tests via interface default methods
- `NestedOrderServiceTest` — `@Nested` BDD-style grouping on a small `OrderService` domain
- `junit-platform.properties` — parallel execution template (commented out)

## Run

```bash
mvn test
```

Requires Java 17+ and Maven. Surefire 3.3.0 picks up JUnit Platform tests automatically.

The `TaggedOrderServiceTest` shows tag filtering: `mvn test -Dgroups=unit` runs only unit tests; the project's `pom.xml` already excludes `slow` and `integration` by default.
