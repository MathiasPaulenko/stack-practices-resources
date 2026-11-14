# SpotBugs Static Analysis — Recursos complementarios

Proyecto ejecutable complementario de la [receta de análisis estático con SpotBugs](https://stackpractices.com/es/recipes/java-spotbugs-static-analysis/) en StackPractices.

## Contenido

- `pom.xml` — build de Maven con spotbugs-maven-plugin 4.9.3.0, `effort=Max`, `threshold=Medium` y el plugin Find Security Bugs.
- `build.gradle` / `settings.gradle` — equivalente en Gradle con Groovy DSL.
- `spotbugs-exclude.xml` — archivo de exclusión FindBugsFilter: clases de test, código generado, exclusiones por clase y por patrón.
- `spotbugs-include-security.xml` — filtro de inclusión que corre solo las categorías `SECURITY`, `CORRECTNESS` y `MALICIOUS_CODE`, para un gate exclusivo de seguridad.
- `github-actions/spotbugs.yml` — workflow de GitHub Actions que corre `spotbugs:check` y sube el reporte XML, con una variante SARIF/code scanning comentada.
- `src/main/java/com/example/spotbugsdemo/` — cuatro clases con bugs intencionales para que los reportes no salgan vacíos:
  - `NullPathBug.java` → `NP_NULL_ON_SOME_PATH`
  - `ExposedRep.java` → `EI_EXPOSE_REP` / `EI_EXPOSE_REP2`
  - `UnclosedResource.java` → `OBL_UNSATISFIED_OBLIGATION`
  - `SqlConcat.java` → `SQL_INJECTION_JDBC` (Find Security Bugs)

## Uso

Maven:

```bash
# Análisis + reporte (el build NO falla por hallazgos)
mvn spotbugs:spotbugs
# Reporte: target/spotbugsXml.xml — o corre mvn spotbugs:gui para el visor de triage

# Gate de CI — falla el build con hallazgos Medium+ (esperado en este demo)
mvn spotbugs:check
```

Gradle (requiere `gradle` instalado, o agrega un wrapper):

```bash
gradle spotbugsMain
# Reportes: build/reports/spotbugs/main/spotbugs.html y .xml
```

Adopción con baseline — silencia los hallazgos existentes y solo verifica los nuevos:

```bash
mvn spotbugs:spotbugs
cp target/spotbugsXml.xml spotbugs-baseline.xml
mvn spotbugs:check -Dspotbugs.excludeBugsFile=spotbugs-baseline.xml
```

Gate solo de seguridad — apunta el filtro de inclusión a `spotbugs-include-security.xml`:

```bash
mvn spotbugs:check -Dspotbugs.includeFilterFile=spotbugs-include-security.xml
```

Requiere Java 17+ y Maven 3.6+ o Gradle 7+.
