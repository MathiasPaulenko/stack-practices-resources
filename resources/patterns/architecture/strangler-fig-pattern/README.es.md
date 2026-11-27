# Patrón Strangler Fig — Código complementario

Ejemplos ejecutables de [Patrón Strangler Fig: migración incremental de sistemas legacy](https://stackpractices.com/es/patterns/strangler-fig-pattern/) en StackPractices.

## Archivos

| Archivo | Qué muestra |
|---|---|
| `nginx.conf` | Routing con reverse proxy: rutas migradas al servicio nuevo, el resto al legacy |
| `strangler_router.py` | Router con feature flags en Flask, porcentaje canary y header de observabilidad |
| `StranglerGateway.java` | Definición de rutas con Spring Cloud Gateway para la misma división |
| `shadow_traffic.py` | Envía peticiones a ambos sistemas, devuelve la respuesta legacy y registra diferencias |
| `cutover.py` | Sigue el estado de migración por ruta y reporta la preparación del cutover |
| `branch_by_abstraction.py` | Cambia implementaciones tras una interfaz común mediante un flag |
| `parallel_run.py` | Ejecuta la misma operación en ambos sistemas y registra las diferencias |

## Uso

- `strangler_router.py` necesita las variables de entorno `LEGACY_URL` y `NEW_SERVICE_URL`, además de `flask` y `requests`.
- `shadow_traffic.py` y `cutover.py` no tienen dependencias salvo `requests`.
- `StranglerGateway.java` requiere Spring Cloud Gateway en el classpath.
- `nginx.conf` encaja en un layout estándar de `conf.d` de Nginx.
