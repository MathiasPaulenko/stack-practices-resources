# Rate Limiting — Recursos complementarios

Código complementario de la [receta de Rate Limiting](https://stackpractices.com/es/recipes/rate-limiting/) en StackPractices.com.

## Qué incluye

| Archivo | Lenguaje | Algoritmo | Despliegue |
|---------|----------|-----------|------------|
| `token_bucket.py` | Python | Token bucket (permite ráfagas) | En memoria, un proceso |
| `fixed_window_redis.js` | JavaScript | Fixed window + presupuestos por endpoint | Redis, multi-instancia |
| `SlidingWindow.java` | Java | Sliding window log (sin ráfagas de borde) | En memoria, un proceso |
| `sliding_window_counter.py` | Python | Contador de sliding window (solape ponderado) | En memoria, O(1) por clave |

## Inicio rápido

```bash
python token_bucket.py          # True
node -e "require('./fixed_window_redis.js')"  # requiere el paquete redis + servidor
javac SlidingWindow.java && java SlidingWindow  # true
```

## Elige tu algoritmo

- **Fixed window** (el JS): empieza aquí — dos comandos de Redis, suficientemente correcto para la mayoría de APIs. El borde deja pasar hasta 2× al filo de la ventana; en ventanas de minutos raramente importa.
- **Token bucket** (el Python): cuando los clientes hacen ráfagas legítimas — sync clients, dashboards que abren muchas llamadas.
- **Sliding window** (el Java): cuando la ráfaga de borde realmente cuesta dinero; cuesta un timestamp por petición.

## Notas de producción

- Clave por `user:{id}` o `api_key`, no por IP — las NATs castigan a inocentes. Límites más estrictos en endpoints de auth.
- Decide fail-open vs fail-closed para caídas de Redis *explícitamente* — el tráfico de lectura suele fallar abierto, login/pagos cerrado.
- Devuelve siempre `429` + `Retry-After`; anuncia `RateLimit-Limit/Remaining/Reset` para que los clientes se dosifiquen.
- La limitación distribuida necesita un almacén compartido — los contadores en memoria multiplican silenciosamente el límite por instancia.
