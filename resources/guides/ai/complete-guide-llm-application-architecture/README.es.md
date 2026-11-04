# Arquitectura de Aplicaciones LLM — Companion

Capas Python ejecutables de la guía de StackPractices
[Guía Completa de Arquitectura de Aplicaciones LLM](https://stackpractices.com/es/guides/complete-guide-llm-application-architecture/).

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `app.py` | Endpoint FastAPI que streamea tokens por SSE con `ChatRequest` tipado |
| `prompts.py` | `PromptRegistry` — templates Jinja2 versionados cargados desde YAML |
| `cache.py` | Cachés exacta y semántica en Redis (basada en SCAN, con nota de índice vectorial) |
| `guardrails.py` | `InputGuardrail` (longitud, patrones de inyección) + `OutputGuardrail` (redacción de PII) |
| `metrics.py` | `LLMMetrics` — peticiones, tokens, latencia p95, tasa de aciertos de caché |
| `router.py` | `ModelRouter` + reintentos con backoff + fallback entre proveedores |
| `test_layers.py` | Tests unitarios de guardrails, métricas y router — sin llamadas a la API |
| `requirements.txt` | Dependencias fijadas |

## Inicio rápido

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...

# Sirve el endpoint de streaming
uvicorn app:app --reload

# Los tests corren completamente offline (sin API key)
pytest test_layers.py -v
```

La caché semántica necesita un Redis local en `localhost:6379`. Todo lo demás
corre de forma autónoma.
