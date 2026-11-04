# LLM Application Architecture — Companion

Runnable Python layers from the StackPractices guide
[Complete Guide to LLM Application Architecture](https://stackpractices.com/guides/complete-guide-llm-application-architecture/).

## Files

| File | Description |
|------|-------------|
| `app.py` | FastAPI endpoint streaming tokens over SSE with a typed `ChatRequest` |
| `prompts.py` | `PromptRegistry` — versioned Jinja2 templates loaded from YAML |
| `cache.py` | Exact-match + semantic caches on Redis (SCAN-based, with a vector-index note) |
| `guardrails.py` | `InputGuardrail` (length, injection patterns) + `OutputGuardrail` (PII redaction) |
| `metrics.py` | `LLMMetrics` — requests, tokens, latency p95, cache hit rate |
| `router.py` | `ModelRouter` + retry with backoff + cross-provider fallback |
| `test_layers.py` | Unit tests for guardrails, metrics and router — no API calls |
| `requirements.txt` | Pinned dependencies |

## Quick start

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...

# Serve the streaming endpoint
uvicorn app:app --reload

# Tests run fully offline (no API key needed)
pytest test_layers.py -v
```

The semantic cache needs a local Redis on `localhost:6379`. Everything else
runs standalone.
