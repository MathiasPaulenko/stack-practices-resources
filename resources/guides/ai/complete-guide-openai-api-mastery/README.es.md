# API de OpenAI — Ejemplos de producción

Ejemplos ejecutables que acompañan a la [guía de la API de OpenAI](https://stackpractices.com/es/guides/complete-guide-openai-api-mastery/).

Requiere `openai>=1.x` y la variable de entorno `OPENAI_API_KEY`. `streaming_sse.py` necesita además `fastapi` y `uvicorn`; `structured_outputs.py` necesita `pydantic`.

| Archivo | Qué muestra |
| --- | --- |
| `responses_api.py` | `responses.create`, encadenado con `previous_response_id`, function tools aplanadas |
| `chat_client.py` | Chat completions y gestión del historial multi-turno |
| `streaming_sse.py` | Streaming de tokens + endpoint `StreamingResponse` de FastAPI |
| `stream_node.js` | El mismo patrón de streaming con el SDK de Node |
| `function_calling.py` | Bucle completo de tool calls con tope de iteraciones y validación de argumentos |
| `structured_outputs.py` | `responses.parse` con `text_format` de Pydantic |
| `retry_backoff.py` | Rate limiter (token bucket), backoff con jitter y mapeo de errores |
| `cost_tracker.py` | Contabilidad de coste por llamada y resumen por modelo |
| `batch_api.py` | Envío de batch en JSONL, polling y descarga de resultados |

## Uso

```bash
pip install openai pydantic fastapi uvicorn
export OPENAI_API_KEY=sk-...
python responses_api.py
```

Para probar el endpoint SSE:

```bash
uvicorn streaming_sse:app --reload
curl -N -X POST localhost:8000/chat/stream -H "Content-Type: application/json" -d "{\"message\": \"hola\"}"
```
