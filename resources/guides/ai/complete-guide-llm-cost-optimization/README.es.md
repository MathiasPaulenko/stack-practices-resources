# Optimización de Costes LLM — Companion

Toolkit ejecutable de [Guía Completa de Optimización de Costes LLM](https://stackpractices.com/es/guides/complete-guide-llm-cost-optimization/).

| Archivo | Descripción |
|---------|-------------|
| `router.py` | `ModelRouter` + `CascadingRouter` (barato primero, escala con UNCERTAIN) |
| `cache.py` | `LLMCache` exacta + `SemanticCache` |
| `budget.py` | `BudgetController` — alerta al 80%, corte al 100% |
| `batch_job.py` | Helpers de Batch API (50% dto., 24h) |
| `token_counter.py` | `TokenManager` con tiktoken |
| `test_cost.py` | Tests unitarios offline |
| `requirements.txt` | Dependencias fijadas |

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
pytest test_cost.py -v   # corre completamente offline
```
