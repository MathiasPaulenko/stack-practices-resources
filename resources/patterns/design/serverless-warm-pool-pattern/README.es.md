# Patrón Serverless Warm Pool

Companion ejecutable del patrón
[Patrón Serverless Warm Pool](https://stackpractices.com/es/patterns/serverless-warm-pool-pattern/).

Un stack CDK que mantiene en caliente una API Lambda: una regla de
EventBridge invoca una pequeña función warmup cada 5 minutos, que envía N
pings async concurrentes a la función API. La función API cortocircuita
con el flag `isWarmup`, así que cada ping mantiene vivo un entorno de
ejecución sin disparar lógica de negocio.

## Archivos

| Archivo | Propósito |
|---|---|
| `warm_pool_stack.py` | Stack CDK (Python): función API, función warmup, schedule de EventBridge, permiso de invocación |
| `warmup_handler.py` | Lambda warmup que reparte N pings async concurrentes con `ThreadPoolExecutor` |
| `warmup_handler.ts` | El mismo handler warmup con AWS SDK v3 y `Promise.all` |
| `api_handler.py` | Handler API con return anticipado ante `isWarmup` (Python) |
| `api_handler.ts` | Handler API con return anticipado ante `isWarmup` (TypeScript) |

## Notas

- `WARM_COUNT` dimensiona el warm pool — ajústalo a las peticiones
  *concurrentes* esperadas, no al volumen de tráfico.
- El intervalo de ping es de 5 minutos; los entornos Lambda suelen
  expirar tras 5-15 minutos de inactividad. Intervalos más cortos
  desperdician invocaciones.
- La función warmup necesita `lambda:InvokeFunction` sobre los ARNs del
  target — el stack lo concede con `api_function.grant_invoke`.
- Para capacidad en caliente garantizada en SLAs estrictos, prefiere
  provisioned concurrency o Lambda SnapStart antes que pings programados.
