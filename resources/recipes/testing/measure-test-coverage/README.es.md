# Medir Cobertura de Test — Recursos complementarios

Configuraciones de cobertura listas para usar de la receta [Medir Cobertura de Test](https://stackpractices.com/es/recipes/measure-test-coverage/) en StackPractices.

| Archivo | Qué es |
|---------|--------|
| `pyproject-coverage.toml` | Config de coverage.py / pytest-cov: cobertura de ramas, reglas `omit`, `fail_under = 80` y `exclude_also` prácticos |
| `vitest.config.ts` | Cobertura en Vitest con la forma correcta de `coverage.thresholds` (Vitest 1.x+) y reporter `lcov` para herramientas de tendencias |
| `jacoco-pom-snippet.xml` | Plugin JaCoCo en Maven: reporte en `test`, goal `check` con reglas BUNDLE más una regla PACKAGE más estricta para el core |
| `coverage-gate.yml` | Pipeline de GitHub Actions: grupos de tests en paralelo emiten cobertura parcial y un job de fusión combina y aplica el gate |

## Notas

- `--cov` recibe el nombre del paquete importable, no el directorio de tests — es la causa más común de reportes al 0%.
- Emite siempre un reporte XML o lcov junto al HTML: el HTML lo leen humanos, el XML lo leen las herramientas.
- Haz gate sobre diffs y tendencias, no sobre un número mágico. Sube los umbrales a medida que mejora la suite.
