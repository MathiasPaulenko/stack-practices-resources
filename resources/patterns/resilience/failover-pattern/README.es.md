# Patrón Failover — Código complementario

Implementaciones ejecutables del
[Patrón Failover](https://stackpractices.com/es/patterns/failover-pattern/)
en StackPractices — el patrón que desvía el tráfico de un sistema primario
caído a un standby sano.

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `failover/health_monitored.py` | `FailoverManager`: failover active-passive guiado por health checks periódicos, con umbrales de fallo/recuperación separados para evitar oscilación |
| `failover/database.py` | `DatabaseFailover`: gestor de conexiones PostgreSQL que sondea el host activo y recorre una lista ordenada de standby |
| `failover/dns.py` | `DNSFailover`: failover por registro DNS para despliegues multi-región (más lento, pero sobrevive a caídas regionales) |
| `failover/active_active.py` | `ActiveActiveManager`: ambos nodos sirven tráfico; un fallo solo encoge el pool sano |
| `failover/cascading.py` | `CascadingFailover`: prueba primario → standby → terciario en orden |
| `failover/client.js` | `FailoverClient`: failover del lado del cliente para navegador/Node con health checks periódicos |
| `failover/nginx.conf` | Upstream de Nginx con servidor `backup` — failover pasivo en pocas directivas |
| `failover/k8s-failover.yaml` | `Service` + `PodDisruptionBudget` de Kubernetes como base de un failover multi-clúster detrás de un LB global |

## Requisitos

- Python 3.10+ con `requests`, `psycopg2` (ejemplo de base de datos) y `dnspython` (ejemplo DNS)
- Node 18+ para `client.js` (`fetch` y `AbortSignal.timeout` incluidos)
- Un clúster de Nginx o Kubernetes corriendo solo para los archivos de configuración

## Uso

```python
from failover.health_monitored import FailoverManager

fo = FailoverManager(
    primary_url="https://api-primary.example.com",
    standby_url="https://api-standby.example.com",
    check_interval=5,       # segundos entre sondeos de salud
    failure_threshold=3,    # fallos consecutivos antes de conmutar
    recovery_threshold=3,   # éxitos consecutivos antes de volver
)
fo.start()

resp = fo.request("GET", "/api/products")   # siempre golpea el nodo activo
```

## Notas

- Los umbrales son lo importante: un sondeo fallido es ruido, varios seguidos
  son señal. La asimetría entre conmutar y volver es deliberada.
- El ejemplo DNS deja `_update_dns` como stub — conéctalo a la API de tu
  proveedor (Route 53, Cloudflare, etc.).
- En producción, prefiere el failover gestionado (RDS, Cloud SQL, `repmgr`,
  HAProxy, load balancers cloud) sobre bucles hechos a mano; estos archivos
  existen para enseñar la semántica.
