# Inyección de Dependencias — Código Companion

Artefactos ejecutables para la [Receta de Inyección de Dependencias](https://stackpractices.com/es/recipes/dependency-injection/) de StackPractices.

## Archivos

| Archivo | Qué es |
|---------|--------|
| `di-container.ts` | Contenedor TypeScript de ~60 líneas: ciclos de vida transient / singleton / scoped + `validate()` |
| `di_container.py` | Contenedor Python con ciclo de vida con ámbito vía context manager |
| `test-container.ts` | `TestContainer` que sobreescribe los registros de producción con fakes, con ejemplo para vitest/jest |

## Uso

Sin dependencias. Copia el archivo que necesites en tu proyecto y adapta los registros del composition root comentado. Llama a `validate()` al arranque para fallar rápido ante registros faltantes, y abre un ámbito por petición/test.

## Relacionados

- [Receta de Inyección de Dependencias (ES)](https://stackpractices.com/es/recipes/dependency-injection/)
- [Dependency Injection recipe (EN)](https://stackpractices.com/recipes/dependency-injection/)
- [Índice de recursos de StackPractices](https://mathiaspaulenko.github.io/stack-practices-resources/)
