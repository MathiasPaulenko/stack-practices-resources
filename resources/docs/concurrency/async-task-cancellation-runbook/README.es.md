# Runbook de cancelación de tareas asíncronas — Recursos companion

Archivos companion del [Runbook de cancelación de tareas asíncronas](https://stackpractices.com/es/docs/async-task-cancellation-runbook/) en StackPractices.com.

## Qué incluye

| Archivo | Lenguaje | Descripción |
|---------|----------|-------------|
| `python_cancel.py` | Python | Cancelación cooperativa con `asyncio.CancelledError`, timeout con `wait_for` y clase `GracefulShutdown` para SIGINT/SIGTERM |
| `node_cancel.mjs` | JavaScript | Cancelación con `AbortController`/`AbortSignal`, `sleep` consciente de la señal, helper de fetch con timeout |
| `go_cancel.go` | Go | Cancelación con `context.Context`, `WithTimeout` y checkpoints en `ctx.Done()` |
| `JavaCancel.java` | Java | Cancelación por interrupción con `Future.cancel(true)` y limpieza |

## Inicio rápido

Cada archivo es autocontenido y auto-cancela la tarea de demo tras ~2 segundos para que veas correr el camino de limpieza.

```bash
python python_cancel.py        # Ctrl+C también dispara el camino de señal
node node_cancel.mjs           # requiere Node 18+ (top-level await, DOMException)
go run go_cancel.go
javac JavaCancel.java && java JavaCancel
```

## Qué observar

- La tarea imprime `processing item N` hasta que llega el cancel, luego ejecuta `cleanup_resources` y relanza la cancelación.
- En `node_cancel.mjs`, `cleanupResources` llama a `sleep(50)` *sin* señal — el patrón de señal opcional es lo que hace segura la limpieza post-abort.
- En `go_cancel.go`, `defer cancel()` es obligatorio; saltárselo fuga la goroutine timer del contexto.
- En `JavaCancel.java`, prueba `future.cancel(false)` y observa que la tarea sigue corriendo en segundo plano.
