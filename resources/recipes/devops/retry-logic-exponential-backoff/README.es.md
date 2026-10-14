# Retry con Backoff Exponencial

Código ejecutable complementario de la receta [Retry con Backoff Exponencial](https://stackpractices.com/es/recipes/retry-logic-exponential-backoff/) en StackPractices.

## Contenido

| Archivo | Lenguaje | Qué muestra |
| --- | --- | --- |
| `retry.py` | Python | Decorador `@retry`: backoff exponencial, full jitter, filtrado de excepciones, hook `on_retry`, `sleep` inyectable |
| `test_retry.py` | Python | Suite pytest — verifica la secuencia exacta de delays, los límites del jitter, el filtrado de excepciones y el callback con un sleep falso |
| `retry.js` | JavaScript | Helper `retry()` con filtrado por status HTTP, ejemplo con clave de idempotencia, `sleep` inyectable |
| `Retry.java` | Java | `Retry.execute()` con `Sleeper` inyectable y filtrado de excepciones reintentables |
| `retry.go` | Go | `withRetry()` con deadline vía context y jitter con `math/rand` |

## Ejecutar

```bash
python retry.py              # demo: la función que falla tiene éxito en el intento 3
python -m pytest test_retry.py -v

node retry.js                # demo sin acceso a red

javac Retry.java && java Retry

go run retry.go
```

Las demos y los tests nunca tocan la red ni esperan de verdad: la función de espera es inyectable para poder verificar directamente la secuencia de backoff.
