# Patrón Ambassador — Ejemplos de Proxy de Infraestructura

Ejemplos ejecutables del recurso [Patrón Ambassador](https://stackpractices.com/es/patterns/ambassador-pattern/) en StackPractices.

Un ambassador es un proxy ubicado entre los clientes y los servicios externos que se hace cargo de los aspectos transversales: pooling de conexiones, reintentos, circuit breaking, monitorización y terminación TLS. Los clientes le hablan como si fuera el servicio real.

## Contenido

| Archivo | Qué es |
|---------|--------|
| `envoy-ambassador.yaml` | Listener + cluster de Envoy: TLS upstream, política de reintentos, umbrales de circuit breaker |
| `ambassador_proxy.py` | Ambassador en Python: reintentos con backoff exponencial, circuit breaker, estadísticas por endpoint |
| `client_example.py` | Cliente que llama al ambassador en vez de a la API real |
| `AmbassadorClient.java` | Ambassador en Java 11+ (`java.net.http`), misma cadena de políticas |
| `nginx-stream-ambassador.conf` | Bloque `stream` de Nginx proxificando TCP en crudo (PostgreSQL) con failover |
| `requirements.txt` | Dependencia de Python (`requests`) |

## Inicio rápido

Ambassador en Python:

```bash
pip install -r requirements.txt
python client_example.py
```

Apuntá `AmbassadorProxy("https://api.external.com")` a cualquier endpoint — por ejemplo `python -m http.server 8080` en local para una prueba de humo.

Ambassador con Envoy:

```bash
envoy -c envoy-ambassador.yaml
curl http://localhost:18080/users/42   # reenviado a api.external.com:443
```

Ambassador Nginx stream: copiá el bloque en tu `nginx.conf` a nivel raíz (fuera de `http {}`), y conectá los clientes de Postgres al host de Nginx en el puerto 5432.
