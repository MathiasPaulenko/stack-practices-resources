# Event Loop de JavaScript — Recursos complementarios

Archivos companion de [Event Loop de JavaScript](https://stackpractices.com/es/recipes/javascript-event-loop/) en StackPractices.

## Archivos

| Archivo | Qué demuestra |
|---------|---------------|
| `event_loop_order.js` | Orden de ejecución de código sync, `process.nextTick`, microtareas (Promise, queueMicrotask) y macrotareas (setTimeout) — con salida esperada en comentarios |
| `chunked_processing.js` | Dividir un recorrido pesado en chunks con `setTimeout` para que el loop siga respondiendo |
| `event_loop_lag.js` | Medir el lag del event loop vía drift del timer mientras corren ráfagas bloqueantes |

## Cómo usar

```bash
node event_loop_order.js      # imprime el orden de scheduling
node chunked_processing.js    # mira cómo los chunks ceden el loop
node event_loop_lag.js        # ctrl+C para parar; el lag pica tras cada ráfaga
```

Sin dependencias — Node.js ≥ 18 puro funciona para los tres scripts.
