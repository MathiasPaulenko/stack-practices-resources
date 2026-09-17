# Soft Assertions con AssertJ en JUnit5

Código companion de [StackPractices: Soft Assertions con AssertJ en JUnit5](https://stackpractices.com/es/recipes/java-junit5-assertions-soft/).

## Requisitos

- Java 17+
- Maven 3.9+
- JUnit Jupiter 5.12.x
- AssertJ Core 3.27.7

## Archivos

| Archivo | Descripción |
| ------ | ----------- |
| `pom.xml` | Proyecto Maven con las dependencias de test JUnit5 + AssertJ, más el `assertj-assertions-generator-maven-plugin` conectado a `generate-test-sources` |
| `src/main/java/domain/User.java` | POJO de dominio que el generador de aserciones lee para emitir `UserAssert`/`SoftAssertions` |
| `src/test/java/UserSoftAssertionsTest.java` | 7 ejemplos ejecutables de soft assertions: `SoftAssertions` básico, lambda `assertSoftly`, colecciones, mensajes personalizados con `.as()`, comparación recursiva, inyección con `@RegisterExtension`, y `assertAll` de JUnit5 para comparar |
| `src/test/java/GeneratedSoftAssertionsTest.java` | 2 tests usando el punto de entrada `domain.SoftAssertions` generado por el plugin y el `UserAssert` tipado (`hasEmail()`, `hasRole()`, `isActive()`) |

El plugin generador (v2.2.0) emite `javax.annotation.Generated`, que el JDK eliminó en Java 11 — la dependencia de test `javax.annotation-api` en `pom.xml` lo cubre.

## Uso

La carpeta es un proyecto Maven listo para usar — solo ejecuta:

```bash
mvn test
```

Todos los tests pasan directamente — los colaboradores del servicio son records stub dentro de la clase de test, así que todo compila sin dependencias externas. Para ver el reporte de fallos agregado, cambia un valor esperado (por ejemplo, `isEqualTo(201)` → `isEqualTo(200)` en `should_validate_order_response`) y vuelve a ejecutar: `assertAll()` lanza un `SoftAssertionError` que lista cada verificación fallida.

## Qué demuestra

- Por qué importan las soft assertions: una ejecución reporta todos los fallos en lugar de detenerse en el primero.
- Los tres puntos de entrada: `new SoftAssertions()`, `assertSoftly(lambda)` y `SoftAssertionsExtension` vía `@RegisterExtension`.
- Descripciones `.as()` para que un reporte de 10 fallos siga siendo legible.
- `usingRecursiveComparison()` enrutado por el proxy soft para comparar objetos campo a campo.
