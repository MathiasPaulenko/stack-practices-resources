# Patrón Timeout — Archivos complementarios

Implementaciones ejecutables de la guía del [Patrón Timeout](https://stackpractices.com/es/patterns/timeout-pattern/).

## Archivos

| Archivo | Qué muestra |
| --- | --- |
| `with_timeout.py` | Decorador que impone un límite duro a funciones síncronas. |
| `deadline_budget.py` | Propagación de deadline: cada capa recibe el presupuesto *restante*, dejando margen al llamador para reaccionar. |
| `test_timeouts.py` | Suite de pytest: las llamadas rápidas pasan, las lentas lanzan error, los presupuestos encogen en la cadena y los expirados fallan rápido. |

## Ejecutar

```bash
pip install pytest
pytest test_timeouts.py
```

## Notas

- `with_timeout` abandona la espera pero no puede matar el hilo trabajador — combínalo con timeouts de socket (`requests.get(url, timeout=...)`, `statement_timeout`) para que el trabajo abandonado muera solo.
- La demo de presupuesto muestra por qué los timeouts externos deben superar la suma de los internos: la diferencia es el tiempo de reacción para reintentos y fallbacks.
