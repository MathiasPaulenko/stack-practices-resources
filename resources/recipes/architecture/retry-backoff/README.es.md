# Retry Backoff — Recursos Complementarios

Versiones ejecutables de las técnicas avanzadas de retry de la
[receta Retry Backoff](https://stackpractices.com/es/recipes/retry-backoff/):
budgets, deadlines y hedged requests.

## Archivos

| Archivo | Lenguaje | Qué demuestra |
|---|---|---|
| `retry_budget.go` | Go | Retry budget con token bucket — limita el tráfico de reintentos por segundo para que una caída parcial no se convierta en DDoS autoinfligido |
| `hedged_request.ts` | TypeScript | Hedged request con cancelación — dispara un duplicado tras un delay, gana la primera respuesta, el perdedor se aborta |
| `retry_deadline.py` | Python | Decorador de retry context-aware — se detiene al llegar a un deadline de reloj y nunca duerme más allá de él |

## Inicio rápido

```bash
# Go (sin dependencias)
go run retry_budget.go

# TypeScript (Deno o tsx)
npx tsx hedged_request.ts

# Python
pip install requests
python retry_deadline.py
```

Cada snippet es autocontenido — cópialo a tu codebase y adapta
el predicado de error reintentable a tu transporte.
