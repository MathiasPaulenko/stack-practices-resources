# Patrón Graceful Shutdown — Código complementario

Implementaciones ejecutables del patrón graceful shutdown de la
[página del patrón en StackPractices](https://stackpractices.com/es/patterns/graceful-shutdown-pattern/).

## Archivos

| Archivo | Qué muestra |
| --- | --- |
| `shutdown/graceful.py` | `HTTPServer` de Python que trackea las requests activas y drena al recibir SIGTERM. |
| `shutdown/graceful.js` | Servidor Express que devuelve 503 mientras sale y termina cuando el contador llega a cero. |
| `shutdown/GracefulShutdownConfig.java` | Configuración `Shutdown.GRACEFUL` de Spring Boot para el Tomcat embebido. |
| `shutdown/ResourceCleanupHook.java` | Hook `SmartLifecycle` que cierra conexiones de base de datos y vacía buffers al inicio de la secuencia de shutdown. |
| `shutdown/worker.py` | Worker en background con threads que termina los jobs en curso antes de salir. |
| `shutdown/deregister.py` | Baja del load balancer antes de drenar (requiere `requests`). |
| `shutdown/phased.py` | Shutdown multi-fase con un timeout por fase. |
| `shutdown/websocket.js` | Servidor WebSocket con `ws` que cierra los clientes con código 1001 antes de salir. |
| `shutdown/k8s-graceful-shutdown.yaml` | Deployment con sleep en `preStop`, readiness probe y `terminationGracePeriodSeconds`. |

## Prueba rápida

```bash
python shutdown/graceful.py        # después: curl localhost:8080/ y Ctrl+C
node shutdown/graceful.js          # necesita `npm install express`
node shutdown/websocket.js         # necesita `npm install ws`
```

Mandá SIGTERM a mitad de una request para ver el drenado: el servidor deja de
aceptar conexiones nuevas, termina las que están en curso y sale limpio en vez
de cortarlas.
