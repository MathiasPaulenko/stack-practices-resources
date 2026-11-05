# Migración Strangler Fig — Ejemplos de Código

Ejemplos TypeScript y Python ejecutables de la guía:
<https://stackpractices.com/es/guides/complete-guide-strangler-fig-migration/>

## Archivos

| Archivo | Qué muestra |
| --- | --- |
| `strangler_router.ts` | Router a nivel aplicación: matching de reglas, rollout por feature flags, fallback al legacy con try/catch |
| `shadow_traffic.ts` | Dark launch: llamadas en paralelo a ambos sistemas, comparación por campos clave |
| `feature_flags.ts` | Estrategias de rollout percentage / user-list / environment / boolean con bucketing estable |
| `dual_write.ts` | Dual-write con orden nuevo-primero y cola de reintentos para fallos del legacy |
| `rollback_manager.ts` | Rollback automático por umbrales de tasa de errores y latencia p99 |
| `cdc_sync.py` | Consumidor Kafka estilo Debezium que replica cambios al nuevo almacén |
| `kong_routes.yaml` | Routing en el borde: split por path entre el servicio nuevo y el monolito legacy |

## Notas

- Los archivos TypeScript son código de biblioteca — conectalos a los tipos
  request/response de tu framework HTTP. `SystemAdapter` es la costura:
  implementala una vez para el legacy y otra para el nuevo.
- `cdc_sync.py` necesita un Kafka corriendo con un conector Debezium (o
  similar) publicando a `legacy-db-changes`. `pip install -r requirements.txt`.
- La guía explica por qué `isEnabled` necesita `await`, por qué los campos del
  flag llevan guards `?.` y por qué las funciones se definen antes del loop de
  consumo — los tres fueron bugs reales de borradores anteriores.
