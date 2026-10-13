# Patrón Bulkhead — Código complementario

Implementaciones ejecutables del patrón bulkhead: aislamiento de hilos, conexiones y llamadas concurrentes por servicio o tenant, para que una dependencia saturada no agote a las demás.

Artículo fuente: [Patrón Bulkhead: Aísla Recursos y Limita el Radio de Impacto](https://stackpractices.com/es/patterns/bulkhead-pattern/)

## Archivos

| Archivo | Qué muestra |
|---------|-------------|
| `exceptions.py` | `BulkheadFullError` y `CircuitBreakerOpenError` compartidas por los demás módulos. |
| `thread_pool.py` | `BulkheadManager` — un `ThreadPoolExecutor` dedicado por servicio con colas acotadas y rechazo fail-fast. |
| `semaphore.py` | `SemaphoreBulkhead` — límite de concurrencia con semáforo; usable como decorador o context manager. |
| `connection_pools.py` | `IsolatedConnectionPools` — pools de conexión psycopg2 separados para rutas críticas y no críticas. Requiere `psycopg2-binary`. |
| `per_tenant.py` | `PerTenantBulkhead` — semáforo por tenant para que un tenant ruidoso no agote la capacidad compartida. |
| `hybrid.py` | `BulkheadWithCircuitBreaker` — límite de concurrencia más ruptura por fallos en un solo wrapper. |
| `ServiceBulkheads.java` | Configuración de `Bulkhead` y `ThreadPoolBulkhead` de resilience4j para llamadas síncronas y asíncronas. |
| `k8s-bulkhead.yaml` | `ResourceQuota` por namespace más límites de CPU/memoria por pod — bulkheads aplicados por la plataforma. |

## Uso

```bash
python thread_pool.py      # imprime el resultado de una tarea y las stats de los pools
python semaphore.py        # ejecuta una llamada decorada y otra con context manager
python per_tenant.py       # adquiere permisos para tres tenants e imprime las stats
python hybrid.py           # una llamada a través del bulkhead + breaker combinado
```

`connection_pools.py` necesita un PostgreSQL accesible y `pip install psycopg2-binary`. `ServiceBulkheads.java` necesita `io.github.resilience4j:resilience4j-bulkhead` en el classpath e implementaciones reales de `paymentClient`/`inventoryClient`.

## Notas

- Todos los bulkheads rechazan al saturarse (`BulkheadFullError`) en lugar de bloquear — esa es la mitad fail-fast del patrón.
- `thread_pool.py` lleva `_active` en un `defaultdict` sin lock por legibilidad; usa un `threading.Lock` si envías tareas desde varios hilos.
- Las cuotas de K8s aíslan *namespaces*; los `resources` a nivel pod aíslan contenedores individuales. Usa ambos.
