# asyncio.Semaphore: Limitar Llamadas API Concurrentes en Python

Código companion para la [receta de StackPractices](https://stackpractices.com/es/recipes/python-asyncio-semaphore-rate-limiting/).

## Requisitos

- Python 3.11+
- Sin dependencias externas para los patrones 1, 3, 4, 5, 6, 7 (solo stdlib)
- El patrón 2 es simulado (sin llamadas HTTP reales)

## Ejecución

```bash
python semaphore_examples.py 1   # Semáforo Básico
python semaphore_examples.py 2   # Limitación de Tasa en API
python semaphore_examples.py 3   # Limitador de Cubo de Tokens
python semaphore_examples.py 4   # Limitación por Host
python semaphore_examples.py 5   # Pool de Conexiones de BD
python semaphore_examples.py 6   # Ajuste Dinámico de Concurrencia
python semaphore_examples.py 7   # Semáforo con Timeout
```

## Patrones

1. **Semáforo Básico** — 10 workers con máximo 3 concurrentes
2. **Limitación de Tasa en API** — 20 URLs con máximo 5 concurrentes (simulado)
3. **Limitador de Cubo de Tokens** — 10 peticiones a 5/seg con capacidad de burst 10
4. **Limitación por Host** — semáforo separado por hostname, máximo 2 por host
5. **Pool de Conexiones de BD** — 30 queries con máximo 10 concurrentes (simulado)
6. **Ajuste Dinámico de Concurrencia** — semáforo adaptativo que sube con éxitos
7. **Semáforo con Timeout** — 10 tareas con timeout de 0.1s, algunas intencionalmente lentas
