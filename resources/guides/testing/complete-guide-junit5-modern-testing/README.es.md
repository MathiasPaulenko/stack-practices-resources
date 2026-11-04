# JUnit 5: Extensiones, Tests Parametrizados y Dinámicos — Ejemplos

Companion ejecutable de la guía de StackPractices
[JUnit 5: Extensiones, Tests Parametrizados y Dinámicos](https://stackpractices.com/es/guides/complete-guide-junit5-modern-testing/).

Proyecto Maven autocontenido con versiones funcionales del código de la guía:

- `LifecycleTest`, `TaggedOrderServiceTest` — anotaciones del ciclo de vida, `@DisplayName`, `@Tag`
- `BasicAssertionsTest` — `assertAll`, mensajes lazy, `assertThrows`, timeouts
- `BasicParameterizedTest` — `@ValueSource`, `@CsvSource`, `@MethodSource`, `@NullAndEmptySource`, nombres visibles personalizados
- `RetryExtension` + `FlakyServiceTest` — un `InvocationInterceptor` personalizado que reintenta tests fallidos
- `DynamicTestsTest` — tests dinámicos con `@TestFactory` desde maps y lists
- `ComparableContract` + `StringComparableTest` — tests de contrato vía métodos default de interfaz
- `NestedOrderServiceTest` — agrupación estilo BDD con `@Nested` sobre un pequeño dominio `OrderService`
- `junit-platform.properties` — plantilla de ejecución en paralelo (comentada)

## Ejecutar

```bash
mvn test
```

Requiere Java 17+ y Maven. Surefire 3.3.0 detecta los tests del JUnit Platform automáticamente.

`TaggedOrderServiceTest` muestra el filtrado por tags: `mvn test -Dgroups=unit` corre solo los tests unitarios; el `pom.xml` del proyecto ya excluye `slow` e `integration` por defecto.
