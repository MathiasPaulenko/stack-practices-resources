# Plantilla de Decisión de Estrategia de Caché — Companion

Companion del doc de StackPractices [Plantilla de Decisión de Estrategia de Caché](https://stackpractices.com/es/docs/cache-strategy-decision-template/).

## Archivos

| Archivo | Ejecutar |
| --- | --- |
| `src/decision_generator.py` | `python src/decision_generator.py` |

Un CLI interactivo (solo stdlib de Python) que recorre las mismas preguntas del árbol de decisión del doc — ritmo de cambio del dato, proporción de escrituras, tolerancia a pérdidas, acceso predecible, consistencia — recomienda una estrategia (no-cache / cache-aside / read-through / write-through / write-back / refresh-ahead) e imprime un **Registro de Decisión de Estrategia de Caché** rellenado, listo para pegar en la documentación del servicio o en un ADR.
